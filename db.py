#!/usr/bin/python3
import hashlib
import configparser
import pymssql
import datetime

class db:

    def __init__(self,config):
        try:
            self.host = config['Database']['Host']
            self.user = config['Database']['User']
            self.database = config['Database']['DB']
            self.password = config['Database']['Password']
            self.port = int(config['Database']['Port'])


        except Exception as e:
            print("Config Error!")
            print(e)
            exit()
        try:    
            self.connect()
        except:
            print("Database Error!")
        
        

    def build(self):
        tables = self.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")  
        print(tables)       
        if(('persons',) not in tables): 
            self.execute('''CREATE TABLE persons
                            (person_id INT IDENTITY (1,1) NOT NULL, 
                            name VARCHAR(100),
                            username VARCHAR(100),
                            status VARCHAR(100),
                            status_description VARCHAR(1000),
                            CONSTRAINT pk_person_id PRIMARY KEY CLUSTERED (person_id));''')

    def destroy(self):
        self.execute("DROP TABLE persons")  
        print("Tables destroyed")

    
    def close(self):
        self.conn.close()

    def connect(self):
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.password, port=self.port, database=self.database)
        self.cur = self.conn.cursor()

    def execute(self,command):
        self.connect()
        self.cur.execute(command)
        self.conn.commit()
        try:
            text_return = self.cur.fetchall()
        except pymssql.OperationalError:
            text_return = None
        self.close()
        return text_return

    def executevar(self,command,operands):
        self.connect()
        self.cur.execute(command,operands)
        self.conn.commit()
        try:
            text_return = self.cur.fetchall()
        except pymssql.OperationalError:
            text_return = None
        self.close()
        return text_return
    
    def insertPerson(self, username, name, status='NICE', status_description="Did nothing wrong."):
        self.executevar('INSERT INTO persons (name, username, status, status_description) VALUES(%s,%s,%s,%s)', (name, username, status, status_description))
        return None
    
    def getPersonsByUsername(self, username):
        persons = self.execute(f'SELECT * FROM persons WHERE username={username}')
        return persons[0]

    def getAllPersons(self):
        persons = self.execute('SELECT * FROM persons')
        return [person for person in persons]

    def getPersonsByStatus(self, status):
        persons = self.execute(f'SELECT * FROM persons WHERE status={status}')
        return [person for person in persons]

    def updatePersonStatus(self, username, status):
        self.execute(f'UPDATE persons SET status=\'{status}\' WHERE username={username}')
    
    def updatePersonStatusDescription(self, username, status_description):
        self.execute(f'UPDATE persons SET status_description=\'{status_description}\' WHERE username={username}')

    def checkPersonExists(self, username):
        users = self.execute(f'SELECT * FROM persons WHERE username=\'{username}\'')
        if len(users) > 0:
            return True
        else:
            return False

    def deletePersonByUsername(self, username):
        self.execute(f'DELETE FROM persons WHERE username=\'{username}\'')
        return None
