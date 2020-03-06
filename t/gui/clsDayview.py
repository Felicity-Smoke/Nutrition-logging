from tkinter import ttk, Label, Button, Frame, Tk, Canvas
import sys
from Fonts import Fonts
from clsDay import Day
import locale
from datetime import date as Date, timedelta

class Dayview(Frame):
    '''
    Todo's:
    * Breite fixieren
    * Tag mit Scrollbar versehen (siehe Suche)
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
        self.headline=Frame(self.dayframe,background='gainsboro') #todo edit color and add to Fonts
        self.heading = Label(self.headline, text='',font=Fonts.hel_11_b,bg=self.headline['background'])
        self.btn_previous=Button(self.headline, text='<',command=self.previous_day,relief='flat',bg=self.headline['background'])
        self.btn_next=Button(self.headline,text='>',command=self.next_day,relief='flat',bg=self.headline['background'])

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
            temp_label = Label(self.table_entries, text=columnheader, font=Fonts.hel_8_b) #todo später eigene Klasse, um Filtern zu ermöglichen
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
            temp_row.append(Label(self.table_entries, text=entry.calories))
            self.draw_food_entry_line(temp_row,row+1)

        sum_name=Label(self.table_entries, text='GESAMT', bg=self.headline['background'])
        sum_amount=Label(self.table_entries, text='',bg=self.headline['background'])
        sum_calories=Label(self.table_entries,text=self._today.calories,bg=self.headline['background'])
        self.draw_food_entry_line([sum_name,sum_amount,sum_calories],self.table_entries.grid_size()[1])
            
        self.table_entries.grid_columnconfigure(1,weight=1)
        self.table_entries.grid_columnconfigure(2,weight=1)
        
    def draw_food_entry_line(self,widgetlist,row_offset):
        for col, widget in enumerate(widgetlist):
                widget.grid(column=col, row=row_offset,padx=1,pady=1,sticky='nswe')
                widget.bind('<ButtonRelease-1>',self.food_dropped)
        
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
