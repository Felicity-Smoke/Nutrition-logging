from tkinter import *
from tkinter import ttk, font
from clsOkCancel import OK_Cancel
from clsNutrient_goals import Nutrient_Goals_GUI
import numpy as np

class Subradiobutton(Radiobutton):
    def __init__(master, var, cnf={}, **kw):
        Radiobutton.__init__(self,master,cnf,**kw)
        self.configure(state = var)

class GUI(Frame):
    def ok(self):
        pass

    def apply(self):
        pass
    def close(self):
        pass
        
    def __init__(self, master=None):
        Frame.__init__(self,master, height=400, width=600)
        self.grid()
        self.create_widgets()

    def mylist(self,start,stop,stepsize):
        ret_list=[]
        i=start
        for j in range(round((stop-start)/stepsize)):
            ret_list.append(round(i,1))
            i+=stepsize
        return ret_list
    
    def position_widget_list(self,widget_list):
        y_offset = 3
        for i,widget in enumerate(widget_list):
            x_offset = 25
            if not type(widget) is Label:
                x_offset += 25
                y_offset=0
                if type(widget) is Subradiobutton:
                    x_offset+=20
            elif widget['text']=='':
                y_offset=0
            widget.grid(column=0, row=i, padx=x_offset, pady=y_offset,sticky=(SW))
            y_offset=3

    def input_time_option_changed(self):
        if self.meal_time_activated.get() == '1':
                self.RB_time1.configure(state = NORMAL)
                self.RB_time2.configure(state = NORMAL)
        else:
            self.RB_time1.configure(state = DISABLED)
            self.RB_time2.configure(state = DISABLED)

    def detailed_goals(self):
        window = Toplevel(self)
        Nutrient_Goals_GUI(window)      
       

    def create_widgets(self):
        # creating tabs
        self.tab_parent=ttk.Notebook(self)
        self.tab_view=Frame(self.tab_parent)
        self.tab_input=Frame(self.tab_parent)
        self.tab_goals=Frame(self.tab_parent)
        self.tab_user=Frame(self.tab_parent)

        self.tab_parent.add(self.tab_view, text="Ansicht")
        self.tab_parent.add(self.tab_input, text="Eingabe")
        self.tab_parent.add(self.tab_goals, text="Ziele")
        self.tab_parent.add(self.tab_user, text="Benutzerdaten")

        offset=5
        self.tab_parent.grid(column=0, row=0, columnspan=offset+3) #TODO: soll über alles (colspan, rowspan), ugly!
        self.columnconfigure(offset-1,weight=1,pad=1)
        self.columnconfigure(offset,weight=0,pad=1)
        self.columnconfigure(offset+1,weight=0,pad=1)
        self.columnconfigure(offset+2,weight=0,pad=1)
    
        # Ansicht Tab
        view_options_var=StringVar()
        self.view_options=[]
        self.view_options.append(Label(self.tab_view, text='Standardansicht'))
        self.view_options.append(ttk.Radiobutton(self.tab_view, text='Übersicht', variable=view_options_var, value='overview'))
        self.view_options.append(ttk.Radiobutton(self.tab_view, text='Eingabe', variable=view_options_var, value='input'))
        self.view_options.append(ttk.Radiobutton(self.tab_view, text='Zuletzt verwendete Ansicht', variable=view_options_var, value='last_view'))

        self.calories=StringVar()
        self.protein=StringVar()
        self.fat=StringVar()
        self.carbs=StringVar() 
        self.view_options.append(Label(self.tab_view, text='Übersicht konfigurieren'))
        self.view_options.append(ttk.Checkbutton(self.tab_view, text='Kalorien anzeigen', variable=self.calories, onvalue=True, offvalue=False))
        self.view_options.append(ttk.Checkbutton(self.tab_view, text='Eiweiß anzeigen', variable=self.protein, onvalue=True, offvalue=False))
        self.view_options.append(ttk.Checkbutton(self.tab_view, text='Kohlenhydrate anzeigen', variable=self.carbs, onvalue=True, offvalue=False))
        self.view_options.append(ttk.Checkbutton(self.tab_view, text='Fett anzeigen', variable=self.fat, onvalue=True, offvalue=False))
        
        self.position_widget_list(self.view_options)
        
        # Eingabe Tab
        self.input_options=[]
        self.input_options.append(Label(self.tab_input, text=''))
        self.comments=StringVar() 
        self.input_options.append(ttk.Checkbutton(self.tab_input, text='Kommentare bei Tagesansicht', variable=self.comments, onvalue=True, offvalue=False))
        self.meal_time_activated=StringVar()
        self.input_options.append(ttk.Checkbutton(self.tab_input, text='Zeitangaben bei der Essenseingabe', variable=self.meal_time_activated, onvalue=True, offvalue=False, command = self.input_time_option_changed))
        #if self.meal_time:
        input_time_option=StringVar()
        self.RB_time1 = ttk.Radiobutton(self.tab_input, text='Aufteilung in Frühstück, Mittagessen, Abendessen und Snacks', variable=input_time_option, value='meals')
        self.RB_time2 = ttk.Radiobutton(self.tab_input, text='Zeitangabe bei der Eingabe', variable=input_time_option, value='time_input')
        self.input_options.append(self.RB_time1)
        self.input_options.append(self.RB_time2)
        self.input_options.append(Label(self.tab_input, text=''))
        self.input_options.append(Button(self.tab_input, text='Favouritenliste zurücksetzen'))


        self.position_widget_list(self.input_options)

        self.RB_time1.configure(state = DISABLED) # in subRadiobutton - Klasse auslagern
        self.RB_time2.configure(state = DISABLED)

            
        # Ziele Tab
        self.goals_options=[]
        self.goals_options.append(Label(self.tab_goals, text=''))
        self.kcal_control_on=StringVar()
        self.goals_options.append(ttk.Checkbutton(self.tab_goals, text='Kalorienkontrolle', variable=self.kcal_control_on, onvalue=True, offvalue=False))
        self.daily_dozen_on=StringVar()
        self.goals_options.append(ttk.Checkbutton(self.tab_goals, text='Tägliches Dutzend', variable=self.daily_dozen_on, onvalue=True, offvalue=False))
        self.iron_on=StringVar()
        self.goals_options.append(ttk.Checkbutton(self.tab_goals, text='Eisenoptimierung', variable=self.iron_on, onvalue=True, offvalue=False))
        self.salt_on=StringVar()
        self.goals_options.append(ttk.Checkbutton(self.tab_goals, text='Salzkontrolle', variable=self.salt_on, onvalue=True, offvalue=False))
        self.goals_options.append(Label(self.tab_goals, text=''))
        self.goals_options.append(Button(self.tab_goals, text='Nährstoffziele detailliert festlegen', command=self.detailed_goals))
        
        self.position_widget_list(self.goals_options)

        # Benutzerdaten tab
        self.user_options=[]

        sex=StringVar()
        self.user_options.append(Label(self.tab_user, text='Geschlecht'))
        self.user_options.append(ttk.Radiobutton(self.tab_user, text='männlich', variable=input_time_option, value='male'))
        self.user_options.append(ttk.Radiobutton(self.tab_user, text='weiblich', variable=input_time_option, value='female'))
        self.user_options.append(Label(self.tab_user, text='Geburtsdatum (TT MM JJJJ)'))
        birthday_day=StringVar()
        birthday_month=StringVar()
        birthday_year=StringVar()
        birthday_frame = Frame(self.tab_user)
        combo_birthday_day = ttk.Combobox(birthday_frame, width=3, textvariable=birthday_day, values=list(map(str,range(1,31))))
        combo_birthday_month = ttk.Combobox(birthday_frame, width=10, textvariable=birthday_month, values=['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'])
        combo_birthday_year = ttk.Combobox(birthday_frame, width=5, textvariable=birthday_year, values=list(map(str,range(1940,201))))
        combo_birthday_day.grid(row=0,column=0)
        combo_birthday_month.grid(row=0,column=1)
        combo_birthday_year.grid(row=0,column=2)
        self.user_options.append(birthday_frame)
        #gewicht
        #größe
        self.user_options.append(Label(self.tab_user, text='Trainingszustand'))
        self.user_options.append(ttk.Radiobutton(self.tab_user, text='Couchpotatoe', variable=input_time_option, value=''))
        self.user_options.append(ttk.Radiobutton(self.tab_user, text='Gelegenheitssportler', variable=input_time_option, value=''))
        self.user_options.append(ttk.Radiobutton(self.tab_user, text='Hobbysportler', variable=input_time_option, value=''))
        self.user_options.append(ttk.Radiobutton(self.tab_user, text='ehrgeiziger Hobbysportler', variable=input_time_option, value=''))
        self.user_options.append(ttk.Radiobutton(self.tab_user, text='Profisportler', variable=input_time_option, value=''))
        self.user_options.append(Label(self.tab_user, text='Körperfettanteil (KFA)'))
        input_kfa=StringVar()
        self.user_options.append(ttk.Combobox(self.tab_user, text='Körperfettanteil (KFA)', textvariable=input_kfa, values=self.mylist(5,30,0.1)))
        
        self.position_widget_list(self.user_options)

        OK_Cancel(self)

  
app=GUI()
app.master.title('Einstellungen')
app.mainloop()
