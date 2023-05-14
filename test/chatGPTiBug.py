import requests
import json
from icecream import ic
import re

headers = {
    'Content-Type': 'application/json',
    'Referer': 'https://leetcode.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
    'x-csrftoken': 'bH9n9V75FEQC2zbciE2gGgaHSxF7u23FWDp87BooR0ANoDE0n6bM6vA323NB1ygH'
}

url = 'https://leetcode.com/graphql/'

query = '''

    query userContestRankingInfo($username: String!) {
  userContestRanking(username: $username) {
    attendedContestsCount
    rating
    globalRanking
    totalParticipants
    topPercentage
    badge {
      name
    }
  }

  userContestRankingHistory(username: $username) {
    attended
    rating
    contest {
      title
    }
  }
}
    
'''

data = {
    "query": query,
    "variables": {
        "username": "ibug"
    },
    "operationName": "userContestRankingInfo"
}

payload = json.dumps(data)

response = requests.post(url, headers=headers, data=payload)
t = json.loads(response.text)

LCData = []
LCData += [[
        "score",
        "Name",
        "contest number",
        "contest name"
    ]]

# for item in t['data']['userContestRanking']:
#     print (item)
#     ic(item)
# print(t['data']['userContestRanking']['rating'])

for contest in t['data']['userContestRankingHistory']:
  if contest['attended'] == True:
    ic(contest)
    # lcContestNumber=0
    # if re.match("第 ([0-9]*) 场周赛",contest['contest']['title']):
    #   lcContestNumber=int(re.match("第 ([0-9]*) 场周赛",contest['contest']['title']).group(1))
    #   lcContestNumber=lcContestNumber*2
    # else:
    #   lcContestNumber=int(re.match("第 ([0-9]*) 场双周赛",contest['contest']['title']).group(1))
    #   lcContestNumber=lcContestNumber*4+273
    # # ic(lcContestNumber)
    # tmp=[int(contest['rating']), Name,\
    #     lcContestNumber, contest['contest']['title']]
    # ic(tmp)
    # LCData.append(tmp)
# ic(LCData)