# import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages  # später woanders hin
from clsFood import Food, Meal
from clsDB import DB
from clsDailyDozen import DailyDozen
from clsSearch import FoodSearch
import re


# _____MAIN_____

# Testdaten
food_db = DB('SchweizerDB.csv')  # später richtige DB
test_search = True
daily_dozen_active = False


# SUCHE
if test_search: 
    tempFood = FoodSearch('Apfel', food_db)
    foods = []

    print(tempFood.get_names())
    # for food_key in tempFood.get_IDs():
    # newFood = Food(food_key, 100, food_db)
    # print(newFood.name)
    # foods.append(newFood)

# ALLGEMEIN
foods = [Food(406, 100, food_db), Food(407, 120, food_db)]  # 19: Apfel, 286: Haferflocken, 406: Kichererbsen
nrs = [429, 320, 264, 734, 333, 45, 321, 893, 746, 328, 669, 558, 259, 563, 574, 193, 486]

for nr in nrs:
    foods.append(Food(nr, 100, food_db))
    
if daily_dozen_active:
    daily_dozen = DailyDozen()

pp = PdfPages('Kreisdiagramme.pdf')

nutrientsum = sum(foods)
for food in foods:
    pp.savefig(food.makros_kreisdiagramm(save=False))
    pp.savefig(food.naehrstofftabelle(save=False))

    if daily_dozen_active:
        daily_dozen.add(food)

if daily_dozen_active:
    print(str(daily_dozen))    
pp.close()


# FOOD & MEAL ADDIEREN:
monday = []
monday.append(Food(19, 180, food_db))
musli = Meal('porridge', 250, 'g')
musli.add_incredient(286, 80, food_db)  # haferflocken
musli.add_incredient(336, 40, food_db)  # joghurt
# musli.calc_nutrients()

monday.append(musli)
# hier sieht man schon wie unterschiedlich die Eingabemethoden sind --> schlecht!
sum_n = Food(2, 0, food_db)  # 2: emtpy
for each_food in monday:
    for key in each_food.nutrients:
        pass
        sum_n.nutrients[key] += each_food.nutrients[key]
    # print(each_food.name + ': ' + str(each_food.nutrients['kcal']))
# print(str(sum_n))
