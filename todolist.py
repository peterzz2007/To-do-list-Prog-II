import tkinter as tk

def window(width, height):
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')


class login(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title = ("To do list")
        self.master.resizable(False, False)
        window(500, 350)
        # Programmas nosaukums iekš loga
        label = tk.Label(self, text="Profila Izvēlne", font= ("Trebuchet", 14 ,"bold"))
        label.place( x=260 ,y= 10)

        #Pogas

        loginz = tk.Button(self, text="Ielogoties profilā", font= "Trebuchet", width= 25)
        loginz.place(x=260 ,y= 40)

        newuser = tk.Button(self, text="Izveidot jaunu profilu", font= "Trebuchet", width= 25, command= self.adduser)
        newuser.place(x=260 ,y= 75)

        self.list = tk.Listbox(self, width = 40, height= 20)
        self.list.place(x=10, y=10)
        self.place(x=0, y=0, width=500, height=350)

    def adduser(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        register(self.master)

class register(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title = ("To do list")
        
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
        print(f"Username is {val2} and the password is {val1}")





root = tk.Tk()
login(root)
root.mainloop()
