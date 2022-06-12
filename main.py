import http.server
import socketserver
import os
import optparse
import threading
import sys
import _thread
import time


USERNAME = "user" #set your username by editing this value within the quotes
PASSWORD = "pass" #set your password by editing the value within the quotes

PATH = r"D:\\" #Change this path to the directory on your computer which you want to make accessible by the server

SCRIPT_PATH = os.getcwd()
ANONYMOUS_PATH = SCRIPT_PATH + '/assets/'

f = open("logs.txt", "a")

uname = ""
passwd = ""


def initvars():
    global uname, passwd
    uname = ""
    passwd = ""


print("PATH : ",PATH)


class GetHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("printing request : ", self.path)
        st = str(self.path)
        f.write(st + "\n")

        authorize(st, PATH, ANONYMOUS_PATH)
        # authorize(st,PATH,ANONYMOUS_PATH) #check if already authorized user, if not, then try to authorize now. If failed, then prohibit access
        http.server.SimpleHTTPRequestHandler.do_GET(self)


def authorize(st,PATH,ANONYMOUS_PATH):
    li = list(st)

    print("HEY THERE")

    print(st)

    global uname
    global passwd

    initvars()

    print("uname is ", uname)
    print("passwd is ", passwd)

    if "username=" in st and "passwd=" in st:
        splitStr = st.split("&")
        print(splitStr)
        uname = splitStr[0][splitStr[0].index("=") + 1:]
        passwd = splitStr[1][splitStr[1].index("=") + 1:]

        print("Received username : ", uname)
        print("Received password : ", passwd)

        if uname == USERNAME and passwd == PASSWORD:
            # time.sleep(5)
            os.chdir(PATH)
        else:
            print("Invalid Username and Password")
            # time.sleep(1)
            os.chdir(ANONYMOUS_PATH)
    else:
        # This means the user is not authorized and not even trying to get authorized, prohibit access
        print("Welcome to the Server")
        # time.sleep(1)
        os.chdir(SCRIPT_PATH)


def StartServer():
    print("Server is up")

    host = "127.0.0.1"
    port = 1560
    # handler = http.server.SimpleHTTPRequestHandler
    handler = GetHandler
    os.chdir(SCRIPT_PATH)

    http_server = socketserver.TCPServer((host, port), handler)
    http_server.serve_forever()


print("Server starting")
initvars()


if __name__ == '__main__':
    cthread = threading.Thread(target=StartServer())
    cthread.daemon = True
    _thread.start_new_thread()
