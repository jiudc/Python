#! python3
import requests
import bs4
import os
import re
import logging
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def creatlog(logname):
    import time
    import os
    currenttime = time.strftime("%Y-%m-%d", time.localtime())
    suffix = ".log"
    logfile = logname + "-" + currenttime + suffix
    path = r'D:\Srclib\doc'
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
startUrl = r'http://1024.91rsxmza.xyz/pw/htm_data/15/1811/1404062.html'
dirName = "Muse"
TIMEOUT = 20
head = {'User-Agent': 'Mozilla/5.0'}
os.makedirs(dirName, exist_ok=True)
os.chdir(os.path.join(os.getcwd(), dirName))
desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
locatorImg = (By.CSS_SELECTOR, "#read_tpc img")
locatorTpc = (By.ID, "subject_tpc")
locatorTitle = (By.CSS_SELECTOR, "#td_tpc > div.tiptop > span.fl.gray")
clickNext = (By.LINK_TEXT, "下一主题")
try:
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    # browser = webdriver.Chrome()

    try:
        browser.get(startUrl)
    except TimeoutException:
        browser.execute_script("window.stop();")  # 调用js脚本使浏览器停止加载

    while True:
        WebDriverWait(browser, TIMEOUT, 0.5).until(EC.presence_of_all_elements_located(locatorImg))
        WebDriverWait(browser, TIMEOUT, 0.5).until(EC.presence_of_element_located(locatorTpc))
        WebDriverWait(browser, TIMEOUT, 0.5).until(EC.presence_of_element_located(locatorTitle))
        WebDriverWait(browser, TIMEOUT, 0.5).until(EC.element_to_be_clickable(clickNext))
        logger.info("Program is processing:" + browser.current_url)
        elems = browser.find_elements_by_css_selector("#read_tpc img")
        title = browser.find_element_by_id("subject_tpc")
        date = browser.find_element_by_css_selector("#td_tpc > div.tiptop > span.fl.gray")
        nextPage = browser.find_element_by_link_text("下一主题")
        dirRegex = re.compile(r'[\u4E00-\u9FA5a-zA-Z0-9]+')
        dirDate = re.compile(r"\d{4}-\d{2}-\d{2}")
        dirName = dirDate.search(date.text).group(0) + "_" + dirRegex.search(title.text).group(0)
        logger.info("*************Target is:" + dirName)
        os.makedirs(dirName, exist_ok=True)
        for elem in elems:
            imgUrl = elem.get_attribute("src")
            try:
                res = requests.get(imgUrl, timeout=105)
                res.raise_for_status()
                logger.info("Download image from imgUrl: " + imgUrl)
                imageFile = open(os.path.join(os.getcwd() + "\\" + dirName, os.path.basename(imgUrl)), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
            except requests.RequestException as e:
                logger.info(e)
        nextPage.click()
except TimeoutException as e:
    logger.info(e)
logger.info("***Finished！***")
