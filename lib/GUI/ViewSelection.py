import clr, wpf, os, re
clr.AddReference("PresentationFramework", "WindowsBase", "PresentationCore", "System.Xml")

from System.Windows import Window, Thickness, WindowStartupLocation, ResizeMode, HorizontalAlignment, VerticalAlignment
from System.Windows.Controls import DockPanel, ListBox, Button, SelectionMode, Dock, ListBoxItem, TextBox, StackPanel, Orientation, TextBlock, CheckBox
from System.Windows.Markup import XamlReader
from System.IO import StringReader
from System.Xml import XmlReader
from System import EventHandler
from System.Collections.Generic import List

PATH_SCRIPT = os.path.dirname(__file__)

class ViewSelection(Window):
    def __init__(self, wrapped_views):
        path_xaml_file = os.path.join(PATH_SCRIPT, "ViewSelection.xaml")
        wpf.LoadComponent(self, path_xaml_file)
        self.original_views = wrapped_views
        self.checkboxes = []

        for vw in wrapped_views:
            cb = CheckBox()
            cb.Content = vw.Display
            cb.Tag = vw
            self.checkboxes.append(cb)

        self.listbox.ItemsSource = self.checkboxes
           
    def OKButton_Click(self, sender, args):
        self.DialogResult = True
        self.Close()

    def CheckAllButton_Click(self, sender, args):
        for cb in self.checkboxes:
            cb.IsChecked = True
        self.refresh_list()

    def UncheckAllButton_Click(self, sender, args):
        for cb in self.checkboxes:
            cb.IsChecked = False
        self.refresh_list()

    def ToggleAllButton_Click(self, sender, args):
        for cb in self.checkboxes:
            cb.IsChecked = not cb.IsChecked
        self.refresh_list()

    def refresh_list(self):
        self.listbox.ItemsSource = None
        self.listbox.ItemsSource = [cb for cb in self.checkboxes if self.search_box.Text.lower() in str(cb.Content).lower()]

    def SearchBox_TextChanged(self, sender, args):
        search_term = self.search_box.Text.lower()
        filtered = [item for item in self.checkboxes if search_term in str(item).lower()]
        self.listbox.ItemsSource = filtered

    def get_selected_items(self):
        selected_wrappers = [cb.Tag for cb in self.checkboxes if cb.IsChecked]
        selected_views = [vw.views for vw in selected_wrappers]
        selected_names = [vw.Display for vw in selected_wrappers]
      
        return selected_wrappers, selected_views, selected_names
    
class ViewWrapper(object):
    def __init__(self, views):
        self.views = views
        self.Display = "{}".format(self.views.Name)
        self.IsSelected = False

    def __str__(self):
        return self.Display
    
    def __repr__(self):
        return self.__str__()
    
    @staticmethod
    def alphanum_key(s):
        parts = re.split('(\d+)', s)
        return [int (p) if p.isdigit() else p.lower() for p in parts]
    




