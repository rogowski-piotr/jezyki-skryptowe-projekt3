import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


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


