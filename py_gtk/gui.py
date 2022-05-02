import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import os
from py_gtk.FilesList import FilesList

  
class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title ="Eksplorator plików")
        self.load(os.getcwd())

    def load(self, path):
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
        hourly_weather = Gtk.MenuItem("Nowy folder")
        hourly_weather.connect("activate", self.add_dir)
        menu1.append(hourly_weather)

        # Drugi przycisk menu
        about_app = Gtk.MenuItem("O aplikacji")
        about_app.connect("activate", self.about_app)

        # Dodanie przycisków do menu
        mb.append(weather)
        mb.append(about_app)
        self.vbox.pack_start(mb, False, False, 0)

        self.hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
        self.textbox = Gtk.Entry()
        self.textbox.set_text(os.getcwd())
        self.go_button = Gtk.Button(label="Przejdź")
        self.go_button.connect("clicked", self.go_to_path)
        self.hbox.pack_start(self.textbox, True, True, 0)
        self.hbox.pack_start(self.go_button, True, True, 0)
        self.vbox.pack_start(self.hbox, True, False, 0)

        # # DOdanie wszystkich widoków aplikacji
        self.stack = Gtk.Stack()
        self.stack.add_named(FilesList(self, path).sw, "files_list")
  
        # Ustawienie przełączania pomiędzy widokami aplikacji
        self.stack_switcher = Gtk.StackSwitcher()
        self.stack_switcher.set_stack(self.stack)
        self.vbox.pack_start(self.stack_switcher, False, False, 0)
        self.vbox.pack_start(self.stack, True, False, 0)

    # Obsługa dodawania nowego pliku
    def add_file(self, _):
        print("nowy plik")
        # AddFileInputPopup(self.textbox.text()).exec()
        # self.stacklayout.currentWidget().update(self.textbox.text())

    # Obsługa dodawania nowego katalogu
    def add_dir(self, _):
        print("nowy folder")
    
    # Obsługa wyświetlania okienka z informacją o aplikacji
    def about_app(self, _):
        with open(os.path.join(os.getcwd(), 'shared', 'about_app.txt'), 'r') as f:
            text = f.read()
        # InfoBox(text)
        print(text)
    
    def go_to_path(self, _):
        print("update path/window content")
        self.stack.get_child_by_name("files_list")

    # def show_city_input(self, _):
    #     self.stack.get_child_by_name("current_weather").set_markup(get_current_weather_text())
    #     self.stack.set_visible_child(self.stack.get_child_by_name("change_city"))

    # def show_author_info(self, _):
    #     self.stack.set_visible_child(self.stack.get_child_by_name("about_app"))


def start_app():
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.set_default_size(650, 550)
    win.show_all()
    Gtk.main()
