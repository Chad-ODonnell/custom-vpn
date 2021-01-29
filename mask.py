# lxml is for parsing XML and HTML, needed for grabbing open IPs.
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback

# Author: Chad O'Donnell
# Purpose: To hide user's IP address with various other IPs.
# Credits: ScrapeHero helped me figure out how to implement this program, I modified it to make it happen.
# Additional Credits: The Hitchhiker's Guide to Python - HTML Scraping.

def get_proxies():
    # Not hard coding URL to give User ability to edit later.
    url_1 = 'https://free-proxy-list.net/'
    response = requests.get(url_1)
    parser = fromstring(response.text)
    proxies = set()
    # This is where we'll start using Website Scrapping - Gathering data from web in needed format.
    # We'll only be collecting the first 10 URLs on free-proxy-list.net. //tbody/tr is the HTML we'll be pulling from.
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


# If you are copy pasting proxy ips, put in the list below
# proxies = ['121.129.127.209:80', '124.41.215.238:45169', '185.93.3.123:8080', '194.182.64.67:3128', '106.0.38.174:8080', '163.172.175.210:3128', '13.92.196.150:8080']
proxies = get_proxies()
# This is used for storing the proxies which we'll use a pool to rotate through later on.
proxy_pool = cycle(proxies)


# Not hard coding URL to give User ability to edit later.
url_2 = 'https://httpbin.org/ip'
for i in range(1,11):
    # Get a proxy from our pool.
    proxy = next(proxy_pool)
    print("Request #%d"%i)
    try:
        response = requests.get(url_2,proxies={"http": proxy, "https": proxy})
        print(response.json())
    except:
        print("Skipping. Connnection error")