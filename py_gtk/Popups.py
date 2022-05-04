import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from shared.FileSystemService import FileSystemService


# Informacyjne okienko
def info_dialog(self, message):
    dialog = Gtk.MessageDialog(
        transient_for=self, flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text="INFORMACJA",
    )
    dialog.format_secondary_text(message)
    dialog.run()
    dialog.destroy()

# Informayjne okienko o błędzie
def error_dialog(self, message):
    dialog = Gtk.MessageDialog(
        transient_for=self, flags=0,
        message_type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.CANCEL,
        text="BŁĄD",
    )
    dialog.format_secondary_text(message)
    dialog.run()
    dialog.destroy()


# Okienko do obsługi dodawania nowego pliku
class AddFileInputPopup(Gtk.Dialog):
    def __init__(self, main_window, path, parent=None):
        super().__init__(self, parent=parent)
        self.path = path
        self.main_window = main_window

        self.set_title("Tworzenie pliku")
        self.add_button("_Potwierdź", Gtk.ResponseType.OK)
        self.connect("response", self.on_response)
        label = Gtk.Label("Wprowadź nazwę pliku:")
        self.vbox.add(label)
        self.input_box = Gtk.Entry()
        self.vbox.add(self.input_box)
        self.show_all()

    def on_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            service = FileSystemService()
            try:
                service.add_new_file(self.path, self.input_box.get_text())
                self.main_window.refresh_main_window()
            except ValueError as ex:
                args = ex.args
                from py_gtk.Popups import error_dialog
                error_dialog(self.main_window, f'Nie można wykonać operacji:\n{args[0]}.\n\nŚlad błędu:\n"{args[1]}".')
            
        dialog.destroy()


# Okienko do obsługi dodawania nowego katalogu
class AddFolderInputPopup(Gtk.Dialog):
    def __init__(self, main_window, path, parent=None):
        super().__init__(self, parent=parent)
        self.path = path
        self.main_window = main_window

        self.set_title("Tworzenie katalogu")
        self.add_button("_Potwierdź", Gtk.ResponseType.OK)
        self.connect("response", self.on_response)
        label = Gtk.Label("Wprowadź nazwę katalogu:")
        self.vbox.add(label)
        self.input_box = Gtk.Entry()
        self.vbox.add(self.input_box)
        self.show_all()

    def on_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            service = FileSystemService()
            try:
                service.add_new_dir(self.path, self.input_box.get_text())
                self.main_window.refresh_main_window()
            except ValueError as ex:
                args = ex.args
                from py_gtk.Popups import error_dialog
                error_dialog(self.main_window, f'Nie można wykonać operacji:\n{args[0]}.\n\nŚlad błędu:\n"{args[1]}".')
        dialog.destroy()


# Okienko do obsługi zmiany nazwy
class ChangeNamePopup(Gtk.Dialog):
    def __init__(self, main_window, path, old_name, parent=None):
        super().__init__(self, parent=parent)
        self.path = path
        self.main_window = main_window
        self.old_name = old_name

        self.set_title("Zmiana nazwy")
        self.add_button("_Potwierdź", Gtk.ResponseType.OK)
        self.connect("response", self.on_response)
        label = Gtk.Label("Wprowadź nową nazwę:")
        self.vbox.add(label)
        self.input_box = Gtk.Entry()
        self.vbox.add(self.input_box)
        self.show_all()

    def on_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            service = FileSystemService()
            try:
                service.change_name(self.path, self.old_name, self.input_box.get_text())
                self.main_window.refresh_main_window()
            except ValueError as ex:
                args = ex.args
                from py_gtk.Popups import error_dialog
                error_dialog(self.main_window, f'Nie można wykonać operacji:\n{args[0]}.\n\nŚlad błędu:\n"{args[1]}".')
        dialog.destroy()


# Okienko do obsługi usuwania pliku/katalogu
class DeletePopup(Gtk.Dialog):
    def __init__(self, main_window, path, file, parent=None):
        super().__init__(self, parent=parent)
        self.path = path
        self.main_window = main_window
        self.file = file

        self.set_title("Usuwanie pliku")
        self.add_button("_Nie", Gtk.ResponseType.CANCEL)
        self.add_button("_Tak", Gtk.ResponseType.OK)
        self.connect("response", self.on_response)
        if file.type == 'd':
            text = f'Czy na pewno chcesz usunąć katalog "{file.name}"?'
        else:
            text = f'Czy na pewno chcesz usunąć plik "{file.name}"?'
        label = Gtk.Label(text)
        self.vbox.add(label)
        self.show_all()

    def on_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            service = FileSystemService()
            try:
                service.delete(self.path, self.file.name, self.file.type)
                self.main_window.refresh_main_window()
            except ValueError as ex:
                args = ex.args
                from py_gtk.Popups import error_dialog
                error_dialog(self.main_window, f'Nie można wykonać operacji:\n{args[0]}.\n\nŚlad błędu:\n"{args[1]}".')
        dialog.destroy()
