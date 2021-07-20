import json
import random
import uuid
import hashlib
import time
from typing import Text
import requests
from flask import Flask
from flask import request
app = Flask(__name__)
robot_key = 'c57c249e-ed34-4e37-9064-dad5004d6420'

# @app.route('/', methods=['POST','GET'])
# def index():
#     json_table = request.get_json()
#     print(json.dumps(json_table))
#     return json_table

@app.route('/translate',methods=['POST','GET'])
def translate():
    try:
        if request.method=='POST':
            json_table = request.get_json()
            print(json.dumps(json_table))
            # FromLang = json_table['FromLang']
            # ToLang = json_table['ToLang']
            Text = json_table['Text']
            UserName = json_table['UserName']
            LinkToTweet = json_table['LinkToTweet']
            TweetEmbedCode = json_table['TweetEmbedCode']
            CreatedAt = json_table['CreatedAt']

            TranslatorText = SelectTranslator(Text)
            print(TranslatorText)
            robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + robot_key
            headers = { 'Content-Type': 'application/json' }
            data_table = {
                "msgtype": "markdown",
                "markdown": {
                    "content": "{} **[@{}](https://twitter.com/{})** \n {}\n{}\n\n[{}]({})\n".format(
                        CreatedAt,
                        UserName,
                        UserName,
                        Text,
                        TranslatorText,
                        LinkToTweet,
                        LinkToTweet
                    )
                }
            }
            data = json.dumps(data_table)
            # requests.post(robot_url, headers = headers, data = data)
            return json_table
    except:
        print('translator error')
    return {}

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
    if RandomInt <= 2:
        returntest = '[有道]' + youdao(text)
    else:
        returntest = '[彩云]' + caiyun(text)
    return returntest

# source = "Lingocloud is the best translation service."
# target = SelectTranslator(source)
# print(target)

if __name__=='__main__':
    app.run(
        debug = True,
        port = 952,
        host = '0.0.0.0',
        ssl_context=('sg.gjol.vip.pem', 'sg.gjol.vip.key')
    )
