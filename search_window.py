
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class SearchWindow(QWidget):
    def __init__(self, Brain, update_info_and_fig):
        super().__init__()
        self.Brain = Brain
        self.update_info_and_fig = update_info_and_fig
        self.setWindowTitle('Recherche de commune par code postal')
        self.resize(600, 300)
        self.search_bar = QLineEdit(self) # barre de recherche
        self.search_bar.setPlaceholderText("Entrez le code postal de la commune")

        search_button = QPushButton("Rechercher", self)
        search_button.clicked.connect(self.perform_search)
        self.label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.search_bar)
        layout.addWidget(self.label)
        layout.addWidget(search_button)
        self.setLayout(layout)

    def perform_search(self):
        try:
            code = int(self.search_bar.text())
            try:
                commune_trouve = self.Brain.df[self.Brain.df['code_postal'] == code].iloc[0]
                self.Brain.Map.set_pos( (commune_trouve.longitude, commune_trouve.latitude) )
                self.update_info_and_fig()
                dico = commune_trouve[['nom_commune_postal'] + self.Brain.VAL.L_str].to_dict()
                formatted_dict = json.dumps(dico, indent=4).replace('"', '').replace(',', '').replace('}', '').replace('{', '')
                msg = f"Commune trouvée :\n{formatted_dict}"
            except: # pas de correspondance sur le code postal
                msg = "Aucune commune trouvée"
        except: # l'utilisateur n'a pas mis de int :
            msg = "Ce n'est pas un code postal"
        self.label.setText(msg)

if __name__ == '__main__': 
    pass
