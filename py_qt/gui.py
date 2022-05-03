import sys, os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from py_qt.FilesList import FilesList
from py_qt.Popups import AddFileInputPopup, AddFolderInputPopup, InfoBox


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.load(QtCore.QDir.currentPath())
    
    def load(self, path):
        self.path = path
        self.setWindowTitle("Eksplorator plików")
        self.pagelayout = QVBoxLayout()
        self.browser_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        # Deklaracja menu
        self.menu_bar = QMenuBar()
        self.pagelayout.addWidget(self.menu_bar)

        # Pierwszy przycisk menu - wysuwany
        file = self.menu_bar.addMenu("Plik")
        action_add_file = QAction("Nowy plik", self)
        file.addAction(action_add_file)
        action_add_file.triggered.connect(self.add_file)
        action_add_dir = QAction("Nowy katalog", self)
        file.addAction(action_add_dir)
        action_add_dir.triggered.connect(self.add_dir)

        # Drugi przycisk
        action_about_app = QAction("O aplikacji", self)
        self.menu_bar.addAction(action_about_app)
        action_about_app.triggered.connect(self.about_app)

        # Linia do wprowadzania ścieżki
        self.textbox = QLineEdit(QtCore.QDir.currentPath())
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)
        self.browser_layout.addWidget(self.textbox)
        button = QPushButton("Przejdź")
        button.move(260, 40)
        button.resize(260, 40)
        button.clicked.connect(self.go_to_path)
        self.browser_layout.addWidget(button)

        self.pagelayout.addLayout(self.browser_layout)
        self.stacklayout.addWidget(FilesList(self, path))
        self.pagelayout.addLayout(self.stacklayout)

        widget = QWidget()
        widget.setLayout(self.pagelayout)
        self.setCentralWidget(widget)


    # Obsługa dodawania nowego pliku
    def add_file(self):
        AddFileInputPopup(self.textbox.text()).exec()
        self.stacklayout.currentWidget().update(self, self.textbox.text(), self.path)

    # Obsługa dodawania nowego katalogu
    def add_dir(self):
        AddFolderInputPopup(self.textbox.text()).exec()
        self.stacklayout.currentWidget().update(self, self.textbox.text(), self.path)

    # Obsługa wyświetlania okienka z informacją o aplikacji
    def about_app(self):
        with open(os.path.join(os.getcwd(), 'shared', 'about_app.txt'), 'r') as f:
            text = f.read()
        InfoBox(text)
    
    # Obsługa przycisku "Przejdź"
    def go_to_path(self):
        self.stacklayout.currentWidget().update(self, self.textbox.text(), self.path)
        

def start_app():  
    app = QApplication(sys.argv)
    app.setApplicationName('Eksplorator plików')
    main = MainWindow()
    main.resize(1000, 550)
    main.show()

    sys.exit(app.exec_())
