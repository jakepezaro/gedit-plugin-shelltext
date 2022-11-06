from subprocess import run, PIPE

try:
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
            action.connect('activate', run_shelltext, self.window)
            self.window.add_action(action)

        def do_deactivate(self):
            self.window.remove_action('shelltext')
except:
    print('not running in gedit')
        
        
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
              <item translatable="yes" id="from-selection">Selection</item>
              <item translatable="yes" id="from-document">Document</item>
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
              <item translatable="yes" id="to-selection">Selection</item>
              <item translatable="yes" id="to-document">Document</item>
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
          <object class="GtkTextView" id="shelltext-command">
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
          <object class="GtkButton" id="execute-button">
            <property name="label">Execute</property>
            <signal name="pressed" handler="shelltext-execute" swapped="no"/>
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
    
    
class TextSelectionWatcher:
    
    def __init__(self, gedit_window, execute_button, source_combo):
        self.gedit_window = gedit_window
        self.document = gedit_window.get_active_document()
        self.execute_button = execute_button
        self.source_combo = source_combo
        self.window_connection = self.gedit_window.connect('notify', self._on_window_notify)
        self.document_connection = self.document.connect('notify', self._on_document_notify)
        self.source_combo_connection = self.source_combo.connect('changed', lambda _: self._on_selection())
        self._on_selection()
        
    def _on_window_notify(self, gedit_window, paramspec):
        if paramspec.name == 'title':
            self.document.disconnect(self.document_connection)
            self.document = self.gedit_window.get_active_document()
            if self.document:
                self.document_connection = self.document.connect('notify', self._on_document_notify)
                self._on_selection()
    
    def _on_document_notify(self, document, paramspec):
        if paramspec.name == 'has-selection':
            self._on_selection()

    def _on_selection(self):
        source = self.source_combo.get_active_id() 
        if source == 'from-document':
            enabled = True
        elif source == 'from-selection' and self.document.get_has_selection():
            enabled = True
        else:
            enabled = False
        self.execute_button.set_sensitive(enabled)

    def get_source_text(self):
        source = self.source_combo.get_active_id()
        if source == 'from-document':
           start = self.document.get_start_iter()
           end = self.document.get_end_iter()
           return self.document.get_text(start, end, False)
        if source == 'from-selection' and self.document.get_has_selection():
           start, end = self.document.get_selection_bounds()
           return self.document.get_text(start, end, False)
    
    def disconnect(self, dialog_window):
        if self.document:
            self.document.disconnect(self.document_connection)
        if self.gedit_window:            
            self.gedit_window.disconnect(self.window_connection)
        if self.source_combo:
            self.source_combo.disconnect(self.source_combo_connection)


def run_shelltext(action, parameters, gedit_window):
    builder = Gtk.Builder()
    builder.add_from_string(dialog_spec)
    cmd = builder.get_object("shelltext-command")

    selection_watcher = TextSelectionWatcher(gedit_window, builder.get_object("execute-button"), builder.get_object("source-combo"))

    builder.connect_signals({
        "shelltext-execute": lambda _: shelltext_execute(cmd.get_buffer(), selection_watcher)
    })
    
    dialog_window = builder.get_object("shelltext-dialog")
    dialog_window.connect('destroy', selection_watcher.disconnect)
    gedit_window.connect('destroy', selection_watcher.disconnect)
    dialog_window.show_all()
    
    
def shelltext_execute(command_buffer, selection_watcher):
    startIter, endIter = command_buffer.get_bounds()   
    source_text = selection_watcher.get_source_text()
    command = command_buffer.get_text(startIter, endIter, False) 
    print(source_text)
    print(command)
    result = apply_shell_command(source_text, command)
    print(result.returncode)
    print(str(result.stdout, 'utf-8'))
    print(str(result.stderr, 'utf-8'))


def apply_shell_command(source_text, command):
    return run(command.split(' '), input=bytes(source_text, 'utf-8'), stdout=PIPE, stderr=PIPE, shell=True)


def parse_command(command):
    commands = []
    current = ''
    in_quote = False
    for c in command:
       is_quote = c == '"'
       is_separator = c == ' '
       if not in_quote and is_quote:
           in_quote = True
           commands.append(current)
           current = ''
           continue
       if in_quote and is_quote:
           in_quote = False
           commands.append(current)
           current = ''
           continue
       if is_separator and not in_quote:
           commands.append(current)
           current = ''
           continue
       current += c
    commands.append(current)
    return commands

# todo
#   non utf-8 documents
#   find out what shell=True is actually doing
#   parse command when shell=False
#   handle pipes when shell=False
