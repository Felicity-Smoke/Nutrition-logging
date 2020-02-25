from datetime import date as Date
from clsDBHandling import DBHandling
from clsShortFoodEntry import ShortFoodEntry

class Day(object):
    #imports: date, dbhandling, shortfoodentry
    def __init__(self, date):
        self._date=date
        self._db_handling = DBHandling()
        self._foodlist=self._db_handling.read_entrys_from_day(self._date)
        self._db_handling.get_several_food_information(self._foodlist)

    @property
    def food_entries(self):
        return self._foodlist

    @property
    def calories(self):
        calories_sum=0
        for food in self._foodlist:
            calories_sum+=food.calories
        return calories_sum
