from discord_bdd import Discord_bdd
from threading import Thread
import json
import socket
import time
import getpass

class Server:

    def __init__(self, host='localhost', port=5566):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.password = getpass.getpass("MySQL Password: \n>")
        self.link = Discord_bdd("root", self.password, "discord")
        print("Connection is started !")
        self.start()


    def start(self):
        while True:
            self.server_socket.listen()
            conn, address = self.server_socket.accept()

            print("Client connected.")
            print(f"Accepted connection from {address}")

            client_thread = Thread(target=self.handle_client_connection, args=(conn,))
            client_thread.start()


    def handle_client_connection(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break


            data = data.decode("utf8")
            data = json.loads(data)


            if data["type"] == "login":
                username = data["username"]
                password = data["password"]
                print(f"Try to login: {username}")
                print(f"mdp: {password}")
                result = self.link.check_login(username, password)
                print(result)
                if result:
                    response_data={"status":"ok"}
                    response_msg=json.dumps(response_data).encode('utf-8')
                    conn.sendall(response_msg)
                else:
                    response_data={"status":"error"}
                    response_msg=json.dumps(response_data).encode('utf-8')
                    conn.sendall(response_msg)
                print(response_data)

            if data["type"] == "signin":
                name = data["name"]
                f_name = data["f_name"]
                password = data["password"]
                mail = data["mail"]
                print(f"Try to sign in: {name}")
                if self.link.create_user(f_name,name, mail, password):
                    response_data={"status":"ok"}
                    response_msg=json.dumps(response_data).encode('utf-8')
                    self.server_socket.send(response_msg)
                else:
                    response_data={"status":"error"}
                    response_msg=json.dumps(response_data).encode('utf-8')
                    self.server_socket.send(response_msg)


            if data["type"] == "message":
                content=data["content"]
                username = data["username"]
                print(f"Message: {content}")
                response_data={"status":"ok"}
                response_msg=json.dumps(response_data).encode('utf-8')
                conn.sendall(response_msg)
                self.send_message(username, content)

            if data["type"] == "history":
                discussionID = data["discussionID"]
                #print(f"History: {usernameA} {usernameB}")
                response_data=self.send_discussion(discussionID)
                response_msg=json.dumps(response_data).encode('utf-8')
                conn.sendall(response_msg)


    def check_login(self, username, password):
        try :
            self.link.check_login(username, password)

        except :
            return False


    def sign_in(self, username, password, mail):
        try :
            self.link.sign_in(username, password, mail)

        except :
            return False
    

    def send_message(self, text, username,id_canal):
        date = time.strftime("%d/%m/%Y")
        hour = time.strftime("%H:%M:%S")
        try :
            self.link.create_message(text, username, date, hour, id_canal)

        except :
            return False

    def delete_message(self, id_message):
        try :
            self.link.delete_message(id_message)

        except :
            return False


    def send_discussion(self, discussionID):
        try :
            self.link.send_discussion(discussionID)

        except :
            return False

server = Server()