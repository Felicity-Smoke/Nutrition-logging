from clsFood import Food, Meal
import re
from datetime import date

class FormerSearch(object):
    def __init__(self, search_term):
        self.date = date.today()
        self.search_term = search_term
       
class FoodSearch(object):
    def __init__(self, search_term, food_db='SchweizerDB.csv'):
        self.food_db = food_db
        
        #Usereinstellungen - sollten später wo geändert werden können
        max_hits_shown = 20
        self.vague_search = False

        #Wird nichts gefunden Fuzzy-Methode anwenden
        self.former_searches = [] #weiter oben definieren - sonst wird jedes Mal überschrieben
        self.former_searches.append(FormerSearch(search_term))

        self.hits = {}
        
        self.search_basic(search_term)

        if self.vague_search and len(self.hits)<max_hits_shown:
            self.search_vague(search_term)

    def search_basic(self, search_term):
        linenumber = 4
        for foodline in self.food_db.table[(linenumber-1):1020]:
            if re.findall(search_term.lower(), (foodline[0] + foodline[1]).lower()):
                self.hits[linenumber] = foodline
            linenumber = linenumber + 1

    def search_vague(self, search_term):
        for i in enumerate(search_term):
            try:
                self.search_basic(search_term[:i-1] + '.' + search_term[i+1:])
                self.search_basic(search_term[:i] + '.' + search_term[i+1:])
            except:
                continue

    def get_IDs(self):
        return self.hits.keys()

    def get_names(self):
        food_names = []
        for food_key in self.hits.values():
            food_names.append(food_key[0])
        return food_names

    def get_foods(self):
        return self.hits.values()

    def get_name_and_category(self):
        name_and_category=[]
        for food in self.hits.values():
            el = {}
            el['name']=food[0]+food[1]
            el['category']=food[2]
            name_and_category.append(el)
