
#GENERAL IMPORTS
import clr, wpf, os
clr.AddReference("System", "PresentationFramework", "WindowsBase", "PresentationCore")

#.NET IMPORTS
from System.Windows import Window, ResourceDictionary
from System.Windows.Controls import DockPanel, ListBox, Button, SelectionMode, Dock, ListBoxItem, TextBox, StackPanel, Orientation, TextBlock
from System.IO import StringReader
from System import EventHandler
from System.Collections.Generic import List
from System import Uri
from pyrevit import forms

PATH_SCRIPT = os.path.dirname(__file__)

class TemplateSelector(Window):
    def __init__(self, items):
         path_xaml_file = os.path.join( PATH_SCRIPT, "SelectViewTemplate_UI.xaml")
         wpf.LoadComponent(self, path_xaml_file)
         self.original_items = list(items)
         self.listbox.ItemsSource = items
         
       
    def OKButton_Click(self, sender, args):
         self.DialogResult = True
         self.Close()
         
    def SearchBox_TextChanged(self, sender, args):
            search_term = self.search_box.Text.lower()
            filtered = [item for item in self.original_items if search_term in str(item).lower()]
            self.listbox.ItemsSource = filtered

    def ListBox_SelectionChanged(self, sender, args):
          selected = self.listbox.SelectedItem

    def Window_Closing(self, sender, args):
        if not self.DialogResult:
          self.DialogResult = False




