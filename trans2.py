import requests
import re
 
string = 'Live as if you were to die tomorrow. Learn as if you were to live forever.'
url = 'https://translate.google.com/?hl=ja#en/ja/'
r = requests.get(url, params={'q': string})
   
pattern = "TRANSLATED_TEXT=\'(.*?)\'"
result = re.search(pattern, r.text).group(1)
    
#print(f'英語：{string}\n日本語：{result}')
print(result)
