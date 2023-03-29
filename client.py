import json
import socket

class Client:

    def __init__(self, host, port=5566):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        print("Client connected !")


    def send_signin(self, name,f_name, mail, password):
        signin_data = {
            "type": "signin",
            "name": name,
            "f_name": f_name,
            "password": password,
            "mail": mail
        }
        msg = json.dumps(signin_data)
        msg = msg.encode("utf8")
        self.client_socket.send(msg)
        response = self.client_socket.recv(1024)
        return response.decode("utf8")


    def send_login(self, username, password):
        login_data = {
            "type": "login",
            "username": username,
            "password": password
        }
        msg = json.dumps(login_data)
        msg = msg.encode("utf8")
        self.client_socket.send(msg)
        response = self.client_socket.recv(1024)
        return response.decode("utf8")

    def discussionID(self, usernameA, usernameB):
        discussion_data = {
            "type": "discussion",
            "usernameA": usernameA,
            "usernameB": usernameB
        }
        msg = json.dumps(discussion_data)
        msg = msg.encode("utf8")
        self.client_socket.send(msg)


    def messageID(self, discussion, message):
        message_data = {
            "type": "message",
            "discussion": discussion,
            "message": message
        }
        msg = json.dumps(message_data)
        msg = msg.encode("utf8")
        self.client_socket.send(msg)


    def askForHistory(self, usernameA, usernameB):
        discussionID = self.discussionID(usernameA, usernameB)
        history_data = {
            "type": "history",
            "discussionID": discussionID
        }
        msg = json.dumps(history_data)
        msg = msg.encode("utf8")
        self.client_socket.send(msg)
        response = self.client_socket.recv(1024)
        return response.decode("utf8")


    def readHistory(self):
        data = self.client_socket.recv(1024)
        data = data.decode("utf8")
        data = json.loads(data)
        print(data)


    def send_message(self, username, content):
        if len(content) <= 0:
            return print("Message cannot be empty !")
        else :
            message_data = {
                "type": "message",
                "username": username,
                "content": content
            }
            msg = json.dumps(message_data)
            msg = msg.encode("utf8")
            self.client_socket.send(msg)


    def send_emoji(self, discussion, message, emoji):
        emoji_data = {
            "type": "emoji",
            "discussion": discussion,
            "message" : message,
            "emoji": emoji
        }
        msg = json.dumps(emoji_data)
        msg = msg.encode("utf8")
        self.client_socket.send(msg)


    def receive_response(self):
        data = self.client_socket.recv(1024)
        return data.decode("utf8")


    def close(self):
        self.client_socket.close()