from tkinter import Button,Frame,Label,Tk,Menu,ttk, font, RIDGE as relief_ridge
import locale
from clsSearch import FoodSearch
from clsMonth import Month, number_color
from clsCalendarDay import CalendarDay

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
        
class Input_Window(Frame):
    def __init__(self, parent,month):
        super().__init__(parent)
        self.month = month
        
        self.active=False

        self.padx = 20
        self.pady = 10
        self.bold_big_font='Helvetica 11 bold'
        self.bold_small_font='Helvetica 8 bold'
        self.bigger_font='Helvetica 10'

        self.calendar_month_frame=Frame(parent)
        self.calendar_month_frame.grid(column=0,row=0, padx=self.padx,pady=self.pady,rowspan=25) #rowspan anpassen

        #header
        self.calendar_headings = []
        self.button_former_month = Button(self.calendar_month_frame,text='<',command=self.goto_previous_month,relief=relief_ridge)
        self.month_heading = Label(self.calendar_month_frame,font=self.bigger_font)
        self.button_next_month = Button(self.calendar_month_frame,text='>',command=self.goto_next_month,relief=relief_ridge)
        self.calendar_headings.append([self.button_former_month,self.month_heading, self.button_next_month])
        self.update_displayed_month()

        #days
        line=[]
        for weekday in ['Mo','Di','Mi','Do','Fr','Sa','So']:
            line.append(Label(self.calendar_month_frame, text=weekday, font=self.bold_small_font))

        self.calendar_headings.append(line)
        self.position_widget_lines(self.calendar_headings,self.calendar_month_frame)
        
        '''
        Optionen
        '''
        self.feature_list = []
        self.feature_list.append(ttk.Checkbutton(parent,text='Tage mit Fleischkonsum kennzeichnen'))
        self.feature_list.append(ttk.Checkbutton(parent,text='Tage mit Milchkonsum kennzeichnen'))
        self.feature_list.append(ttk.Checkbutton(parent,text='Tage mit pflanzlicher Ernährung kennzeichnen'))
        self.feature_list.append(ttk.Checkbutton(parent,text='Kalorienbilanz des Tages darstellen'))
        self.feature_list.append(ttk.Checkbutton(parent,text='Tage mit Eiweißdefizit kennzeichnen'))

        col = 1 #anders lösen!
        self.position_widget_list(self.feature_list, col)

        parent.grid_rowconfigure(0,minsize=200)

        # Kontextmenü
        self.menu_food = Menu(self, font="TkMenuFont", tearoff=0)
        self.menu_food.add_command(label="Eigenschaften", command=self.food_properties)
        self.bind("<Button-3>", self.popup) #Todo nur auf die einzelnen Foods binden!

        self.menu_meal = Menu(self, font='TkMenuFont', tearoff=0)
        self.menu_meal.add_command(label='Zutaten anpassen')

    def quit(self):
        self.quit()
        
    def position_widget_lines(self,widget_list, master=None, row_offset=0):
        y_offset = 1
        x_offset = 1
        columnspan=1
        header = False
        for row,widgetline in enumerate(widget_list):
            if len(widgetline)<7:
                header = True
            for column,widget in enumerate(widgetline):
                if header and column==1:
                    columnspan=5
                elif header and column==2:
                    columnspan=1
                    column=6
                    header=False
                widget.grid(column=column, row=row+row_offset, padx=x_offset, pady=y_offset,sticky='nsew', columnspan=columnspan)
            if master:
                master.grid_rowconfigure(row,weight=1)
                
    def goto_next_month(self):
        self.month = self.month.next()
        self.update_displayed_month()

    def goto_previous_month(self):
        self.month = self.month.previous()
        self.update_displayed_month()

    def update_displayed_month(self):
        self.month_heading['text']=f"{self.month.name} {self.month.year}"
        self.draw_days_of_list(self.month.calendardays)
    
    def position_widget_list(self,widget_list, column=0):
        y_offset = 1
        x_offset = 1
        columnspan=1
        header = False
        for row,widget in enumerate(widget_list):
                widget.grid(column=column, row=row, padx=x_offset, pady=y_offset,sticky='nsew', columnspan=columnspan)        
        
    def draw_days_of_list(self,days):
        self.clear_days()
        self.calendar_itemlines = []
        line = []
        for day in days:
            line.append(CalendarDay(self.calendar_month_frame, text=day.number,fg=day.color))
            if len(line) == 7:
                self.calendar_itemlines.append(line)
                line=[]

        self.position_widget_lines(self.calendar_itemlines,self.calendar_month_frame,row_offset=2)
        

    def clear_days(self):
        for slave in self.calendar_month_frame.grid_slaves():
            if type(slave) == CalendarDay:
                slave.destroy()
        
    def popup(self, event):
        self.menu_food.tk_popup(event.x_root, event.y_root)
        self.print_found_foods()

    def food_properties(self):
        print('Kontextmenü erfolgreich getestet')



locale.setlocale(locale.LC_ALL,"")
root = Tk()
window = Input_Window(root,Month.from_date())
window.grid(row=0,column=0)
root.geometry("600x300")
root.mainloop()
