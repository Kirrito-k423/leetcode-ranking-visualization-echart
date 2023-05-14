
# 参考：https://blog.csdn.net/qq_32424059/article/details/106071201

# 找到 userContestRankingInfo

import requests, urllib
from bs4 import BeautifulSoup
import json
 
USERNAME = "shaojiemike"
name = "graphql/noj-go"
oprationName = "userContestRankingInfo"
url = "https://leetcode.cn/"+name+"?"+\
        "operationName=" + oprationName + \
        "&variables={%22userSlug%22:%22" + USERNAME + "%22}"+\
        "&query=\n    query userContestRankingInfo($userSlug:String!) {\n  userContestRanking(userSlug: $userSlug) {\n    attendedContestsCount\n    rating\n    globalRanking\n    localRanking\n    globalTotalParticipants\n    localTotalParticipants\n    topPercentage\n  }\n  userContestRankingHistory(userSlug: $userSlug) {\n    attended\n    totalProblems\n    trendingDirection\n    finishTimeInSeconds\n    rating\n    score\n    ranking\n    contest {\n      title\n      titleCn\n      startTime\n    }\n  }\n}\n    "


def open_url(url):
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/5'
                          '37.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    req = urllib.request.Request(url, headers=head)
    response = urllib.request.urlopen(req)
 
    html = response.read()
    html_str = html.decode('utf-8')
    t = json.loads(html_str)
 
    for item in t['data']['userContestRankingHistory']:
        print (item)
 
 
if __name__ == '__main__':
    url = url.replace(" ", "%20")
    url = url.replace("%20%20", "%20")
    url = url.replace("%20%20", "%20")
    url = url.replace("%20%20", "%20")
    # url = url.replace("%22", "")  this is \"\"
    url = url.replace("\n", "")
    print(url)
    open_url(url)