from graphqlclient import GraphQLClient
import json
from icecream import ic
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

variables = {
  "userSlug":"shaojiemike"
}

result = client.execute(query=query, variables=variables)
t = json.loads(result)

for item in t['data']['userContestRanking']:
    print (item)
    ic(item)
print(t['data']['userContestRanking']['rating'])