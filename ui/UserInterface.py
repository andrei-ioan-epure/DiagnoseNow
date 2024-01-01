from PySide6.QtCore import QFile, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QListWidget, QPushButton, QLabel, QListWidgetItem

from DempsterShafer import DempsterShafer
from constants.Constants import REGULI, IPOTEZE, DENUMIRI
from exception.ui.UserInterfaceException import UserInterfaceException


class UserInterface(QApplication):
    def __init__(self, args, ui_file_name) -> None:
        super().__init__(args)

        ui_file = QFile(ui_file_name)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        if not self.window:
            raise UserInterfaceException(f"Could not load window {loader.errorString()}")

        self.list_symptoms = self.window.findChild(QListWidget, 'listSymptoms')
        self.list_diseases = self.window.findChild(QListWidget, 'listDiseases')
        self.calculate_button = self.window.findChild(QPushButton, 'calculateButton')
        self.result_label = self.window.findChild(QLabel, 'resultLabel')
        self.result_label.setWordWrap(True)

        self.calculate_button.clicked.connect(self.calculate_result)


    def start(self):

        symptoms = ["Febra", "Greturi", "Tuse", "Dureri de cap"]
        diseases = ["Nimic", "Gripa", "Raceala", "COVID-19", "Meningita"]

        for symptom in symptoms:
            item = QListWidgetItem(symptom)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.list_symptoms.addItem(item)

        for disease in diseases:
            item = QListWidgetItem(disease)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.list_diseases.addItem(item)

        self.window.show()
        return self.exec()

    def calculate_result(self):

        checked_symptoms = [item.text() for item in self.list_symptoms.findItems("", Qt.MatchContains) if
                            item.checkState() == Qt.Checked]
        checked_diseases = [item.text() for item in self.list_diseases.findItems("", Qt.MatchContains) if
                            item.checkState() == Qt.Checked]

        print("Checked symptoms:", checked_symptoms)
        print("Checked diseases:", checked_diseases)

        if not checked_diseases and not checked_symptoms:
            self.result_label.setText("Nimic de procesat !")
        else:
            if not checked_symptoms:
                self.result_label.setText("Selectati simptome !")
            else:
                dempsterShafer = DempsterShafer()

                SELECTED_RULES = {symptom: REGULI[symptom] for symptom in checked_symptoms if symptom in REGULI}

                print("Reguli:")
                dempsterShafer.add_missing_rules(IPOTEZE, SELECTED_RULES)
                print(SELECTED_RULES)

                print("Intersect:")
                intersection = dempsterShafer.intersect(SELECTED_RULES)
                print(intersection)

                print("Numitor:")
                numitor = dempsterShafer.denominator(intersection)
                print(numitor)

                print("BBA:")
                bba = dempsterShafer.BBA(intersection, numitor)
                print(bba)

                print("Bel:")
                Bel = dempsterShafer.belief(bba)
                print(Bel)

                print("Prob")
                Pl = dempsterShafer.plauzibilitatea(Bel)
                print(Pl)

                print("Rezultat:")
                result = ""
                for key, value in Bel.items():
                    denumire = ' sau '.join([DENUMIRI[elem] for elem in key])
                    print(f'Posibilitatea de {denumire} : [{Bel[key]},{Pl[key]}]')
                    if not checked_diseases:
                        result = result + f'Posibilitatea de {denumire} : [{round(Bel[key], 2)},{round(Pl[key], 2)}]\n'
                    else:
                        if any(DENUMIRI[elem].capitalize() in checked_diseases for elem in key):
                            result = result + f'Posibilitatea de {denumire} : [{round(Bel[key]*100, 2)},{round(Pl[key]*100, 2)}]\n'

                self.result_label.setText(result)
