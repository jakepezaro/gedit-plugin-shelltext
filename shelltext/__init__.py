import gi
gi.require_version('Gedit', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import GLib, Gio, GObject, Gtk, Gdk, Gedit

class AppActivatable(GObject.Object, Gedit.AppActivatable):
    __gtype_name__ = "ExternalToolsAppActivatable"

    app = GObject.Property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.tools_section = self.extend_menu("tools-section-1")
        shelltext_menu_item = Gio.MenuItem.new('ShellText', 'run_shelltext')
        self.tools_section.append_menu_item(shelltext_menu_item)

    def do_deactivate(self):
        self.tools_section.remove_items()