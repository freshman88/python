"""
spider
"""


from urllib import request
from urllib.parse import urlparse,urljoin
from bs4 import BeautifulSoup
from mydb import SiteService,InnerUrlService,OuterUrlService,FetchFailedUrlService

from urllib.error import URLError, HTTPError


def fetch_task(url,baseurl):
    try:
        print('fetching url: '+url)
        response=request.urlopen(url)
        content=response.read()

        site_serv.put(url,content)
        innerurl_serv.put(baseurl,url)
        print('fetched url: '+url)        

        soup=BeautifulSoup(content)
        for tag in soup.find_all('a'):
            if not tag.has_attr('href'):
                continue
            href=tag['href']
            if href.startswith('#') or href.startswith('javascript:'):
                continue
            if not urlparse(href).scheme:
                # related path
                sub_url=urljoin(url,href)
                fetch_set.add(sub_url)
            else:
                # absolute path
                outerurl_serv.put(baseurl,href)

        # print(soup.prettify())
    except URLError as e:
        failed_url_serv.put(baseurl,url)
        print('fetch failed! url: '+url)
        print(e)

def fetch(url):
    fetch_set.add(url)
    while fetch_set.__len__() > 0:
        sub_url=fetch_set.pop()
        if sub_url not in fetched_set:
            fetch_task(sub_url, url)
            fetched_set.add(sub_url)
    print('Done!')


myurl='http://www.w3school.com.cn'
# myurl='http://172.16.128.165/swagger/'

fetch_set=set()
fetched_set=set()
site_serv=SiteService()
innerurl_serv=InnerUrlService()
outerurl_serv=OuterUrlService()
failed_url_serv=FetchFailedUrlService()
fetch(myurl)

# print all
# site_serv=SiteService(reload=False)
# for row in site_serv.find_all_url():
#     print(row)
# innerurl_serv=InnerUrlService(reload=False)
# for row in innerurl_serv.find_all():
#     print(row)
# print(site_serv.find_content('http://172.16.128.165/swagger/'))

# outerurl_serv=OuterUrlService(reload=False)
# for row in outerurl_serv.find_all():
#     print(row)
