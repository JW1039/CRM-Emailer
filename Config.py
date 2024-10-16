import tkinter as tk
import json
from os import getenv, mkdir, path

class ConfigDialog():

    def __init__(self):
        self.elements = {}
        self.write_path = getenv("APPDATA")

        self.window = tk.Tk()
        self.window.title("Configuration")
        self.window.geometry("500x300")

        self.elements['lblTitle'] = tk.Label(self.window, text="Email Login",font=('Arial',17))

        self.elements['lblUser'] = tk.Label(self.window,text='Email:')
        self.elements['enyUser'] =  tk.Entry(self.window, width=35)

        self.elements['lblPass'] = tk.Label(self.window,text='Password:')
        self.elements['enyPass'] =  tk.Entry(self.window, width=35, show="*")

        self.elements['lblUserTitle'] = tk.Label(self.window,text='Your Information:', font=('Arial', 17))

        self.elements['lblUserName'] = tk.Label(self.window,text='Your Name:')

        self.elements['enyUserName'] =  tk.Entry(self.window, width=35)

        self.elements['lblSubject'] = tk.Label(self.window,text='Subject:')
        self.elements['enySubject'] =  tk.Entry(self.window, width=50)

        file_path = self.write_path + "\Emailer\config.json"

        if path.exists(file_path):
            with open(file_path) as json_file:
                config_file = json.load(json_file)

                try:
                    self.elements['enyUser'].insert(0,config_file['email'])
                except:
                    pass
                try:
                    self.elements['enyPass'].insert(0,config_file['password'])
                except:
                    pass

                try:
                    self.elements['enyUserName'].insert(0,config_file['name'])
                except:
                    pass
                try:
                    self.elements['enySubject'].insert(0,config_file['subject'])
                except:
                    self.elements['enySubject'].insert(0, "Notice for {{OWNER NAME}}")


        self.elements['btnSubmit'] = tk.Button(self.window, text="Save", command=self.onSubmit,bg="#290769", fg="white")

        self.pack()

    def __getitem__(self, key):
        return self.elements[key]


    def pack(self):
        for key in self.elements:
            self.elements[key].pack()


    def onSubmit(self):

        data = {'email': self.elements['enyUser'].get(),
                'password': self.elements['enyPass'].get(),
                'name': self.elements['enyUserName'].get(),
                'subject': self.elements['enySubject'].get()}
        

        # Serializing json
        json_object = json.dumps(data, indent=4)
        
        if not path.isdir(self.write_path + '\Emailer'):
            mkdir(self.write_path + '\Emailer')

        with open(self.write_path + "\Emailer\config.json", "w") as outfile:
            outfile.write(json_object)
        
        tk.messagebox.showinfo("INFO","Successfully updated configuration!")
        self.window.destroy()

        
class Config():
    def __init__(self, data = None):

        if data is not None:
            try:
                self.name = data['name']
                self.email = data['email']
                self.password = data['password']
                self.password = data['subject']
            except:
                pass

        else:
            self.update()

        
    def update(self):

        file_path = getenv("APPDATA") + "\Emailer\config.json"
        if path.exists(file_path):
            with open(file_path) as json_file:
                config_file = json.load(json_file)

                try:
                    self.name = config_file['name']
                    self.email = config_file['email']
                    self.password = config_file['password']
                    self.subject = config_file['subject']
                except:
                    pass