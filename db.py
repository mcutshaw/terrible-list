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
                            name TEXT,
                            username TEXT,
                            status VARCHAR(100),
                            status_description TEXT,
                            CONSTRAINT pk_person_id PRIMARY KEY CLUSTERED (person_id),
                            CONSTRAINT uc_username UNIQUE (username));''')

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
    
    def insertJobs(self, name, job_depends = None, status='STOPPED', start_date= None, started_date = None, completed_date = None, cancelable = 1):
        if start_date == None:
            start_date = str(datetime.datetime.now())

        self.executevar('INSERT INTO `jobs` (name, job_depends, status, start, started_date, completed_date, cancelable) VALUES(%s,%s,%s,%s,%s,%s,%s)', (name, job_depends, status, start_date, started_date, completed_date, cancelable))
        id = self.cur.lastrowid
        return id
    
    def getJobByName(self, name):
        jobs = self.execute(f'SELECT * FROM `jobs` WHERE name={name}')
        return jobs[0]

    def getAllJobs(self):
        jobs = self.execute('SELECT * FROM `jobs`')
        return [job for job in jobs]
    
    def getReadyJobs(self):
        jobs = self.execute('SELECT * FROM jobs WHERE status=\'READY\' AND (start<=NOW() or start=NULL)')
        return [job for job in jobs]

    def updateJobStatus(self, job_id, status):
        self.execute(f'UPDATE `jobs` SET status=\'{status}\' WHERE job_id={job_id}')

    def updateJobStartedDate(self, job_id, started_date):
        self.execute(f'UPDATE `jobs` SET started_date=\'{started_date}\' WHERE job_id={job_id}')

    def updateJobCompletedDate(self, job_id, completed_date):
        self.execute(f'UPDATE `jobs` SET completed_date=\'{completed_date}\' WHERE job_id={job_id}')

    ###Tasks
    def insertTasks(self, job_id, operation, arguments=None, task_depends=None, status='READY', log=None, started_date=None, completed_date=None):
        self.executevar('INSERT INTO `tasks` (job_id, operation, arguments, task_depends, status, log, started_date, completed_date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)', (job_id, operation, arguments, task_depends, status, log, started_date, completed_date))
        id = self.cur.lastrowid
        return id
    
    def getTasksByJob(self, job_id):
        tasks = self.execute(f'SELECT * FROM `tasks` WHERE job_id={job_id}')
        return [task for task in tasks]

    def getTaskByID(self, task_id):
        tasks = self.execute(f'SELECT * FROM `tasks` WHERE task_id={task_id}')
        return tasks[0]
    
    def getLastInfoTableTask(self, table):
        tasks = self.execute(f'SELECT * FROM `tasks` WHERE operation=\'UPDATEDB\' AND arguments=\'{table}\' ORDER BY completed_date DESC LIMIT 1')
        if tasks == ():
            return None
        print(tasks)
        return tasks[0]
    
    def updateTaskStatus(self, task_id, status):
        self.execute(f'UPDATE `tasks` SET status=\'{status}\' WHERE task_id={task_id}')

    def updateTaskStartedDate(self, task_id, started_date):
        self.execute(f'UPDATE `tasks` SET started_date=\'{started_date}\' WHERE task_id={task_id}')

    def updateTaskCompletedDate(self, task_id, completed_date):
        self.execute(f'UPDATE `tasks` SET completed_date=\'{completed_date}\' WHERE task_id={task_id}')

    def updateTaskLog(self, task_id, log):
        query = f'UPDATE `tasks` SET log=\'{log}\' WHERE task_id={task_id}'
        print(query)
        self.execute(query)

    ###Users
    def insertUser(self, username, role='admin', disabled=False):
        self.executevar('INSERT INTO `users` (username, role, disabled) VALUES(%s,%s,%s)', (username, role, disabled))
        id = self.cur.lastrowid
        return id
    
    def getUserByName(self, username):
        users = self.execute(f'SELECT * FROM `users` WHERE username=\'{username}\'')
        return [user for user in users]
    
    def getUsers(self):
        users = self.execute(f'SELECT * FROM `users`')
        return [user for user in users]

    def checkUserActive(self, username):
        users = self.execute(f'SELECT * FROM `users` WHERE username=\'{username}\' and disabled=false')
        if len(users) > 0:
            return True
        else:
            return False


    def checkUserExists(self, username):
        users = self.execute(f'SELECT * FROM `users` WHERE username=\'{username}\'')
        if len(users) > 0:
            return True
        else:
            return False

    def deleteUserByName(self, username):
        self.execute(f'DELETE FROM `users` WHERE username=\'{username}\'')
        return None
