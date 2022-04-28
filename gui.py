import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from FilesList import FilesList
from InputPopup import AddFileInputPopup


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # self.path = QtCore.QDir.currentPath()
        self.load(QtCore.QDir.currentPath())
    
    def load(self, path):

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

    def add_file(self):
        print("adding file")
        path = self.textbox.text()
        AddFileInputPopup(path)
        
    def add_dir(self):
        print("adding folder")

    def about_app(self):
        # popup
        print("about app")
    
    def go_to_path(self):
        print("go to path")
        self.stacklayout.currentWidget().update(self.textbox.text())
        

def start_app():  
    app = QApplication(sys.argv)
    app.setApplicationName('Eksplorator plików')

    translator = QtCore.QTranslator(app)
    translator.load("translate/de_DE.qm")
    app.installTranslator(translator)

    main = MainWindow()
    main.resize(1000, 550)
    main.show()

    sys.exit(app.exec_())
