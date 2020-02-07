from tkinter import Label, Button, Frame, PhotoImage, Menu, Tk
from clsMainButton import MainButton
from Calendar import Calendar
from clsMonth import Month

'''
aktuelle Mätzchen:
- Kalender image ist kleiner als die anderen 2
- die Symbolnaviagtionsleiste lässt sich trotz sticky und grid_rowconfigure nicht strecken
- MainButtons anklicken funktioniert nicht

'''
class GUI(Tk):
    def __init__(self,master=None):
        Tk.__init__(self)

        size_image = 6 #var gehört wo anders hin!
        self.photo_overview = PhotoImage(file="Icons/Overview.png").subsample(size_image,size_image)
        self.photo_food = PhotoImage(file="Icons/Essen.png").subsample(size_image,size_image)
        self.photo_calender = PhotoImage(file="Icons/Kalender.png").subsample(size_image,size_image)

        self.symbolnavigation_bar=Frame(self, bg='lightgrey')
        self.symbolnavigation_bar.grid(column=0,row=0,sticky='nsw')
        self.symbolnavigation_bar.bind('<Enter>', self.enter_symbolnavigation_bar)
        self.symbolnavigation_bar.bind('<Leave>', self.leave_symbolnavigation_bar)

        self.operationframe = Frame(self)
        self.operationframe.grid(column=1,row=0,sticky='nsew')
        
        self.mainbuttons = []
        self.B1 = MainButton(self.symbolnavigation_bar,text='Übersicht',command=self.view('activate_overview'),image=self.photo_overview)
        self.B2 = MainButton(self.symbolnavigation_bar,text='Essen eingeben',command = self.view('activate_food_input'),image=self.photo_food)
        self.B3 = MainButton(self.symbolnavigation_bar,text='Kalender',command=self.view('activate_calender'), image=self.photo_calender,height=80, width = 80)
        self.mainbuttons.append(self.B1)
        self.mainbuttons.append(self.B2)
        self.mainbuttons.append(self.B3)
        
        for row,mainbutton in enumerate(self.mainbuttons):
            mainbutton.grid(row=row,column=0,sticky=('nsw'))
        self.symbolnavigation_bar.grid_columnconfigure(0,weight=1) #Todo: does not work as exp
        self.grid_columnconfigure(0,weight=1)

        self.option_add('*tearOff', False)
        self.menubar = Menu(self)
        self.config(menu=self.menubar)

        self.menu_file=Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='Datei')
        self.menu_file.add_command(label='Beenden', command = self.quit())

        self.menu_extras=Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_extras, label='Extras')
        self.menu_extras.add_command(label='Einstellungen', command = self.settings)

        self.menu_view=Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_view, label='Ansicht')
        self.menu_view.add_command(label='Übersicht')
        self.menu_view.add_command(label='Essen eingeben')
        self.menu_view.add_command(label='Kalender')        

        
    def settings(self):
        print('show settings')

        
        #self.menu_extras.add_command(self, text='Einstellungen')

            
    def view(self, view_name):
        for button in self.mainbuttons:
            button.not_chosen()
            
        if view_name == 'activate_overview':
            pass
            #self.B1.chosen()

        elif view_name == 'activate_food_iniput':
            pass
            #self.B2.chosen()

        elif view_name == 'activate_calender':
            print('called')
            view = Calendar(self.operationframe,Month.from_date())

    def enter_symbolnavigation_bar(self, e):
        for button in self.mainbuttons:
            button.show_text()

    def leave_symbolnavigation_bar(self, e):
        for button in self.mainbuttons:
            button.hide_text()




root=GUI()
#root.grid()
root.title('Ernährungstagebuch')
root.geometry('300x200')
root.mainloop()

