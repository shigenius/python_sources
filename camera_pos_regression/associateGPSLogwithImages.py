import json
import datetime
import os
import glob
import argparse
import math
import re

parser = argparse.ArgumentParser(
        description='')
parser.add_argument('dpath', help='Path to json dir')
args = parser.parse_args()

#os.listdir(path)
print(args.dpath)
jsonpaths=glob.glob(args.dpath+'/*')

# json統合
logs=[]
for fpath in jsonpaths:
    f = open(fpath)
    data = json.load(f)
    logs.extend(data)
timestanp = [logs[i]["tm"] for i in range(len(logs))] #unixtime
#print(timestanp)
# JST
#timestanp=[int(datetime.datetime.fromtimestamp(logs[i]["tm"]).strftime('%y%m%d%H%M%S')) for i in range(len(logs))]


movpaths = glob.glob('./*.mov')
movdirs = [re.sub(r'\.mov', "", i) for i in movpaths]
imgpaths = [glob.glob(i+'/*') for i in movdirs]
imgpaths = [flatten for inner in imgpaths for flatten in inner] # flatten
#print(imgpaths)
phototime = [int(i[2:12])+((int(i[-8:-4])-1)/2) for i in imgpaths] #ちゃんと正規表現で書いた方がいい
print(phototime)

with open('./GT.txt', 'w') as f: # output file
    #targettime=os.stat(movpaths[0]).st_mtime
    for targettime in phototime:
        print("target time :",targettime)
        #print(datetime.datetime.fromtimestamp(os.path.getctime(movpaths[0])).strftime('%Y/%m/%d %H:%M:%S'))
        
        # targetの作成日に一番近い時間の探索
        approximation = 0
        for i in timestanp:
            if(math.fabs(targettime-i) < math.fabs(approximation-i)):
                approximation = i
        
        print("approximate time :",approximation)
        
        #appriximationのindexを取得
        index=timestanp.index(approximation)
        #print(index)
        #print(logs[index])
        #print(type(logs[index]["he"]))
        print("lo:",logs[index]["lo"],"la:",logs[index]["la"],"he:",logs[index]["he"])
        f.write('%s %.13f %.13f %s\n' % (os.path.abspath(imgpaths[phototime.index(targettime)]),logs[index]["lo"],logs[index]["la"],logs[index]["he"]))
