import sys
from PyQt5.QtWidgets import *


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.setWindowTitle("Eksplorator plików")
        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        browser_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()
        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(browser_layout)
        pagelayout.addLayout(self.stacklayout)

        textbox = QLineEdit(self)
        textbox.move(20, 20)
        textbox.resize(280,40)
        browser_layout.addWidget(textbox)

        button = QPushButton("Przejdź")
        button.move(260, 40)
        button.resize(260, 40)
        browser_layout.addWidget(button)

        btn = QPushButton("Opcja1")
        btn.pressed.connect(self.show_current_weather)
        button_layout.addWidget(btn)
        # self.stacklayout.addWidget(someWidget1)

        btn = QPushButton("Opcja2")
        btn.pressed.connect(self.show_hourly_weather)
        button_layout.addWidget(btn)
        # self.stacklayout.addWidget(someWidget2)

        btn = QPushButton("Opcja3")
        btn.pressed.connect(self.show_city_input)
        button_layout.addWidget(btn)
        # self.stacklayout.addWidget(someWidget3)

        btn = QPushButton("O autorze")
        btn.pressed.connect(self.show_author_info)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(QLabel("Autor: Piotr Rogowski"))

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)


    def show_current_weather(self):
        self.stacklayout.setCurrentIndex(0)
        self.stacklayout.currentWidget().refresh() 

    def show_hourly_weather(self):
        self.stacklayout.setCurrentIndex(1)
        self.stacklayout.currentWidget().refresh()
        self.stacklayout.removeWidget(self.stacklayout.currentWidget())
        # self.stacklayout.addWidget(HourlyWeather())

    def show_city_input(self):
        self.stacklayout.setCurrentIndex(2)
        self.stacklayout.currentWidget().show()

    def show_author_info(self):
        self.stacklayout.setCurrentIndex(3)


def start_app():     
    app = QApplication(sys.argv)
    app.setApplicationName('Eksplorator plików')

    main = MyWindow()
    main.resize(650, 550)
    main.show()

    sys.exit(app.exec_())
