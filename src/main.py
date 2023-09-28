from icecream import ic
import re
import config  # 加载配置
import global_variable as glv
import copy
from crawlerCN import crawlerCnByName, questionCnByName
from crawlerCom import crawlerComByName
import json
from predictInfo import *
import random
import time


# take second element for sort
def takeSecond(elem):
    return elem[2]

def take4(elem):
    return elem[4]

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

def contestInfo():

    taskList = glv._get("cnTaskList")
    taskList2 = glv._get("comTaskList")

    LCData = []

    ic("先统计每个人参加的所有不同的场次")
    joinedContest = set()
    addContest = set()
    ic("国内")
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
    ic("国外")
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
                
    ic("预测的比赛")
    lastLCCN = lccnLastContestNumber()
    result = predictNewContestNumber()
    ic(lastLCCN, result)
    for newContestNumber in result:
        # if(newContestNumber > lastLCCN):
        print(newContestNumber)
        joinCount = 0
        for Name, LCName in taskList.items():
            sleep_time = random.uniform(0.5, 1)
            time.sleep(sleep_time)
            if getPredictScore(newContestNumber, glv._get("predictName")[Name]):
                joinCount += 1
        for Name, LCName in taskList2.items():
            sleep_time = random.uniform(0.5, 1)
            time.sleep(sleep_time)
            if getPredictScore(newContestNumber, glv._get("predictName")[Name]):
                joinCount += 1
        ic(joinCount)
        if joinCount > 0:
            joinedContest.add(newContestNumber)
            addContest.add(newContestNumber)
    ic(joinedContest)
    ic(addContest)

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
        for addContestNum in addContest:
            sleep_time = random.uniform(0.5, 1)
            time.sleep(sleep_time)
            score = getPredictScore(addContestNum, glv._get("predictName")[Name])
            if score:
                if addContestNum % 2 == 0:
                    cnTile = "第 {} 场周赛".format(addContestNum // 2)
                else:
                    cnTile = "第 {} 场双周赛".format((addContestNum-273)//4)
                tmp=[int(score), Name,\
                        addContestNum, cnTile]
                tmpList.append(tmp)       
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
        for addContestNum in addContest:
            sleep_time = random.uniform(0.5, 1)
            time.sleep(sleep_time)
            score = getPredictScore(addContestNum, glv._get("predictName")[Name])
            if score:
                if addContestNum % 2 == 0:
                    cnTile = "第 {} 场周赛".format(addContestNum // 2)
                else:
                    cnTile = "第 {} 场双周赛".format((addContestNum-273)//4)
                tmp=[int(score), Name,\
                        addContestNum, cnTile]
                tmpList.append(tmp)  
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

def questionInfo():
    # Retrieve the exercise count information for each user, including items of varying difficulty levels such as simple, intermediate, and challenging questions.
    taskList = glv._get("cnTaskList")

    # 国内
    sortData = []
    nameData = []
    HARDData = []
    MEDIUMData = []
    EASYData = []
    for Name, LCName in taskList.items():    
        [e, h, m ] = questionCnByName(LCName)
        ic(LCName,e,h,m)
        sortData.append([Name,e,h,m,e+h+m])


    sortData.sort(key=take4)
    for [Name, e, h, m, sum] in sortData:
        nameData+=[Name]
        HARDData.append(h)
        MEDIUMData.append(m)
        EASYData.append(e)
    questionData = []
    questionData.insert(0,nameData)
    questionData.insert(1,HARDData)
    questionData.insert(2,MEDIUMData)
    questionData.insert(3,EASYData)
    my_list_json = json.dumps(questionData)
    with open('question.json', 'w') as f:
        f.write(my_list_json)

    
if __name__ == "__main__":
    contestInfo()
    questionInfo()