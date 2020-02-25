import sqlite3
from clsShortFoodEntry import ShortFoodEntry

'''
- Konzept noch verbesserungsfähig! Init, klassenvariablen, ...

+ die Klasse existiert zumindest und wird verwendet
'''
class DBHandling:
    def __init__(self):
        self._db=None
    
    def read_entrys_from_day(self, date): 
        entries_from_date=[]
        try:
            self._open_db()
            cursor=self._db.cursor()

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
        except:
        finally:
            self._close_db()
        return entries_from_date

    def get_several_food_information(self, list_of_food):
        for food in list_of_food:
            self.get_food_information(self,food)

    def get_food_information(self, short_food_entry):

        try:
            self._open_db()
            cursor=self._db.cursor()

            cursor.execute('SELECT Name, Kategorie, kCal FROM Food WHERE id=?', (short_food_entry.key,))
            result=cursor.fetchone()
        except:
        finally:
            self._close_db()

        if result:
            short_food_entry.name=result[0]
            short_food_entry.category=result[1]
            short_food_entry.kCal_per_100=result[2]
        else:
            print('ID' + str(entry.key) + ' not found in database!')

    def write_entry(self, date, food):#untested!
        try:
            self._open_db()
            cursor=self._db.cursor()

            cursor.execute('INSERT INTO FoodEntries (Food_ID, Menge,Datum,Mahlzeit,Gericht) VALUES (?,?,?,?,?)', \
                           (food.key,food.amount,str(date),1,0,))
            cursor.fetchone()
            self._db.commit()            
        except:
        finally:
            self._close_db()
            
    def _open_db(self):
        self._db=sqlit3.connect('Food.db')
    def _close_db(self):
        self._db.close()
