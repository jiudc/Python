import logging
import time
import os


def creatlog(logname):
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
