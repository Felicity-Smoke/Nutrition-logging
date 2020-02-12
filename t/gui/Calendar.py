from tkinter import Button,Frame,Label,Tk,Menu,ttk, FLAT as relief
import locale
from clsMonth import Month, number_color
from clsCalendarDay import CalendarDay
from Fonts import Fonts

'''
Kalender (ähnlich wie Windows-Version)
 - jeder Tag sollte angeklickt werden können für Detailansicht des Tages
        > Doppelklick: Tagesansicht öffnet sich, der Tag kann bearbeitet werden o.Ä.
        > einfacher Klick: Die Daten des Tages werden angezeigt, verglichen mit den Solldaten (Falls vorhanden)
        > Klick mit gedrückter Strg-Taste: Wartet auf einen zweiten Tag um die Statistik über den ausgewählten Zeitraum anzuzeigen
 - durch das Ziehen über Tage sollte eine Statistik erstellt werden können
 - Über CBs am Rand sollten kurzinfos für jeden Tag eingeblendet werden können (begrenzte Anzahl - vlt 3)

später gesamten Kalender als eigene Klasse

Momentane Mätzchen:
- Klick über doppeltes Binding realisiert
- flackert beim Monatswechsel (vlt einfach Größe fixieren)
- CBs nur Optik, keine Funktion
'''
        
class Calendar (Frame):
    def __init__(self, parent,month):
        super().__init__(parent)
        self.month = month
        
        self.active=False
        self.container_days = []

        self.padx_frame = 20
        self.pady_frame = 10
        self.padx=1
        self.pady=1

        self.calendar_month_frame=Frame(parent)
        self.calendar_month_frame.grid(column=0,row=0, padx=self.padx_frame,pady=self.pady_frame,rowspan=25, sticky='N') #rowspan anpassen
        parent.grid_rowconfigure(0,minsize=100)

        #header
        self.button_former_month = Button(self.calendar_month_frame,text='<',command=self.goto_previous_month,relief=relief)
        self.month_heading = Label(self.calendar_month_frame,font=Fonts.hel_10)
        self.button_next_month = Button(self.calendar_month_frame,text='>',command=self.goto_next_month,relief=relief)

        self.button_former_month.grid(column=0,row=0,padx=self.padx,pady=self.pady,sticky='nsew')
        self.month_heading.grid(column=1,row=0,padx=self.padx,pady=self.pady,columnspan=5,sticky='nsew')
        self.button_next_month.grid(column=6,row=0,padx=self.padx,pady=self.pady,sticky='nsew')
       
        #days
        weekday_labels=[]
        for weekday in ['Mo','Di','Mi','Do','Fr','Sa','So']:
            weekday_labels.append(Label(self.calendar_month_frame, text=weekday, font=Fonts.hel_8_b))
        for column,weekday in enumerate(weekday_labels):
            weekday.grid(column=column,row=1,padx=self.padx,pady=self.pady,sticky='nsew')
                    
        self.draw_container_days()
        self.update_displayed_month()
        
        '''
        Optionen
        
        self.feature_list = []
        self.feature_list.append(ttk.Checkbutton(parent,text='Tage mit Fleischkonsum kennzeichnen'))
        self.feature_list.append(ttk.Checkbutton(parent,text='Tage mit Milchkonsum kennzeichnen'))
        self.feature_list.append(ttk.Checkbutton(parent,text='Tage mit pflanzlicher Ernährung kennzeichnen'))
        self.feature_list.append(ttk.Checkbutton(parent,text='Kalorienbilanz des Tages darstellen'))
        self.feature_list.append(ttk.Checkbutton(parent,text='Tage mit Eiweißdefizit kennzeichnen'))

        self.position_widget_list(self.feature_list, column=1)
        '''

        # Kontextmenü
        self.menu_food = Menu(self, font="TkMenuFont", tearoff=0)
        self.menu_food.add_command(label="Eigenschaften", command=self.food_properties)
        self.bind("<Button-3>", self.popup) #Todo nur auf die einzelnen Foods binden!

        self.menu_meal = Menu(self, font='TkMenuFont', tearoff=0)
        self.menu_meal.add_command(label='Zutaten anpassen')
                
    def goto_next_month(self):
        self.month = self.month.next()
        self.update_displayed_month()

    def goto_previous_month(self):
        self.month = self.month.previous()
        self.update_displayed_month()

    def update_displayed_month(self):
        self.month_heading['text']=f"{self.month.name} {self.month.year}"
        self.update_display_days(self.month.calendardays)
    
    def position_widget_list(self,widget_list, column=0):
        for row,widget in enumerate(widget_list):
                widget.grid(column=column, row=row, padx=self.padx, pady=self.pady,sticky='nsew')

    def draw_container_days(self):
        self.container_days = []
        for x in range(6):
            line = []
            for y in range(7):
                line.append(CalendarDay(self.calendar_month_frame))
            self.container_days.append(line)
            
        self.position_container_days(self.container_days,self.calendar_month_frame,row_offset=2)

    def position_container_days(self,widget_list, master=None, row_offset=0):
        for row,widgetline in enumerate(widget_list):
            for column,widget in enumerate(widgetline):
                widget.grid(column=column, row=row+row_offset, padx=self.padx, pady=self.pady,sticky='nsew')
            if master:
                master.grid_rowconfigure(row,weight=1)
                
    def update_display_days(self,days):
        unpositioned_weeks=[]
        for container_week in self.container_days:
            unpositioned_week = []
            for container_day in container_week:
                if days:
                    container_day.change_day(days[0].number)
                    container_day.change_textcolor(days[0].color)
                    del days[0]
                    if not container_day.grid_info():
                        unpositioned_week.append(container_day)                                           
                else:
                    container_day.grid_forget()
            unpositioned_weeks.append(unpositioned_week)
        self.position_container_days(unpositioned_weeks,self.calendar_month_frame,row_offset=self.calendar_month_frame.grid_size()[1])
        
    def clear_days(self, startitem=0):
        count = 0
        for slave in self.calendar_month_frame.grid_slaves():
            if type(slave) == CalendarDay:
                count+=1
                if count>startitem:
                    slave.forget()
        
    def popup(self, event):
        self.menu_food.tk_popup(event.x_root, event.y_root)
        self.print_found_foods()

    def food_properties(self):
        print('Kontextmenü erfolgreich getestet')


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL,"")
    root = Tk()
    window = Calendar(root,Month.from_date())
    window.grid(row=0,column=0)
    root.mainloop()

