#from clsDBHandling import DBHandling
'''
short weg bringen, vollständige Food klasse daraus machen!
'''
class ShortFoodEntry(object):
    def __init__(self, key, amount):
        self._key = key
        self._amount = amount

        #db_handling=DBHandling
        #db_handling.add_data_from_db(db_handling,self)

    @property
    def name(self):
        return self._name
    @property
    def category(self):
        return self._category
    @property
    def kCal(self):
        return self._kCal_per_100*self.amount/100
    @property
    def kCal_per_100(self):
        return self._kCal_per_100

    
    @property
    def key(self):
        return self._key
    @property
    def amount(self):
        return self._amount
