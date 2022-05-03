import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from shared.FileSystemService import FileSystemService
from shared.FileSystemElement import File
from py_gtk.Popups import ChangeNamePopup, DeletePopup, error_dialog


class FilesList(Gtk.Widget):
    def __init__(self, parent_window, path):
        super().__init__()
        self.parent_window = parent_window
        self.path = 'init_path'
        self.load(path)
    
    def load(self, path):
        # Pobranie listy wszystkich plików w danym katalogu
        self.return_code = 0
        service = FileSystemService()
        if service.goto_path(path) == -1:
            error_dialog(self.parent_window, "BŁĄÐ elo")
            self.return_code = -1
        else:
            self.path = path

        files = service.list_files()
        
        # Ustawienia tabelki z zawartością katalogu
        self.sw = Gtk.ScrolledWindow()
        self.table = Gtk.Table(8, len(files))
        self.table.set_row_spacings(10)
        self.table.set_col_spacings(10)

        # Nagłówek tabeli
        self.table.attach(FilesListHeader().hbox, 0, 1, 0, 1)

        # Zawartość tabeli
        for i in range(1, len(files)+1):
            self.table.attach(FilesListRow(self.parent_window, files[i-1], self.path).hbox, 0, 1, i, i+1)
        
        self.sw.add_with_viewport(self.table)
        self.sw.set_propagate_natural_height(True)
        self.sw.set_propagate_natural_width(True)

    # Odświeżanie głównego widoku aplikacji
    def update(self, new_path):
        self.load(new_path)


# Klasa reprezentująca wiersz w widoku danego katalogu
class FilesListRow(Gtk.Widget):
    def __init__(self, parent_window, file, path):
        self.parent_window = parent_window
        self.hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
        label = Gtk.Label(file.name)
        label.set_max_width_chars(20)
        self.hbox.pack_start(label, 1, 1, 0)
        self.hbox.pack_start(Gtk.Label(file.type), 1, 1, 0)
        self.hbox.pack_start(Gtk.Label(file.permissions), 1, 1, 0)
        self.hbox.pack_start(Gtk.Label(file.group), 1, 1, 0)
        self.hbox.pack_start(Gtk.Label(file.owner), 1, 1, 0)
        self.hbox.pack_start(Gtk.Label(file.date), 1, 1, 0)
        self.hbox.pack_start(Gtk.Label(file.size), 1, 1, 0)
        self.hbox.pack_start(Gtk.Label(file.permissions), 1, 1, 0)

        options = Gtk.ListStore(int,str)
        options.append([1,"Zmień nazwę"])
        options.append([2,"Usuń"])
        if file.type == 'd':
            options.append([3,"Przejdź"])
        self.combo = Gtk.ComboBox.new_with_model_and_entry(options)
        self.combo.set_entry_text_column(1)
        self.combo.connect('changed', lambda combobox : 
            self.combobox_on_change(self.combo, path, file))
        self.hbox.pack_start(self.combo, 1, 1, 0)
    
    def combobox_on_change(self, combobox, path, file: File):
        treeiter = combobox.get_active_iter()
        model = combobox.get_model()
        id = model[treeiter][0] - 1

        if id == 0:         # "Zmień nazwę"
            print(f"Changing name for {path}/{file.name}")
            ChangeNamePopup(self.parent_window, path, file.name)
            self.parent_window.refresh_main_window()
            
        elif id == 1:       # "Usuń"
            print(f"Deleting {path}/{file.name}")
            DeletePopup(self.parent_window, path, file)
            self.parent_window.refresh_main_window()
            
        elif id == 2:       # "Przejdź" (tylko w katalogach)
            if file.name == '.':
                self.parent_window.refresh_main_window()
                self.parent_window.textbox.set_text(path)
            elif file.name == '..':
                # Ręczne usunięcie, aby nie było dodawanych ".." w ścieżce
                new_path = path[0:path.rfind('/')]
                self.parent_window.path = new_path
                self.parent_window.textbox.set_text(new_path)
                self.parent_window.refresh_main_window()   
            else:
                self.parent_window.textbox.set_text(f'{path}/{file.name}')
                self.parent_window.refresh_main_window()   


# Klasa reprezentująca wiersz/nagłówek tabelki z widokiem danego katalogu 
class FilesListHeader(Gtk.Widget):
    def __init__(self):
        self.hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
        self.hbox.pack_start(Gtk.Label('Nazwa'), 1, 1, 0)
        self.hbox.pack_start(Gtk.Label('Typ'), 1, 1, 0)
        self.hbox.pack_start(Gtk.Label('Uprawienia'), 1, 1, 0)
        self.hbox.pack_start(Gtk.Label('Grupa'), 1, 1, 0)
        self.hbox.pack_start(Gtk.Label('Właściciel'), 1, 1, 0)
        self.hbox.pack_start(Gtk.Label('Data'), 1, 1, 0)
        self.hbox.pack_start(Gtk.Label('Rozmiar'), 1, 1, 0)
        self.hbox.pack_start(Gtk.Label('Opcje'), 1, 1, 0)
