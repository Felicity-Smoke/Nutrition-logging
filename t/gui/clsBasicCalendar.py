from tkinter import Button,Frame,Label,Tk,Menu,ttk
from clsMonth import Month, number_color
from clsCalendarDay import CalendarDay
from Fonts import Fonts
from datetime import date as Date
import locale

'''
Kalender (ähnlich wie in Windows)
 - jeder Tag sollte angeklickt werden können für Detailansicht des Tages
        > Doppelklick: Tagesansicht öffnet sich, der Tag kann bearbeitet werden o.Ä.
        > einfacher Klick: Die Daten des Tages werden angezeigt, verglichen mit den Solldaten (Falls vorhanden)
        > Klick mit gedrückter Strg-Taste: Wartet auf einen zweiten Tag um die Statistik über den ausgewählten Zeitraum anzuzeigen
 - durch das Ziehen über Tage sollte eine Statistik erstellt werden können

- Es könnte ein Monatsdurchschnittswert für alles mögliche angezeigt werden

Momentane Mätzchen/Überlegungen:
- vlt generell alle Tage (clsDay) mit initialisieren?
- Klick momentan über doppeltes Binding realisiert
- flackert beim Monatswechsel (vlt einfach Größe fixieren)
'''

class BasicCalendar(Frame):
    def __init__(self,parent,month=None,mode=0):
        super().__init__(parent)
        self.month = month
        if self.month is None:
            print('Month is None')
            self.month = Month(Date.today().year,Date.today().month)
        self.mode=mode
        
        self.active=False
        self._container_days = []
        self.clicked_day=None

        self.padx_frame = 20
        self.pady_frame = 10
        self.padx=1
        self.pady=1

        self.calendar_month_frame=Frame(parent)
        self.calendar_month_frame.grid(column=0,row=0, padx=self.padx_frame,pady=self.pady_frame,rowspan=25, sticky='N') #rowspan anpassen
        parent.grid_rowconfigure(0,minsize=100)

        #header
        self.button_former_month = Button(self.calendar_month_frame,text='<',command=self.goto_previous_month,relief='flat')
        self.month_heading = Label(self.calendar_month_frame,font=Fonts.hel_10)
        self.button_next_month = Button(self.calendar_month_frame,text='>',command=self.goto_next_month,relief='flat')

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

    @property
    def get_clicked_day(self):
        for day in self.days:
            if day.was_double_clicked:
                return day.day
        return False

    @property
    def days(self):
        days=[]
        for week in self._container_days:
            for day in week:
                days.append(day)
        return days            
                    
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
        self._container_days = []
        for x in range(6):
            line = []
            for y in range(7):
                line.append(CalendarDay(self.calendar_month_frame,mode=self.mode))
            self._container_days.append(line)
            
        self.position_container_days(self._container_days,self.calendar_month_frame,row_offset=2)

    def position_container_days(self,widget_list, master=None, row_offset=0):
        for row,widgetline in enumerate(widget_list):
            for column,widget in enumerate(widgetline):
                widget.grid(column=column, row=row+row_offset, padx=self.padx, pady=self.pady,sticky='nsew')
            if master:
                master.grid_rowconfigure(row,weight=1)
                
    def update_display_days(self,days):
        unpositioned_weeks=[]
        for container_week in self._container_days:
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

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL,"")
    root = Tk()
    window = BasicCalendar(root,Month.from_date(),mode=1)
    window.grid(row=0,column=0)
    root.mainloop()
    
