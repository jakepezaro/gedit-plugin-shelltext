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
    <property name="title">ShellText</property>
    <property name="default-width">800</property>
    <child>
      <object class="GtkGrid" id="layout-grid">
        <property name="column-spacing">10</property>
        <property name="row-spacing">10</property>
        <property name="margin-start">5</property>
        <property name="margin-end">5</property>
        <property name="margin-top">5</property>
        <property name="margin-bottom">5</property>
      
        <child>
          <object class="GtkLabel" id="source-label">
            <property name="label">Source</property>
          </object>
          <packing>
              <property name="left-attach">0</property>
              <property name="top-attach">0</property>
          </packing>        
        </child>
        <child>
          <object class="GtkComboBoxText" id="source-combo">
            <items>
              <item translatable="yes" id="from_selection">Selection</item>
              <item translatable="yes" id="from_document">Document</item>
            </items>
          </object>
          <packing>
            <property name="left-attach">1</property>
            <property name="top-attach">0</property>
          </packing>        
        </child>
        
        <child>
          <object class="GtkLabel" id="destination-label">
            <property name="label">Destination</property>
          </object>
          <packing>
              <property name="left-attach">0</property>
              <property name="top-attach">1</property>
          </packing>        
        </child>
        <child>
          <object class="GtkComboBoxText" id="destination-combo">
            <items>
              <item translatable="yes" id="to_selection">Selection</item>
              <item translatable="yes" id="to_document">Document</item>
            </items>
          </object>
          <packing>
            <property name="left-attach">1</property>
            <property name="top-attach">1</property>
          </packing>        
        </child>
        
        <child>
          <object class="GtkLabel" id="spacer">
            <property name="vexpand">True</property>
          </object>
          <packing>
              <property name="left-attach">0</property>
              <property name="top-attach">2</property>
              <property name="width">2</property>
          </packing>        
        </child>
        
        <child>
          <object class="GtkTextView" id="commands">
            <property name="expand">True</property>
          </object>
          <packing>
            <property name="left-attach">2</property>
            <property name="top-attach">0</property>
            <property name="height">3</property>
            <property name="width">2</property>
          </packing>
        </child>
        
        <child>
          <object class="GtkLabel" id="history-label">
            <property name="label">History</property>  
          </object>
          <packing>
              <property name="left-attach">0</property>
              <property name="top-attach">3</property>
          </packing>        
        </child>
        <child>
          <object class="GtkComboBoxText">
            <property name="hexpand">True</property>
            <items>
              <item translatable="yes" id="history">...</item>
            </items>
          </object>
          <packing>
            <property name="left-attach">2</property>
            <property name="top-attach">3</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="execute">
            <property name="label">Execute</property>  
          </object>
          <packing>
              <property name="left-attach">3</property>
              <property name="top-attach">3</property>
          </packing>        
        </child>        
        
      </object>
    </child>
  </object>
</interface>'''      
        
        
def run_shelltext(action, parameters):
    builder = Gtk.Builder()
    builder.add_from_string(dialog_spec)
    window = builder.get_object("shelltext-dialog")
    window.show_all()