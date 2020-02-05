from clsDB import DB
import matplotlib.pyplot as plt

empty_food_line = 3

class Meal(object):
    def __init__(self, name, amount=0, unit=''):
        self.name = name
        self.amount = amount
        self.unit = unit

        self.incredients = {} #ToDo: Sortierung nach zuletzt verwendeter Menge (wenn das überhaupt geht)
        self.nutrients = Food(empty_food_line,0).nutrients 

    def del_incredient(self, incredient_id): #ID als zeilennummer
         del self.incredients[incredient_id]
        
    def add_incredient(self, incredient_id, amount = 0, db=False):
        self.incredients[incredient_id] = Food(incredient_id,amount,db)

    def change_amount_incredient(self, incredient_id, new_amount):
        self.incredients[incredient_id].amount = new_amount

    def change_amount(self, new_amount):
        if new_amount <= 1:
            self.amount = sum(self.incredients.values().amount)*new_amount
        else:
            self.amount = new_amount

    def calc_nutrients(self): #privat
        for key,value in self.nutrients:
            self.nutrients[key] = sum(self.incredients[key])
        

    #Meals und Foods müssen addiert werden können! --- vlt auch nicht, es reicht genau genommen die Nutrients separat zu addieren!
    #bei Meals soll als Menge auch 1 oder 1/2 (o.Ä.) auswählbar sein

class Nutrient(object):    
    def __init__(self, name, column, unit, amount = 0):
        self.name = name
        self.column = column
        self.unit = unit
        self.amount = amount

    def __add__(self, other):
        total_amount = 0
        if self.unit == other.unit:
            total_amount = self.amount + other.amount
        else:
            print('Problem while adding Nutrients - different units')
        return Nutrient(self.name, 0, self.unit, total_amount)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __str__(self):
        return self.name + ' '*(25 - len(self.name)) + str(self.amount) + self.unit

class MakroNutrient(Nutrient):
    def __init__(self, name, column, unit, kcal, amount = 0):
        Nutrient.__init__(self, name, column, unit, amount = 0)
        
        self.kcal = kcal

    def get_calories(self):
        return self.amount*self.kcal

class Part_Of_MakroNutrient(MakroNutrient):
    def __init__(self, name, column, unit, kcal, makro_key, amount = 0):
        MakroNutrient.__init__(self, name, column, unit, kcal, amount = 0)
        self.makro_key = makro_key
        
#später umbau auf mehrere Klassen die erben; neue Klassen: Makros [-> Bedarf anders ausrechnen, kcal-Angabe]
class Food(object): 
    def __init__(self,line_number, amount, database = False):
        if not database:
            self.food_db = DB('SchweizerDB.csv')
        else:
            self.food_db = database
        
        line_number = line_number - 1
        self.basic_keys = ['kcal','fat','sat_fat','carbs','sugar','fibres','protein']
        self.amount = amount        
        self.name = ''
        self.category = ''

        self.nutrients = {}
        #0? TODO: Vital_Basic rausfinden
        self.nutrients['kcal'] = Nutrient('Energie', 6, 'kcal')
        self.nutrients['fat'] = MakroNutrient('Fett', 7, 'g', 9)
        self.nutrients['carbs'] = MakroNutrient('Kohlenhydrate', 12, 'g', 4)
        self.nutrients['protein'] = MakroNutrient('Eiweiß', 16, 'g', 4)

        self.nutrients['sat_fat'] = Part_Of_MakroNutrient('ges. Fett', 8, 'g', 9, 'fat') 
        self.nutrients['mono_fat'] = Part_Of_MakroNutrient('einfach unges. Fett', 9, 'g', 9, 'fat') 
        self.nutrients['poly_fat'] = Part_Of_MakroNutrient('mehrfach unges. Fett', 10, 'g', 9, 'fat') 
        self.nutrients['cholesterin'] = Nutrient('Cholesterin', 11, 'mg', 0)
        self.nutrients['sugar'] = Part_Of_MakroNutrient('Zucker', 13, 'g', 4, 'carbs')
        self.nutrients['starch'] = Part_Of_MakroNutrient('Stärke', 14, 'g', 4, 'carbs')
        self.nutrients['fibres'] = Nutrient('Ballaststoffe', 15, 'g')

        self.nutrients['salt'] = Nutrient('Salz', 17, 'g', 0)
        self.nutrients['betacarotin'] = Nutrient('Betacarotin', 23, 'ug', 0)
        self.nutrients['vit_b1'] = Nutrient('Vitamin B1', 24, 'mg', 0)
        self.nutrients['vit_b2'] = Nutrient('Vitamin B2', 25, 'mg', 0)
        self.nutrients['vit_b6'] = Nutrient('Vitamin B6', 26, 'mg', 0)
        self.nutrients['vit_b12'] = Nutrient('Vitamin B12', 27, 'ug', 0)
        self.nutrients['niacin'] = Nutrient('Niacin', 28, 'mg', 0)
        self.nutrients['folat'] = Nutrient('Folat', 29, 'ug', 0)
        self.nutrients['pantothenacid'] = Nutrient('Pantotensäure', 30, 'mg', 0)
        self.nutrients['vit_c'] = Nutrient('Vitamin C', 31, 'mg', 0)
        self.nutrients['vit_d'] = Nutrient('Vitmain D', 32, 'ug', 0)
        self.nutrients['calium'] = Nutrient('Kalium', 34, 'mg', 0)
        self.nutrients['natrium'] = Nutrient('Natrium', 35, 'mg', 0)
        self.nutrients['chlorid'] = Nutrient('Chlorid', 36, 'mg', 0)
        self.nutrients['calcium'] = Nutrient('Calzium', 37, 'mg', 0)
        self.nutrients['magnesium'] = Nutrient('Magnesium', 38, 'mg', 0)
        self.nutrients['phosphor'] = Nutrient('Phosphor', 39, 'mg', 0)
        self.nutrients['iron'] = Nutrient('Eisen', 40, 'mg', 0)
        self.nutrients['jod'] = Nutrient('Jod', 41, 'ug', 0)
        self.nutrients['zink'] = Nutrient('Zink', 42, 'mg', 0)
        self.nutrients['selen'] = Nutrient('Selen', 43, 'ug', 0)

        if line_number > 3 or line_number < 1022: #Grenzen Testen! 
            self.get_values_from_DB(line_number)
        else:
            self.get_values_from_DB(1) #leeres Food anlegen (0)

    def __add__(self, other):
        added_Obj = Food(2,0)
        added_Obj.name = 'Added Foods'
        added_Obj.amount = self.amount + other.amount
        for nutrient_key in self.nutrients:
            added_Obj.nutrients[nutrient_key] = self.nutrients[nutrient_key] + other.nutrients[nutrient_key]                                    
            added_Obj.nutrients[nutrient_key].amount = self.nutrients[nutrient_key].amount*self.amount/100 + other.nutrients[nutrient_key].amount*self.amount/100                                    
        return added_Obj
    
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __str__(self):
        heading =  'Nährwerte %s für 100g\n' % (self.name) #todo: unit wäre gut, g für essen oke, aber was ist mit Flüssigkeiten? ml?
        table = ''
        for nutrient in self.nutrients.values():
            table += str(nutrient) + '\n'
        return heading + table
        
    def get_values_from_DB(self, line_number):
        self.name = self.food_db.table[line_number][0]
    
        if len(self.food_db.table[line_number][1])>0:
            self.name += ', ' + self.food_db.table[line_number][1]

        self.category = self.food_db.table[line_number][2]

        for nutrient in self.nutrients.values():
            nutrient.amount = self.food_db.table[line_number][nutrient.column]

    def print_all_nutrients(self):
        print(str(self))

    def print_nutrients(self, additional_nutrients = []):
        if len(additional_nutrients == 0):
            heading = 'Makronährstoffe'
        else:
            heading = 'Nährstoffe'
        heading += str(self.name) + '\n'
        table = ''

        for key in self.basic_keys + additional_nutrients:
            table = table + str(self.nutrients[key]) + '\n'  
        print(heading + table)

    #gehört das hier her? iwie komisch!
    def makros_kreisdiagramm(self):
        #plt.figure(figsize=(1,1))
        plt.clf()
        plt.axis("equal")
        label_dist = 0.3
        pct_dist = 0.8
        colors = {'fat':'red','sat_fat':'firebrick','carbs':'blue','sugar':'dodgerblue','fibres':'darkblue','protein':'green'}
        data = {}
        labels = {}
        
        for key in self.basic_keys[1:]:
            try:
                if self.nutrients[key].get_calories()/self.nutrients['kcal'].amount>=0.01:
                    data[key] = self.nutrients[key].get_calories()
                    labels[key] = self.nutrients[key].name

                    if type(self.nutrients[key]) is Part_Of_MakroNutrient:
                        data[self.nutrients[key].makro_key] -= data[key]

                        if data[self.nutrients[key].makro_key]/self.nutrients['kcal'].amount<0.01:
                            del data[self.nutrients[key].makro_key]
                            del colors[self.nutrients[key].makro_key]
                            del labels[self.nutrients[key].makro_key]

                        elif data[self.nutrients[key].makro_key]/self.nutrients['kcal'].amount<0.1:
                            labels[self.nutrients[key].makro_key] = ''

                    if self.nutrients[key].get_calories()/self.nutrients['kcal'].amount<0.1:
                        labels[key] = ''
                else:
                    del colors[key]
            except:
                del colors[key]
                continue
         
        if not (len(colors) == len(data) and len(colors) == len(labels)):
            print('Error while creating piechart! Länge der Arrays Daten, Beschriftung und Farben passt nicht zusammen!')
            print('Länge Farben: ' + str(len(colors)))
            print('Länge Daten: '  + str(len(data)))
            print('Länge Beschriftung: ' + str(len(labels)))
            #vlt iwann besseres Errorhandling schreiben
            
        plt.pie(list(data.values()), colors=list(colors.values()), labels = labels.values(), labeldistance = label_dist, pctdistance = pct_dist, autopct = "%1.1f%%")
        plt.title(self.name)
        plt.savefig(self.name + '.png')
        #plt.show() #braucht man später nicht mehr


    def naehrstofftabelle(self, mode = 'basic', additional_nutrients = []):
        #ToDo: Bessere Lösungsmöglichkeit für mode finden!

        if mode == 'basic':
            keys = self.basic_keys
        elif mode == 'all':
            keys = self.nutrients.keys()
        elif mode == 'iron':
            keys = self.basic_keys
            keys.append('iron')
        else:
            keys = self.basic_keys

        keys = keys + additional_nutrients
            
        fig, ax = plt.subplots()
        ax.xaxis.set_visible(False) 
        ax.yaxis.set_visible(False)
        table = []
        
        #Tabelle Überschrift: Name, Menge, (%Bedarf?), (%Kcal?) -> deshalb auch unterschiedliche Modi
        for key in keys:
            table.append([self.nutrients[key].name, str(self.nutrients[key].amount) + self.nutrients[key].unit])
        collabel=("Nährstoff", "Menge")
        ax.table(cellText=table,colLabels=collabel, loc='center')

        fig.tight_layout()
        #speichern fehlt noch!
        plt.show()
        
        #TODO: folgende Werte wo anders speichern/lesen:
        kcal_need = 2400
        percentage_fat = 30
        percentage_carbs = 40
        percentage_protein = 30
        


