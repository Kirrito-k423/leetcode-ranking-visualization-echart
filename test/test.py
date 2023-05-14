import requests, urllib
from bs4 import BeautifulSoup
import json
 
USERNAME = "awayfuture-tfjify50il"
url = "https://leetcode-cn.com/graphql?oprationName=recentSubmissions&variables={%22userSlug%22:%22" + USERNAME + "%22}&query=query%20recentSubmissions($userSlug:%20String!){recentSubmissions(userSlug:%20$userSlug){status%20lang%20question{questionFrontendId%20title%20translatedTitle%20titleSlug%20__typename}submitTime%20__typename}}"
 
def open_url(url):
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/5'
                          '37.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    req = urllib.request.Request(url, headers=head)
    response = urllib.request.urlopen(req)
 
    html = response.read()
    html_str = html.decode('utf-8')
    t = json.loads(html_str)
 
    for item in t['data']['recentSubmissions']:
        print (item)
 
 
if __name__ == '__main__':
    open_url(url)