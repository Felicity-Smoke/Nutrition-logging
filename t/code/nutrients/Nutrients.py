
# import matplotlib.pyplot as plt
#from matplotlib.backends.backend_pdf import PdfPages #später woanders hin
from clsFood import Food, Meal
from clsDB import DB
from clsDailyDozen import DailyDozen

import re
from datetime import date

class FormerSearch(object):
    def __init__(self, search_term):
        self.date = date.today()
        self.search_term = search_term
       
class FoodSearch(object):
    def __init__(self, search_term, food_db):
        self.food_db = food_db
        
        #Usereinstellungen - sollten später wo geändert werden können
        max_hits_shown = 20
        self.vague_search = False

        #Wird nichts gefunden Fuzzy-Methode anwenden

        self.former_searches = [] #weiter oben definieren - sonst wird jedes Mal überschrieben (oder eígene Klasse)
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
        

# _____MAIN_____

#Testdaten
food_db = DB('SchweizerDB.csv') #später richtige DB
test_search = False
daily_dozen_active = False


# SUCHE
if test_search:
    tempFood = FoodSearch('Apfel', food_db)
    foods = []
    
    for food_key in tempFood.hits.keys():
        newFood = Food(food_key, 100, food_db)
        print(newFood.name)
        foods.append(newFood)



# ALLGEMEIN
foods = [Food(406,100,food_db), Food(407,120,food_db)] #19: Apfel, 286: Haferflocken, 406: Kichererbsen
foods.extend([Food(429,200,food_db),Food(320,333,food_db),Food(264,33,food_db),Food(734,333,food_db),Food(945,321,food_db)])
if daily_dozen_active:
    daily_dozen = DailyDozen()

#pp = PdfPages('Kreisdiagramme.pdf')

nutrientsum = sum(foods)
for food in foods:
    #pp.savefig(food.makros_kreisdiagramm())
    #food.naehrstofftabelle()

    if daily_dozen_active:
        daily_dozen.add(food)

if daily_dozen_active:
    print(str(daily_dozen))
    
#pp.close()


# FOOD & MEAL ADDIEREN:
monday = []
monday.append(Food(19,180,food_db))
musli = Meal('porridge', 250, 'g')
musli.add_incredient(286,80,food_db)#haferflocken
musli.add_incredient(336,40,food_db)#joghurt
#musli.calc_nutrients()

monday.append(musli)
#hier sieht man schon wie unterschiedlich die Eingabemethoden sind --> schlecht!
sum_n = Food(2,0,food_db) #2: emtpy
for each_food in monday:
    for key in each_food.nutrients:
        pass
        sum_n.nutrients[key] += each_food.nutrients[key]
    #print(each_food.name + ': ' + str(each_food.nutrients['kcal']))
#print(str(sum_n))
