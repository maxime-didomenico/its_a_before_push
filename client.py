import json
import socket

class Client:

    def __init__(self, host='localhost', port=5566):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        print("Client connected !")


    def sign_in(self, username, password, mail):
        signin_data = {
            "type": "signin",
            "username": username,
            "password": password,
            "mail": mail
        }
        msg = json.dumps(signin_data)
        msg = msg.encode("utf8")
        self.client_socket.sendall(msg)


    def send_login(self, username, password):
        login_data = {
            "type": "login",
            "username": username,
            "password": password
        }
        msg = json.dumps(login_data)
        msg = msg.encode("utf8")
        self.client_socket.sendall(msg)


    def discussionID(self, usernameA, usernameB):
        discussion_data = {
            "type": "discussion",
            "usernameA": usernameA,
            "usernameB": usernameB
        }
        msg = json.dumps(discussion_data)
        msg = msg.encode("utf8")
        self.client_socket.sendall(msg)


    def messageID(self, discussion, message):
        message_data = {
            "type": "message",
            "discussion": discussion,
            "message": message
        }
        msg = json.dumps(message_data)
        msg = msg.encode("utf8")
        self.client_socket.sendall(msg)


    def askForHistory(self, usernameA, usernameB):
        discussionID = self.discussionID(usernameA, usernameB)
        history_data = {
            "type": "history",
            "discussionID": discussionID
        }
        msg = json.dumps(history_data)
        msg = msg.encode("utf8")
        self.client_socket.sendall(msg)


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
            self.client_socket.sendall(msg)


    def send_emoji(self, discussion, message, emoji):
        emoji_data = {
            "type": "emoji",
            "discussion": discussion,
            "message" : message,
            "emoji": emoji
        }
        msg = json.dumps(emoji_data)
        msg = msg.encode("utf8")
        self.client_socket.sendall(msg)


    def receive_response(self):
        data = self.client_socket.recv(1024)
        print(f"Received data: {data}")


    def close(self):
        self.client_socket.close()
        

client = Client()


# à modifier quand on aura l'interface (on aura pas 1 milliard de while 
# à la con)

try :
    
    cond = 0
    while cond == 0:
        login = input("Enter your login : ")
        password = input("Enter your password : ")
        
        if cond == 0:
            
            try :
                client.send_login(login, password)
                check_log = client.receive_response()
                
                if check_log == True:
                    print("Login successful !")
                
                else :
                    print("Login failed !")
                
                while True:

                    check = input("Do you want to send a message ? (y/n) : ")
                    
                    if cond == 1:
                        break

                    if check == "y":
                        content = input("Enter your message : ")
                        client.send_message(login, content)

                    if check == "n":
                        logout = input("Do you want to logout ? (y/n) : ")
                        if logout == "y":
                            cond = 1
                            break
                        else:
                            client.close()
                            check_log = False
                            break
                    
                    client.receive_response()

            except :
                print("Login failed !")
                False

        else:
            break

except :
    print("Connection failed !")

finally :
    print("Client logged out.")
    client.close()