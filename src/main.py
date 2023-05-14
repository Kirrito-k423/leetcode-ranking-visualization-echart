from graphqlclient import GraphQLClient
import json
from icecream import ic
import re
import config  # 加载配置
import global_variable as glv
import copy


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

# take second element for sort
def takeSecond(elem):
    return elem[2]

def correctContestName(result):
    for item in result:
        if item[2] % 2 == 1:
            item[3] = "第 " + str(int((item[2]-273)/4)) + " 场双周赛"
        else:
            item[3] = "第 " + str(int(item[2]/2)) + " 场周赛"
    return result

def fullList(tmpList, joinedContest):
    result = []
    for contestNum in joinedContest:
        flag = False
        for i in range(len(tmpList)):
            item = tmpList[i]
            if contestNum < item[2] and i==0:
                tmp = copy.deepcopy(item)
                tmp[2] = copy.deepcopy(contestNum)
                result.append(tmp)
                flag = True
                break
            elif contestNum < item[2]:
                tmp = copy.deepcopy(tmpList[i-1])
                tmp[2] = copy.deepcopy(contestNum)
                result.append(tmp)
                flag = True
                break
        if not flag:
            tmp = copy.deepcopy(tmpList[i])
            tmp[2] = copy.deepcopy(contestNum)
            result.append(tmp)
    result.sort(key=takeSecond)
    return correctContestName(result)

def main():

    taskList = glv._get("taskList")
    LCData = []

    joinedContest = set()
    for Name, LCName in taskList.items():
        variables = {
            "userSlug":LCName
        }

        result = client.execute(query=query, variables=variables)
        t = json.loads(result)

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
                joinedContest.add(lcContestNumber)
    ic(joinedContest)
    for Name, LCName in taskList.items():
        tmpList = []
        variables = {
            "userSlug":LCName
        }

        result = client.execute(query=query, variables=variables)
        t = json.loads(result)

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
                tmpList.append(tmp)
                ic(tmp)
        # ic(tmpList)
        LCData+=fullList(tmpList, joinedContest)
    LCData.sort(key=takeSecond)
    ic(LCData)
    LCData.insert(0,[
                "score",
                "Name",
                "contest number",
                "contest name"
            ])
    # ic(LCData)
    my_list_json = json.dumps(LCData)
    with open('my_list.json', 'w') as f:
        f.write(my_list_json)

if __name__ == "__main__":
    main()