import psycopg2
import configparser

# importing details from config.ini
config = configparser.ConfigParser()
config.read('config_db.ini')  # reading the config file
host = config.get('postgresql', 'host')  # getting host id
database = config.get('postgresql','database')
user = config.get('postgresql','user')
password_db = config.get('postgresql','password')
port = config.get('postgresql', 'port')  # getting port number

class database_user():
    def __init__(self) :
        self.conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password_db,
                port=port
            )
        
    def write_user(self,username, name, email_id, password):
        try:
            # create a cursor object
            cur = self.conn.cursor()
            # create a table
            cur.execute("CREATE TABLE IF NOT EXISTS Userdetail (id SERIAL PRIMARY KEY, username VARCHAR(255) UNIQUE,full_name VARCHAR(255), email VARCHAR(255), hashed_password VARCHAR(255))")
            cur.execute(
                "INSERT INTO Userdetail (username, full_name, email, hashed_password ) VALUES (%s,%s,%s,%s)", (username, name, email_id, password))
            # commit the changes
            self.conn.commit()
            # close the cursor and connection
            cur.close()
            self.conn.close()
            return "User registered successfully."
        except Exception as err:
            return "Not able to write query to DB due to "+str(err)


    def query_user(self,username):
        try:    
            # create a cursor object
            cur = self.conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Userdetail (id SERIAL PRIMARY KEY, username VARCHAR(255) UNIQUE,full_name VARCHAR(255), email VARCHAR(255), hashed_password VARCHAR(255))")
            # execute the SQL query
            query = """
            SELECT id FROM Userdetail WHERE username = %s
            """
            cur.execute(query, (username,))
            # fetch all rows
            rows = cur.fetchall()
            # close the cursor and connection
            cur.close()
            self.conn.close()
            return rows
        except Exception as err:
            print(err)
            return False

    def user_detail(self,username):
        try:
            # create a cursor object
            cur = self.conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Userdetail (id SERIAL PRIMARY KEY, username VARCHAR(255) UNIQUE,full_name VARCHAR(255), email VARCHAR(255), hashed_password VARCHAR(255))")
            # execute the SQL query
            select_query = """
            SELECT id, username, full_name, email, hashed_password FROM Userdetail WHERE username = %s
            """
            cur.execute(select_query, (username,))
            # fetch all rows
            rows = cur.fetchall()[0]
            result = {}
            for i in range(len(cur.description)):
                result[cur.description[i].name] = rows[i]
            # close the cursor and connection
            cur.close()
            self.conn.close()
            return result
        except Exception as err:
            print(err)
            return False

    def update_user(self,username, name, email_id):
        try:
            # create a cursor object
            cur = self.conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Userdetail (id SERIAL PRIMARY KEY, username VARCHAR(255) UNIQUE,full_name VARCHAR(255), email VARCHAR(255), hashed_password VARCHAR(255))")
            # execute the SQL query
            update_query = """
            UPDATE Userdetail
            SET full_name = %s, email = %s
            WHERE username = %s"""
            cur.execute(update_query, (name, email_id, username))
            # Commit the transaction and close the cursor and connection
            self.conn.commit()
            cur.close()
            self.conn.close()
            return "User updated successfully"
        except Exception as err:
            print(err)
            return False

    def delete_user(self,username):
        try:
            # create a cursor object
            cur = self.conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Userdetail (id SERIAL PRIMARY KEY, username VARCHAR(255) UNIQUE,full_name VARCHAR(255), email VARCHAR(255), hashed_password VARCHAR(255))")
            # execute the SQL query
            # Define the delete query with parameters
            delete_query = """
                DELETE FROM Userdetail
                WHERE username = %s
            """
            # Execute the delete query with the value
            cur.execute(delete_query, (username,))
            # Commit the transaction and close the cursor and connection
            self.conn.commit()
            cur.close()
            self.conn.close()
            return "User deleted successfully"
        except Exception as err:
            print(err)
            return False

    def all_users(self, id):
        try:
            # create a cursor object
            cur = self.conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Userdetail (id SERIAL PRIMARY KEY, username VARCHAR(255) UNIQUE,full_name VARCHAR(255), email VARCHAR(255), hashed_password VARCHAR(255))")
            # execute the SQL query
            # Define the delete query with parameters
            sel_query = """
                SELECT * FROM Userdetail LIMIT %s
            """
            # Execute the delete query with the value
            cur.execute(sel_query,(id,))
            rows = cur.fetchall()
            # Commit the transaction and close the cursor and connection
            cur.close()
            self.conn.close()
            return rows
        except Exception as err:
            print(err)
            return False

    def all_activity(self, id):
        try:
            # create a cursor object
            cur = self.conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Activity_log (id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, query VARCHAR NOT NULL, response VARCHAR NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES Userdetail(id))")
            # execute the SQL query
            # Define the delete query with parameters
            sel_query = """
                SELECT * FROM Activity_log LIMIT %s
            """
            # Execute the delete query with the value
            cur.execute(sel_query,(id,))
            rows = cur.fetchall()
            # Commit the transaction and close the cursor and connection
            cur.close()
            self.conn.close()
            return rows
        except Exception as err:
            print(err)
            return False

    def write_activity(self,user_id, name, query, response):
        try:
            # create a cursor object
            cur = self.conn.cursor()
            # create a table
            cur.execute("CREATE TABLE IF NOT EXISTS Activity_log (id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, query VARCHAR NOT NULL, response VARCHAR NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES Userdetail(id))")
            cur.execute(
                "INSERT INTO Activity_log (name,query,response, user_id) VALUES (%s,%s,%s,%s)", (name, query, response, user_id))
            # commit the changes
            self.conn.commit()
            # close the cursor and connection
            cur.close()
            self.conn.close()
            return "Activity added successfully."
        except Exception as err:
            return "Not able to write log to DB due to "+str(err)