from graphqlclient import GraphQLClient
import json


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

def crawlerCnByName(LCName):
    variables = {
        "userSlug":LCName
    }
    result = client.execute(query=query, variables=variables)
    return json.loads(result)