import tkinter as tk
from Email import EmailWidget

class ResultView():

    def __init__(self, window, crm, callback) -> None:
        self.window = window
        self.callback = callback
        self.elements = {}
        self.elements["frmMain"] = tk.Frame(self.window, height=200,bg="lightblue", width=200, borderwidth=20)
        self.elements["frmMain"].pack()

        self.elements['btnBack'] = tk.Button(self.elements['frmMain'], text='↶', command=self.back)
        self.elements['btnBack'].grid(row=0,column=0)

        self.elements['enyGPT'] = tk.Text(self.elements['frmMain'], width=50, height=15, font=('Arial',11))
        self.elements['enyGPT'].insert(tk.END,crm['result'])
        self.elements['enyGPT'].grid(row=0,column=1,pady=(0,10))
        self.disableInput()

        # Add buttons to the frame
        self.elements['btnDecline'] = tk.Button(self.elements['frmMain'], text="❌", fg="red", command=self.decline)
        self.elements['btnDecline'].grid(row=1,column=0)

        self.elements['btnEdit'] = tk.Button(self.elements['frmMain'], text="Edit", command=self.edit)
        self.elements['btnEdit'].grid(row=1,column=1)


        self.elements['btnAccept'] = tk.Button(self.elements['frmMain'], text="✔", fg="green", command=self.accept)
        self.elements['btnAccept'].grid(row=1,column=2)

    def __getitem__(self, key):
        return self.elements[key]

    def disableInput(self):
        self.elements['enyGPT'].config(state="disabled")
    
    def enableInput(self):
        self.elements['enyGPT'].config(state="normal")


    def accept(self):
        self.callback(self, "accept",self.elements['enyGPT'].get("1.0",tk.END))

    def decline(self):
        self.callback(self, "decline")

    def edit(self):
        self.elements['btnEdit'].config(text="Save",command=self.save)
        self.enableInput()

    def save(self):
        self.elements['btnEdit'].config(text="Edit",command=self.edit)
        self.callback(self, "save",self.elements['enyGPT'].get("1.0",tk.END))
        self.disableInput()

    def back(self):
        self.callback(self, 'back')

    def destroy(self):
        for key in self.elements:
            self.elements[key].destroy()




class ResultViews():
    def __init__(self,window, crm_results, destroyCallback):
        self.crm_results = crm_results
        self.window = window
        self.views = []
        self.current_result = 0
        self.setResultView()
        self.destroyCallback = destroyCallback

    def setResultView(self):
        res_view = ResultView(self.window,self.crm_results[self.current_result],self.handleCallback)
        self.views.append(res_view)
        self.updateListBox()
        return res_view

    def nextResultView(self,this):
        self.current_result += 1
        if self.current_result < self.crm_results.length:
            self.setResultView()
            this.destroy()
        else:
            this.destroy()

            if hasattr(self,'listbox') == False:
                self.listbox = tk.Listbox(self.window, width=50)
                self.listbox.bind("<<ListboxSelect>>", self.onListBoxSelect)
                self.listbox.pack()

                self.btnContinue = tk.Button(self.window, text='Send Emails', command=self.sendEmails)
                self.btnContinue.pack()

        self.updateListBox()
    
    def prevResultView(self,this):
        if self.current_result > 0:
            self.current_result -= 1
            self.setResultView()
            this.destroy()

        self.updateListBox()

    def handleCallback(self, this, arg, input_text=""):
        
        if arg == "accept":
            self.crm_results[self.current_result]['result'] = input_text
            self.nextResultView(this)
        elif arg == "save":
            self.crm_results[self.current_result]['result'] = input_text
        elif arg == "decline":
            self.crm_results.delete(self.current_result)
            this.destroy()
            if self.crm_results.length == 0:
                self.destroy()
            elif self.current_result < self.crm_results.length - 1:
                self.setResultView()    
            else:    
                self.nextResultView(this)

        elif arg == "back":
            self.prevResultView(this)
        
    def destroyLast(self):
        self.views[-1].destroy() 
    
    def onListBoxSelect(self, evt=None):
        if len(self.listbox.curselection()) > 0:
            self.destroyLast()
            self.current_result = self.listbox.curselection()[0]
            self.setResultView()
    
    def updateListBox(self):
        if hasattr(self,'listbox'):
            self.listbox.delete(0,tk.END)
            i = 1
            for r in self.crm_results:
                self.listbox.insert(i, r['email'] + ' | ' + r['business'])
                i += 1

            self.listbox.selection_set(self.current_result) 


    def sendEmails(self):
        self.listbox.destroy()
        self.btnContinue.destroy()
        self.emailWidget = EmailWidget(self.window, self.crm_results, self.destroy)

    def destroy(self):
        try:
            self.listbox.destroy()
        except:
            pass

        for v in self.views:
            try:
                v.destroy()
            except:
                pass
        
        try:
            self.btnContinue.destroy()
        except:
            pass

        self.destroyCallback()