import tkinter as tk
import sqlite3

def window(width, height):
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

loginindex = 0

class login(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.wm_title("To do list")
        self.master.resizable(False, False)

        window(500, 350)
        # Programmas nosaukums iekš loga
        label = tk.Label(self, text="Profila Izvēlne", font= ("Trebuchet", 14 ,"bold"))
        label.place( x=260 ,y= 10)

        #Pogas

        loginz = tk.Button(self, text="Ielogoties profilā", font= "Trebuchet", width= 25, command= self.enteruser)
        loginz.place(x=260 ,y= 40)

        newuser = tk.Button(self, text="Izveidot jaunu profilu", font= "Trebuchet", width= 25, command= self.adduser)
        newuser.place(x=260 ,y= 75)

        deleteuser = tk.Button(self, text="Dzēst profilu", font= "Trebuchet", width= 25, command= self.deleteuserc)
        deleteuser.place(x=260 ,y= 110)

        self.list = tk.Listbox(self, width = 27, height= 17, font= "Trebuchet")
        self.list.place(x=10, y=10)
        self.place(x=0, y=0, width=500, height=350)

        conn = sqlite3.connect('todolist.db')
        c = conn.cursor()
        c.execute('''
                CREATE TABLE IF NOT EXISTS PROFILE(
                    PROFILE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    PROFILE_NAME TEXT NOT NULL UNIQUE,
                    PROFILE_PASSWORD TEXT, 
                    LAST_ACTIVE DATE 
                                    )
        ''')
        c.execute(''' SELECT * FROM PROFILE''')
        for row in c.fetchall():
            self.list.insert(tk.END, row[1])
        conn.commit()
        conn.close()

    def enteruser(self):
        global loginindex
        selected_index = self.list.curselection()
        if selected_index:
            index = selected_index[0]
            getpass = self.list.get(index)
            loginindex = index
            conn = sqlite3.connect('todolist.db')
            c = conn.cursor()
            c.execute(''' SELECT  * FROM PROFILE WHERE PROFILE_NAME = ?''', (getpass,))
            for row in c.fetchall():
                self.psswrd = row[2]
            conn.commit()
            conn.close()
            

        if self.psswrd == None:
            pass
        else:
            passwordtext = tk.Label(self, text="Ievadiet paroli", font= "Trebuchet")
            passwordtext.place( x=260 ,y= 145)
            self.password = tk.Entry(self, width= 25, font= "Trebuchet")
            self.password.place(x= 260, y = 170)
            backbtn = tk.Button(self, text="Ielogoties", font= "Trebuchet", width= 8, command= self.passwordsys)
            backbtn.place(x= 405, y = 195)

    def passwordsys(self):
        self.entered_pass = self.password.get()
        if self.psswrd == self.entered_pass:
            for widget in self.winfo_children():
                widget.destroy()
                self.destroy()
                MainWindow(self.master)
            print("Password correct")
        else:
            print("Password incorrect")


            
        
    


    def deleteuserc(self):
        selected_index = self.list.curselection()
        if selected_index:
            index = selected_index[0]
            userdelete = self.list.get(index)
            conn = sqlite3.connect('todolist.db')
            c = conn.cursor()
            c.execute(''' DELETE FROM PROFILE WHERE PROFILE_NAME = ?''', (userdelete,))
            c.execute(''' DELETE FROM SQLITE_SEQUENCE WHERE NAME = 'PROFILE' ''')
            conn.commit()
            conn.close()
            self.list.delete(index)


    def adduser(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        register(self.master)
        
class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.wm_title("To do list")
        window(500, 350)

        conn = sqlite3.connect('todolist.db')
        c = conn.cursor()
        c.execute(''' SELECT  * FROM PROFILE WHERE PROFILE_ID = ?''', (loginindex + 1,))
        for row in c.fetchall():
         x = row[1]
        
        conn.commit()
        conn.close()
        label = tk.Label(self, text=f"Ielogojies profilā:", font= ("Trebuchet", 15, "bold"))
        label.place(x=300 ,y= 270)

        username = tk.Label(self, text=f"{x}", font= ("Trebuchet", 15, "bold"))
        username.place(x=300 ,y= 300)

        todolist = tk.Listbox(self, width = 31, height= 15, font= "Trebuchet")
        todolist.place(x=10, y=40)

        addtask = tk.Button(self, text="Pievienot uzdevumu", font= "Trebuchet", width= 20 ,command= self.newtask)
        addtask.place(x=300 ,y= 10)

        edittask = tk.Button(self, text="Rediģēt uzdevumu", font= "Trebuchet", width= 20)
        edittask.place(x=300 ,y= 50)

        deletetask = tk.Button(self, text="Dzēst uzdevumu", font= "Trebuchet", width= 20)
        deletetask.place(x=300 ,y= 90)

        addnotes = tk.Button(self, text="Pievienot piezīmi", font= "Trebuchet", width= 20)
        addnotes.place(x=300 ,y= 130)

        self.username = tk.Entry(self, width= 31, font= "Trebuchet")
        self.username.place(x= 10, y = 10)

        self.place(x=0, y=0, width=500, height=350)


    def popupBonus():
            popupBonusWindow = tk.Tk()
            popupBonusWindow.wm_title("Window")
            labelBonus = Label(popupBonusWindow, text="Input")
            labelBonus.grid(row=0, column=0)
            
        


class register(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.wm_title("To do list")
        
        window(315, 250)
        # Programmas nosaukums iekš loga
        label = tk.Label(self, text="Profila veidošana", font= ("Trebuchet", 20, "bold"))
        label.place( x=20 ,y= 10)

        usernametext = tk.Label(self, text="Profila nosaukums", font= "Trebuchet")
        usernametext.place( x=20 ,y= 55)
        self.username = tk.Entry(self, width= 30, font= "Trebuchet")
        self.username.place(x= 20, y = 80)

        passwordtext = tk.Label(self, text="Profila parole", font= "Trebuchet")
        passwordtext.place( x=20 ,y= 105)
        self.password = tk.Entry(self, width= 30, font= "Trebuchet")
        self.password.place(x= 20, y = 130)

        backbtn = tk.Button(self, text="atpakaļ", font= "Trebuchet", width= 8, command=self.backbtn)
        backbtn.place(x= 20, y = 160)

        create = tk.Button(self, text="Izveidot", font= "Trebuchet", width= 8, command=self.createprofile)
        create.place(x= 213, y = 160)
        self.place(x=0, y=0, width=500, height=350)

    
    def backbtn(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        login(self.master)

    def createprofile(self):
        val1 = self.password.get()
        val2 = self.username.get()
        conn = sqlite3.connect('todolist.db')
        c = conn.cursor()
        c.execute("INSERT INTO PROFILE ( PROFILE_NAME, PROFILE_PASSWORD) VALUES ( ?, ?)", ( val2, val1))
        conn.commit()
        conn.close()
       
        print(f"Username is {val2} and the password is {val1}")
    




print(loginindex)
root = tk.Tk()
login(root)
root.mainloop()





root = tk.Tk()
login(root)
root.mainloop()
