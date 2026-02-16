### How to run spider script after make setup & configuration
### *******  How to Setup & Run Spiders Documentation *******

### The tool is made in python 3
extract it to your system.

### *** Step-1 ***
````
-> You need to install an IDE for managing project. Please  
    download and install Editor PyCharm Community Edition.

-> you need to install scrapy, just open terminal
 window in pycharm and write command:
````
> `pip install scrapy`

> `pip install scrapy-rotating-proxies`

> `pip install elasticsearch`

> `pip install scrapeops-scrapy==0.5.6` 

#### ElasticSearch [Installation / Setup Tutorial](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html)

### Note: ** Please add only activated proxies into "proxies.txt" file located 
### in spiders folder **

### Note: Now Set your project interpreter in which you have scrapy installed.

### ** Where to Add Proxies **
````
In proxies.txt file, please add your http proxies. Format should be like 
 Server-IP-Address:Port like us-wa.proxymesh.com:31280.

You will also need to add proxies username and password for proxies
 authentication in .env file, that file should be placed in project root folder.
 Here are the variables:
 
PROXY_USERNAME=your_proxy_username
PROXY_PASSWORD=your_proxy_password

````
**Note:** Also, make check your proxy service and may be you will need to add your
 system IPV4 Address on Proxies Server for authentication purpose. proxies 
 have been integrated now and like previously we did in scraped.



### *** Step-2 ***
#### Before running make What to make sure control is in the folder
`/mbworld_forums/mbworld_forums/spiders`

### Run web scraping script command:

> python3 -m mbworld_meta_spider.py

or 

> scrapy crawl mbworld_meta_spider

**Note:** "mbworld_meta_spider" is the name of spider, that scrape forums meta data.

> python3 -m mbworld_spider

or

> scrapy crawl mbworld_spider

**Note:** "mbworld_spider" is the name of spider, that scrape forums threads data.


### *** Step-3 ***
#### Now where will you get the output?
````
when you run script after completed Script execution, `mbworld_meta_spider` script will store the meta information file in `output` directory.
The spider `mbworld_spider` will extract and insert the forums threads data via ElasticSearch.
````
### ** Elastic search implemented **

````
*** Step-4 ***
for any query please send me message.
````

#### Best Regards,
### Arslan Shakar
