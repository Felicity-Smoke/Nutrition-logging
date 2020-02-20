from tkinter import ttk, Entry, Label, Button, Frame, Tk, Menu, Canvas
from clsSearch import FoodSearch
import sys
from Search_code import FoodSearch as Search, Searchterm, FoodBasic
from Fonts import Fonts
from clsDay import Day
import locale
from datetime import date as Date, timedelta
        
class Dayview(Frame):
    '''
    Todo's:
    * auslagern in eigenes cls-File
    * Tag mit Scrollbar versehen
    * food_drop_event
    '''
    
    def __init__(self, parent, date):
        super().__init__(parent)
        self._date=date
        self._today = Day(self._date)
        locale.setlocale(locale.LC_ALL,"")

        #self.grid()

        self.dayframe = Frame(self,background=Fonts.action_bg)
        self.dayframe.grid(column=0,row=0, padx=Fonts.framedistance, pady=Fonts.framedistance)

        # headline
        self.headline=Frame(self.dayframe,)
        self.heading = Label(self.headline, text='',font=Fonts.hel_11_b)
        self.btn_previous=Button(self.headline, text='<',command=self.previous_day,relief='flat')
        self.btn_next=Button(self.headline,text='>',command=self.next_day,relief='flat')

        self.headline.grid(row=0,column=0,padx=Fonts.table_cell_distance,pady=(Fonts.table_cell_distance,0),sticky='nsew') #columnspan
        self.heading.grid(row=0,column=1,sticky='nsew')
        self.btn_previous.grid(row=0,column=0)
        self.btn_next.grid(row=0,column=2)
        self.headline.columnconfigure(1,weight=1)

        # table
        self.table_entries=Frame(self.dayframe,background=Fonts.table_bg)
        self.table_entries.grid(row=1,column=0,padx=Fonts.table_cell_distance,pady=(0,Fonts.table_cell_distance),sticky='nsew')

        header=['Name', 'Menge', 'kCal']
        for col,columnheader in enumerate(header):
            temp_label = Label(self.table_entries, text=columnheader, font=Fonts.hel_8_b) #später eigene Klasse, um Filtern zu ermöglichen
            temp_label.grid(column=col, row=0, padx=1,pady=1,sticky='nswe')

        self.update_day_view()

    def update_day_view(self):
        self.heading['text'] = self._date.strftime('%A %d. %B %Y')
        self._today=Day(self._date)
        self.delete_former_food_entries()
        self.draw_food_entries()

    def draw_food_entries(self):
        for row, entry in enumerate(self._today.food_entries):
            temp_row=[]
            temp_row.append(Label(self.table_entries, text=entry.name, anchor='w'))
            temp_row.append(Label(self.table_entries, text=entry.amount))
            temp_row.append(Label(self.table_entries, text=entry.kCal))
            for col, widget in enumerate(temp_row):
                widget.grid(column=col, row=row+1,padx=1,pady=1,sticky='nswe')
                widget.bind('<ButtonRelease-1>',self.food_dropped)
        self.table_entries.grid_columnconfigure(1,weight=1)
        self.table_entries.grid_columnconfigure(2,weight=1)

    def food_dropped(self,event):
        self['cursor']='heart'

    def next_day(self):
        self._date+=timedelta(days=1)
        self.update_day_view()

    def previous_day(self):
        self._date-=timedelta(days=1)
        self.update_day_view()

    def delete_former_food_entries(self):
        for element in self.table_entries.grid_slaves():
            if int(element.grid_info()["row"]) > 0:
                element.grid_forget()

'''
Stand Input_Window:
- sieht eher mies aus
- schlechtes Naming - eigentlich wird hier nur ausgewählt, nicht eingegeben (Drag, aber kein Drop)

+ Suche funktioniert bereits gut, aktiviert durch Enter in der Suchleiste, in der Food.db gefundene Datensätze werden angezeigt
- Suche funktioniert nur einmalig, dann Fehlermeldung!

Next steps:
- implement scrolling via canvas - half done :-///
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
        self.category_box = ttk.Combobox(self.searchline, values=['Früchte','Süssigkeiten','Getreideprodukte, Hülsenfrüchte und Kartoffeln', 'Gemüse', 'Brote, Flocken und Frühstückscerealien','Nüsse, Samen und Ölfrüchte','Gerichte', 'Fette und Öle','Fisch','Speziallebensmittel','Salzige Snacks','Eier','Milch und Milchprodukte','Fleisch- und Wurstwaren','Fleisch und Innereien','Alkoholhaltige Getränke','']) #todo: Kategorien auslagern
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
        self.results=Frame(self)#, background='blue')
        self.canvas=Canvas(self.results, background='green')
        self.scrollbar = ttk.Scrollbar(self.results, orient='vertical', command=self.canvas.yview)

        self.found_food_frame=Frame(self.canvas, background=Fonts.table_bg)
        self.canvas.create_window(0, 0, anchor='nw', window=self.found_food_frame,height=180,width=150)
        
        self.found_food_header=Label(self.found_food_frame, text='Suchergebnisse:', anchor='w', font=Fonts.hel_11_b, width=50)     

        self.results.grid(row=3,column=0,sticky='w',padx=Fonts.framedistance,pady=Fonts.framedistance) #ToDo row/columnspan sinnvoll u. vlt als variable festlegene
        self.canvas.grid(row=0,column=0,padx=2,pady=2)#todo delete padding
        self.found_food_frame.grid(row=0, column=0, sticky='wesn',padx=2,pady=2) #todo delete padding
        self.found_food_header.grid(column=0,row=0,columnspan=3,sticky='wesn', padx=2, pady=2)

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

        #self.results['height']=150 todo: does not do anything
        if len(self.found_foods)>10: #10 nur als bsp... todo: besseren wert überlegen, vlt skalierbar
            self.canvas.update_idletasks() #no idea what this does
            self.canvas.configure(yscrollcommand=self.scrollbar.set)
            self.scrollbar.grid(row=0,column=1, sticky='ns',padx=2,pady=2)#,rowspan=10)
        else:
            self.scrollbar.grid_forget()
            

    def motion_active(self,event):
        self['cursor']='fleur'

    def motion_stopped(self,event):
        self['cursor']='left_ptr'
        
if __name__ == '__main__':        
    root = Tk()
    app = Input_Window(root)
    root.mainloop()
