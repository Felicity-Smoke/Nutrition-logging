'''
short weg bringen, vollständige Food klasse daraus machen!
'''
class ShortFoodEntry(object):
    def __init__(self, key, amount):
        self._key = key
        self._amount = amount
        self._name=''
        self._category=''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        if type(value) is str:
            self._name=value
            
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self,value):
        #todo: if value in CATEGORIES:
        self._category=value
        
    @property
    def kCal(self):
        return self._kCal_per_100*self.amount/100
            
    @property
    def kCal_per_100(self):
        return self._kCal_per_100

    @kCal_per_100.setter
    def kCal_per_100(self,value):
        if type(value) is int or type(value) is float:
            self._kCal_per_100 = value
    
    @property
    def key(self):
        return self._key
    @property
    def amount(self):
        return self._amount
