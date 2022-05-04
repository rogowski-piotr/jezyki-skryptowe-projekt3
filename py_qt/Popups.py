from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from shared.FileSystemService import FileSystemService


# Informacyjne okienko
class InfoBox:
    def __init__(self, msg: str) -> None:
        mbox = QMessageBox()
        mbox.setText(msg)
        mbox.setWindowTitle("INFORMACJA")
        mbox.setStandardButtons(QMessageBox.Ok)
        mbox.exec_()


# Informayjne okienko o błędzie
class ErrorBox:
    def __init__(self, msg: str) -> None:
        mbox = QMessageBox()
        mbox.setText(msg)
        mbox.setWindowTitle("BŁĄD")
        mbox.exec_()


# Okienko do obsługi dodawania nowego pliku
class AddFileInputPopup(QDialog):
    def __init__(self, path):
        super().__init__()
        self.setWindowTitle("Tworzenie pliku")
        self.path = path

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("Potwierdź", QDialogButtonBox.RejectRole)
        self.buttonBox.rejected.connect(self.create_file)
    
        self.layout = QVBoxLayout()
        message = QLabel("Wprowadź nazwę pliku:")
        self.layout.addWidget(message)
        self.input_box = QLineEdit()
        self.layout.addWidget(self.input_box)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    
    def create_file(self):
        service = FileSystemService()
        try:
            service.add_new_file(self.path, self.input_box.text())
        except ValueError as ex:
            from py_qt.Popups import ErrorBox
            args = ex.args
            ErrorBox(f'Nie można wykonać operacji: "{args[0]}".\n\nŚlad błędu:\n"{args[1]}".')
        self.close()


# Okienko do obsługi dodawania nowego katalogu
class AddFolderInputPopup(QDialog):
    def __init__(self, path):
        super().__init__()
        self.setWindowTitle("Tworzenie katalogu")
        self.path = path

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("Potwierdź", QDialogButtonBox.RejectRole)
        self.buttonBox.rejected.connect(self.create_folder)
    
        self.layout = QVBoxLayout()
        message = QLabel("Wprowadź nazwę katalogu:")
        self.layout.addWidget(message)
        self.input_box = QLineEdit()
        self.layout.addWidget(self.input_box)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    
    def create_folder(self):
        service = FileSystemService()
        try:
            service.add_new_dir(self.path, self.input_box.text())
        except ValueError as ex:
            from py_qt.Popups import ErrorBox
            args = ex.args
            ErrorBox(f'Nie można wykonać operacji: "{args[0]}".\n\nŚlad błędu:\n"{args[1]}".')
        self.close()
    

# Okienko do obsługi zmiany nazwy
class ChangeNamePopup(QDialog):
    def __init__(self, path, old_name):
        super().__init__()
        self.setWindowTitle("Zmiana nazwy")
        self.path = path
        self.old_name = old_name

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("Potwierdź", QDialogButtonBox.RejectRole)
        self.buttonBox.rejected.connect(self.change_name)
    
        self.layout = QVBoxLayout()
        message = QLabel("Wprowadź nową nazwę:")
        self.layout.addWidget(message)
        self.input_box = QLineEdit()
        self.layout.addWidget(self.input_box)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    
    def change_name(self):
        service = FileSystemService()
        try:
            service.change_name(self.path, self.old_name, self.input_box.text())
        except ValueError as ex:
            from py_qt.Popups import ErrorBox
            args = ex.args
            ErrorBox(f'Nie można wykonać operacji: "{args[0]}".\n\nŚlad błędu:\n"{args[1]}".')
        self.close()


# Okienko do obsługi usuwania pliku/katalogu
class Delete(QDialog):
    def __init__(self, path, file): 
        super().__init__()
        self.setWindowTitle("Usuwanie pliku")
        self.path = path
        self.file = file

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("Tak", QDialogButtonBox.RejectRole)
        self.buttonBox.rejected.connect(self.delete)
    
        self.layout = QVBoxLayout()
        if file.type == 'd':
            text = f'Czy na pewno chcesz usunąć katalog "{file.name}"?'
        else:
            text = f'Czy na pewno chcesz usunąć plik "{file.name}"?'
        message = QLabel(text)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    
    def delete(self):
        service = FileSystemService()
        try:
            service.delete(self.path, self.file.name, self.file.type)
        except ValueError as ex:
            from py_qt.Popups import ErrorBox
            args = ex.args
            ErrorBox(f'Nie można wykonać operacji: "{args[0]}".\n\nŚlad błędu:\n"{args[1]}".')
            self.close()
            # raise ValueError
        self.close()
