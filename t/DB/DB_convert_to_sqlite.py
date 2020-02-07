import sqlite3

'''
Hier wird die 'SchweizerDB' in die Datenbank umgeschrieben
Das Skript wird normalerweise lediglich einmal ausgeführt.
'''

with open('SchweizerDB.csv', mode='r') as csv_file: #, encoding='latin-1'
    #handeln falls db nicht im Verzeichnis
    table = [line.split(';') for line in csv_file]

header = 0

for i,line in enumerate(table):
    for j, column in enumerate(line):
        if i == header:
            table[i][j] = column
            continue     
        if j>4:
              try:
                  temp = column.replace(',','.')
                  table[i][j] = float(temp)
              except ValueError as e:
                  table[i][j] = 0

db_connection = sqlite3.connect('Food.db')
cursor = db_connection.cursor()

#gibts mehrere Tables in einer DB? Können diese generell verbunden werden? Ohh my dear, i am in desperate need of a fast db-intro -.-
cursor.execute("DROP TABLE IF EXISTS Food")
cursor.execute('CREATE TABLE Food (id INTEGER PRIMARY KEY, Name TEXT, Kategorie TEXT, Unterkategorie TEXT, \
                Dichte INTEGER, Einheit TEXT, kCal INTEGER, Fett REAL, gesFett REAL, einfachUngesFett REAL, \
                mehrfachUngesFett REAL, Cholesterin INTEGER, Carbs REAL, Zucker REAL, Staerke REAL, Ballaststoffe REAL, \
                Protein REAL);')

for food in table:
    if food[0] == 'Name':
        continue
    
    category = food[1]
    category1 = ''
    category2 = ''
    cut_index = category.find('/')
    if not cut_index == -1:
        category1 = category[:cut_index]
        category2 = category[cut_index+1:].strip()
    else:
        category1 = category

    unit = food[3]
    unit = unit.replace('pro 100','')
    unit = unit.strip()

    cursor.execute('INSERT INTO Food (Name, Kategorie, Unterkategorie, Dichte, Einheit, kCal, Fett, gesFett, \
                    einfachUngesFett, mehrfachUngesFett, Cholesterin, Carbs, Zucker, Staerke, Ballaststoffe, \
                    Protein) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', \
                   (food[0].strip(), category1, category2, food[2], unit, food[5], food[6], food[7], food[8], food[9],\
                    food[10],food[11],food[12],food[13],food[14],food[15]))
    cursor.fetchone()

db_connection.commit()
db_connection.close()


