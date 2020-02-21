from tkinter import Button,Frame,Label

class CalendarDay(Frame):
    def __init__(self,master=None, text='', fg='', cnf={}, **kw):
        Frame.__init__(self,master, cnf, **kw)
        self.day=text
        self.double_clicked=False

        self.active_color = 'whitesmoke'
        self.passive_color = 'lightgrey'

        self['background'] = self.passive_color
        
        self.bind('<Button-1>', self.clicked_day)         # bind left mouse clicks
        self.bind('<Double-1>', self.double_clicked_day)  # bind double left clicks
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        if fg=='':
            fg='black' #default
            
        self.day_label=Label(self,text=self.day,background=self['background'],fg=fg,anchor='e')
        self.day_label.grid(column=0,row=0)
        self.day_label.bind('<Button-1>', self.clicked_day)
        self.day_label.bind('<Double-1>', self.double_clicked_day)
        self.day_label.lower() #does not work!
            
    def on_enter(self, e):
        self.set_active()      
        for slave in self.grid_slaves():
            slave.config(bg=self.active_color)

    def on_leave(self, e):
        self.set_inactive()
        for slave in self.grid_slaves():
            slave.config(bg=self.passive_color)
        
    def clicked_day(self, event):
            self.after(300, self.clicked, event)

    def clicked(self,event):
        if self.double_clicked:
            self.double_clicked=False
            print('Doppelklick auf ' + str(self.number) + ' (Todo: Fenster öffnen)')
        else:
            self['background'] = self.active_color
            print(str(self.number) + ' wurde geklickt!')

    def double_clicked_day(self, event):
        self.double_clicked=True

    def set_active(self):
        self.config(bg=self.active_color)

    def set_inactive(self):
        self.config(bg=self.passive_color)

    def change_day(self, new_day):
        self.day=new_day
        self.day_label['text']=self.day

    def change_textcolor(self, new_color):
        self.day_label['foreground']=new_color

    @property
    def number(self):
        return self.day

    @property
    def is_active(self):
        return self['background']==self.active_color
