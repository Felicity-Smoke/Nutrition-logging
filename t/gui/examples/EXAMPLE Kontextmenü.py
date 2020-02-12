from tkinter import ttk, Entry, Label, Button, Frame, Tk, Menu
#from Fonts import Fonts

class kontextmenü():
    def __init__(self):

        self.menu_food = Menu(self, tearoff=0) #, font=Fonts.tk_menu_font
        self.menu_food.add_command(label="Eigenschaften", command=self.food_properties)
        self.bind("<Button-3>", self.popup) #Todo nur auf die einzelnen Foods binden!



    def food_properties(self):
        print('Kontextmenü erfolgreich getestet')


        
