import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from shared.FileSystemService import FileSystemService
from shared.FileSystemElement import File


class FilesList(Gtk.Widget):
    def __init__(self, parent_window, path):
        super().__init__()
        # self.grid = Gtk.Grid()
        self.parent = parent_window

        service = FileSystemService()
        service.goto_path(path)
        files = service.list_files()
        
        self.sw = Gtk.ScrolledWindow()
        table = Gtk.Table(8, len(files))
        table.set_row_spacings(10)
        table.set_col_spacings(10)

        # Nagłówek tabeli
        table.attach(FilesListHeader().hbox, 0, 1, 0, 1)

        # Zawartość tabeli
        for i in range(1, len(files)+1):
            table.attach(FilesListRow(files[i-1], path).hbox, 0, 1, i, i+1)
            
        self.sw.add_with_viewport(table)
        self.sw.set_propagate_natural_height(True)
        self.sw.set_propagate_natural_width(True)
        # self.sw.set_hadjustment()
        # self.sw.set_vadjustment()


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

class FilesListRow(Gtk.Widget):
    def __init__(self, file, path):
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
            FilesListRow.combobox_on_change(self.combo, path, file))
        self.hbox.pack_start(self.combo, 1, 1, 0)
    
    @staticmethod
    def combobox_on_change(combobox, path, file: File):
        treeiter = combobox.get_active_iter()
        model = combobox.get_model()
        id = model[treeiter][0] - 1

        if id == 0:         # "Zmień nazwę"
            print(f"Changing name for {path}/{file.name}")
            # ChangeNamePopup(path, file.name).exec()
            # main_window.stacklayout.currentWidget().update(path)
        elif id == 1:       # "Usuń"
            print(f"Deleting {path}/{file.name}")

            # Delete(path, file).exec()
            # main_window.stacklayout.currentWidget().update(path)
        # elif id == 2:       # "Przejdź" (tylko w katalogach)
        #     if file.name == '.':
        #         main_window.stacklayout.currentWidget().update(path)
        #         main_window.textbox.setText(path)
        #     elif file.name == '..':
                # Ręczne usunięcie, aby nie było dodawanych ".." w ścieżce
                # main_window.stacklayout.currentWidget().update(path[0:path.rfind('/')])
                # main_window.textbox.setText(path[0:path.rfind('/')])
            # else:
            #     main_window.stacklayout.currentWidget().update(f'{path}/{file.name}')
            #     main_window.textbox.setText(f'{path}/{file.name}')
