import json
import demjson

data = b'{\n  "Text": "kankan kankan  test  test 122  aabb",\n  "UserName": "dFKq3rPdUrf2ifu",\n  "LinkToTweet": "http://twitter.com/dFKq3rPdUrf2ifu/status/1417423117723471872",\n  "TweetEmbedCode": "<blockquote class="twitter-tweet">\n  <p lang="en" dir="ltr">kankan kankan  test  test 122  aabb</p>\n  &mdash; \xe7\x9c\x8b\xe7\x9c\x8b (@dFKq3rPdUrf2ifu)\n  <a href="https://twitter.com/dFKq3rPdUrf2ifu/status/1417423117723471872">Jul 20, 2021</a>\n</blockquote>\n<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n",\n  "CreatedAt": "July 20, 2021 at 05:56PM"\n}'

utf8 =data.decode('utf-8') 
# utf8 = utf8.replace('\r', '\\r').replace('\n', '\\n')
print(utf8)
print(demjson.encode(data))