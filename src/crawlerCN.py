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

client2 = GraphQLClient('https://leetcode.cn/graphql/')

query2 = '''
query userQuestionProgress($userSlug: String!) {
  userProfileUserQuestionProgress(userSlug: $userSlug) {
    numAcceptedQuestions {
      difficulty
      count
    }
    numFailedQuestions {
      difficulty
      count
    }
    numUntouchedQuestions {
      difficulty
      count
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

def questionCnByName(LCName):
  variables = {
  "userSlug":LCName
  }

  result = client2.execute(query=query2, variables=variables)
  t = json.loads(result)
  e = 0
  h = 0
  m = 0
  for item in t['data']['userProfileUserQuestionProgress']['numAcceptedQuestions']:
    if item['difficulty'] == 'EASY':
      e=item['count']
    if item['difficulty'] == 'MEDIUM':
      m=item['count']
    if item['difficulty'] == 'HARD':
      h=item['count']
  return [e,h,m]