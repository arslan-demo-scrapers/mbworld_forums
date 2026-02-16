# MBWorld Forums Scraper -- Setup & Run Guide

## Overview

This tool is built using **Python 3.9** and the **Scrapy Framework**.\
Please install **Python 3.x (latest version recommended)** before
proceeding.

------------------------------------------------------------------------

# How to Setup & Run Spiders

## Step 1 -- Install Development Environment & Dependencies

### Install IDE (Recommended)

Download and install **PyCharm Community Edition**:
https://www.jetbrains.com/pycharm/download/

------------------------------------------------------------------------

### Install Required Python Packages

Open terminal and run:

``` bash
pip install scrapy==2.13.4
pip install elasticsearch
pip install scrapy-rotating-proxies
pip install scrapeops-scrapy==0.5.6
```

------------------------------------------------------------------------

### Install ElasticSearch

Follow official guide:
https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html

⚠ Make sure your project interpreter is set correctly where Scrapy is
installed.

------------------------------------------------------------------------

# Proxy Configuration

## Where to Add Proxies

Add only activated HTTP proxies and one proxy per line inside:

    resources/proxies.txt

This file must be placed in the project root directory.

------------------------------------------------------------------------

## Proxy Format

    Server-IP-Address:Port

Examples:

    us-wa.proxymesh.com:31280
    123.241.162.321:29842

------------------------------------------------------------------------

## Proxy Authentication

If authentication is required, add credentials inside `.env` file in
project root:

    PROXY_USERNAME=your_proxy_username
    PROXY_PASSWORD=your_proxy_password

⚠ Ensure: - Proxy service is active - Your IPv4 address is whitelisted
if required - Only working proxies are used

------------------------------------------------------------------------

# Step 2 -- Run the Spiders

Before running, navigate to:

    /mbworld_forums/mbworld_forums/spiders

------------------------------------------------------------------------

## Run Meta Spider

``` bash
python3 -m mbworld_meta_spider.py
```

OR

``` bash
scrapy crawl mbworld_meta_spider
```

This spider scrapes forum metadata.

------------------------------------------------------------------------

## Run Threads Spider

``` bash
python3 -m mbworld_spider
```

OR

``` bash
scrapy crawl mbworld_spider
```

This spider scrapes forum threads data.

------------------------------------------------------------------------

# Step 3 -- Output & Data Storage

After execution:

### mbworld_meta_spider

-   Stores meta information files inside `output` directory.

### mbworld_spider

-   Extracts forum threads data
-   Inserts scraped data directly into ElasticSearch

⚠ Ensure ElasticSearch service is running before executing spiders.

------------------------------------------------------------------------

# Support

For any queries or assistance, feel free to contact.

------------------------------------------------------------------------

Best Regards,\
Arslan Shakar
