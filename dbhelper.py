import mysql.connector#package,to connect to mysql

class DBhelper:

    def __init__(self):
        # to connect to the database
        try:
            self.conn=mysql.connector.connect(host='localhost',user='root',password='',database='finder')
            self.mycursor=self.conn.cursor()#conn=connected,stores in mycursor
            print("Connected to DB")#after connection is done
        except Exception as e:
            print(e)#printing,if it is not connected to db

    def check_login(self,email,password):

        self.mycursor.execute("SELECT * FROM users WHERE email LIKE '{}' AND password LIKE '{}'".format(email,password))
        data=self.mycursor.fetchall()
        # print(data)
        return data

    def insert_user(self,name,email,password,filename):
        # write query
        try:
            #print("INSERT INTO users (user_id,name,email,password) VALUES (NULL,'{}','{}','{}')".format(name,email,password))
            self.mycursor.execute("INSERT INTO users (user_id,name,email,password,dp) VALUES (NULL,'{}','{}','{}','{}')".format(name,email,password,filename))
            self.conn.commit()#for create,update,dlt
            return 1
        except Exception as e:
            print(e)
            return 0

    def update_profile(self,user_id,info):
        try:
            self.mycursor.execute("UPDATE users SET bio='{}',age={},gender='{}',city='{}' WHERE user_id={}".format(info[0],info[1],info[2],info[3],user_id))
            self.conn.commit()
            return 1
        except:
            return 0

    def fetch_others(self,user_id):
        self.mycursor.execute("SELECT * FROM users WHERE user_id NOT LIKE {}".format(user_id))
        data=self.mycursor.fetchall()
        return data

    def propose(self,romeo_id,juliet_id):
        self.mycursor.execute("SELECT * FROM proposals WHERE romeo_id={} AND juliet_id={}".format(romeo_id, juliet_id))
        data=self.mycursor.fetchall()
        if len(data)!=0:
            return -1
        else:
            try:
                self.mycursor.execute("INSERT INTO proposals (proposal_id,romeo_id,juliet_id) VALUES (NULL,{},{})".format(romeo_id,juliet_id))
                self.conn.commit()
                return 1
            except:
                return 0

    def view_proposals(self,romeo_id):
        self.mycursor.execute("SELECT * FROM proposals JOIN users ON users.user_id=proposals.juliet_id WHERE romeo_id={}".format(romeo_id))
        data=self.mycursor.fetchall()
        return data

    def view_requests(self, juliet_id):
        self.mycursor.execute("SELECT * FROM proposals JOIN users ON users.user_id=proposals.romeo_id WHERE juliet_id={}".format(juliet_id))
        data = self.mycursor.fetchall()
        return data

    def view_matches(self,user_id):
        self.mycursor.execute("SELECT * FROM proposals JOIN users ON users.user_id=proposals.juliet_id WHERE juliet_id in (SELECT romeo_id FROM `proposals` WHERE juliet_id={}) AND romeo_id={}".format(user_id,user_id))
        data=self.mycursor.fetchall()
        return data
        # obj=DBhelper()
        # obj.check_login("virat@gmail.com","12345")