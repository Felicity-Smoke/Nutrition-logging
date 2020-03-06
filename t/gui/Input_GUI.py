from tkinter import ttk, Entry, Label, Button, Frame, Tk, Menu, Canvas
import sys
from Search_code import FoodSearch as Search, Searchterm
from Fonts import Fonts
from datetime import date as Date, timedelta
from clsDayview import Dayview

'''
Stand Input_Window:
- sieht eher mies aus
- schlechtes Naming - eigentlich wird hier nur ausgewählt, nicht eingegeben (Drag, aber kein Drop)

+ Suche funktioniert bereits gut, aktiviert durch Enter in der Suchleiste,
    in der Food.db gefundene Datensätze werden inkl. Scrollbar angezeigt

Next steps:
- Scrollbar über Mausrad aktivieren - binding
- Namenslabel für foods begrenzen oder Feld in db (wenn in db, dann auch gleich tailing commas vernichten)
* Drag n Drop von Suchfenser zu Tagesfenser (inkl. Mauszeiger)
- Button-commands hinzufügen
'''
        
class Input_Window(Frame):
    def __init__(self, parent):
        super(Input_Window, self).__init__(parent)
        self.parent = parent
        
        self.active=False
        self.grid(row=0,column=0)
        
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
        self.input_navigation_buttons=[]
        self.input_navigation_buttons.append(Button(self.input_navigation, text='Oft verwendete'))
        self.input_navigation_buttons.append(Button(self.input_navigation, text='Favouriten'))
        self.input_navigation_buttons.append(Button(self.input_navigation, text='Gestern'))
        self.input_navigation_buttons.append(Button(self.input_navigation, text='Tag wählen'))

        self.input_navigation.grid(row=1,column=0, padx=Fonts.framedistance, pady=Fonts.framedistance,sticky='w')
        for col,input_navigation_button in enumerate(self.input_navigation_buttons):
            input_navigation_button.grid(column=col, row=0, padx=Fonts.framedistance, pady=0, sticky='w')

        # found_food
        self.results=Frame(self)
        self.canvas=Canvas(self.results)
        self.scrollbar = ttk.Scrollbar(self.results, orient='vertical', command=self.canvas.yview)
        self.canvas.bind('<MouseWheel>',self.onMouseWheel)
        self.found_food_frame=Frame(self.canvas, background=Fonts.table_bg)
        self.found_food_frame.bind('<MouseWheel>',self.onMouseWheel)
        self.canvas.create_window(0, 0, anchor='nw', window=self.found_food_frame)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.found_food_header=Label(self.found_food_frame, text='Suchergebnisse:', anchor='w', font=Fonts.hel_11_b )     

        self.results.grid(row=3,column=0,sticky='w',padx=Fonts.framedistance,pady=Fonts.framedistance) 
        self.canvas.grid(row=0,column=0)
        self.found_food_header.grid(column=0,row=0,columnspan=3,sticky='wesn', padx=2, pady=2)

        # Dayview
        self.day_frame = Dayview(self,Date.today())
        self.day_frame.grid(column=3, row=0, rowspan=3)

    def onMouseWheel(self,event):
        self.canvas.yview("scroll",event.delta,"units")
        return
    
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
        found_food_labels=[]
        for found_food in self.found_foods:
            if self.category:
                if not self.category == found_food.category:
                    continue
            name_label = Label(self.found_food_frame, text=found_food.name, anchor='w') 
            category_label = Label(self.found_food_frame, text=found_food.category, anchor='w')
            found_food_labels.append([name_label,category_label])
        self.update_found_food_view(found_food_labels)

    def update_found_food_view(self,found_food_labels):
        self.del_old_found_foods()
        for row,food in enumerate(found_food_labels):
            for col,element in enumerate(food):
                element.grid(row=row+1, column=col, padx=1,pady=1, sticky='wsen')
                element.bind('<B1-Motion>',self.motion_active)
                element.bind('<ButtonRelease-1>',self.motion_stopped)

        if len(self.found_foods)>10: #10 nur als bsp... todo: besseren wert überlegen, vlt skalierbar
            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))
            self.scrollbar.grid(row=0,column=1, sticky='ns')
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
