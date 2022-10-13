import gi
gi.require_version('Gedit', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import GLib, Gio, GObject, Gtk, Gdk, Gedit

class AppActivatable(GObject.Object, Gedit.AppActivatable):
    __gtype_name__ = "ExternalToolsAppActivatable"

    app = GObject.Property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)
        self.menu = None

    def do_activate(self):
        self.tools_section = self.extend_menu("tools-section-1")
        external_tools_submenu = Gio.Menu()
        item = Gio.MenuItem.new_submenu(_("ZZZZZZZExternal ToolsXXX"), external_tools_submenu)
        external_tools_submenu_section = Gio.Menu()
        external_tools_submenu.append_section(None, external_tools_submenu_section)
        self.tools_section.append_menu_item(item)
        self.menu = external_tools_submenu_section

    def do_deactivate(self):
        self.menu.remove_all()
        self.tools_section = None