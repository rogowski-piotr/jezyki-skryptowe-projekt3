from PyQt5 import QtWidgets
from shared.FileSystemService import FileSystemService
from py_qt.Popups import ChangeNamePopup, Delete


class FilesList(QtWidgets.QWidget):
    def __init__(self, main_window, path):
        super().__init__()
        self.main_window = main_window
        self.init_ui(path)
        # Dodanie widoku do okna (po raz pierwszy)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.scroll)

    def load(self, path):
        # Update widoku (nowa ścieżka)
        self.init_ui(path)
        # Usunięcie poprzedniego widoku i dodanie nowego
        self.layout.removeItem(self.layout.itemAt(0))
        self.layout.addWidget(self.scroll)
    
    # Układ elementów w oknie
    def init_ui(self, path):
        self.path = path
        mygroupbox = QtWidgets.QGroupBox(path)
        self.myform = QtWidgets.QFormLayout()

        service = FileSystemService()
        service.goto_path(path)
        files = service.list_files()

        # Widok zawartości ścieżki w formie tabelki z labelkami i comboboxem
        self.myform.addRow(FilesListHeader(self.main_window).table_header)
        for file in files:
            self.myform.addRow(FilesListRow(self.main_window, file, path).box)
        
        mygroupbox.setLayout(self.myform)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(mygroupbox)
        self.scroll.setWidgetResizable(True)

    def update(self, path):
        self.load(path)


# Klasa reprezentująca wiersz w widoku danego katalogu
class FilesListRow(QtWidgets.QWidget):
    def __init__(self, main_window, file, path):
        super().__init__()
        self.main_window = main_window
        self.file = file
        self.box = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(self.file.name)
        label.setToolTip(self.file.name)
        label.setGeometry(0, 0, int(main_window.frameGeometry().width()*0.4), 0)
        label.setMinimumWidth(int(main_window.frameGeometry().width()*0.4))
        self.box.addWidget(label)

        label = QtWidgets.QLabel(self.file.type)
        label.setStyleSheet('padding-right:10px')
        label.setGeometry(0, 0, int(main_window.frameGeometry().width()*0.05), 0)
        self.box.addWidget(label)

        label = QtWidgets.QLabel(self.file.permissions)
        label.setStyleSheet('padding-right:10px')
        label.setGeometry(0, 0, int(main_window.frameGeometry().width()*0.15), 0)
        self.box.addWidget(label)

        label = QtWidgets.QLabel(self.file.group)
        label.setStyleSheet('padding-right:10px')
        label.setGeometry(0, 0, int(main_window.frameGeometry().width()*0.1), 0)
        self.box.addWidget(label)

        label = QtWidgets.QLabel(self.file.owner)
        label.setStyleSheet('padding-right:10px')
        label.setGeometry(0, 0, int(main_window.frameGeometry().width()*0.15), 0)
        self.box.addWidget(label)

        label = QtWidgets.QLabel(self.file.date)
        label.setStyleSheet('padding-right:10px')
        label.setGeometry(0, 0, int(main_window.frameGeometry().width()*0.1), 0)
        self.box.addWidget(label)

        self.combo = QtWidgets.QComboBox()
        self.combo.addItem('Zmień nazwę')
        self.combo.addItem('Usuń')
        if file.type == 'd':
            self.combo.addItem('Przejdź')
        self.combo.setStyleSheet('padding-right:10px')
        self.combo.setCurrentIndex(-1)
        self.combo.setGeometry(0, 0, int(main_window.frameGeometry().width()*0.15), 0)
        self.combo.activated[str].connect(lambda: FilesListRow.combo_on_click( \
            self.main_window, self.combo.currentText(), self.combo.currentIndex(), file, path))
        self.box.addWidget(self.combo)
        
    @staticmethod
    def combo_on_click(main_window, name, id, file, path):
        if id == 0:         # "Zmień nazwę"
            ChangeNamePopup(path, file.name).exec()
            main_window.stacklayout.currentWidget().update(path)
        elif id == 1:       # "Usuń"
            Delete(path, file).exec()
            main_window.stacklayout.currentWidget().update(path)
        elif id == 2:       # "Przejdź" (tylko w katalogach)
            if file.name == '.':
                main_window.stacklayout.currentWidget().update(path)
                main_window.textbox.setText(path)
            elif file.name == '..':
                # Ręczne usunięcie, aby nie było dodawanych ".." w ścieżce
                main_window.stacklayout.currentWidget().update(path[0:path.rfind('/')])
                main_window.textbox.setText(path[0:path.rfind('/')])
            else:
                main_window.stacklayout.currentWidget().update(f'{path}/{file.name}')
                main_window.textbox.setText(f'{path}/{file.name}')

      
# Klasa reprezentująca wiersz/nagłówek tabelki z widokiem danego katalogu 
class FilesListHeader(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.table_header = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('Nazwa')
        label.setGeometry(0, 0, int(main_window.frameGeometry().width()*0.4), 0)
        label.setMinimumWidth(int(main_window.frameGeometry().width()*0.4))
        self.table_header.addWidget(label)

        label = QtWidgets.QLabel('Typ')
        label.setGeometry(0, 0, int(main_window.frameGeometry().width()*0.05), 0)
        self.table_header.addWidget(label)

        label = QtWidgets.QLabel('Uprawienia')
        label.setGeometry(0, 0, int(main_window.frameGeometry().width()*0.15), 0)
        self.table_header.addWidget(label)

        label = QtWidgets.QLabel('Grupa')
        label.setGeometry(0, 0, int(main_window.frameGeometry().width()*0.1), 0)
        self.table_header.addWidget(label)

        label = QtWidgets.QLabel('Właściciel')
        label.setGeometry(0, 0, int(main_window.frameGeometry().width()*0.15), 0)
        self.table_header.addWidget(label)

        label = QtWidgets.QLabel('Data')
        label.setGeometry(0, 0, int(main_window.frameGeometry().width()*0.1), 0)
        self.table_header.addWidget(label)

        label = QtWidgets.QLabel('Opcje')
        label.setGeometry(0, 0, int(main_window.frameGeometry().width()*0.15), 0)
        self.table_header.addWidget(label)
