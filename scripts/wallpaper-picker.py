#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import subprocess

dialog = Gtk.FileChooserDialog(
    title="Selecionar Wallpaper",
    action=Gtk.FileChooserAction.OPEN,
)
dialog.add_buttons(
    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
    Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
)

filter_img = Gtk.FileFilter()
filter_img.set_name("Imagens")
filter_img.add_mime_type("image/png")
filter_img.add_mime_type("image/jpeg")
dialog.add_filter(filter_img)
dialog.set_current_folder("/home/silas/Imagens/papeis-de-parede")

response = dialog.run()
if response == Gtk.ResponseType.OK:
    path = dialog.get_filename()
    with open("/home/silas/.config/wpaperd/wallpaper.toml", "w") as f:
        f.write("[eDP-1]\n")
        f.write('path = "' + path + '"\n')
        f.write("[HDMI-A-1]\n")
        f.write('path = "' + path + '"\n')
    subprocess.run(["wpaperctl", "reload"])
dialog.destroy()
