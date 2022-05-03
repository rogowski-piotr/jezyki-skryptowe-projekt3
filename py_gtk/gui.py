import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import os
from py_gtk.FilesList import FilesList
from py_gtk.Popups import info_dialog, AddFileInputPopup, AddFolderInputPopup
from gi.repository import Pango as pango

  
class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title ="Eksplorator plików")
        self.load(os.getcwd())

    def load(self, path):
        self.path = path
        self.set_border_width(10)
  
        # Przechowywanie układu widoku aplikacji
        self.vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        self.add(self.vbox)

        # Menu
        mb = Gtk.MenuBar()

        # Pierwszy przycisk menu - wysuwany
        menu1 = Gtk.Menu()
        weather = Gtk.MenuItem("Plik")
        weather.set_submenu(menu1)
        current_weather_menu = Gtk.MenuItem("Nowy plik")
        current_weather_menu.connect("activate", self.add_file)
        menu1.append(current_weather_menu)
        sep = Gtk.SeparatorMenuItem()
        menu1.append(sep)
        hourly_weather = Gtk.MenuItem("Nowy katalog")
        hourly_weather.connect("activate", self.add_dir)
        menu1.append(hourly_weather)

        # Drugi przycisk menu
        about_app = Gtk.MenuItem("O aplikacji")
        about_app.connect("activate", self.about_app)

        # Dodanie przycisków do menu
        mb.append(weather)
        mb.append(about_app)
        self.vbox.pack_start(mb, False, False, 0)

        # Dodanie paska ze ścieżką
        self.hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
        self.textbox = Gtk.Entry()
        self.textbox.set_text(os.getcwd())
        self.go_button = Gtk.Button(label="Przejdź")
        self.go_button.connect("clicked", self.go_to_path) #, self.files_list)
        self.hbox.pack_start(self.textbox, True, True, 0)
        self.hbox.pack_start(self.go_button, True, True, 0)
        self.vbox.pack_start(self.hbox, True, False, 0)

        # Dodanie głównego widoku aplikacji
        self.label = Gtk.Label(self.path)
        self.label.set_ellipsize(pango.EllipsizeMode.END)
        self.label.set_alignment(0,0)
        self.main_content_vbox = Gtk.VBox(False, 0)
        self.vbox.pack_end(self.main_content_vbox, True, False, 0)
        self.main_content_vbox.pack_start(self.label, False, True, 1)
        self.sw = FilesList(self, path).sw
        self.main_content_vbox.pack_start(self.sw, False, True, 1)


    # Obsługa dodawania nowego pliku
    def add_file(self, _):
        AddFileInputPopup(self, self.textbox.get_text()).show()

    # Obsługa dodawania nowego katalogu
    def add_dir(self, _):
        AddFolderInputPopup(self, self.textbox.get_text()).show()
    
    # Obsługa wyświetlania okienka z informacją o aplikacji
    def about_app(self, _):
        with open(os.path.join(os.getcwd(), 'shared', 'about_app.txt'), 'r') as f:
            text = f.read()
        info_dialog(text)
    
    # Obsługa przejścia do innej ścieżki
    def go_to_path(self, _):
        self.refresh_main_window()
        
    def refresh_main_window(self):
        new_content = FilesList(self, self.textbox.get_text())
        if new_content.return_code == 0:
            self.label.set_text(self.textbox.get_text())
            self.main_content_vbox.remove(self.sw)
            self.sw = new_content.sw
            self.main_content_vbox.pack_start(self.sw, False, True, 1)
            self.show_all()
            self.path = self.textbox.get_text()
        else:
            self.textbox.set_text(self.path)

def start_app():
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.set_default_size(650, 550)
    win.show_all()
    Gtk.main()
