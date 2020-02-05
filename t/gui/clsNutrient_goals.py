from tkinter import *
from tkinter import ttk, font
from clsOkCancel import OK_Cancel
import json #später in Externem File

class Nutrients_Goals_Handling(): #später in externem file
    def __init__(self):
        self.filename = 'Nutrient_Goals.json'
        self.data = {}
        #self.read()

    def save(self):
        with open(self.filename, 'w') as outfile:
            json.dump(self.data, outfile)

    def read(self):
        with open(self.filename) as json_file:
            self.data=json.load(json_file)
        

        
class NutrientLine(Frame):
    def __init__(self, master, name, recommanded):
        self.rownumber = master.grid_slaves()[0].grid_info()['row'] +1
        self.activated = StringVar()
        self.cb = Checkbutton(master, variable=self.activated, onvalue=True, offvalue=False, command = self.cb_changed)
        self.cb.grid(row = self.rownumber, column = 0)
        
        self.parameters = []
        self.parameters.append(Label(master, text=name, font='TkDefaultFont'))
        self.amount = StringVar()
        self.unit = StringVar()
        self.parameters.append(ttk.Combobox(master, textvariable=self.amount, values=[0,1,2,3,4])) #menge - ausfüllen mit default oder vorherigen Wert!
        self.parameters.append(ttk.Combobox(master, textvariable=self.unit, values=['g','% der kCal', 'g/kg Körpergewicht'])) #Einheit - Möglichkeiten: je kg Körpergewicht; g; % von kcal;
        #iwie automatisch auch berechnen lassen - zb. beim Protein mit Training sehr sinnvoll!
        self.parameters.append(Label(master, text = str(recommanded[0])+recommanded[1], font='TkDefaultFont'))

        for i,element in enumerate(self.parameters):
            element.grid(row = self.rownumber, column = i+1, padx=10, pady=3, sticky = (W))
            
    def cb_changed(self):
        if self.activated.get()=='1':
            for each in self.parameters:
                each.configure(state=NORMAL)
        else:
            for each in self.parameters:
                each.configure(state=DISABLED)
    
class Nutrient_Goals_GUI(Frame):
    def ok(self):
        pass

    def apply(self):
        pass

    def close(self):
        pass
    
    def __init__(self, master=None):
        Frame.__init__(self,master, height=400, width=600)
        self.grid()
        self.createWidgets()
       
    def createWidgets(self):
        data_handling = Nutrients_Goals_Handling()
    
        # Table head
        column_names=['Ein/Aus', 'Nährstoff', 'Menge', 'Einheit', 'Empfohlene Menge']

        for i,name in enumerate(column_names):
            temp_label = Label(self, text=name, font='TkHeadingFont')
            temp_label.grid(column=i, row=0, sticky=(SW), padx=10, pady=10)

        # Nutrient lines        
        makros = ['Fett', 'Kohlenhydrate', 'Eiweiß']
        mikros = ['Vitamin C', 'Eisen', 'Selen', 'Zink', 'Magnesium', 'Kalzium', 'Jod', 'Kalium']

        
        for nutrient in 'Kalorien'+makros+mikros:
            NutrientLine(self, nutrient,data_handling.data[nutrient])
    
        OK_Cancel(self)

