#! python3
import requests
import bs4
import os
import re
import logging


def creatlog(logname):
    import time
    import os
    currenttime = time.strftime("%Y-%m-%d", time.localtime())
    suffix = ".log"
    logfile = logname + "-" + currenttime + suffix
    path = r'C:\Users\Liudingchao\Documents'
    os.chdir(os.path.join(path))
    os.makedirs('logs', exist_ok=True)
    os.chdir(os.getcwd() + os.sep + 'logs')
    if not os.path.exists(logfile):
        f = open(logfile, 'w')
        f.close()
        print(logfile + " have been created!")
    else:
        print(logfile + " have already existed!")
    logger = logging.getLogger(logname)
    logger.setLevel(logging.INFO)
    logFormat = '[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s'
    # 生成文件handle
    f_handle = logging.FileHandler(logfile, mode='a')
    f_handle.setLevel(logging.WARNING)
    f_handle.setFormatter(logging.Formatter(logFormat))
    # 生成控制台handle
    s_handle = logging.StreamHandler()
    s_handle.setLevel(logging.INFO)
    s_handle.setFormatter(logging.Formatter(logFormat))
    logger.addHandler(f_handle)
    logger.addHandler(s_handle)
    os.chdir(os.path.join(path))
    logger.info("Current word directory is: " + os.getcwd())
    return logger


logger = creatlog("picture")  # 建立日志
startUrl = r"http://1024.91rsxmza.xyz/pw/"
dirName = "Fashion"
head = {'User-Agent': 'Mozilla/5.0'}
os.makedirs(dirName, exist_ok=True)
os.chdir(os.path.join(os.getcwd(), dirName))
volCount = 1
pageCount = 1
url = startUrl + "thread-htm-fid-15.html"
try:
    res = requests.get(url, headers=head, timeout=105)
    res.encoding = 'utf-8'
    res.raise_for_status
except requests.RequestException as e:
    logger.info(e.message)
soup = bs4.BeautifulSoup(res.text, features="html5lib")
titleGroup = soup.find_all(id=re.compile("a_ajax_.*"), href=re.compile("htm_data/.*"))
for title in titleGroup:
    titleUrl = startUrl + title["href"]
    try:
        dirRegex = re.compile(r'[\u4E00-\u9FA5]+')
        dirDate = re.compile(r"\d{2}\.\d{2}")
        dirName = dirDate.search(title.text).group(0) + "_" + dirRegex.search(title.text).group(0)
        os.makedirs(dirName, exist_ok=True)
        logger.info("Current work directory is:" + os.getcwd())
        logger.info('Downing page %s...' % titleUrl)
        res = requests.get(titleUrl, headers=head, timeout=105)
        res.encoding = 'utf-8'
        res.raise_for_status()
    except requests.RequestException as e:
        logger.info(e.message)
    soup = bs4.BeautifulSoup(res.text, features="html5lib")
    imgGroup = soup.select("#read_tpc  img")
    for img in imgGroup:
        imgUrl = img["src"]
        try:
            res = requests.get(imgUrl, timeout=105)
            res.raise_for_status()
            logger.info("Download image from imgUrl: " + imgUrl)
            imageFile = open(os.path.join(os.getcwd()+"\\"+dirName, os.path.basename(imgUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
        except requests.RequestException as e:
            logger.info("e.message")
logger.info("***Finished！***")
