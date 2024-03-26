  
import pandas as pd
import os
import sys

import settings
from window import *
from smart import *



if __name__ == '__main__':
    script_rep = os.getcwd()
    project_rep = os.path.dirname(script_rep)

    commune_file = project_rep+"//pretraitement//data1.csv"
    commune = pd.read_csv(commune_file)
    
    x0 = commune[commune.code_postal == 75013].longitude.iloc[0]
    y0 = commune[commune.code_postal == 75013].latitude.iloc[0]
    
    Map = MyMap([x0, y0], 15, 10)
    
    VAL = VALUES(["population", "nombre_debit", "nombre_festival"])
    
    Brain = TheBrain(commune_file, Map, VAL, 500)
    
    app = QApplication(sys.argv)
    fenetre = MaFenetre(Brain)
    print("ouverture en cours ..")
    fenetre.show()
    print("fenetre ouverte")
    app.exec()
    print("fermeture")
