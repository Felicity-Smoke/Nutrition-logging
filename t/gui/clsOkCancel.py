from tkinter import*
from tkinter import ttk

class OK_Cancel(Frame): #Todo: Rename!
    def __init__(self, master):
        Frame.__init__(self, master)
    
        # creating buttons
        buttonwidth=10
        self.button_ok=Button(self, text='OK', width=buttonwidth, command=master.ok())
        self.button_apply=Button(self, text='Übernehmen', width=buttonwidth, command=master.apply())
        self.button_cancel=Button(self, text='Abbrechen', width=buttonwidth, command=master.close())

        # position buttons
        self.button_ok.grid(column=0, row=0, sticky=(E))
        self.button_apply.grid(column=1, row=0, sticky=(E))
        self.button_cancel.grid(column=2, row=0, sticky=(E))

        
        row = master.grid_slaves()[0].grid_info()['row'] +1
        columnspan = master.grid_slaves()[0].grid_info()['column'] +1

        self.grid(row=row, column=0, columnspan=columnspan, sticky=(E), padx=5, pady=5)
        self.columnconfigure(0,weight=1)
        
