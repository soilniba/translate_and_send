robot_key = 'c57c249e-ed34-4e37-9064-dad5004d6420'
from json import dumps
from requests import post
from flask import Flask
from flask import request
app = Flask(__name__)
# from translate import Translator
from googletrans import Translator
translator = Translator(service_urls=[
      'translate.google.com',
    ])

@app.route('/', methods=['POST','GET'])
def index():
    json_table = request.get_json()
    print(json.dumps(json_table))
    return json_table

@app.route('/translate',methods=['POST','GET'])
def translate():
    if request.method=='POST':
        json_table = request.get_json()
        print(dumps(json_table))
        FromLang = json_table['FromLang']
        ToLang = json_table['ToLang']
        Text = json_table['Text']
        UserName = json_table['UserName']
        LinkToTweet = json_table['LinkToTweet']
        TweetEmbedCode = json_table['TweetEmbedCode']
        CreatedAt = json_table['CreatedAt']
        # 翻译
        try:
            # translator = Translator(from_lang = FromLang,to_lang = ToLang)
            # TranslatorText = translator.translate(Text)
            TranslatorText = translator.translate(Text, src = 'en', dest = 'zh-cn')
            print(TranslatorText)
            robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + robot_key
            headers = { 'Content-Type': 'application/json' }
            data_table = {
                "msgtype": "markdown",
                "markdown": {
                    "content": "{} **[@elonmusk](https://twitter.com/elonmusk)** \n {}\n{}\n\n[{}]({}})\n".format(
                        CreatedAt, 
                        Text, 
                        TranslatorText,
                        'https://twitter.com/elonmusk',
                        'https://twitter.com/elonmusk'
                        )
                }
            }
            data = dumps(data_table)
            post(robot_url, headers = headers, data = data)
        except:
            print('translator error')
        return json_table

if __name__=='__main__':
    app.run(
        debug = True,
        port = 9527,
    )