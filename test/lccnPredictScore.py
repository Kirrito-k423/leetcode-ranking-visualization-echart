from icecream import ic
import requests
def getPredictScore(contestNum, username):
    if contestNum % 2 == 0:
        contest_name = "weekly-contest-{}".format(contestNum // 2)
    else:
        contest_name = "biweekly-contest-{}".format((contestNum-273)//4)
    url = ("https://lccn.lbao.site/api/v1/contest-records/"
       f"user?contest_name={contest_name}"
       f"&username={username}&archived=false")
    response = requests.get(url)
    data = response.json()
    ic(data)
    ic(data[0]['new_rating'])


getPredictScore(698, "shaojiemike")
getPredictScore(697, "chivier")
getPredictScore(697, "iBug")
getPredictScore(698, "iBug")