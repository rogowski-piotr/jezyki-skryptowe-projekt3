from PyQt5.QtWidgets import *
from PyQt5 import QtCore


class AddFileInputPopup(QWidget):
    def __init__(self, path, parent = None):
        # super(AddFileInputPopup, self).__init__(parent)
        # win = QWidget()
        # l1 = QLabel("Name")
        # nm = QLineEdit()
        # l2 = QLabel("Address")
        # add1 = QLineEdit()
        # add2 = QLineEdit()
        # fbox = QFormLayout()
        # fbox.addRow(l1,nm)
        # vbox = QVBoxLayout()
        # vbox.addWidget(add1)
        # vbox.addWidget(add2)
        # fbox.addRow(l2,vbox)
        # hbox = QHBoxLayout()
        # r1 = QRadioButton("Male")
        # r2 = QRadioButton("Female")
        # hbox.addWidget(r1)
        # hbox.addWidget(r2)
        # hbox.addStretch()
        # fbox.addRow(QLabel("sex"),hbox)
        # fbox.addRow(QPushButton("Submit"),QPushButton("Cancel"))
        # self.setLayout(fbox)
        # self.setWindowTitle("Dodawanie pliku")
        # self.show()
        

        # self.translator = QtCore.QTranslator()
        # self.translator.load("qt_pl", QM_FILES[self.config['locale']])
        super(AddFileInputPopup, self).__init__(parent)
        input_box = QInputDialog()
        input_box.setOkButtonText("Dodaj")
        # setCancelButtonText("Anuluj")
        name, _ = input_box.getText(self, 'Dodawanie pliku', 'Wprowadź nazwę pliku:')
        print(name)



def add_file_popup():
    # mbox = QtWidgets.QMessageBox()
    # mbox.setText(path)
    # mbox.setWindowTitle("INFORMACJA")
    # mbox.setDetailedText("The details are as follows:")
    # mbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    # mbox.exec_()
    input_box = QInputDialog() 
    print(input_box.okButtonText() )
    input_box.setOkButtonText("Dodaj")
    input_box.setCancelButtonText("Anuluj")
    name, _ = input_box.getText('Dodawanie pliku', 'Wprowadź nazwę pliku:')
    print(name)


class AddFolderInputPopup(QWidget):
    def __init__(self, path, message):
        super().__init__()
