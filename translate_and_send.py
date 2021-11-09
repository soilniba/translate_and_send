import json
import demjson
import random
import uuid
import hashlib
import time
from typing import Text
import requests
from flask import Flask
from flask import request
app = Flask(__name__)
wx_robot_key = 'c57c249e-ed34-4e37-9064-dad5004d6420'
feishu_robot_key = '86b74a8b-d1d4-4965-ad4f-56aec55f298a'
# https://open.feishu.cn/open-apis/bot/v2/hook/86b74a8b-d1d4-4965-ad4f-56aec55f298a
# @app.route('/', methods=['POST','GET'])
# def index():
#     json_table = request.get_json()
#     print(json.dumps(json_table))
#     return json_table

@app.route('/translate',methods=['POST','GET'])
def translate():
    try:
        if request.method=='POST':
            url_args = request.args
            print(url_args)
            print(url_args.get("UserName"))
            print(url_args.get("LinkToTweet"))
            print(url_args.get("CreatedAt"))
            post_data = request.get_data()
            print(post_data)

            Text = post_data.decode('utf-8')
            UserName = url_args.get("UserName")
            LinkToTweet = url_args.get("LinkToTweet")
            CreatedAt = url_args.get("CreatedAt")

            # # json_table = request.get_json(force=True)
            # json_table = demjson.encode(post_data)
            # # json_table = json.loads(post_data)
            # print(json.dumps(json_table))
            # Text = json_table['Text']
            # UserName = json_table['UserName']
            # LinkToTweet = json_table['LinkToTweet']
            # CreatedAt = json_table['CreatedAt']

            try:
                # TranslatorText = SelectTranslator(Text)
                # print(TranslatorText)

                # # 发送到微信机器人
                # wx_content = "{} **[@{}](https://twitter.com/{})** \n {}\n{}\n\n[{}]({})\n".format(
                #             CreatedAt,
                #             UserName,
                #             UserName,
                #             Text,
                #             TranslatorText,
                #             LinkToTweet,
                #             LinkToTweet
                #         )
                # send_wx_robot(wx_robot_key, wx_content)

                # 发送到飞书机器人
                feishu_content = {"content": []}
                # feishu_content["title"] = TranslatorText
                feishu_content["content"].append([
                    {
                        "tag": "a",
                        "text": CreatedAt,
                        "href": LinkToTweet
                    },
                    # {
                    #     "tag": "a",
                    #     "text": UserName,
                    #     "href": 'https://twitter.com/' + UserName
                    # },
                ])
                feishu_content["content"].append([
                    {
                        "tag": "text",
                        "text": "\n{}".format(Text),
                        # "text": "\n{}\n\n{}".format(Text, LinkToTweet),
                        # "text": "\n{}\n{}\n\n{}".format(Text, TranslatorText, LinkToTweet),
                    },
                ])
                send_feishu_robot(feishu_robot_key, feishu_content)
            except:
                print('translator error')
    except:
        print('post error')
    return {}

def send_wx_robot(robot_key, content):
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({
        "msgtype": "markdown", 
        "markdown": { "content": content },
    })
    response = requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + robot_key, headers=headers, data=data)

def send_feishu_robot(robot_key, content):
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": content
            }
        }
    })
    response = requests.post('https://open.feishu.cn/open-apis/bot/v2/hook/' + robot_key, headers=headers, data=data)
    print(response)

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '36044cb9bfbba320'
APP_SECRET = 'bmPfUNL8xii05KpjfqgF2Q8XFWtlWwKz'

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()

def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)

def youdao(q):
    # q = "json() returns a JSON object of the result (if the result was written in JSON format, if not it raises an error). Python requests are generally used to fetch the content from a particular resource URI. Whenever we make a request to a specified URI through Python, it returns a response"
    data = {}
    data['from'] = 'auto'
    data['to'] = 'zh-CHS'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    # data['vocabId'] = "您的用户词表ID"

    response = do_request(data)
    # print(response.content)
    json_data = json.loads(response.text)
    # print(json.dumps(json_data))
    # print(json_data['translation'][0])
    return json_data['translation'][0]

def caiyun(source):
    direction = 'auto2zh'
    url = "http://api.interpreter.caiyunai.com/v1/translator"
    #WARNING, this token is a test token for new developers, and it should be replaced by your token
    token = "1k9v5nhzo36ukir8cs7y"

    payload = {
            "source" : source, 
            "trans_type" : direction,
            "request_id" : "demo",
            "detect": True,
            }

    headers = {
            'content-type': "application/json",
            'x-authorization': "token " + token,
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    return json.loads(response.text)['target']

def SelectTranslator(text):
    # TranslatorList = [caiyun, youdao]
    # fnTranslator = random.choice(TranslatorList)
    RandomInt = random.randint(1,10)
    if RandomInt <= 5:
        returntest = '[有道]\n' + youdao(text)
    else:
        returntest = '[彩云]\n' + caiyun(text)
    return returntest

# source = "Lingocloud is the best translation service."
# target = SelectTranslator(source)
# print(target)

if __name__=='__main__':
    app.run(
        debug = True,
        port = 952,
        host = '0.0.0.0',
        # ssl_context=('sg.gjol.vip.pem', 'sg.gjol.vip.key')
    )

    # test测试
    # Text = ' Starlink is designed for low to medium population density, which means we can hit max users in some areas fast. \nPlease sign up early to ensure a spot. As more satellites roll out, SpaceX will be able to serve more. \nhttps://t.co/Q1VvqVmJ2i\n'
    # UserName = 'elonmusk'
    # LinkToTweet = 'https://twitter.com/elonmusk/status/1446125877494833162'
    # CreatedAt = 'October 07, 2021 at 10:50PM'
    # TranslatorText = SelectTranslator(Text)
    # feishu_content = {"content": []}
    # # feishu_content["title"] = TranslatorText
    # feishu_content["content"].append([
    #     {
    #         "tag": "text",
    #         "text": CreatedAt,
    #     },
    #     {
    #         "tag": "a",
    #         "text": UserName,
    #         "href": 'https://twitter.com/' + UserName
    #     },
    # ])
    # feishu_content["content"].append([
    #     {
    #         "tag": "text",
    #         "text": "\n{}{}\n{}".format(Text, TranslatorText, LinkToTweet),
    #     },
    # ])
    # send_feishu_robot(feishu_robot_key, feishu_content)