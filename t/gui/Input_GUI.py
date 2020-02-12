from tkinter import ttk, Entry, Label, Button, Frame, Tk, Menu, W as sticky_W
from clsSearch import FoodSearch
import sys
from Search_code import FoodSearch as Search, Searchterm, FoodBasic
from Fonts import Fonts

class ShortEntry(object):
    def __init__(self, key, amount):
        self.__key = key
        self.__amount = amount

    @property
    def key(self):
        return self.__key
    @property
    def amount(self):
        return self.__amount
    
import sqlite3
import locale
from datetime import date as Date
class Dayview(Frame):
    def __init__(self, parent, date):
        super().__init__(parent)
        self.date=date
        locale.setlocale(locale.LC_ALL,"")

        self.grid()
        
        self.heading = Label(self, text=self.date.strftime('%A %d. %B %Y'),font=Fonts.hel_11_b)
        self.heading.grid(row=0,column=0,columnspan=5) #columnspan

        self.todays_entries=self.read_todays_entrys_from_db(self.date)

        db_connection=sqlite3.connect('Food.db')
        cursor=db_connection.cursor()

        sumKCal=0        
        for entry in self.todays_entries:
            cursor.execute('SELECT Name, Kategorie, kCal FROM Food WHERE id=?', (entry.key,))
            result=cursor.fetchone()
            if result:
                print(str(entry.amount) + 'g ' +result[0] + ' zu je ' + str(result[2]) + 'kCal')
                sumKCal+=result[2]*entry.amount/100
            else:
                print('ID ' + str(entry.key) + ' not found!')

        print('Gesamtkalorien am ' + self.date.strftime('%d. %b. %Y') + ': ' + str(sumKCal))
            
        

    def read_todays_entrys_from_db(self, date): #gehört hier unbedingt raus! DB-Zugriffe nicht im GUI-File! (self deswegen bewusst entkoppelt)
        entries_from_date=[]
        db_connection=sqlite3.connect('Food.db')
        cursor=db_connection.cursor()

        #db_timestring: YYYY,MM,DD
        month = str(date.month)
        if len(month)==1:
            month='0'+month
        day=str(date.day)
        if len(day)==1:
            day='0'+day
        db_timestring = str(date.year) + ',' + month + ',' + day
        
        cursor.execute('SELECT Food_ID, Menge FROM FoodEntries WHERE Datum=?',(db_timestring,))
        result = cursor.fetchone()
        
        while result:
            entries_from_date.append(ShortEntry(result[0],result[1]))
            result = cursor.fetchone()
            
        db_connection.close()
        return entries_from_date

'''
Stand Input_Window:
- sieht richtig mies aus
- ist nicht gut organisiert

+ Suche funktioniert bereits gut, aktiviert durch Enter in der Suchleiste, in der Food.db gefundene Datensätze werden angezeigt
'''
        
class Input_Window(Frame):
    def __init__(self, parent):
        super(Input_Window, self).__init__(parent)
        self.parent = parent
        
        self.active=False
        self.grid(row=0,column=0)

        self.padx = 20
        self.pady = 10
        self.category='' 

        self.search_line = Entry(self)
        self.search_line.bind('<Return>', self.search_triggered)
        self.category_box = ttk.Combobox(self, values=['Früchte','Süssigkeiten','Getreideprodukte, Hülsenfrüchte und Kartoffeln', 'Gemüse', 'Brote, Flocken und Frühstückscerealien','Nüsse, Samen und Ölfrüchte','Gerichte', 'Fette und Öle','Fisch','Speziallebensmittel','Salzige Snacks','Eier','Milch und Milchprodukte','Fleisch- und Wurstwaren','Fleisch und Innereien','Alkoholhaltige Getränke',''])
        self.category_box.bind("<<ComboboxSelected>>", self.category_changed)
        #vlt doch noch auf Listbox umändern, dann könnte man mehrere Kategorien auswählen
        
        self.new_item = Button(self, text='Neu')
        self.last_foods = Button(self, text='Zuletzt verwendete')
        self.favourite_foods = Button(self, text='Favouriten')
        self.copy_day=Button(self, text='Duplizieren')

        self.found_food_frame=Frame(self)
        self.found_food_header=Label(self.found_food_frame, text='Suchergebnisse:', anchor=sticky_W, font=Fonts.hel_11_b)

        '''
        self.added_food=Frame(self)
        self.added_food.grid(row=4,column=0, rowspan=3,columnspan=3) #ToDo row/columnspan sinnvoll u. vlt als variable festlegene
        self.header_food=Label(self.added_food, text='Lebensmittel', width=30, anchor=sticky_W)
        self.header_amount=Label(self.added_food, text='Menge',anchor=sticky_W)
        self.header_unit=Label(self.added_food, text='Einheit',anchor=sticky_W)

        self.header_names=[self.header_food,self.header_amount,self.header_unit]
        for column,header_name in enumerate(self.header_names):
            header_name.grid(row=0,column=column,padx=2,pady=2,sticky=sticky_W)
        '''
        
        self.found_food_labels =[]

        self.search_line.grid(row=0,column=0, padx=self.padx, pady=self.pady)
        self.category_box.grid(column=1,row=0, padx=self.padx, pady=self.pady)
        self.new_item.grid(column=2, row=0, padx=self.padx, pady=self.pady)
        self.last_foods.grid(column=0, row=1, padx=self.padx, pady=self.pady, sticky=sticky_W)
        self.favourite_foods.grid(column=1, row=1, padx=self.padx, pady=self.pady, sticky=sticky_W)
        self.copy_day.grid(column=2, row=1, padx=self.padx, pady=self.pady, sticky=sticky_W)
        self.found_food_frame.grid(row=3, column=0, rowspan=1,columnspan=2, sticky=sticky_W) #ToDo row/columnspan sinnvoll u. vlt als variable festlegene
        self.found_food_header.grid(column=0,row=0,columnspan=2,sticky=sticky_W, padx=self.padx, pady=self.pady/2)

        self.day_frame = Dayview(self,Date.today())
        self.day_frame.grid(column=3, row=0, rowspan=3)

    def category_changed(self,event):
        self.category = self.category_box.get()
        self.create_new_found_food_labels()
        
    def search_triggered(self,event):
        food_search = Search(Searchterm(self.search_line.get()))
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
            name_label = Label(self.found_food_frame, text=str(found_food.key)+'   '+found_food.name, anchor=sticky_W) #todo: mehrzeilig
            category_label = Label(self.found_food_frame, text=found_food.category, anchor=sticky_W)
            self.found_food_labels.append([name_label,category_label])
        self.update_found_food_view()

    def update_found_food_view(self):
        self.del_old_found_foods()
        for row,food in enumerate(self.found_food_labels):
            for col,element in enumerate(food):
                element.grid(row=row+1, column=col, padx=self.padx,pady=0, sticky=sticky_W)                

if __name__ == '__main__':        
    root = Tk()
    app = Input_Window(root)
    root.mainloop()
