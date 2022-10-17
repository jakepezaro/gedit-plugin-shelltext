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
        shelltext_menu_item = Gio.MenuItem.new('ShellText', 'win.shelltext')
        self.tools_section.append_menu_item(shelltext_menu_item)
        self.app.add_accelerator('<Control><Shift>R', 'win.shelltext', None)

    def do_deactivate(self):
        self.tools_section.remove_items()
        self.app.remove_accelerator('win.shelltext', None)
        

class WindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "ExternalToolsWindowActivatable"

    window = GObject.Property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        action = Gio.SimpleAction(name='shelltext')
        action.connect('activate', run_shelltext)
        self.window.add_action(action)

    def do_deactivate(self):
        self.window.remove_action('shelltext')
        

dialog_spec = '''<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <object class="GtkWindow" id="shelltext-dialog">
    <property name="can_focus">False</property>
    <child>
      <object class="GtkButton" id="button1">
        <property name="label" translatable="yes">button</property>
        <property name="use-action-appearance">False</property>
        <property name="visible">True</property>
        <property name="can-focus">True</property>
        <property name="receives-default">True</property>
      </object>
    </child>
  </object>
</interface>'''      
        
        
def run_shelltext(action, parameters):
    print('running shelltext')
    builder = Gtk.Builder()
    builder.add_from_string(dialog_spec)
    window = builder.get_object("shelltext-dialog")
    window.show_all()
    print('done')