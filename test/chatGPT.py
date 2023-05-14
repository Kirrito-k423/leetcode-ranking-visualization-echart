from graphqlclient import GraphQLClient
import json
from icecream import ic
import re
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

for contest in t['data']['userContestRankingHistory']:
  if contest['attended'] == True:
    # ic(contest)
    lcContestNumber=0
    if re.match("第 ([0-9]*) 场周赛",contest['contest']['title']):
      lcContestNumber=int(re.match("第 ([0-9]*) 场周赛",contest['contest']['title']).group(1))
      lcContestNumber=lcContestNumber*2
    else:
      lcContestNumber=int(re.match("第 ([0-9]*) 场双周赛",contest['contest']['title']).group(1))
      lcContestNumber=lcContestNumber*4+273
    # ic(lcContestNumber)
    tmp=[int(contest['rating']), Name,\
        lcContestNumber, contest['contest']['title']]
    ic(tmp)
    LCData.append(tmp)
ic(LCData)
my_list_json = json.dumps(LCData)
with open('my_list.json', 'w') as f:
  f.write(my_list_json)
