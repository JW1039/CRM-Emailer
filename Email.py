import smtplib, ssl
from random import randint
import time
from Config import Config
from CRM import CRM
from tkinter import ttk
import tkinter as tk


class Email():

    def __init__(self, conf: Config):

        self.conf = conf

        self.context = ssl.create_default_context()
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        self.server = smtplib.SMTP(smtp_server,port)
        self.server.starttls(context=self.context) # Secure the connection
        self.server.login(conf.email, conf.password)

        self.email = self.conf.email


    def send(self,to, subject,message):
        send_message = "Subject:%s\n\n%s" % (subject, message)
        self.server.sendmail(self.email, to, send_message)

    def t_send(self,to, subject,message):
        pass


    def end(self):
        self.server.quit()






class EmailWidget():
    def __init__(self, window, results: CRM, destroyCallback):
        self.results = results
        self.window = window
        self.elements = {}
        self.destroyCallback = destroyCallback
        self.conf = Config()
        self.emails = Email(self.conf)

        self.sendEmails()



    def pack(self):
        for e in self.elements:
            self.elements[e].pack()

    def destroy(self):
        for e in self.elements:
            self.elements[e].destroy()
    
    def sendEmails(self):

        self.elements['lblProgress'] = tk.Label(self.window, text='Send Emails...')
        self.elements['progress'] = ttk.Progressbar(self.window, mode='determinate', orient = tk.HORIZONTAL, length = int(self.window.winfo_width()/2))
        self.elements['lblProgress'].pack()
        self.elements['progress'].pack()
       
        idx = 0
        for r in self.results:
            time.sleep(randint(1,3))
            self.emails.send(r['email'], self.conf.subject.replace('{{OWNER NAME}}', r['name']), r['result'])
            self.elements['lblProgress']['text'] = 'Sending Emails... ' + str(idx+1) + '/' + str(self.results.length)
            self.elements['progress']['value'] = int(((idx+1)/self.results.length)*100)
            self.window.update()
            idx += 1

        self.elements['progress'].destroy()
        self.elements['lblProgress']['text'] = "Successfully Sent All Emails!"
        self.elements['btnEnd'] = tk.Button(self.window, text="Return to CRM Picker", command=self.onEnd)
        self.elements['btnEnd'].pack()
        

    def onEnd(self):
        self.destroy()
        self.destroyCallback()
