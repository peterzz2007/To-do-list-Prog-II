import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
import hashlib

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
        self.list.bind("<<ListboxSelect>>", self.on_select)
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
        c.execute(''' SELECT PROFILE_NAME, LAST_ACTIVE FROM PROFILE''')
        for row in c.fetchall():
            display_text = f"{row[0]} - ielogojies: {row[1]}"
            self.list.insert(tk.END, display_text)
        conn.commit()
        conn.close()

    def on_select(self, event):
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
        try:
            if self.psswrd == '':
                self.passwordtext.destroy()
                self.password.destroy()
                self.loginbtn.destroy()
            self.selecttext.destroy()
        except AttributeError:
            pass


    def enteruser(self):
        global loginindex
        selected_index = self.list.curselection()

        if selected_index:
            index = selected_index[0]
            fulltext = self.list.get(index)
            getpass = fulltext.split(" - ")[0].strip()
            loginindex = index
            conn = sqlite3.connect('todolist.db')
            c = conn.cursor()
            c.execute(''' SELECT  * FROM PROFILE WHERE PROFILE_NAME = ?''', (getpass,))
            for row in c.fetchall():
                self.psswrd = row[2]
            conn.commit()
            conn.close()
            
        try:
            if self.psswrd == '':
                for widget in self.winfo_children():
                    widget.destroy()
                    self.destroy()
                MainWindow(self.master)
                
            else:
                self.passwordtext = tk.Label(self, text="Ievadiet paroli", font= "Trebuchet")
                self.passwordtext.place( x=260 ,y= 145)
                self.password = tk.Entry(self, width= 25, font= "Trebuchet")
                self.password.place(x= 260, y = 170)
                self.loginbtn = tk.Button(self, text="Ielogoties", font= "Trebuchet", width= 8, command= self.passwordsys)
                self.loginbtn.place(x= 405, y = 195)
        except AttributeError:
            self.selecttext = tk.Label(self, text="Izvēlies profilu!", font= ("Trebuchet" ,15, "bold"))
            self.selecttext.place( x=260 ,y= 145)

    def passwordsys(self):
        self.entered_pass = self.password.get()
        ent_password = self.entered_pass
        ent_hashed = hashlib.sha256(ent_password.encode()).hexdigest()

        if self.psswrd == ent_hashed:
            for widget in self.winfo_children():
                widget.destroy()
                self.destroy()
            MainWindow(self.master)
        

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
        self.master.resizable(False, False)
        conn = sqlite3.connect('todolist.db')
        c = conn.cursor()
        c.execute('''
                CREATE TABLE IF NOT EXISTS TASK(
                    TASK_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    TASK_NAME TEXT NOT NULL UNIQUE,
                    TASK_DESC TEXT, 
                    TASK_NOTES TEXT,
                    TASK_DUE DATE,
                    PROFILE_ID INTEGER,
                    CATEGORY_ID INTEGER, 
                    FOREIGN KEY (PROFILE_ID) REFERENCES PROFILE(PROFILE_ID),
                    FOREIGN KEY (CATEGORY_ID) REFERENCES CATEGORY(CATEGORY_ID)
                                    )
        ''')
        c.execute('''
                CREATE TABLE IF NOT EXISTS CATEGORY(
                    CATEGORY_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    CATEGORY_NAME TEXT NOT NULL UNIQUE,
                    CATEGORY_DESC TEXT
                                    )
        ''')
        c.execute(''' SELECT  * FROM PROFILE WHERE PROFILE_ID = ?''', (loginindex + 1,))
        for row in c.fetchall():
         self.x = row[1]



        now = datetime.now()
        formatted_date = now.strftime("%d.%m.%Y")

        c.execute(''' UPDATE PROFILE SET LAST_ACTIVE = ? WHERE PROFILE_ID = ?''', (formatted_date, loginindex + 1,))
        

        label = tk.Label(self, text=f"Ielogojies profilā:", font= ("Trebuchet", 15, "bold"))
        label.place(x=300 ,y= 270)

        username = tk.Label(self, text=f"{self.x}", font= ("Trebuchet", 15, "bold"))
        username.place(x=300 ,y= 300)

        self.todolist = tk.Listbox(self, width = 31, height= 15, font= "Trebuchet", exportselection=False)
        self.todolist.bind("<Double-1>", self.task_view)
        self.todolist.place(x=10, y=40)

        addtask = tk.Button(self, text="Pievienot uzdevumu", font= "Trebuchet", width= 20 ,command= self.newtask)
        addtask.place(x=300 ,y= 10)

        edittask = tk.Button(self, text="Rediģēt uzdevumu", font= "Trebuchet", width= 20 ,command= self.taskeditor)
        edittask.place(x=300 ,y= 50)

        deletetask = tk.Button(self, text="Dzēst uzdevumu", font= "Trebuchet", width= 20, command= self.deletetaskc)
        deletetask.place(x=300 ,y= 90)

        addnotes = tk.Button(self, text="Pievienot piezīmi", font= "Trebuchet", width= 20, command= self.noteseditor)
        addnotes.place(x=300 ,y= 130)

        catedit = tk.Button(self, text="Kategorijas", font= "Trebuchet", width= 20,command= self.catmenu)
        catedit.place(x=300 ,y= 170)

        logout = tk.Button(self, text="Iziet no profila", font= "Trebuchet", width= 20,command= self.logout)
        logout.place(x=300 ,y= 210)

        self.category = ttk.Combobox(self, width= 29, font= "Trebuchet")
        self.category.bind("<<ComboboxSelected>>", self.task_filter)
        self.category.place(x= 10, y = 10)

        c.execute("SELECT * FROM CATEGORY")
        data = c.fetchall()
        self.catmapz = {row[1]:row[0] for row in data}
        self.category['values'] = ["Visi uzdevumi"] + list(self.catmapz.keys())
        conn.commit()
        conn.close()

        self.place(x=0, y=0, width=500, height=350)
        #self.laiks()

    def task_view(self, event):
        self.newtaskWindow = tk.Tk()
        self.newtaskWindow.wm_title("Uzdevums")
        self.newtaskWindow.wm_geometry("300x200")
        self.master.resizable(False, False)

        conn = sqlite3.connect('todolist.db')
        c = conn.cursor()
        selected_index = self.todolist.curselection()
        if selected_index:
            index = selected_index[0]
            fulltext = self.todolist.get(index)
            task_id = fulltext.split(" - ")[0].strip()
            print(task_id)
        c.execute("SELECT TASK_NAME, TASK_DESC, TASK_NOTES FROM TASK WHERE TASK_NAME = ?", (task_id,))
        for row in c.fetchall():
            self.task_name = row[0]
            self.task_desc = row[1]
            if row[2] == None:
                self.task_notes = "Nav piezīmju"
            else:
                self.task_notes = row[2]
        conn.commit()
        conn.close()  

        tasklabel = tk.Label(self.newtaskWindow, text=f"{self.task_name}", font= ("Trebuchet", 15, "bold"))
        tasklabel.place(x=10, y=5)
        taskdesctext = tk.Label(self.newtaskWindow, text="Apraksts", font= ("Trebuchet", 10))
        taskdesctext.place(x=10, y=40)
        taskdesc = tk.Label(self.newtaskWindow, text=f"{self.task_desc}", font= ("Trebuchet", 12))
        taskdesc.place(x=10, y=60)
        tasknotestext = tk.Label(self.newtaskWindow, text="Piezīmes", font= ("Trebuchet", 10))
        tasknotestext.place(x=10, y=100)
        tasknotes = tk.Label(self.newtaskWindow, text=f"{self.task_notes}", font= ("Trebuchet", 12))
        tasknotes.place(x=10, y=120)

    def task_filter(self, event=None):
        selected_name = self.category.get()
        cat_id = self.catmapz.get(selected_name)
        self.todolist.delete(0,tk.END)
        today = datetime.now().strftime("%d.%m.%Y") 
        conn = sqlite3.connect('todolist.db')
        c = conn.cursor()
        if selected_name == "Visi uzdevumi":

            c.execute("SELECT TASK_NAME, TASK_DUE FROM TASK WHERE PROFILE_ID = ?", (loginindex + 1,))
            data = c.fetchall()
            self.todolist.delete(0,tk.END)
            for row in data:
                taskname = row[0]
                duedate = row[1]

                date = datetime.strptime(duedate, "%d.%m.%Y").strftime("%d.%m.%Y") if duedate else "Nav limita"
                if duedate and duedate < today:
                    text = f"{taskname} - (Nokavēts!)"
                else:
                    text = f"{taskname} - (pildāms līdz: {date})"

                self.todolist.insert(tk.END, text)
        else:
            cat_id = self.catmapz.get(selected_name)
            c.execute("SELECT TASK_NAME, TASK_DUE FROM TASK WHERE PROFILE_ID = ? AND CATEGORY_ID = ?", 
                  (loginindex + 1, cat_id))
            data = c.fetchall()
            self.todolist.delete(0,tk.END)
            for row in data:
                taskname = row[0]
                duedate = row[1]

                date = datetime.strptime(duedate, "%d.%m.%Y").strftime("%d.%m.%Y") if duedate else "Nav limita"
                if duedate and duedate < today:
                    text = f"{taskname} - (Nokavēts!)"
                else:
                    text = f"{taskname} - (pildāms līdz: {date})"

                self.todolist.insert(tk.END, text)
        c.execute("SELECT TASK_NAME, TASK_DUE FROM TASK WHERE PROFILE_ID = ?", (loginindex + 1,))
            
        
        
        conn.close()

    def newtask(self):
            self.newtaskWindow = tk.Tk()
            self.newtaskWindow.wm_title("Jauns Uzdevums")
            self.newtaskWindow.wm_geometry("250x280")
            self.master.resizable(False, False)

            labeltest = tk.Label(self.newtaskWindow, text="Uzdevuma parametri", font= ("Trebuchet", 15, "bold"))
            labeltest.place(x=10, y=5)

            tasktext = tk.Label(self.newtaskWindow, text="Nosaukums", font= ("Trebuchet", 12))
            tasktext.place(x=10, y=35)
            self.task = tk.Entry(self.newtaskWindow, font= "Trebuchet", width= 25)
            self.task.place(x=10, y=60)

            descriptiontext = tk.Label(self.newtaskWindow, text="Apraksts", font= ("Trebuchet", 12))
            descriptiontext.place(x=10, y=85)
            self.description = tk.Entry(self.newtaskWindow, font= "Trebuchet", width= 25)
            self.description.place(x=10, y=110)

            timelimittext = tk.Label(self.newtaskWindow, text="Termiņš (dd.mm.gggg)", font= ("Trebuchet", 12))
            timelimittext.place(x=10, y=135)
            self.timelimit = tk.Entry(self.newtaskWindow, font= "Trebuchet", width= 25)
            self.timelimit.place(x=10, y=160)

            categorytext = tk.Label(self.newtaskWindow, text="Kategorija", font= ("Trebuchet", 12))
            categorytext.place(x=10, y=185)
            self.catelist = ttk.Combobox(self.newtaskWindow, font= "Trebuchet", width= 23)
            self.catelist.place(x=10, y=210)

            conn = sqlite3.connect('todolist.db')
            c = conn.cursor()
            c.execute("SELECT * FROM CATEGORY")
            data = c.fetchall()
            self.catmap = {row[1]:row[0] for row in data}
            self.catelist['values'] = list(self.catmap.keys())
            conn.commit()
            conn.close()

            bbtn = tk.Button(self.newtaskWindow, text= "atcelt", font=("Trebuchet", 10), width= 5,command= self.newtaskWindow.destroy)
            bbtn.place(x= 10, y= 240)

            donebtn = tk.Button(self.newtaskWindow, text= "Izveidot", font=("Trebuchet",10),width=5, command= self.createtask)
            donebtn.place(x= 190, y=240)
            self.newtaskWindow.place(x=10, y=10, width=300, height=250)
            self.newtaskWindow.mainloop()
            self.task_filter()

            

    def taskeditor(self):
            self.taskeditorw = tk.Tk()
            self.taskeditorw.wm_title("Rediģēt uzdevumu")
            self.taskeditorw.wm_geometry("250x280")
            self.master.resizable(False, False)
            
            labeltest = tk.Label(self.taskeditorw, text="Uzdevuma parametri", font= ("Trebuchet", 15, "bold"))
            labeltest.place(x=10, y=5)

            tasktext = tk.Label(self.taskeditorw, text="Nosaukums", font= ("Trebuchet", 12))
            tasktext.place(x=10, y=35)
            self.task = tk.Entry(self.taskeditorw, font= "Trebuchet", width= 25)
            self.task.place(x=10, y=60)

            descriptiontext = tk.Label(self.taskeditorw, text="Apraksts", font= ("Trebuchet", 12))
            descriptiontext.place(x=10, y=85)
            self.description = tk.Entry(self.taskeditorw, font= "Trebuchet", width= 25)
            self.description.place(x=10, y=110)

            timelimittext = tk.Label(self.taskeditorw, text="Termiņš (dd.mm.gggg)", font= ("Trebuchet", 12))
            timelimittext.place(x=10, y=135)
            self.timelimit = tk.Entry(self.taskeditorw, font= "Trebuchet", width= 25)
            self.timelimit.place(x=10, y=160)

            categorytext = tk.Label(self.taskeditorw, text="Kategorija", font= ("Trebuchet", 12))
            categorytext.place(x=10, y=185)
            self.catelistedit = ttk.Combobox(self.taskeditorw, font= "Trebuchet", width= 23)
            self.catelistedit.place(x=10, y=210)

            bbtn = tk.Button(self.taskeditorw, text= "atcelt", font=("Trebuchet", 10), width= 5, command= self.taskeditorw.destroy)
            bbtn.place(x= 10, y= 240)

            donebtn = tk.Button(self.taskeditorw, text= "Izveidot", font=("Trebuchet",10),width=5, command= self.edittask)
            donebtn.place(x= 190, y=240)
            

            selected_index = self.todolist.curselection()
            if selected_index:
                index = selected_index[0]
                fulltext = self.todolist.get(index)
                self.taskname = fulltext.split(" - ")[0].strip()
                conn = sqlite3.connect('todolist.db')
                c = conn.cursor()
                c.execute("""SELECT TASK_NAME, TASK_DESC, TASK_DUE, CATEGORY_ID FROM TASK WHERE TASK_NAME = ?""", (self.taskname,))
                row = c.fetchone()

                if row:
                    self.task.insert(0, row[0])        
                    self.description.insert(0, row[1]) 
                    self.timelimit.insert(0, row[2])
                    print (row[0], row[1], row[2])
            
                conn.commit()
                conn.close()
            
            conn = sqlite3.connect('todolist.db')
            c = conn.cursor()
            c.execute("SELECT * FROM CATEGORY")
            data = c.fetchall()
            self.catmap = {row[1]:row[0] for row in data}
            self.catelistedit['values'] = list(self.catmap.keys())
            conn.commit()
            conn.close()

            self.taskeditorw.place(x=10, y=10, width=300, height=250)
            

            self.taskeditorw.mainloop()
            self.task_filter()

    def createtask(self):
        selected_name = self.catelist.get()
        cat_id = self.catmap.get(selected_name)
        val1 = self.task.get()
        val2 = self.description.get()
        val3 = self.timelimit.get()
        val4 = loginindex + 1
        self.task.delete(0, tk.END)
        self.description.delete(0, tk.END)
        self.timelimit.delete(0, tk.END)
        self.todolist.delete(0, tk.END)
        conn = sqlite3.connect('todolist.db')
        c = conn.cursor()
        c.execute("INSERT INTO TASK ( TASK_NAME, TASK_DESC, TASK_DUE, PROFILE_ID, CATEGORY_ID) VALUES ( ?, ?, ?, ?, ?)", ( val1, val2, val3, val4, cat_id))
        c.execute(''' SELECT * FROM TASK WHERE PROFILE_ID = ?''', (loginindex + 1,))
        for row in c.fetchall():
            self.todolist.insert(tk.END, row[1])
        conn.commit()
        conn.close()
        self.newtaskWindow.destroy()
        self.task_filter()
        

    def edittask(self):
        selected_name = self.catelistedit.get()
        cat_id = self.catmap.get(selected_name)
        val1 = self.task.get()
        val2 = self.description.get()
        val3 = self.timelimit.get()
        self.task.delete(0, tk.END)
        self.description.delete(0, tk.END)
        self.timelimit.delete(0, tk.END)
        selected_index = self.todolist.curselection()
        if selected_index:
            index = selected_index[0]
            fulltext = self.todolist.get(index)
            self.taskname = fulltext.split(" - ")[0].strip()
            conn = sqlite3.connect('todolist.db')
            c = conn.cursor()
            c.execute("""
                UPDATE TASK 
                SET TASK_NAME = ?,
                TASK_DESC = ?, TASK_DUE = ?, CATEGORY_ID = ?
                WHERE TASK_NAME = ?
            """, (val1, val2, val3, cat_id, self.taskname))
            self.todolist.delete(0, tk.END)
            c.execute(''' SELECT * FROM TASK WHERE PROFILE_ID = ?''', (loginindex + 1,))
            for row in c.fetchall():
                self.todolist.insert(tk.END, row[1])
            
            conn.commit()
            conn.close()
            conn = sqlite3.connect('todolist.db')
        self.taskeditorw.destroy()
        self.task_filter()
     

    def logout(self):
        for widget in self.winfo_children():
            widget.destroy()
            self.destroy()
        login(self.master)
    
    def deletetaskc(self):
        selected_index = self.todolist.curselection()
        if selected_index:
            index = selected_index[0]
            fulltext = self.todolist.get(index)
            self.taskname = fulltext.split(" - ")[0].strip()
            conn = sqlite3.connect('todolist.db')
            c = conn.cursor()
            c.execute(''' DELETE FROM TASK WHERE TASK_NAME = ?''', (self.taskname,))
            c.execute(''' DELETE FROM SQLITE_SEQUENCE WHERE NAME = 'TASK' ''' )
            conn.commit()
            conn.close()
            self.todolist.delete(index)
            self.task_filter()
    
    def noteseditor(self):
            self.noteseditorw = tk.Tk()
            self.noteseditorw.wm_title("Pievienot piezīmi")
            self.noteseditorw.wm_geometry("400x120")
            self.master.resizable(False, False)

            labelnotes = tk.Label(self.noteseditorw, text="Pievienot piezīmi", font= ("Trebuchet", 15, "bold"))
            labelnotes.place(x=10, y=5)

            notestext = tk.Label(self.noteseditorw, text="Pievienojot piezīmi, iepriekšējā piezīme tiks dzēsta!", font= ("Trebuchet", 12))
            notestext.place(x=10, y=35)
            self.notes = tk.Entry(self.noteseditorw, font= "Trebuchet", width= 42)
            self.notes.place(x=10, y=60)

            bbtn = tk.Button(self.noteseditorw, text= "atcelt", font=("Trebuchet", 10), width= 5,command= self.noteseditorw.destroy)
            bbtn.place(x= 10, y= 90)

            donebtn = tk.Button(self.noteseditorw, text= "Izveidot", font=("Trebuchet",10),width=5, command= self.addnote)
            donebtn.place(x= 340, y=90)

            self.noteseditorw.place(x=10, y=10, width=400, height=120)
            self.noteseditorw.mainloop()
            self.task_filter()

    def addnote(self):
        val1 = self.notes.get()
        selected_index = self.todolist.curselection()
        if selected_index:
            index = selected_index[0]
            self.taskname = self.todolist.get(index)
            conn = sqlite3.connect('todolist.db')
            c = conn.cursor()
            c.execute("""UPDATE TASK SET TASK_NOTES = ? WHERE TASK_NAME = ?""", (val1, self.taskname))
        
            conn.commit()
            conn.close()
            self.noteseditorw.destroy()
            self.task_filter()

    def catmenu(self):
        self.catmenuw = tk.Tk()
        self.catmenuw.wm_title("Kategorijas")
        self.catmenuw.wm_geometry("450x200")
        self.master.resizable(False, False)
        
        labelnotes = tk.Label(self.catmenuw, text="Kategoriju izveide & rediģēšana", font= ("Trebuchet", 15, "bold"))
        labelnotes.place(x=10, y=5)

        notestext = tk.Label(self.catmenuw, text="Kategoriju saraksts", font= ("Trebuchet", 12))
        notestext.place(x=10, y=35)
        self.catlist = tk.Listbox(self.catmenuw, width = 25, height= 8, font= "Trebuchet")
        self.catlist.place(x=10, y=40)

        addtask = tk.Button(self.catmenuw, text="Pievienot kategoriju", font= "Trebuchet", width= 20 ,command= self.addcat)
        addtask.place(x=250 ,y= 40)

        edittask = tk.Button(self.catmenuw, text="Rediģēt kategoriju", font= "Trebuchet", width= 20 ,command= self.cateditor)
        edittask.place(x=250 ,y= 80)

        deletetask = tk.Button(self.catmenuw, text="Dzēst kategoriju", font= "Trebuchet", width= 20, command= self.deletecat)
        deletetask.place(x=250 ,y= 120)

        backbtn = tk.Button(self.catmenuw, text="Atcelt", font= "Trebuchet", width= 20, command= self.catmenuw.destroy)
        backbtn.place(x=250 ,y= 160)

        conn = sqlite3.connect('todolist.db')
        c = conn.cursor()
        c.execute(''' SELECT * FROM CATEGORY ''')
        for row in c.fetchall():
            self.catlist.insert(tk.END, row[1])
        self.catmenuw.place(x=10, y=10, width=450, height=200)
        self.catmenuw.mainloop()
        self.task_filter()
        
    def addcat(self):
            self.addcatw = tk.Tk()
            self.addcatw.wm_title("Jauna kategorija")
            self.addcatw.wm_geometry("250x190")
            self.master.resizable(False, False)

            labeltest = tk.Label(self.addcatw, text="Pievienot kategoriju", font= ("Trebuchet", 15, "bold"))
            labeltest.place(x=10, y=5)

            cattext = tk.Label(self.addcatw, text="Nosaukums", font= ("Trebuchet", 12))
            cattext.place(x=10, y=35)
            self.cat = tk.Entry(self.addcatw, font= "Trebuchet", width= 25)
            self.cat.place(x=10, y=60)

            descriptiontext = tk.Label(self.addcatw, text="Apraksts", font= ("Trebuchet", 12))
            descriptiontext.place(x=10, y=85)
            self.description = tk.Entry(self.addcatw, font= "Trebuchet", width= 25)
            self.description.place(x=10, y=110)

            bbtn = tk.Button(self.addcatw, text= "atcelt", font=("Trebuchet", 10), width= 5,command= self.addcatw.destroy)
            bbtn.place(x= 10, y= 150)

            donebtn = tk.Button(self.addcatw, text= "Izveidot", font=("Trebuchet",10),width=5, command= self.createcat)
            donebtn.place(x= 190, y=150)
            self.addcatw.place(x=10, y=10, width=300, height=190)
            
            self.addcatw.mainloop()
            self.task_filter()
    
    def createcat(self):
        val1 = self.cat.get()
        val2 = self.description.get()
        self.description.delete(0, tk.END)
        self.cat.delete(0, tk.END)
        self.catlist.delete(0, tk.END)
        conn = sqlite3.connect('todolist.db')
        c = conn.cursor()
        c.execute("INSERT INTO CATEGORY ( CATEGORY_NAME, CATEGORY_DESC) VALUES ( ?, ?)", ( val1, val2))
        c.execute(''' SELECT * FROM CATEGORY ''')
        for row in c.fetchall():
            self.catlist.insert(tk.END, row[1])
        conn.commit()
        conn.close()
        self.addcatw.destroy()
        self.task_filter()
    
    def cateditor(self):
            self.cateditorw = tk.Tk()
            self.cateditorw.wm_title("Jauna kategorija")
            self.cateditorw.wm_geometry("250x190")
            self.master.resizable(False, False)

            labeltest = tk.Label(self.cateditorw, text="Pievienot kategoriju", font= ("Trebuchet", 15, "bold"))
            labeltest.place(x=10, y=5)

            cattext = tk.Label(self.cateditorw, text="Nosaukums", font= ("Trebuchet", 12))
            cattext.place(x=10, y=35)
            self.cat = tk.Entry(self.cateditorw, font= "Trebuchet", width= 25)
            self.cat.place(x=10, y=60)

            descriptiontext = tk.Label(self.cateditorw, text="Apraksts", font= ("Trebuchet", 12))
            descriptiontext.place(x=10, y=85)
            self.description = tk.Entry(self.cateditorw, font= "Trebuchet", width= 25)
            self.description.place(x=10, y=110)

            bbtn = tk.Button(self.cateditorw, text= "atcelt", font=("Trebuchet", 10), width= 5,command= self.cateditorw.destroy)
            bbtn.place(x= 10, y= 150)

            donebtn = tk.Button(self.cateditorw, text= "Izveidot", font=("Trebuchet",10),width=5, command= self.editcat)
            donebtn.place(x= 190, y=150)
            self.cateditorw.place(x=10, y=10, width=300, height=190)
            
            self.cateditorw.mainloop()
            self.task_filter()

    def deletecat(self):
        selected_index = self.catlist.curselection()
        if selected_index:
            index = selected_index[0]
            catname = self.catlist.get(index)
            conn = sqlite3.connect('todolist.db')
            c = conn.cursor()
            c.execute(''' DELETE FROM CATEGORY WHERE CATEGORY_NAME = ?''', (catname,))
            c.execute(''' DELETE FROM SQLITE_SEQUENCE WHERE NAME = 'CATEGORY' ''' )
            conn.commit()
            conn.close()
            self.catlist.delete(index)
            self.task_filter()
    
    def editcat(self):
        val1 = self.cat.get()
        val2 = self.description.get()
        self.cat.delete(0, tk.END)
        self.description.delete(0, tk.END)
        selected_index = self.catlist.curselection()
        if selected_index:
            index = selected_index[0]
            self.catname = self.catlist.get(index)
            conn = sqlite3.connect('todolist.db')
            c = conn.cursor()
            c.execute("""
                UPDATE CATEGORY 
                SET CATEGORY_NAME = ?,
                CATEGORY_DESC = ?
                WHERE CATEGORY_NAME = ?
            """, (val1, val2, self.catname))
            self.catlist.delete(0, tk.END)
            c.execute(''' SELECT * FROM CATEGORY''')
            for row in c.fetchall():
                self.catlist.insert(tk.END, row[1])
            conn.commit()
            conn.close()
            self.cateditorw.destroy()
            self.task_filter()

        


class register(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.wm_title("To do list")
        self.master.resizable(False, False)
        
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
        hashval1 = hashlib.sha256(val1.encode()).hexdigest()
        val2 = self.username.get()
        self.password.delete(0, tk.END)
        self.username.delete(0, tk.END)
        conn = sqlite3.connect('todolist.db')
        c = conn.cursor()
        c.execute("INSERT INTO PROFILE ( PROFILE_NAME, PROFILE_PASSWORD) VALUES ( ?, ?)", ( val2, hashval1))
        
        conn.commit()
        conn.close()
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        login(self.master)
    




print(loginindex)
root = tk.Tk()
login(root)
root.mainloop()
