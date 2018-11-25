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
    logging.info("Current word directory is: " + os.getcwd())
    return logger


logger = creatlog("cartoon")  # 建立日志
startUrl = r"https://www.fzdm.com/manhua/21"
MAX_RETRIES = 20
dirName = "杀戮都市"
head = {'User-Agent': 'Mozilla/5.0'}
os.makedirs(dirName, exist_ok=True)
volCount = 1
pageCount = 1
stepChapterUrl = "/Vol_02/"
url = startUrl + stepChapterUrl
while not url.endswith('#'):
    # Step1-Download the website page
    logging.info('Downing page %s...' % url)
    try:
        res = requests.get(url, headers=head, timeout=105)
        res.encoding = 'utf-8'
        res.raise_for_status()
    except requests.RequestException as e:
        logger.info(e.message)
    soup = bs4.BeautifulSoup(res.text, features="html5lib")
    # Step2-Find the url of comic image.
    regexMhurl = re.compile(r'\d{2,4}/.*jpg', re.MULTILINE | re.DOTALL)
    regexMhss = re.compile(r'p1\.[0-9a-zA-Z]+\.net?', re.MULTILINE | re.DOTALL)
    scriptMhurl = soup.find("script", text=regexMhurl)
    scriptMhss = soup.find("script", text=regexMhss)
    comicElem = soup.find("script", text=regexMhurl)
    mhUrl = regexMhurl.search(scriptMhurl.text).group(0)
    mhss = regexMhss.search(scriptMhss.text).group(0)
    if not mhUrl or not mhss:
        logger.info("Can not find comic image address!")
    else:
        comicUrl = "http://" + mhss + "/" + mhUrl
        logger.info('Downing image from %s ...' % comicUrl)
        try:
            res = requests.get(comicUrl, timeout=105)
            res.raise_for_status()
        except requests.RequestException as e:
            logger.info("e.message")
        # Step3-Save image to directory
        imageFile = open(os.path.join(dirName, "Chapter" + stepChapterUrl[1:-1] + "_Page" + str(pageCount) + mhUrl[-4:]), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
    # Step4-Get the Next button's url.
    tagNextPage = soup.find(class_="pure-button pure-button-primary", text="下一页")
    tagNextChapter = soup.find(class_="pure-button pure-button-primary", text="下一话吧")
    if not tagNextPage:
        if not tagNextChapter:
            break
        else:
            stepChapterUrl = tagNextChapter['href'][2:]
            url = startUrl + stepChapterUrl
            volCount += 1
            pageCount = 1
    else:
        url = startUrl + stepChapterUrl + "/" + tagNextPage['href']
        pageCount += 1
    print(url)
logger.info("***Finished！***")
