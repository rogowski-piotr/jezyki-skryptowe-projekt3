from PyQt5 import QtWidgets


class FilesListRow(QtWidgets.QWidget):
    def __init__(self, main_window, file, path):
        super().__init__()
        self.file = file
        self.box = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(self.file.name)
        label.setToolTip(self.file.name)
        label.setStyleSheet('padding-right:10px')
        # label.setGeometry(0, 0, main_window.frameGeometry().width()*0.15, 0)
        # label.setMinimumWidth(50)
        label.setFixedWidth(100)        
        # label.setGeometry(0, 0, main_window.frameGeometry().width()*0.15, 0)
        # label.setFixedWidth(main_window.frameGeometry().width()*0.15)
        self.box.addWidget(label)

        label = QtWidgets.QLabel(self.file.type)
        label.setStyleSheet('padding-right:10px')
        label.setGeometry(0, 0, main_window.frameGeometry().width()*0.1, 0)
        self.box.addWidget(label)

        label = QtWidgets.QLabel(self.file.permissions)
        label.setStyleSheet('padding-right:10px')
        label.setGeometry(0, 0, main_window.frameGeometry().width()*0.15, 0)
        self.box.addWidget(label)

        label = QtWidgets.QLabel(self.file.group)
        label.setStyleSheet('padding-right:10px')
        label.setGeometry(0, 0, main_window.frameGeometry().width()*0.1, 0)
        self.box.addWidget(label)

        label = QtWidgets.QLabel(self.file.owner)
        label.setStyleSheet('padding-right:10px')
        label.setGeometry(0, 0, main_window.frameGeometry().width()*0.15, 0)
        self.box.addWidget(label)

        label = QtWidgets.QLabel(self.file.date)
        label.setStyleSheet('padding-right:10px')
        label.setGeometry(0, 0, main_window.frameGeometry().width()*0.1, 0)
        self.box.addWidget(label)

        self.combo = QtWidgets.QComboBox()
        self.combo.addItem('Zmień nazwę')
        self.combo.addItem('Usuń')
        self.combo.setStyleSheet('padding-right:10px')
        self.combo.setGeometry(0, 0, main_window.frameGeometry().width()*0.15, 0)
        self.combo.activated[str].connect(lambda: FilesListRow.combo_on_click(self.combo.currentText(), self.combo.currentIndex(), file, path))
        self.box.addWidget(self.combo)
        
    @staticmethod
    def combo_on_click(name, id, file, path):
        print(f"Clicked [{id}] {name} for file {path}/{file.name}")


class FilesListHeader(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.table_header = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('Nazwa')
        label.setFixedWidth(100)        
        # label.setGeometry(0, 0, main_window.frameGeometry().width()*0.15, 0)
        # label.setMinimumWidth(main_window.frameGeometry().width()*0.15)
        self.table_header.addWidget(label)
        label = QtWidgets.QLabel('Typ')
        label.setGeometry(0, 0, main_window.frameGeometry().width()*0.1, 0)
        self.table_header.addWidget(label)
        label = QtWidgets.QLabel('Uprawienia')
        label.setGeometry(0, 0, main_window.frameGeometry().width()*0.15, 0)
        self.table_header.addWidget(label)
        label = QtWidgets.QLabel('Grupa')
        label.setGeometry(0, 0, main_window.frameGeometry().width()*0.1, 0)
        self.table_header.addWidget(label)
        label = QtWidgets.QLabel('Właściciel')
        label.setGeometry(0, 0, main_window.frameGeometry().width()*0.15, 0)
        self.table_header.addWidget(label)
        label = QtWidgets.QLabel('Data')
        label.setGeometry(0, 0, main_window.frameGeometry().width()*0.1, 0)
        self.table_header.addWidget(label)
        label = QtWidgets.QLabel('Opcje')
        label.setGeometry(0, 0, main_window.frameGeometry().width()*0.15, 0)
        self.table_header.addWidget(label)
