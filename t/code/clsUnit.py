# selbe Ebene wie food
# -> muss auch auf DB zugreifen
class Amount():
    def __init__(unit,amount)
base = 'g'
val = 1
ka = 5
mass_units = {'g' = 1, 'Portion': val, 'Tasse': val, 'mg' = 1000, 'µg' = 1000000, 'ug' = 1000000, 'dag' = 0.1, 'kg' = 0.001, 'TL' = ka, 'EL' = ka}
liquid_units = {'ml' = 1, 'Portion': val, 'Tasse': val, 'l' = 0.001, 'cl' = 0.1, 'TL' = ka, 'EL' = ka}
# verbessern! für val braucht man die Dichte und/oder Portionsgröße -> muss aus DB ausgelesen werden
# Als Std-Einheit entweder g oder ml wählen - aus Energie, Kilojoule - Spalte auslesen (pro 100g/ml) - intern immer so speichern!
# Sobald der User einmal was anderes auswählt, in DB speichern und zukünftig als Standard wählen
