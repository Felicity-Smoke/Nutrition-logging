from tkinter import Button,Frame,Label,PhotoImage
class DayClickedEvent():
    def __init__(self, day):
        self._day=day

class Logo():
    def __init__(self, png):
        self._filepath=png
        
        
class Logos():
    MAX_ACTIVE_LOGOS = 3
    def __init__(self):
        self._plant_logo = PhotoImage(file="Icons/green.png") #subsample(size_image,size_image)
        self._active_logos =[]
        self._unprocessed_changes = False

    def add_logo(self,logo):
        if len(self._active_logos)<MAX_ACTIVE_LOGOS:
            self._active_logos.append(logo)
            return True
        else:
            return False

    def delete_logo(self,logo):
        if logo in self._active_logos:
            self._active_logos.remove(logo)
            self._unprocessed_changes = True

    def delete_all_logos(self):
        if len(self._active_logos)>0:
            self._unprocessed_changes = True
            self._active_logos=[]
        
    @property
    def plant_logo(self):
        return self._plant_logo
    
    @property
    def unprocessed_changes(self):
        return self._unprocessed_changes
    
    @unprocessed_changes.setter
    def unprocessed_changes(self,value):
        if type(value) is bool:
            self._unprocessed_changes=value        
        
class CalendarDay(Frame):
    def __init__(self,master=None, text='', fg='black', cnf={}, **kw):
        Frame.__init__(self,master, cnf, **kw)
        self._day_text=text
        self.double_clicked=False
        self.logos=Logos()

        self.active_color = 'whitesmoke'
        self.passive_color = 'lightgrey'

        self['background'] = self.passive_color       

        self.bind('<Button-1>', self.clicked_day)         # bind left mouse clicks
        self.bind('<Double-1>', self.double_clicked_day)  # bind double left clicks
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
            
        self.day_label=Label(self,text=self._day_text,background=self['background'],fg=fg,anchor='e')
        self.day_label.grid(column=0,row=0)
        #self.day_label.bind('<Button-1>', self.clicked_day)
        #self.day_label.bind('<Double-1>', self.double_clicked_day)
        self.day_label.lower() #does not work!

        self.logo_frame=Frame(self,background=self['background'])
        self.logo_frame.grid(column=0,row=1)

        size=1
        self.logo1=Label(self.logo_frame,width=size,height=size,background=self['background'])
        self.logo2=Label(self.logo_frame,width=size,height=size,background=self['background'])
        self.logo3=Label(self.logo_frame,width=size,height=size,background=self['background'])
        logolabels = [self.logo1,self.logo2,self.logo3]
        for column,logo in enumerate(logolabels):
            logo.grid(row=0,column=column,padx=1,pady=1,sticky='nswe')
        
            
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
            #self._eventlist.append(DayClickedEvent(self.number))  

    def double_clicked_day(self, event):
        self.double_clicked=True

    def set_active(self):
        self.config(bg=self.active_color)

    def set_inactive(self):
        self.config(bg=self.passive_color)

    def change_day(self, new_day): # wird das wo verwendet?? - sonst löschen!
        self._day_text=new_day
        self.day_label['text']=self._day_text

    def change_textcolor(self, new_color):
        self.day_label['foreground']=new_color

    def add_logo(self, logo):
        #self.active_logos.append(self.logos.plant_logo)
        #self.logo1['text']='text'
        img=PhotoImage(file="Icons/green.png")
        self.logo1.configure(image=img)
        self.logo1.image = img

    def delete_logo(self, logo):
        print('delete_logo in ClsCalendarDay unfinished')
        self.logos.delete_logo(logo)

    def delete_all_logos(self):
        self.logos.delete_all()
        
    @property
    def number(self):#sollte gelöscht werden, number ist komische bezeichnung!
        return self._day_text

    @property
    def from_actual_month(self):
        return self.day_label['foreground']=='black'
    
    @property
    def is_active(self):
        return self['background']==self.active_color

    @property
    def eventlist(self):
        return self._eventlist

    @property
    def day(self):
        day=1
        try:
            day = int(self._day_text)
        except:
            print('Exception, Tag kann nicht in int gecastet werden: ' + self._day_text)
            day = 1 #mieser ansatz aber temporär okay TODO
        return day

    def event_done(self):
        print('not implemented yet')
        return
    
