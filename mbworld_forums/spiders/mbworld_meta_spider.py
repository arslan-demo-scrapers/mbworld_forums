from copy import deepcopy

from scrapy.crawler import CrawlerProcess

from mbworld_forums.mbworld_forums.spiders.mbworld_spider import MBWorldSpider
from mbworld_forums.mbworld_forums.utils.clean_utils import clean
from mbworld_forums.mbworld_forums.utils.file_utils import get_feed
from mbworld_forums.mbworld_forums.utils.spider_utils import retry_invalid_response


class MBWorldMetaSpider(MBWorldSpider):
    name = "mbworld_meta_spider"

    custom_settings = {
        'FEEDS': get_feed(filepath=MBWorldSpider.forum_meta_filepath, csv_headers=MBWorldSpider.forum_meta_headers),
    }

    @retry_invalid_response
    def parse(self, response):
        yield from [self.get_forum_meta(row_sel) for sel in response.css('.trow-group')[1:7]
                    for row_sel in sel.css('.trow')]

    def get_forum_meta(self, sel):
        if not clean(self.get_forum_title(sel)):
            return

        forum_meta = deepcopy(self.forum_meta_default_item)
        forum_meta['forum_title'] = self.get_forum_title(sel)
        forum_meta['forum_url'] = self.get_forum_url(sel)
        forum_meta['forum_description'] = self.get_forum_desc(sel)
        forum_meta['last_post_title'] = self.get_last_post_title(sel)
        forum_meta['last_post_url'] = self.get_last_post_url(sel)
        forum_meta['last_post_published_date'] = self.get_last_post_published_date(sel)
        forum_meta['last_post_published_time'] = self.get_last_post_published_time(sel)
        forum_meta['total_threads'] = self.get_total_forum_threads(sel)
        forum_meta['total_posts'] = self.get_total_forum_posts(sel)

        is_scrape_forum_path = self.forum_paths.get(self.get_forum_url(sel).rstrip('/'), '')
        if is_scrape_forum_path:
            forum_meta['scrape_forum_path'] = is_scrape_forum_path

        return forum_meta

    def get_forum_title(self, sel):
        return clean(sel.css('h3 a ::text').get())

    def get_forum_url(self, sel):
        return sel.css('h3 a::attr(href)').get('').rstrip('/')

    def get_forum_desc(self, sel):
        return clean(sel.css('h3 + div.smallfont::text').get())

    def get_last_post_title(self, sel):
        return clean(sel.css('.lastpost a ::text').get())

    def get_last_post_url(self, sel):
        return sel.css('.lastpost .text-right a::attr(href)').get()

    def get_last_post_published_date(self, sel):
        return self.get_appropriate_date(clean(sel.css('.lastpost .text-right::text').get()))

    def get_last_post_published_time(self, sel):
        return clean(sel.css('.lastpost .text-right .time::text').get())

    def get_total_forum_threads(self, sel):
        return clean(sel.css('.threadcount::text').get())

    def get_total_forum_posts(self, sel):
        return clean(sel.css('.postcount::text').get())


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(MBWorldMetaSpider)
    process.start()
