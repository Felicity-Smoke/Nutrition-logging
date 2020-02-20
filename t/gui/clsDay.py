from datetime import date as Date
from clsDBHandling import DBHandling
from clsShortFoodEntry import ShortFoodEntry

class Day(object):
    #imports: date, dbhandling, shortfoodentry
    def __init__(self, date):
        self._date=date
        self._db_handling = DBHandling
        self._foodlist=self._db_handling.read_entrys_from_day(self._db_handling,self._date)
        self._db_handling.get_several_food_information(self._db_handling,self._foodlist)

    @property
    def food_entries(self):
        return self._foodlist
