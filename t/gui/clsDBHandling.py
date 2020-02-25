import sqlite3
from clsShortFoodEntry import ShortFoodEntry
from datetime import date as Date
'''
- Konzept noch verbesserungsfähig! Init, klassenvariablen, ...

+ die Klasse existiert zumindest und wird verwendet
+ Tests sind vorhanden
'''
class DBHandling:
    def __init__(self):
        self._db=None
    
    def read_entrys_from_day(self, date): 
        entries_from_date=[]
        try:
            self._open_db()
            cursor=self._db.cursor()
        
            cursor.execute('SELECT Food_ID, Menge FROM FoodEntries WHERE Datum=?',(str(date),))
            result = cursor.fetchone()
        
            while result:
                entries_from_date.append(ShortFoodEntry(result[0],result[1]))
                result = cursor.fetchone()
        except:
            pass
        finally:
            self._close_db()
            
        return entries_from_date

    def get_several_food_information(self, list_of_food):
        for food in list_of_food:
            self.get_food_information(food)

    def get_food_information(self, short_food_entry):

        try:
            self._open_db()
            cursor=self._db.cursor()

            cursor.execute('SELECT Name, Kategorie, kCal FROM Food WHERE id=?', (short_food_entry.key,))
            result=cursor.fetchone()
        except:
            pass
        finally:
            self._close_db()

        if result:
            short_food_entry.name=result[0]
            short_food_entry.category=result[1]
            short_food_entry.kCal_per_100=result[2]
        else:
            print('ID' + str(entry.key) + ' not found in database!')

    def write_entry(self, date, food):
        try:
            self._open_db()
            cursor=self._db.cursor()

            cursor.execute('INSERT INTO FoodEntries (Food_ID, Menge,Datum,Mahlzeit,Gericht) VALUES (?,?,?,?,?)', \
                           (food.key,food.amount,str(date),1,0,))
            cursor.fetchone()
            self._db.commit()            
        except:
            pass
        finally:
            self._close_db()
            
    def _open_db(self):
        self._db=sqlite3.connect('Food.db')
    def _close_db(self):
        self._db.close()

if __name__ == '__main__':
    read1=True
    read2=True
    write=False
    
    db = DBHandling()

    # read entrys from day
    if read1:
        entries = db.read_entrys_from_day(Date(2020,2,25))
        print(str(len(entries)))
        for entry in entries:

            # get food information
            if read2:
                db.get_food_information(entry)
                print(str(entry.key) + ' ' + entry.name)
            else:
                print(str(entry.key))

        # write entry
        if write:
            food = entries[0]
            food.amount=999
            food._key+=1 # Zugriff auf '_' - Variable nur für Testzweck!
            db.write_entry(Date.today(),food)


        
