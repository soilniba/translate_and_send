import json
import demjson

data = b'{\n  "Text": "We created our own connector, as there was no standard back then &amp; Tesla was only maker of long range electric cars. \n\nIt\xe2\x80\x99s one fairly slim connector for both low &amp; high power charging. \n\nThat said, we\xe2\x80\x99re making our Supercharger network open to other EVs later this year.",\n  "UserName": "dFKq3rPdUrf2ifu",\n  "LinkToTweet": "http://twitter.com/dFKq3rPdUrf2ifu/status/1417784826153693184",\n  "CreatedAt": "July 21, 2021 at 05:53PM"\n}'


utf8 =data.decode('utf-8') 
# utf8 = utf8.replace('\n', '')
print(utf8)
json_table = demjson.decode(data)
# json_table = json.loads(data)
print(json_table)
print(json_table['Text'])