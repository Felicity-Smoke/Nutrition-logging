import sqlite3

'''
Hier wird die 'Days.csv' in die Datenbank umgeschrieben
in Days.csv befinden sich ein paar übungsdatensätz für das spätere Nutrientlogging
Das Skript wird normalerweise lediglich einmal ausgeführt
'''

with open('Days.csv', mode='r') as csv_file: #, encoding='latin-1'
    table = [line.split(';') for line in csv_file]

header = 0

for i,line in enumerate(table):
    for j, cell in enumerate(line):
        if i == header:
            table[i][j] = cell
            continue     
        if not j==3:
            try:
                table[i][j] = float(cell)
            except ValueError as e:
                table[i][j] = 0
                print('ValueError - konnte nicht auf float casten!')
        else:
            table[i][j]=str(cell)

db_connection = sqlite3.connect('Food.db')
cursor = db_connection.cursor()

#gibts mehrere Tables in einer DB? Können diese generell verbunden werden? Ohh my dear, i am in desperate need of a fast db-intro -.-
cursor.execute("DROP TABLE IF EXISTS FoodEntries")
cursor.execute('CREATE TABLE FoodEntries (id INTEGER PRIMARY KEY, Food_ID INTEGER, Menge INTEGER, Datum TEXT, \
                Mahlzeit INTEGER, Gericht Integer);')

for food in table:
    if food[0] == 'ID':
        continue #skip first Header-line

    cursor.execute('INSERT INTO FoodEntries (id, Food_ID, Menge, Datum, Mahlzeit, Gericht) VALUES (?,?,?,?,?,?)', \
                   (food[0], food[1], food[2], food[3], food[4], food[5]))
    cursor.fetchone()

db_connection.commit()
db_connection.close()


