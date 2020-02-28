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

    def _get_category_list():
        for food in self._foodlist:
            if not food.category in self._category_list:
                self._category_list.append(food.category)
                
    @property
    def food_entries(self):
        return self._foodlist

    @property
    def calories(self):
        calories_sum=0
        for food in self._foodlist:
            calories_sum+=food.calories
        return format(calories_sum, '.2f')

    def is_vegan(self):
        not_vegan = ['Eier','Fisch','Milch und Milchprodukte', 'Fleisch- und Wurstwaren','Fleisch und Innereien']
        if len(self._category_list)<1:
            self._get_category_list()
            
        for each in not_vegan:
            if each in self._category_list:
                print('return not vegan')
                return False
        print('return vegan')
        return True
                
