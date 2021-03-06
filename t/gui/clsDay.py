from datetime import date as Date
from clsDBHandling import DBHandling
from clsShortFoodEntry import ShortFoodEntry

'''
Todos:
- Kategorie-Namen auslagern
'''
class Day(object):
    def __init__(self, date):
        self._date=date
        self._db_handling = DBHandling()
        self._foodlist=self._db_handling.read_entrys_from_day(self._date)
        self._db_handling.get_several_food_information(self._foodlist)
        self._category_list=[]

    def _get_category_list(self):
        for food in self._foodlist:
            if not food.category in self._category_list:
                self._category_list.append(food.category)

    def add(self,food):
        self._db_handling.write_entry(self._date, food)
        self._reload()

    def _reload(self):
        self._foodlist=self._db_handling.read_entrys_from_day(self._date)
        self._db_handling.get_several_food_information(self._foodlist)
        self._category_list=[]
        
    @property
    def food_entries(self):
        return self._foodlist

    @property
    def calories(self):
        calories_sum=0
        for food in self._foodlist:
            calories_sum+=food.calories
        return format(calories_sum, '.2f')

    def meets_criterias(self, categories, needed): #rename!!
        if len(self._category_list)<1:
            self._get_category_list()

        for each in categories:
            if each in self._category_list:
                if needed == True:
                    return True
                else:
                    return False
        return not needed              
