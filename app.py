from tkinter import *
from dbhelper import DBhelper
from tkinter import messagebox
from PIL import Image,ImageTk
from tkinter import filedialog
import os,shutil


class Login:
    def __init__(self):
        self.db=DBhelper()#loading the database
        self.root = Tk()#root is created once
        self.root.title("My Login App")#slaves of the root are created more than once
        self.root.configure(background="red")
        self.root.minsize(300, 500)
        self.root.maxsize(300, 500)
        self.load_gui()

    def load_gui(self):
        self.clear()
        self.label1 = Label(self.root, text="Tinder", fg="white", bg="red")
        self.label1.configure(font=("Times", 30, "bold"))
        self.label1.pack(pady=(10, 10))  # puts lbel on gui#three line forming label


        self.label2 = Label(self.root, text="Email:", fg="white", bg="#7D05FC")  #fg=foreground bg=background
        self.label2.configure(font=("Times", 20, "italic"))
        self.label2.pack(pady=(5, 5))  # padding in y direction

        self.email = Entry(self.root)
        self.email.pack(pady=(0, 10), ipadx=30, ipady=5)  # to take a text input
        # setting margin x=0,y=10,.....again setting x,y


        self.label3 = Label(self.root, text="Password:", fg="white", bg="#7D05FC")
        self.label3.configure(font=("Times", 20, "italic"))
        self.label3.pack(pady=(5, 5))  # padding in y direction

        self.password = Entry(self.root)
        self.password.pack(pady=(0, 10), ipadx=30, ipady=5)


        # adding button
        self.login = Button(self.root, text="Login", bg="white",command=lambda: self.btn_click())
        #aftter clicking button command is getting storred
        self.login.pack(pady=(3, 10), ipadx=35, ipady=0.5)  # 1 is for increasing the y height

        self.label4=Label(self.root,text="Not a member?sign up",fg="white",bg="#7D05FC")
        self.label4.configure(font=("Times", 15, "italic"))
        self.label4.pack(pady=(5, 5))

        self.register = Button(self.root, text="sign up", bg="white", command=lambda: self.register_gui())
        # aftter clicking button command is getting storred
        self.register.pack(pady=(5, 10), ipadx=35, ipady=1)

        self.root.mainloop()#same like getch

    def register_gui(self):#for signing up purpose
        self.clear()

        self.label0 = Label(self.root, text="Tinder", fg="white", bg="red")
        self.label0.configure(font=("Times", 30, "bold"))
        self.label0.pack(pady=(10, 10))  # puts lbel on gui#three line forming label

        self.label1 = Label(self.root, text="Nane:", fg="white", bg="#7D05FC")  # fg=foreground bg=background
        self.label1.configure(font=("Times", 20, "italic"))
        self.label1.pack(pady=(5, 5))  # padding in y direction

        self.name = Entry(self.root)
        self.name.pack(pady=(0, 10), ipadx=30, ipady=5)  # to take a text input
        # setting margin x=0,y=10,.....again setting x,y

        self.label2 = Label(self.root, text="Email:", fg="white", bg="#7D05FC")  # fg=foreground bg=background
        self.label2.configure(font=("Times", 20, "italic"))
        self.label2.pack(pady=(5, 5))  # padding in y direction

        self.email = Entry(self.root)
        self.email.pack(pady=(0, 10), ipadx=30, ipady=5)

        self.label3 = Label(self.root, text="Password:", fg="white", bg="#7D05FC")
        self.label3.configure(font=("Times", 20, "italic"))
        self.label3.pack(pady=(5, 5))  # padding in y direction

        self.password = Entry(self.root)
        self.password.pack(pady=(0, 10), ipadx=30, ipady=5)

        self.filebtn=Button(self.root,text="Upload dp",command=lambda: self.upload_file())
        self.filebtn.pack(pady=(5,5))

        self.filename=Label(self.root)
        self.filename.pack(pady=(5,5))


        # adding button
        self.register = Button(self.root, text="sign up", bg="white", command=lambda: self.reg_submit())
        # aftter clicking button command is getting storred
        self.register.pack(pady=(3, 10), ipadx=55, ipady=0.5)  # 1 is for increasing the y height

        self.label4 = Label(self.root, text="Already a member?sign up", fg="white", bg="#7D05FC")
        self.label4.configure(font=("Times", 15, "italic"))
        self.label4.pack(pady=(5, 5))

        self.login = Button(self.root, text="login", bg="white", command=lambda: self.load_gui())
        # aftter clicking button command is getting storred
        self.login.pack(pady=(5, 10), ipadx=35, ipady=1)

    def upload_file(self):
        filename=filedialog.askopenfilename(initialdir="/images",title="Something")
        self.filename.configure(text=filename)

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def btn_click(self):
        email=self.email.get()
        password=self.password.get()

        data=self.db.check_login(email,password)

        if len(data)>0:#not empty string
            #messagebox.showinfo("login successful","you may procced now!")
            self.clear()
            self.user_id=data[0][0]#to fetch 1st data of 1st tuple
            self.user_data=data[0]
            self.load_user_info()
        else:
            messagebox.showerror("Error","Incorrect email/password")

    def load_user_info(self):
        self.main_window(self.user_data)#all the data to main window

    def logout(self):#session expire
        self.user_id=''
        self.user_data=''
        self.load_gui()

    def view_others(self,index=0):#default index=0
        #fetch data of all other users,to connect db---->dbhelper
        data=self.db.fetch_others(self.user_id)
        #print(data)
        num=len(data)
        self.main_window(data[index],mode=2,index=index,num=num)#num for number of users

    def navbar(self):#for creating the menu bar
        menu=Menu(self.root)
        self.root.config(menu=menu)
        filemenu=Menu(menu)
        menu.add_cascade(label="Home",menu=filemenu)
        filemenu.add_command(label="My profile",command=lambda: self.main_window(self.user_data))#passing user data to main window
        filemenu.add_command(label="Edit profile",command=lambda: self.edit_profile())
        filemenu.add_command(label="View profile",command=lambda: self.view_others())
        filemenu.add_command(label="Logout",command=lambda: self.logout())#for make the ac expire

        helpmenu=Menu(menu)
        menu.add_cascade(label="Proposals",menu=helpmenu)
        helpmenu.add_command(label="My proposals",command=lambda: self.view_proposals())
        helpmenu.add_command(label="My requests",command=lambda: self.view_requests())
        helpmenu.add_command(label="My matches",command=lambda: self.view_matches())

    def view_matches(self,index=0):
        self.clear()
        # step 1:fetch data from db
        data = self.db.view_matches(self.user_id)
        # step2:call main_window func
        num = len(data)
        new_data = []
        for i in data:
            new_data.append(i[3:])
        self.main_window(new_data[index], mode=3, index=index, num=num)

    def view_requests(self,index=0):
        #step 1:fetch data from db
        data=self.db.view_requests(self.user_id)
        #step2:call main_window func
        num=len(data)
        new_data=[]
        for i in data:
            new_data.append(i[3:])
        self.main_window(new_data[index],mode=3,index=index,num=num)

    def view_proposals(self,index=0):
        #step 1:fetch data from db
        data=self.db.view_proposals(self.user_id)
        #step2:call main_window func
        num=len(data)
        new_data=[]
        for i in data:
            new_data.append(i[3:])
        self.main_window(new_data[index],mode=3,index=index,num=num)

    def main_window(self,data,mode=1,index=None,num=None):#all guis are controlled by this,mode=1-->seeing own profile
        self.clear()
        self.navbar()

        imageUrl="images/{}".format(data[8])
        load=Image.open(imageUrl)
        load=load.resize((200, 200), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img=Label(image=render)
        img.image=render
        img.pack()

        self.label1=Label(self.root,text="Name:"+data[1],fg="white", bg="#7D05FC")#passing index 1=name to label in gui
        self.label1.configure(font=("Times", 15, "bold"))
        self.label1.pack(pady=(10,10))

        if len(data[7]) != 0:
            self.label2 = Label(self.root, text="From:" + data[7], fg="white", bg="#7D05FC")  # passing index 1=name to label in gui
            self.label2.configure(font=("Times", 15, "bold"))
            self.label2.pack(pady=(10, 10))

        if len(data[6]) != 0:
            self.label3 = Label(self.root, text="Not interested in:" + data[6], fg="white",bg="#7D05FC")  # passing index 1=name to label in gui
            self.label3.configure(font=("Times", 15, "bold"))
            self.label3.pack(pady=(10, 10))

        if len(data[4]) != 0:
            self.label4 = Label(self.root, text="About me:" + data[4], fg="white", bg="#7D05FC")  # passing index 1=name to label in gui
            self.label4.configure(font=("Times", 10))
            self.label4.pack(pady=(10, 10))

        if mode==2:#showing others profile
            frame = Frame(self.root)
            frame.pack()

            if index!=0:
                previous = Button(frame, text="Previous", command=lambda: self.view_others(index - 1))  # adding button in frame,after 0,-1 comes,-2,---
                previous.pack(side='left')
            propose = Button(frame, text="Propose",command=lambda: self.propose(self.user_id,data[0]))#1st data user_id,fetching that
            propose.pack(side='left')
            if index!=(num-1):
                next = Button(frame, text="Next",command=lambda: self.view_others(index+1))#after last id,code phat rha
                next.pack(side='left')
        if mode==3:#showing others profile
            frame = Frame(self.root)
            frame.pack()

            if index!=0:
                previous = Button(frame, text="Previous", command=lambda: self.view_proposals(index - 1))  # adding button in frame,after 0,-1 comes,-2,---
                previous.pack(side='left')
            if index!=(num-1):
                next = Button(frame, text="Next",command=lambda: self.view_proposals(index=index+1))#after last id,code phat rha
                next.pack(side='left')
    def propose(self,romeo_id,juliet_id):#from db
        response=self.db.propose(romeo_id,juliet_id)
        if response==1:
            messagebox.showinfo("Success","Proposal sent successfully.Fingers crossed!")
        elif response==-1:
            messagebox.showerror("Error","u have already proposed this user!!")
        else:
            messagebox.showerror("Error","Some error occured")

    def edit_profile(self):
        self.clear()
        self.label0 = Label(self.root, text="Edit Profile", fg="white", bg="red")
        self.label0.configure(font=("Times", 30, "bold"))
        self.label0.pack(pady=(10, 10))  # puts lbel on gui#three line forming label

        self.label1 = Label(self.root, text="Bio:", fg="white", bg="#7D05FC")  # fg=foreground bg=background
        self.label1.configure(font=("Times", 20, "italic"))
        self.label1.pack(pady=(5, 5))  # padding in y direction

        self.bio = Entry(self.root)
        self.bio.pack(pady=(0, 10), ipadx=30, ipady=5)  # to take a text input
        # setting margin x=0,y=10,.....again setting x,y

        self.label2 = Label(self.root, text="Age:", fg="white", bg="#7D05FC")  # fg=foreground bg=background
        self.label2.configure(font=("Times", 20, "italic"))
        self.label2.pack(pady=(5, 5))  # padding in y direction

        self.age = Entry(self.root)
        self.age.pack(pady=(0, 10), ipadx=30, ipady=5)

        self.label3 = Label(self.root, text="Gender:", fg="white", bg="#7D05FC")
        self.label3.configure(font=("Times", 20, "italic"))
        self.label3.pack(pady=(5, 5))  # padding in y direction

        self.gender = Entry(self.root)
        self.gender.pack(pady=(0, 10), ipadx=30, ipady=5)

        self.label4= Label(self.root, text="City:", fg="white", bg="#7D05FC")
        self.label4.configure(font=("Times", 20, "italic"))
        self.label4.pack(pady=(5, 5))  # padding in y direction

        self.city = Entry(self.root)
        self.city.pack(pady=(0, 10), ipadx=30, ipady=5)
        # adding button
        self.edit = Button(self.root, text="Edit Profile", bg="white", command=lambda: self.update_profile())
        # aftter clicking button command is getting storred
        self.edit.pack(pady=(3, 10), ipadx=55, ipady=0.5)  # 1 is for increasing the y height

    def update_profile(self):
        bio=self.bio.get()
        age=self.age.get()
        gender=self.gender.get()
        city=self.city.get()

        info=[bio,age,gender,city]
        response=self.db.update_profile(self.user_id,info)
        if response==1:
            messagebox.showinfo("Successs","Profile updated")
        else:
            messagebox.showerror("Error", "Error occupied")
    def reg_submit(self):
        name=self.name.get()
        email=self.email.get()
        password=self.password.get()
        filename=self.filename['text'].split('/')[-1]

        response=self.db.insert_user(name,email,password,filename)#calling database function to take new input
        #print(self.filename['text'])
        #print("C:\\Users\\Chitraneswa\\PycharmProjects\\finder\\images\\th (28).jpg"+filename)
        if response==1:
            shutil.copyfile(self.filename['text'],"C:\\Users\\Chitraneswa\\PycharmProjects\\finder\\images\\th (28).jpg"+filename)
            messagebox.showinfo("Registration successful","you may login now!")
        else:
            messagebox.showerror("Error","Database Error")

obj = Login()
#obj.load_gui()