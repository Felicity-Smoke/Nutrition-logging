from tkinter import Button,Frame,Label,Tk,Menu,ttk,IntVar
import locale
from clsMonth import Month, number_color
from clsCalendarDay import CalendarDay, Logos
from clsDay import Day
from Fonts import Fonts
from datetime import date as Date
from clsBasicCalendar import BasicCalendar

'''
Kalender (ähnlich wie in Windows)
 - jeder Tag sollte angeklickt werden können für Detailansicht des Tages
        > Doppelklick: Tagesansicht öffnet sich, der Tag kann bearbeitet werden o.Ä.
        > einfacher Klick: Die Daten des Tages werden angezeigt, verglichen mit den Solldaten (Falls vorhanden)
        > Klick mit gedrückter Strg-Taste: Wartet auf einen zweiten Tag um die Statistik über den ausgewählten Zeitraum anzuzeigen
 - durch das Ziehen über Tage sollte eine Statistik erstellt werden können
 - Über CBs am Rand sollten kurzinfos für jeden Tag eingeblendet werden können (begrenzte Anzahl - vlt 3)

- Es könnte ein Monatsdurchschnittswert für alles mögliche angezeigt werden

Momentane Mätzchen/Überlegungen:
- vlt generell alle Tage (clsDay) mit initialisieren?
- Klick über doppeltes Binding realisiert
- flackert beim Monatswechsel (vlt einfach Größe fixieren)
'''
        
class Calendar (BasicCalendar):
    def __init__(self, parent,month):
        super().__init__(parent,month)        
        '''
        Optionen
        '''

        self.feature_frame=Frame(parent)
        self.feature_frame.grid(row=0,column=1)
        self.feature_list = []
        self.show_is_vegan=IntVar()
        self.show_meat_days=IntVar()
        self.show_dairy_days=IntVar()
        self.show_calories=IntVar()
        self.show_proteins=IntVar()
        self.feature_list.append(ttk.Checkbutton(self.feature_frame,variable=self.show_meat_days,text='Tage mit Fleischkonsum kennzeichnen',command=self.show_meat_days_CB_changed))
        self.feature_list.append(ttk.Checkbutton(self.feature_frame,variable=self.show_dairy_days, text='Tage mit Milchkonsum kennzeichnen',command=self.show_dairy_days_CB_changed))
        self.feature_list.append(ttk.Checkbutton(self.feature_frame,variable=self.show_is_vegan, text='Tage mit pflanzlicher Ernährung kennzeichnen',command=self.show_vegan_days_CB_changed))
        self.feature_list.append(ttk.Checkbutton(self.feature_frame,variable=self.show_calories,text='Kalorienbilanz in % anzeigen',command=self.show_calories_CB_changed))
        self.feature_list.append(ttk.Checkbutton(self.feature_frame,variable=self.show_proteins,text='Eiweiß-Deckung in % anzeigen',command=self.show_proteins_CB_changed))

        self.position_widget_list(self.feature_list)
        
        # Kontextmenü
        self.menu_food = Menu(self, font="TkMenuFont", tearoff=0)
        self.menu_food.add_command(label="Eigenschaften", command=self.food_properties)
        self.bind("<Button-3>", self.popup) #Todo nur auf die einzelnen Foods binden!

        self.menu_meal = Menu(self, font='TkMenuFont', tearoff=0)
        self.menu_meal.add_command(label='Zutaten anpassen')

    def show_calories_CB_changed(self):
            for dayline in self.container_days:
                for day in dayline:
                    if day.from_actual_month:
                        if self.show_calories.get():
                            sum_calories=float(Day(Date(self.month.year,self.month.month,day.day)).calories)
                            day.add_text(format(sum_calories*100/2000, '.0f')) #2000 als Richtwert!
                        else:
                            day.delete_text()

    def show_proteins_CB_changed(self):
        pass
    
    def show_dairy_days_CB_changed(self): 
        if self.show_dairy_days.get():
            categories=['Milch und Milchprodukte'] #Süßigkeiten
            self.set_logos_to_month(Logos.dairy, categories, True)
        
        else:
            self.delete_logos_from_month(Logos.dairy)
            
    def show_meat_days_CB_changed(self):
        if self.show_meat_days.get():
            categories=['Fleisch- und Wurstwaren','Fleisch und Innereien'] #'Fisch'?
            self.set_logos_to_month(Logos.meat, categories, True)
        
        else:
            self.delete_logos_from_month(Logos.meat)
                    
    def show_vegan_days_CB_changed(self):
        if self.show_is_vegan.get():
            categories=['Eier','Fisch','Milch und Milchprodukte', 'Fleisch- und Wurstwaren','Fleisch und Innereien']
            self.set_logos_to_month(Logos.vegan, categories, False)
        
        else:
            self.delete_logos_from_month(Logos.vegan)

    def set_logos_to_month(self, logo, categories, needed):
        success=True
        for dayline in self.container_days:
            for day in dayline:
                if day.from_actual_month:
                    if Day(Date(self.month.year,self.month.month,day.day)).meets_criterias(categories,needed):
                        success = success and day.add_logo(logo)
        if not success:
            print('Es konnten nicht alle Symbole gesetzt werden')
        
    def delete_logos_from_month(self,logo):
        for dayline in self.container_days:
            for day in dayline:
                 day.delete_logo(logo)
                    
 
        
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

