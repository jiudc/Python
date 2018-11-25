#! python3
import os
import requests
import bs4

path = r"C:\Users\Liudingchao\Src\Download"
os.chdir(os.path.join(path))
dir = os.getcwd()
print("my name:" + dir)
res = requests.get('http://baidu.com')
res.raise_for_status()
searchSoup = bs4.BeautifulSoup(res.text)

