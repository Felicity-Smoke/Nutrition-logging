from tkinter import Label, Button, Frame, PhotoImage
from clsMainButton import MainButton        
        
class GUI(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master,height=800,width=1200)
        self.grid()
        self.create_widgets()

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
            pass
            #self.B3.chosen()

    def enter_symbolnavigation_bar(self, e):
        for button in self.mainbuttons:
            button.show_text()

    def leave_symbolnavigation_bar(self, e):
        for button in self.mainbuttons:
            button.hide_text()

    def create_widgets(self):
        size_image = 6 #var gehört wo anders hin!
        self.photo_overview = PhotoImage(file="Icons/Overview.png").subsample(size_image,size_image)
        self.photo_food = PhotoImage(file="Icons/Essen.png").subsample(size_image,size_image)
        self.photo_calender = PhotoImage(file="Icons/Kalender.png").subsample(size_image,size_image)

        self.symbolnavigation_bar=Frame(self)
        self.symbolnavigation_bar.grid(column=0,row=0,rowspan=5 )#5 vlt noch bearbeiten!
        self.symbolnavigation_bar.bind('<Enter>', self.enter_symbolnavigation_bar)
        self.symbolnavigation_bar.bind('<Leave>', self.leave_symbolnavigation_bar)

        self.mainbuttons = []
        self.B1 = MainButton(self.symbolnavigation_bar,text='Übersicht',command=self.view('activate_overview'),image=self.photo_overview)
        self.B2 = MainButton(self.symbolnavigation_bar,text='Essen eingeben',command = self.view('activate_food_input'),image=self.photo_food)
        self.B3 = MainButton(self.symbolnavigation_bar,text='Kalender',command=self.view('activate_calender'), image=self.photo_calender,height=60, width = 60)
        self.mainbuttons.append(self.B1)
        self.mainbuttons.append(self.B2)
        self.mainbuttons.append(self.B3)

        print(str(len(self.mainbuttons)))
        print(self.mainbuttons)
        
        for row,mainbutton in enumerate(self.mainbuttons):
            mainbutton.grid(row=row,column=0,sticky=('W')) 



app=GUI()
app.master.title('Ernährungstagebuch')
app.mainloop()
