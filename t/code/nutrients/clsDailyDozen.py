class Single_DailyDozen(object):
    def __init__(self, amount, needed_amount, category_keys, name_keys = []):
        self.amount = amount
        self.needed_amount = needed_amount
        self.category_keys = category_keys
        self.name_keys = name_keys

    def __add__(self, other):
        total_amount = self.amount + other.amount()
        return Single_DailyDozen(total_amount,self.needed_amount, self.category_keys, self.name_keys)

    def __radd__(self,other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

class DailyDozen(object):
    def __init__(self):
        self.dozen = {}

        self.dozen['Beeren'] = Single_DailyDozen(0, 150, ['früchte','beeren'],['beere'])
        self.dozen['anderes Obst'] = Single_DailyDozen(0, 300, ['früchte'],[] )
        self.dozen['Kreuzblütler'] = Single_DailyDozen(0, 300, ['gemüse'],['brokkoli','rucola','rukola','kohl','radieschen','kresse'] )
        self.dozen['grünes Blattgemüse'] = Single_DailyDozen(0, 200, ['gemüse'],['kohl','rüben','spinat','mangold'])
        self.dozen['anderes Gemüse'] = Single_DailyDozen(0, 200, ['gemüse'],[] )
        self.dozen['Hülsenfrüchte'] = Single_DailyDozen(0, 300, ['hülsenfrüchte'],['erbse','bohne','soja','linse','tempeh','edamame','hülsenfrüchte'])
        self.dozen['Vollkornprodukte'] = Single_DailyDozen(0, 300, ['getreide','vollkorn','brot','flocken'],[]) # [] korrekt hier?
        self.dozen['Leinsamen'] = Single_DailyDozen(0, 50, ['nüsse','samen'],['leinsamen'])     
        self.dozen['Nüsse'] = Single_DailyDozen(0, 50, ['nüsse','samen'],[])
        self.dozen['Gewürze'] = Single_DailyDozen(0, 10, ['gewürz','kräuter'],[])

    def add(self, food):
        #Code sieht kacke aus - vlt refactern 
        possible_keys = []
        for key, single_dozen in self.dozen.items(): #braucht man keys wirklich?
            for cat_key in single_dozen.category_keys:
                if cat_key in food.category.lower(): # or cat_key in food.name: #braucht man das auch? (theoretisch nein
                    if len(single_dozen.name_keys) == 0:
                        single_dozen.amount = single_dozen.amount + food.amount
                        break
                    else:
                        for name_key in single_dozen.name_keys:
                            if name_key in food.name.lower():
                                single_dozen.amount = single_dozen.amount + food.amount
                                break
        
    def __add__(self, other):
        ret_obj = DailyDozen()
        for key in self.dozen.keys():
            ret_obj.dozen[key] = self.dozen[key] + other.dozen[key]    
        return ret_obj

    def __radd__(self,other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __str__(self):
        heading =  'Tägliches Dutzend: \n'
        table = ''
        for key in self.dozen.keys():
            amount = self.dozen[key].amount
            need = self.dozen[key].needed_amount
            
            table = table + key + ':' + ' '*(23-len(key)) + '%ig/%ig (%i%%) \n' % (amount, need, amount*100/need)    
        return heading + table



