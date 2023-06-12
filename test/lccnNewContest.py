

# lccn上是不是有新的竞赛
# LC.cn 上最新的是第几场

from graphqlclient import GraphQLClient
import json
from icecream import ic
import re
import requests

def lccnLastContestNumber():
    client = GraphQLClient('https://leetcode.cn/graphql/noj-go/')
    query = '''
    query userContestRankingInfo($userSlug: String!) {
    userContestRanking(userSlug: $userSlug) {
        attendedContestsCount
        rating
    }
    userContestRankingHistory(userSlug: $userSlug) {
        attended
        trendingDirection
        rating
        contest {
        title
        }
    }
    }
    '''
    Name="谭邵杰"
    LCName = "shaojiemike"
    variables = {
    "userSlug":LCName
    }

    result = client.execute(query=query, variables=variables)
    t = json.loads(result)

    # for item in t['data']['userContestRanking']:
    #     print (item)
    #     ic(item)
    # print(t['data']['userContestRanking']['rating'])
    LCData = []
    LCData += [[
            "score",
            "Name",
            "contest number",
            "contest name"
        ]]

    contest = t['data']['userContestRankingHistory'][-1]
    ic(contest)

    lcContestNumber=0
    if re.match("第 ([0-9]*) 场周赛",contest['contest']['title']):
        lcContestNumber=int(re.match("第 ([0-9]*) 场周赛",contest['contest']['title']).group(1))
        lcContestNumber=lcContestNumber*2
    else:
        lcContestNumber=int(re.match("第 ([0-9]*) 场双周赛",contest['contest']['title']).group(1))
        lcContestNumber=lcContestNumber*4+273
    ic(lcContestNumber)
    return lcContestNumber

def predictNewContestNumber():
    url = "https://lccn.lbao.site/api/v1/contests/?skip=0&limit=2"

    response = requests.get(url)
    data = response.json()
    ic(data)
    result = []
    for contest in data:
        title = contest["title"]
        # ic(title)
        lcContestNumber=0
        if re.match("Weekly Contest ([0-9]*)",title):
            lcContestNumber=int(re.match("Weekly Contest ([0-9]*)",title).group(1))
            lcContestNumber=lcContestNumber*2
        else:
            lcContestNumber=int(re.match("Biweekly Contest ([0-9]*)",title).group(1))
            lcContestNumber=lcContestNumber*4+273
        ic(lcContestNumber)
        result.append(lcContestNumber)
    return result
    
lastLCCN = lccnLastContestNumber()
result = predictNewContestNumber()
for newContestNumber in result:
    if(newContestNumber > lastLCCN):
        print(newContestNumber)
