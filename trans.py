# coding: utf-8

import sys
import requests

argvs = sys.argv
argc = len(argvs)

url = "https://translate.google.com/translate_a/single"

headers = {
    "Host": "translate.google.com",
    "Accept": "*/*",
    "Cookie": "",
    "User-Agent": "GoogleTranslate/5.9.59004 (iPhone; iOS 10.2; ja; iPhone9,1)",
    "Accept-Language": "ja-jp",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    }

sentence = " ".join(argvs[1:])

params = {
    "client": "it",
    "dt": ["t", "rmt", "bd", "rms", "qca", "ss", "md", "ld", "ex"],
    "otf": "2",
    "dj": "1",
    "q": sentence,
    "hl": "ja",
    "ie": "UTF-8",
    "oe": "UTF-8",
    "sl": "en",
    "tl": "ja",
    }


res = requests.get(
    url=url,
    headers=headers,
    params=params,
    )

res = res.json()
print(res["sentences"][0]["trans"])