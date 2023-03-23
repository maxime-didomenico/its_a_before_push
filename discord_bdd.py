import mysql.connector

class Discord_bdd:

    def __init__(self, user, password, database, host='localhost'):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def get_message(self, id):
        self.cursor.execute("SELECT * FROM Messages WHERE id = %s", (id,))
        return self.cursor.fetchone()

    def get_all_messages(self):
        self.cursor.execute("SELECT * FROM messages")
        return self.cursor.fetchall()

    def add_message(self, text, id_utilisateur, id_canal):
        self.cursor.execute("INSERT INTO Messages (text, id_utilisateur, id_canal) VALUES (%s, %s, %s)",
                            (text, id_utilisateur, id_canal))
        self.connection.commit()

    def update_message(self, text, id_utilisateur, id_canal):
        self.cursor.execute("UPDATE Messages SET message = %s WHERE id = %s", (text, id_utilisateur, id_canal))
        self.connection.commit()

    def delete_message(self, id):
        self.cursor.execute("DELETE FROM Messages WHERE id = %s", (id,))
        self.connection.commit()

    def create_user(self, nom, email, mdp):
        self.cursor.execute("INSERT INTO Utilisateurs (nom_utilisateur, email_utilisateur, mot_de_passe) VALUES (%s, %s, %s)"
                            , (nom, email, mdp))
        self.connection.commit()

    def get_user(self, nom):
        self.cursor.execute("SELECT * FROM Utilisateurs WHERE nom_utilisateur = %s", (nom,))
        return self.cursor.fetchone()

# connexion = Discord_bdd('root', 'azerty', 'discord')
