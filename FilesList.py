from PyQt5 import QtWidgets
from FileSystemService import FileSystemService
from files_list_row import FilesListRow, FilesListHeader


class FilesList(QtWidgets.QWidget):
    def __init__(self, main_window, path):
        super().__init__()
        self.main_window = main_window
        print(f"path = {path}")
        mygroupbox = QtWidgets.QGroupBox(path)
        self.myform = QtWidgets.QFormLayout()

        service = FileSystemService()
        service.goto_path(path)
        files = service.list_files()

        # Table headers and content
        self.myform.addRow(FilesListHeader(self.main_window).table_header)
        for file in files:
            self.myform.addRow(FilesListRow(self.main_window, file, path).box)
        
        mygroupbox.setLayout(self.myform)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        # self.deleteLater()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(scroll)

    def load(self, path):
        print(f"path = {path}")
        self.counter += 1
        mygroupbox = QtWidgets.QGroupBox(path)
        self.myform = QtWidgets.QFormLayout()

        service = FileSystemService()
        service.goto_path(path)
        files = service.list_files()

        # Table headers and content
        self.myform.addRow(FilesListHeader(self.main_window).table_header) 
        for file in files:
            self.myform.addRow(FilesListRow(self.main_window, file, path).box)
        
        mygroupbox.setLayout(self.myform)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        self.layout.removeItem(self.layout.itemAt(0))
        self.layout.addWidget(scroll)


    def update(self, path):
        print(f'updating {path}')
        self.load(path)
