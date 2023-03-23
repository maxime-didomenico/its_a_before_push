import mysql.connector


class Speaker:

    def __init__(self):

        self.log = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "1",
            database = "discord"
        )
        self.cursor = self.log.cursor()

    def sign_in(self, username, password):
        try :
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            val = (username, password)
            self.cursor.execute(sql, val)
            self.log.commit()
            print(self.cursor.rowcount, "record inserted.")

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return False
        
    def check_login(self, username, password):
        try :
            sql = "SELECT * FROM users WHERE username = %s AND password = %s"
            val = (username, password)
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()
            if result:
                return True
            else:
                return False

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return False
        
    def send_message(self, username, content):
        try :
            sql = "INSERT INTO messages (username, content) VALUES (%s, %s)"
            val = (username, content)
            self.cursor.execute(sql, val)
            self.log.commit()
            print(self.cursor.rowcount, "record inserted.")

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return False
        
    def send_discussion(self, discussionID):
        try :
            sql = "SELECT * FROM messages WHERE discussionID = %s"
            val = (discussionID)
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()
            if result:
                return result

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return False