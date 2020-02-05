class DB(object):
    """description of class"""

    #allgemeiner gestalten, sodass es auch für andere DBs passend ist
    def __init__(self, db_name):
        with open(db_name, mode='r', encoding='latin-1') as csv_file:
            #handeln falls db nicht im Verzeichnis
            self.table = [line.split(';') for line in csv_file]

        for i,line in enumerate(self.table):
            for j, column in enumerate(line):
                if j>5:
                      try:
                          temp = column.replace(',','.')
                          self.table[i][j] = float(temp)
                      except ValueError as e:
                          self.table[i][j] = 0


