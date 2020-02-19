import sqlite3
from clsShortFoodEntry import ShortFoodEntry

'''
- Konzept noch verbesserungsfähig! Init, klassenvariablen, ...

+ die Klasse existiert zumindest und wird verwendet
'''
class DBHandling:
    def __init__(self):
        pass
    
    def read_entrys_from_day(self, date): #gehört hier unbedingt raus! DB-Zugriffe nicht im GUI-File! (self deswegen bewusst entkoppelt)
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
            entries_from_date.append(ShortFoodEntry(result[0],result[1]))
            result = cursor.fetchone()
            
        db_connection.close()
        return entries_from_date

    #def add_data_from_db(self, short_food_entry):
        
