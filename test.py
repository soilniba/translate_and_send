import json
import demjson

data = b'{\n  "Text": "kankan kankan  test  test 122  aabb",\n  "UserName": "dFKq3rPdUrf2ifu",\n  "LinkToTweet": "http://twitter.com/dFKq3rPdUrf2ifu/status/1417423117723471872",\n  "CreatedAt": "July 20, 2021 at 05:56PM"\n}'

utf8 =data.decode('utf-8') 
# utf8 = utf8.replace('\n', '')
print(utf8)
# json_table = demjson.decode(data)
json_table = json.loads(data)
print(json_table)
print(json_table['Text'])