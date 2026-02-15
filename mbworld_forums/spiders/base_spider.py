import os

from scrapy import Spider

from mbworld_forums.mbworld_forums.static import forum_meta_headers, handle_httpstatus_list
from mbworld_forums.mbworld_forums.utils.clean_utils import clean
from mbworld_forums.mbworld_forums.utils.date_time_utils import get_today, get_tomorrow_date, \
    get_yesterday_date, convert_date_to_mysql_format
from mbworld_forums.mbworld_forums.utils.file_utils import write_to_csv, delete_file, \
    get_csv_records, get_json_records, get_jl_records

try:
    from mbworld_forums.mbworld_forums.local_elasticsearch import ElasticSearchConfig
except Exception as err:
    from mbworld_forums.mbworld_forums.elastic_search import ElasticSearchConfig


class BaseSpider(Spider):
    name = "base_spider"
    filepath = '../output/post_ids.csv'
    forum_meta_filepath = '../forum_meta_files'
    forum_meta_filepath = f'{forum_meta_filepath}/base_meta.csv'
    base_url = 'https://quotes.toscrape.com/'

    start_urls = [
        base_url,
    ]

    file_headers = [
        "id", "message_id",
        # "make", "model", "creation_time", "date_published",
        # "page_url", "author", "subject", "body", "forum_path", "post_type", "date_modified",
    ]

    forum_meta_headers = [
        "scrape_forum_path", "forum_title", "forum_url", "last_post_title", "last_post_url",
        "last_post_published_date", "last_post_published_time", "total_threads", "total_posts",
        "forum_description",
    ]

    meta = {
        'handle_httpstatus_list': handle_httpstatus_list,
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    forum_meta_default_item = {
        'scrape_forum_path': 1
    }

    def __init__(self, index=None, pipeline=None, **kwargs):
        super().__init__(**kwargs)
        self.index_arg = index
        self.pipeline_arg = pipeline
        self.forum_paths = self.get_forum_paths(self.forum_meta_filepath)
        self.scraped_message_ids = self.get_scraped_threads_ids(self.filepath)
        self.elastic_search = ElasticSearchConfig(forum_index=self.index_arg or self.name.strip('_spider'))

    def clean_make_model(self, text, junkies=[]):
        junk_data = [
            'Forums', 'Vendor', 'Classifieds', 'Vehicles', 'Forum',
            'Aftermarket Products, Reviews & Installation', 'Member meet ups!', 'Engines',
            'Suspension', 'Lighting', 'Stereo/Audio', 'Custom Offsets', 'Wheels & Tires',
            'General Truck Tech', 'Truck Talk'
        ]

        if junkies:
            junk_data += junkies

        for e in junk_data:
            text = clean(text.replace(e, ''))
        return clean(text)

    def get_appropriate_date(self, str_date):
        if 'yesterday' in str_date.lower() or 'day' in str_date.lower():
            return get_yesterday_date()
        elif 'tomorrow' in str_date.lower():
            return get_tomorrow_date()
        elif 'today' in str_date.lower() or 'hour' in str_date.lower() or 'minute' in str_date.lower():
            return get_today()
        return convert_date_to_mysql_format(str_date)

    def get_scraped_threads_ids(self, filepath):
        if '.csv' in filepath:
            return [r['message_id'] for r in get_csv_records(filepath) if r]
        elif '.json' in filepath:
            return [r['message_id'] for r in get_json_records(filepath) if r]

        return [r['message_id'] for r in get_jl_records(filepath) if r]

    # def get_scraped_threads_ids_set(self, filepath):
    #     if '.csv' in filepath:
    #         return {r['id'] for r in get_csv_records(filepath) if r}
    #     elif '.json' in filepath:
    #         return {r['id'] for r in get_json_records(filepath) if r}
    #
    #     return {r['id'] for r in get_jl_records(filepath) if r}

    def update_forum_meta_file(self, forum_meta_records):
        delete_file(self.forum_meta_filepath)

        for rec in forum_meta_records:
            write_to_csv(rec, self.forum_meta_filepath, forum_meta_headers)

    def get_forum_paths(self, filepath):
        return {r['forum_url'].rstrip('/'): r['scrape_forum_path'] for r in get_csv_records(filepath)
                if r and r.get('scrape_forum_path')}

    def get_csv_writer(self, filepath, csv_headers):
        if not os.path.exists(filepath) or self.has_records(filepath) < 1:
            file = open(filepath, mode='w', encoding='utf-8')
            file.write(','.join(h for h in csv_headers) + '\n')
            return file

        return open(filepath, mode='a+', encoding='utf-8')

    def has_records(self, filepath):
        if not os.path.exists(filepath):
            return 0
        # return len([r for r in DictReader(open(filepath, encoding='utf-8')) if r])
        return len([clean(r) for r in open(filepath, encoding='utf-8').readlines()[:5] if clean(r)])

    def write_to_csv(self, item, filepath, csv_headers):
        if not item:
            return
        row = ','.join('"{}"'.format(item.get(h, '')) for h in csv_headers) + '\n'
        csv_writer = self.get_csv_writer(filepath, csv_headers)
        csv_writer.write(row)
        csv_writer.close()
        print(f"Forum meta record inserted into a csv file-> {filepath}\n{item}")
