import sqlite3
from clsShortFoodEntry import ShortFoodEntry

'''
- Konzept noch verbesserungsfähig! Init, klassenvariablen, ...

+ die Klasse existiert zumindest und wird verwendet
'''
class DBHandling:
    def __init__(self):
        pass
    
    def read_entrys_from_day(self, date): 
        entries_from_date=[]
        db_connection=sqlite3.connect('Food.db')
        cursor=db_connection.cursor()

        #db_timestring: YYYY,MM,DD -> Wieso?? Todo: umändern!
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
            entries_from_date.append(ShortFoodEntry(result[0],result[1]))
            result = cursor.fetchone()
            
        db_connection.close()
        return entries_from_date

    def get_several_food_information(self, list_of_food):
        for food in list_of_food:
            self.get_food_information(self,food)

    def get_food_information(self, short_food_entry):

        db_connection=sqlite3.connect('Food.db')
        cursor=db_connection.cursor()

        cursor.execute('SELECT Name, Kategorie, kCal FROM Food WHERE id=?', (short_food_entry.key,))
        result=cursor.fetchone()
        db_connection.close()

        if result:
            short_food_entry.name=result[0]
            short_food_entry.category=result[1]
            short_food_entry.kCal_per_100=result[2]
        else:
            print('ID' + str(entry.key) + ' not found in database!')
        
        
