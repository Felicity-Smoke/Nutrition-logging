from tkinter import *
from tkinter import ttk, font
from clsSearch import FoodSearch
from clsDB import DB # passt hier eig gar nicht rein.. logik aus gui raus bringen!
import sys

class Input_Window(Frame):
    def __init__(self, parent):
        super(Input_Window, self).__init__(parent)
        self.parent = parent
        
        self.active=False
        self.grid(row=0,column=0)
        self.init_widgets()

    def quit(self):
        sys.exit()

    def init_widgets(self):
        self.padx = 20
        self.pady = 10
        self.bold_font='Helvetica 11 bold'
        self.category='' #kann '' wieder ausgewählt werden? (falls der User die Kategorie wieder abwählen will 

        self.search_line = Entry(self)
        self.search_line.bind('<Return>', self.search_triggered)
        self.search_line.grid(row=0,column=0, padx=self.padx, pady=self.pady)
        self.category_box = ttk.Combobox(self, values=['Früchte','Süssigkeiten','Gerichte','Getreideprodukte, Hülsenfrüchte und Kartoffeln', 'Gemüse', 'Brote, Flocken und Frühstückscerealien','Nüsse, Samen und Ölfrüchte','Gerichte', 'Fette und Öle','Fisch','Speziallebensmittel','Salzige Snacks','Eier','Milch und Milchprodukte','Fleisch- und Wurstwaren','Fleisch und Innereien','Alkoholhaltige Getränke'])
        #Wunschkategorien: 'Obst','Gemüse','Hülsenfrüchte','Getreide','Nüsse & Samen','Getränke','Öl & Dressing','Eier','Fleisch & Fisch','Milchprodukte','Gerichte'
        self.category_box.grid(column=1,row=0, padx=self.padx, pady=self.pady)
        self.category_box.bind("<<ComboboxSelected>>", self.category_changed)
        #vlt doch noch auf Listbox umändern, dann könnte man mehrere Kategorien auswählen
        self.new_item = Button(self, text='Neu')
        self.new_item.grid(column=2, row=0, padx=self.padx, pady=self.pady)

        self.last_foods = Button(self, text='Zuletzt verwendete')
        self.last_foods.grid(column=0, row=1, padx=self.padx, pady=self.pady, sticky=W)

        self.favourite_foods = Button(self, text='Favouriten')
        self.favourite_foods.grid(column=1, row=1, padx=self.padx, pady=self.pady, sticky=W)

        self.copy_day=Button(self, text='Duplizieren')
        self.copy_day.grid(column=2, row=1, padx=self.padx, pady=self.pady, sticky=W)

        self.menu_food = Menu(self, font="TkMenuFont", tearoff=0)
        self.menu_food.add_command(label="Eigenschaften", command=self.food_properties)
        self.bind("<Button-3>", self.popup) #Todo nur auf die einzelnen Foods binden!

        self.menu_meal = Menu(self, font='TkMenuFont', tearoff=0)
        self.menu_meal.add_command(label='Zutaten anpassen')

        self.found_food_frame=Frame(self)
        self.found_food_frame.grid(row=3, column=0, rowspan=1,columnspan=2, sticky=W) #ToDo row/columnspan sinnvoll u. vlt als variable festlegene
        self.found_food_header=Label(self.found_food_frame, text='Suchergebnisse:', anchor=W, font=self.bold_font)
        self.found_food_header.grid(column=0,row=0,columnspan=2,sticky=W, padx=self.padx, pady=self.pady/2)
        

        self.added_food=Frame(self)
        self.added_food.grid(row=4,column=0, rowspan=3,columnspan=3) #ToDo row/columnspan sinnvoll u. vlt als variable festlegene
        self.header_food=Label(self.added_food, text='Lebensmittel', width=30, anchor=W)
        self.header_amount=Label(self.added_food, text='Menge',anchor=W)
        self.header_unit=Label(self.added_food, text='Einheit',anchor=W)

        self.header_names=[self.header_food,self.header_amount,self.header_unit]
        for column,header_name in enumerate(self.header_names):
            header_name.grid(row=0,column=column,padx=2,pady=2,sticky=W)

        self.found_food_labels =[]
        
    def popup(self, event):
        self.menu_food.tk_popup(event.x_root, event.y_root)
        self.print_found_foods()

    def food_properties(self):
        print('Kontextmenü erfolgreich getestet')

    def category_changed(self,event):
        print('Cat. changed')
        self.category = self.category_box.get()
        self.create_new_found_food_labels()

        #wird nur eine Kategorie angegeben, kein Suchbegriff, sollten die Ergebnisse nach bisheriger Häufigkeit sortiert werden!
        
    def search_triggered(self,event):
        search_text = self.search_line.get()
        print('part is still missing: Get food names from search term')
        food_search = FoodSearch(search_text, DB('SchweizerDB.csv'))
        f1={'name': 'Apfel', 'category': 'Obst'}  #testdata
        f2={'name': 'Paranuss', 'category': 'Nüsse & Samen'}
        self.found_foods=[f1,f2]
        self.create_new_found_food_labels()

    def del_old_found_foods(self):
        for label in self.found_food_frame.grid_slaves():
            if int(label.grid_info()["row"]) > 0:
                label.grid_forget()
                
    def create_new_found_food_labels(self):
        self.del_old_found_foods()
        self.found_food_labels=[]
        self.category=self.category_box.get()
        for found_food in self.found_foods:
            if self.category:
                if not self.category == found_food['category']:
                    continue
            name_label = Label(self.found_food_frame, text=found_food['name'], anchor=W) #todo: mehrzeilig
            category_label = Label(self.found_food_frame, text=found_food['category'], anchor=W)
            self.found_food_labels.append([name_label,category_label])
        self.update_found_food_view()

    def update_found_food_view(self):
        self.del_old_found_foods()
        for row,food in enumerate(self.found_food_labels):
            for col,element in enumerate(food):
                element.grid(row=row+1, column=col, padx=self.padx,pady=0, sticky=W)                

        
root = Tk()
app = Input_Window(root)
root.mainloop()
