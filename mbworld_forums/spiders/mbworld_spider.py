from copy import deepcopy
from datetime import date, timedelta

from scrapy import Request
from scrapy.crawler import CrawlerProcess

try:
    from mbworld_forums.mbworld_forums.local_elasticsearch import ElasticSearchConfig
except Exception as err:
    from mbworld_forums.mbworld_forums.elastic_search import ElasticSearchConfig
from mbworld_forums.mbworld_forums.spiders.base_spider import BaseSpider
from mbworld_forums.mbworld_forums.static import file_headers, forum_meta_filepath
from mbworld_forums.mbworld_forums.utils.clean_utils import clean
from mbworld_forums.mbworld_forums.utils.file_utils import get_feed
from mbworld_forums.mbworld_forums.utils.spider_utils import retry_invalid_response
from mbworld_forums.mbworld_forums.utils.date_time_utils import convert_time_12h_to_24h, \
    convert_date_to_mysql_format, time_delta_formatting


class MBWorldSpider(BaseSpider):
    name = "mbworld_spider"
    base_url = 'https://mbworld.org/'
    forums_url = 'https://mbworld.org/forums/'
    filepath = '../output/mbworld_post_ids.csv'
    forum_meta_filepath = f'{forum_meta_filepath}/mbworld_meta_data.csv'

    start_urls = [
        forums_url,
    ]

    custom_settings = {
        'FEEDS': get_feed(filepath=filepath, file_type='csv', csv_headers=file_headers, overwrite=True),
    }

    headers = {
        'authority': 'mbworld.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.elastic_search = ElasticSearchConfig(forum_index=self.index_arg or "mbworld")
        self.scraped_message_ids = self.get_scraped_threads_ids(self.filepath)
        self.forum_paths = self.get_forum_paths(self.forum_meta_filepath)

    def start_requests(self):
        yield Request(url=self.forums_url, callback=self.parse, meta=self.meta, headers=self.headers)

    @retry_invalid_response
    def parse(self, response):
        return [response.follow(url_s, callback=self.parse_listings, headers=self.headers, meta=response.meta)
                for sel in response.css('.trow-group')[1:7] for url_s in sel.css('h3 a')
                if 'classfied' not in url_s.get().lower() and self.is_scrape_forum_posts(url_s)]

    @retry_invalid_response
    def parse_listings(self, response):
        for url_s in response.css('div[id*="td_threadtitle_"] h4 a'):
            if 'Sticky ' in url_s.get():
                continue
            yield response.follow(url_s, callback=self.parse_thread, headers=self.headers, meta=deepcopy(self.meta))

        yield from response.follow_all(css='a[rel="next"]:not([href="javascript:void(0)"])',
                                       callback=self.parse_listings, headers=self.headers, meta=response.meta)

    @retry_invalid_response
    def parse_thread(self, response):
        threads = []

        post = dict(
            subject=self.get_title(response),
            id=self.get_thread_id(response),
            make=self.get_make_by(response),
            model=self.get_model(response),
            page_url=response.url,
        )

        if 'is_initial' not in response.meta:
            response.meta['is_initial'] = True
            response.meta['date_published'] = self.get_published_date(response)

        for i, sel in enumerate(response.css('#posts [id^="edit"]'), start=0):
            try:
                item = deepcopy(post)
                pid = self.get_post_id(sel)

                item['message_id'] = pid
                item["creation_time"] = self.get_creation_time(sel)
                item["date_published"] = response.meta['date_published']
                item["date_modified"] = self.get_modified_date(sel)
                item["author"] = self.get_author(sel)
                item['post_type'] = 'initial' if i == 0 else 'answer'
                item['body'] = self.get_post_description(sel)
                # item['body_html'] = self.get_description_html(sel)
                item["forum_path"] = self.get_forum(response)

                if pid not in self.scraped_message_ids:
                    threads.append(
                        {
                            "_index": self.elastic_search.index,
                            "_id": pid,
                            "_source": item,
                            "pipeline": self.pipeline_arg,
                        }
                    )

                    yield item
                else:
                    print(f"Filtered Duplicate Post ID = {pid}")
                self.scraped_message_ids.append(pid)
            except Exception as err:
                print(err)

        self.elastic_search.insert_bulk(threads)

        yield from response.follow_all(css='a[rel="next"]:not([href="javascript:void(0)"])',
                                       callback=self.parse_thread, meta=response.meta, headers=self.headers)

    def get_title(self, sel):
        return clean(sel.css('h1.threadtitle::text').get())

    def get_thread_id(self, response):
        return response.css('[name="searchthreadid"]::attr(value)').get()

    def get_post_id(self, sel):
        return sel.css('[id^="edit"]::attr(id)').get('').replace('edit', '')

    def get_make_by(self, response):
        return self.clean_make_model(self.get_bread_crums(response)[0]) or "Mercedes-Benz"

    def get_model(self, response):
        return self.clean_make_model(self.get_bread_crums(response)[-1])

    def get_creation_time(self, sel):
        sym = '|' if '|' in self.get_date_time(sel) else ','
        temp = self.get_date_time(sel).split(sym)[1:]
        return convert_time_12h_to_24h("".join(clean(e) for e in temp if clean(e)))

    def get_published_date(self, response):
        d = response.css('#posts [id^="edit"] .tcell')[0].css('::text').getall()
        d = "".join([clean(e) for e in d if clean(e)][:1]).split("|")[0].strip()
        return convert_date_to_mysql_format(self.get_appropriate_date(d))

    def get_modified_date(self, sel):
        d = "".join(clean(e) for e in self.get_date_time(sel).split('|')[:1] if clean(e))
        return convert_date_to_mysql_format(self.get_appropriate_date(d).split()[0])

    def get_date_time(self, sel):
        return "".join([clean(e) for e in sel.css('.tcell')[0].css('::text').getall() if clean(e)][:1])

    def get_author(self, sel):
        return clean(sel.css('.bigusername::text').get())

    def get_post_description(self, sel):
        return '\n'.join([clean(e) for e in sel.css('[id*="post_message_"] ::text').getall() if clean(e)])

    def get_description_html(self, sel):
        return sel.css('[id*="post_message_"]').get()

    def get_bread_crums(self, response):
        breadcrumbs = response.css('.breadcrumbs')[0].css('li a::text').getall()[1:]
        return [clean(e) for e in breadcrumbs if clean(e)]

    def get_forum(self, response):
        return ' > '.join(self.get_bread_crums(response))

    def get_formatted_date(self, date):
        return '-'.join(clean(date.replace('T', ' ').split('.')[0]).split('-')[:3])

    def get_today(self):
        return time_delta_formatting(date.today())

    def get_yesterday_date(self):
        return time_delta_formatting(date.today() - timedelta(days=1))

    def get_tomorrow_date(self):
        return time_delta_formatting(date.today() + timedelta(days=1))

    def is_scrape_forum_posts(self, sel):
        forum_url = sel.css('*::attr(href)').get('').rstrip('/')
        return '1' in self.forum_paths.get(forum_url, '')


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(MBWorldSpider)
    process.start()
