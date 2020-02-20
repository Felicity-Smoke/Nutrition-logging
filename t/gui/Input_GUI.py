from tkinter import ttk, Entry, Label, Button, Frame, Tk, Menu
from clsSearch import FoodSearch
import sys
from Search_code import FoodSearch as Search, Searchterm, FoodBasic
from Fonts import Fonts
from clsDay import Day
import locale
from datetime import date as Date
        
class Dayview(Frame):
    def __init__(self, parent, date):
        super().__init__(parent)
        self.date=date
        locale.setlocale(locale.LC_ALL,"")

        self.grid()

        self.dayframe = Frame(self,background=Fonts.action_bg)
        self.dayframe.grid(column=0,row=0, padx=Fonts.framedistance, pady=Fonts.framedistance)
        
        self.heading = Label(self.dayframe, text=self.date.strftime('%A %d. %B %Y'),font=Fonts.hel_11_b)
        self.heading.grid(row=0,column=0,columnspan=5,padx=Fonts.table_cell_distance,pady=(Fonts.table_cell_distance,0),sticky='nsew') #columnspan

        self.table_entries=Frame(self.dayframe,background=Fonts.table_bg)
        self.table_entries.grid(row=1,column=0, columnspan=5,padx=Fonts.table_cell_distance,pady=(0,Fonts.table_cell_distance))

        header=['Name', 'Menge', 'kCal']
        for col,columnheader in enumerate(header):
            temp_label = Label(self.table_entries, text=columnheader, font=Fonts.hel_8_b) #später eigene Klasse, um Filtern zu ermöglichen
            temp_label.grid(column=col, row=0, padx=1,pady=1,sticky='nswe')

        today = Day(self.date)

        for row, entry in enumerate(today.food_entries):
            temp_row=[]
            temp_row.append(Label(self.table_entries, text=entry.name, anchor='w'))
            temp_row.append(Label(self.table_entries, text=entry.amount))
            temp_row.append(Label(self.table_entries, text=entry.kCal))
            for col, widget in enumerate(temp_row):
                widget.grid(column=col, row=row+1,padx=1,pady=1,sticky='nswe')
                widget.bind('<ButtonRelease-1>',self.food_dropped)

    def food_dropped(self,event):
        self['cursor']='heart'

'''
Stand Input_Window:
- sieht eher mies aus
- schlechtes Naming - eigentlich wird hier nur ausgewählt, nicht eingegeben (Drag, aber kein Drop)

+ Suche funktioniert bereits gut, aktiviert durch Enter in der Suchleiste, in der Food.db gefundene Datensätze werden angezeigt

Next steps:
* Drag n Drop von Suchfenser zu Tagesfenser (inkl. Mauszeiger)
'''
        
class Input_Window(Frame):
    def __init__(self, parent):
        super(Input_Window, self).__init__(parent)
        self.parent = parent
        
        self.active=False
        self.grid(row=0,column=0)
        
        self.found_food_labels =[]
        self.category=''

        # searchline
        self.searchline = Frame(self)      
        self.search_entry = Entry(self.searchline)
        self.search_entry.bind('<Return>', self.search_triggered)
        self.category_box = ttk.Combobox(self.searchline, values=['Früchte','Süssigkeiten','Getreideprodukte, Hülsenfrüchte und Kartoffeln', 'Gemüse', 'Brote, Flocken und Frühstückscerealien','Nüsse, Samen und Ölfrüchte','Gerichte', 'Fette und Öle','Fisch','Speziallebensmittel','Salzige Snacks','Eier','Milch und Milchprodukte','Fleisch- und Wurstwaren','Fleisch und Innereien','Alkoholhaltige Getränke',''])
        self.category_box.bind("<<ComboboxSelected>>", self.category_changed)
        #vlt doch noch auf Listbox umändern, dann könnte man mehrere Kategorien auswählen
        self.search_btn = Button(self.searchline, text='Suchen')#, command=self.search_triggered()) todo
        
        self.searchline.grid(row=0,column=0, padx=Fonts.framedistance, pady=Fonts.framedistance, sticky='w')
        self.search_entry.grid(row=0,column=0, padx=Fonts.framedistance, pady=0)
        self.category_box.grid(row=0,column=1, padx=Fonts.framedistance, pady=0)
        self.search_btn.grid(row=0, column=2, padx=Fonts.framedistance, pady=0)

        # input_navigation
        self.input_navigation = Frame(self)
        self.last_foods = Button(self.input_navigation, text='Oft verwendete')
        self.favourite_foods = Button(self.input_navigation, text='Favouriten')
        self.yesterday = Button(self.input_navigation, text='Gestern')
        self.choose_day = Button(self.input_navigation, text='Tag wählen')

        self.input_navigation.grid(row=1,column=0, padx=Fonts.framedistance, pady=Fonts.framedistance,sticky='w')
        self.last_foods.grid(column=0, row=0, padx=Fonts.framedistance, pady=0, sticky='w')
        self.favourite_foods.grid(column=1, row=0, padx=Fonts.framedistance, pady=0, sticky='w')
        self.yesterday.grid(column=2, row=0, padx=Fonts.framedistance, pady=0, sticky='w')
        self.choose_day.grid(column=3, row=0, padx=Fonts.framedistance, pady=0, sticky='w')

        # found_food
        self.found_food_frame=Frame(self, background=Fonts.table_bg)
        self.found_food_header=Label(self.found_food_frame, text='Suchergebnisse:', anchor='w', font=Fonts.hel_11_b, width=50)
    
        self.found_food_frame.grid(row=3, column=0, sticky='w', padx=Fonts.framedistance,pady=Fonts.framedistance) #ToDo row/columnspan sinnvoll u. vlt als variable festlegene
        self.found_food_header.grid(column=0,row=0,columnspan=2,sticky='wesn', padx=1, pady=1)

        self.day_frame = Dayview(self,Date.today())
        self.day_frame.grid(column=3, row=0, rowspan=3)

    def category_changed(self,event):
        self.category = self.category_box.get()
        self.create_new_found_food_labels()
        
    def search_triggered(self,event):
        food_search = Search(Searchterm(self.search_entry.get()))
        self.found_foods=food_search.get_basicfood_objects
        self.create_new_found_food_labels()

    def del_old_found_foods(self):
        for label in self.found_food_frame.grid_slaves():
            if int(label.grid_info()["row"]) > 0:
                label.grid_forget()
                
    def create_new_found_food_labels(self):
        self.del_old_found_foods()
        self.found_food_labels=[]
        for found_food in self.found_foods:
            if self.category:
                if not self.category == found_food.category:
                    continue
            #TODO: ID(key) hier wieder raus nehmen!
            name_label = Label(self.found_food_frame, text=str(found_food.key)+'   '+found_food.name, anchor='w') #todo: mehrzeilig
            category_label = Label(self.found_food_frame, text=found_food.category, anchor='w')
            self.found_food_labels.append([name_label,category_label])
        self.update_found_food_view()

    def update_found_food_view(self):
        self.del_old_found_foods()
        for row,food in enumerate(self.found_food_labels):
            for col,element in enumerate(food):
                element.grid(row=row+1, column=col, padx=1,pady=1, sticky='wsen')
                element.bind('<B1-Motion>',self.motion_active)
                element.bind('<ButtonRelease-1>',self.motion_stopped)

    def motion_active(self,event):
        self['cursor']='fleur'

    def motion_stopped(self,event):
        self['cursor']='left_ptr'
        
if __name__ == '__main__':        
    root = Tk()
    app = Input_Window(root)
    root.mainloop()
