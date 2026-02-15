forum_meta_filepath = '../forum_meta_files'

handle_httpstatus_list = [
    400, 401, 402, 403, 404, 405, 406, 407, 409, 412,
    500, 501, 502, 503, 504, 505, 506, 507, 509,
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
