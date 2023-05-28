from icecream import ic
import re
import config  # 加载配置
import global_variable as glv
import copy
from crawlerCN import crawlerCnByName
from crawlerCom import crawlerComByName
import json



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

    taskList = glv._get("cnTaskList")
    taskList2 = glv._get("comTaskList")

    LCData = []

    # 先统计每个人参加的所有不同的场次
    joinedContest = set()
    # 国内
    for Name, LCName in taskList.items():
        t = crawlerCnByName(LCName)
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
    # 国外
    for Name, LCName in taskList2.items():
        t = crawlerComByName(LCName)
        for contest in t['data']['userContestRankingHistory']:
            if contest['attended'] == True:
                ic(contest)
                lcContestNumber=0
                if re.match("Weekly Contest ([0-9]*)",contest['contest']['title']):
                    lcContestNumber=int(re.match("Weekly Contest ([0-9]*)",contest['contest']['title']).group(1))
                    lcContestNumber=lcContestNumber*2
                else:
                    lcContestNumber=int(re.match("Biweekly Contest ([0-9]*)",contest['contest']['title']).group(1))
                    lcContestNumber=lcContestNumber*4+273
                ic(lcContestNumber)
                joinedContest.add(lcContestNumber)
    ic(joinedContest)

    # 然后各场次读取分数的数据
    # 国内
    for Name, LCName in taskList.items():
        tmpList = []
        t = crawlerCnByName(LCName)
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
        # 补全，使得每人的分数连续
        LCData+=fullList(tmpList, joinedContest)

    # 国内
    for Name, LCName in taskList2.items():
        tmpList = []
        t = crawlerComByName(LCName)
        for contest in t['data']['userContestRankingHistory']:
            if contest['attended'] == True:
                # ic(contest)
                lcContestNumber=0
                cnTile = ""
                if re.match("Weekly Contest ([0-9]*)",contest['contest']['title']):
                    lcContestNumber=int(re.match("Weekly Contest ([0-9]*)",contest['contest']['title']).group(1))
                    cnTile = "第 {} 场周赛".format(lcContestNumber)
                    lcContestNumber=lcContestNumber*2    
                else:
                    lcContestNumber=int(re.match("Biweekly Contest ([0-9]*)",contest['contest']['title']).group(1))
                    cnTile = "第 {} 场双周赛".format(lcContestNumber)
                    lcContestNumber=lcContestNumber*4+273
                # ic(lcContestNumber)
                tmp=[int(contest['rating']), Name,\
                    lcContestNumber, cnTile]
                tmpList.append(tmp)
                ic(tmp)
        # ic(tmpList)
        # 补全，使得每人的分数连续
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