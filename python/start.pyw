#! python3
# 用于打开常用网站
import webbrowser, os
# webbrowser.open('https://stackoverflow.com/')
# webbrowser.open('https://www.52pojie.cn/')
# webbrowser.open('https://www.liaoxuefeng.com/')
# webbrowser.open('https://github.com/')
path = r"C:\Users\Liudingchao\Src\Study"
os.chdir(os.path.join(path))
print(os.getcwd())
os.system('WINWORD.EXE Java_Serious.docx')