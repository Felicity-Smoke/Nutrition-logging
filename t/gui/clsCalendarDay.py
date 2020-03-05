from tkinter import Button,Frame,Label,PhotoImage, Tk
from Fonts import Fonts

class DayClickedEvent():
    def __init__(self, day):
        self._day=day

class Logo():
    def __init__(self, name, png):
        self._name=name
        self._filepath=png

    @property
    def image(self):
        return PhotoImage(file=self._filepath)

    def name(self):
        return self._name
         
class Logos():
    MAX_ACTIVE_LOGOS = 3
    
    vegan=Logo('vegan','Icons/green.png')
    dairy=Logo('dairy','Icons/dairy.png')
    meat=Logo('meat','Icons/meat.png')
    #caloriebilanz=Logo('calories',)
    
    def __init__(self):
        pass
        
class CalendarDay(Frame):
    def __init__(self,master=None, text='', fg='black', cnf={}, **kw):
        Frame.__init__(self,master, cnf, **kw)
        self._day_text=text
        self.double_clicked=False

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

        self.active_logos=[]
        self.logo_frame=Frame(self,background=self['background'])
        self.logo_frame.grid(column=0,row=1)

        self.logolabels=[]
        for i in range(Logos.MAX_ACTIVE_LOGOS):
            self.logolabels.append(Label(self.logo_frame, image='', width=1,height=1,background=self['background'],font=Fonts.mini))

        for column,logolabel in enumerate(self.logolabels):
            logolabel.grid(row=0,column=column,padx=1,pady=1,sticky='nswe')
            
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
        nr_of_logos=len(self.active_logos)
        if nr_of_logos<4 and not logo.name in self.active_logos:
            img=logo.image
            self.logolabels[nr_of_logos].configure(image=img)
            self.logolabels[nr_of_logos].image=img
            self.active_logos.append(logo.name)
            return True
        return False

    def add_text(self, text):
        nr_of_logos=len(self.active_logos) #rename! vlt. nr_of_items
        if nr_of_logos<4 and not 'text' in self.active_logos:
            self.logolabels[nr_of_logos].configure(text=text)
            self.active_logos.append('text')
            return True
        return False
    
    def delete_logo(self, logo):
        for i,logoitem in enumerate(self.active_logos):
            if logoitem==logo.name:
                img=''
                self.logolabels[i].configure(image=img)
                self.logolabels[i].image=img
                del self.active_logos[i]

    def delete_text(self):
        for i,logoitem in enumerate(self.active_logos):
            if logoitem=='text':
                self.logolabels[i].configure(text='')
                del self.active_logos[i]
                
    def delete_all_logos(self): #rename .. items
        for label in self.logolabels:
            label.configure(text='')
            img=''
            label.configure(image=img)
            label.image=img
        self.active_logos=[]
                              
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
    
if __name__ == '__main__':
    root = Tk()
    window = CalendarDay(root,1)
    window.grid(row=0,column=0)
    window.add_logo(Logos.vegan)
    #how to wait?
    
