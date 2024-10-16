import tkinter as tk
from tkinter import filedialog, ttk
from Config import ConfigDialog, Config
from ChatGPT import ChatGPT
from CRM import CRM
from ResultView import ResultViews


class MenuBar():

    def __init__(self, window) -> None:
        WIDTH = 600
        HEIGHT = 600
        # COLOURS:
        MAIN_BG = "#290769"
        self.window = window
        self.elements = {}
        self.elements['menubar'] = tk.Frame(window, bg=MAIN_BG, height=HEIGHT*0.1)
        self.elements['menubar'].grid(row=1,column=2)
        self.elements['menubar'].pack(side="top",fill="x", ipady=10)

        self.elements['lblTitle'] = tk.Label(self.elements['menubar'], text="Emailer", font=("Arial",16), bg=MAIN_BG, fg="white")
        self.elements['lblTitle'].pack(side="left")


        self.elements['btnConf'] = tk.Button(self.elements['menubar'],text='Config', command=self.onConfig, bg=MAIN_BG, fg='white')
        self.elements['btnConf'].pack(side='right')


    def onConfig(self):
        config = ConfigDialog()


class FilePicker():
    
    def __init__(self,window, conf, destroyCallback):
        self.window = window
        self.conf = conf
        self.lblChoose = tk.Label(window, text='Select CRM', font=('Arial',15))
        self.lblChoose.pack()
        self.btnChoose = tk.Button(window,text='Choose File', command=self.onChooseFile, bg="#290769", fg='white')
        self.btnChoose.pack()
        self.destroyCallback = destroyCallback

    def onChooseFile(self):
        filename = filedialog.askopenfilename()
        crm_loaded = CRM(filename)
        self.btnChoose.destroy()
        self.lblChoose.destroy()

        idx = 0
        gpt = ChatGPT()
        
        lblProgress = tk.Label(self.window)
        progress = ttk.Progressbar(self.window, mode='determinate', orient = tk.HORIZONTAL, length = int(self.window.winfo_width()/2))
        
        lblProgress.pack()
        progress.pack()
        

        for crm in crm_loaded:

            lblProgress['text'] = 'Fetching ' + str(idx+1) + '/' + str(crm_loaded.length)

            progress['value'] = int(((idx+1)/crm_loaded.length)*100)
            self.window.update()
                
            crm_loaded[idx]['result'] = gpt.get(crm['name'],crm['business'],crm['info'], self.conf.name)
            idx += 1

        progress.destroy()
        lblProgress.destroy()
        gpt.end()
        self.res_views = ResultViews(self.window,crm_loaded, self.destroyCallback)

    def destroy(self):
        self.lblChoose.destroy()
        self.btnChoose.destroy()

    def create(self):
        self.lblChoose.pack()
        self.btnChoose.pack()




    
    
