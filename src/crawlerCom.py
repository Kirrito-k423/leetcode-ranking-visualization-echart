import requests
import json

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

def crawlerComByName(LCName):
    data = {
        "query": query,
        "variables": {
            "username": LCName
        },
        "operationName": "userContestRankingInfo"
    }
    payload = json.dumps(data)

    response = requests.post(url, headers=headers, data=payload)
    return json.loads(response.text)