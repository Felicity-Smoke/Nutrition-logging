import sqlite3
import re
from datetime import date


class Searchterm(object):
    def __init__(self, searchterm, vague_search=False, category=''):
        self.searchterm = searchterm
        self.vague_search = vague_search
        self.category = category

    @property
    def get_nr_of_words(self):
        return len(self.searchterm.split())

    @property
    def get_searchterm(self):
        return self.searchterm

    @property
    def get_list_of_words(self):
        return self.searchterm.split()

    @property
    def is_search_vague_active(self):
        return self.vague_search

    @property
    def get_re(self):
        words = self.get_list_of_words
        reg_exp = ''
        for word in words:
            reg_exp += word+'&'
        return reg_exp[:-1]

    def does_match(self, food_name):
        for term in self.get_list_of_words:
            if not re.findall(term, food_name, re.IGNORECASE):
                return False
        return True


class FoodSearch(object):
    db_label_name = 'Name'
    db_food_table = 'Food'
    db_label_category = 'Kategorie'

    db_connection = sqlite3.connect('Food.db')
    cursor = db_connection.cursor()

    cursor.execute('SELECT Name FROM Food')  # format(name = db_label_name, table = db_label_name))

    all_entries_by_name = []  # ToDo: als member, call o.Ä.
    for entry in cursor.fetchall():
        all_entries_by_name.append(entry[0])
        
    def __init__(self, searchterm_obj):
        cursor = FoodSearch.cursor     
        self.found_food_names = []
        self.all_rows = []

        for food_name in FoodSearch.all_entries_by_name:
            if searchterm_obj.does_match(food_name):
                self.found_food_names.append(food_name)
        
        for found_food_name in self.found_food_names:
            cursor.execute('SELECT Name, Kategorie FROM Food WHERE Name=?', (found_food_name,))
            self.all_rows.append(cursor.fetchone())

            # cursor.execute('SELECT {name}, {category} FROM {food} WHERE Name={searched} LIMIT {limit}'.\
            # format(name = FoodSearch.db_label_name, category = FoodSearch.db_label_category, searched = found_food_name, food = FoodSearch.db_food_table, limit = max_hits_shown))
                
        FoodSearch.db_connection.close()

        # Wird nichts gefunden Fuzzy-Methode anwenden
        if searchterm_obj.is_search_vague_active is True and len(self.found_food_names) < 30:
            self.search_vague(searchterm_obj)

        for row in self.all_rows:
            print(str(row))
            
    def search_basic(self, search_term):
        linenumber = 4
        for foodline in self.food_db.table[(linenumber-1):1020]:
            if re.findall(search_term.lower(), (foodline[0] + foodline[1]).lower()):
                self.hits[linenumber] = foodline
            linenumber = linenumber + 1

    def search_vague(self, search_term):
        print('Ungefähre Suche aktiv')
        for i in enumerate(search_term):
            try:
                self.search_basic(search_term[:i-1] + '.' + search_term[i+1:])
                self.search_basic(search_term[:i] + '.' + search_term[i+1:])
            except:
                continue

    @property
    def get_IDs(self):
        pass

    @property
    def get_names(self):
        return self.found_food_names

    @property
    def get_foods(self):
        pass
        # return self.hits.values()

    @property
    def get_name_and_category(self):
        return self.all_rows
            
# _____MAIN_____

# SUCHE
# searchterm_obj = Searchterm('Apfel')
# tempFood = FoodSearch(searchterm_obj)
