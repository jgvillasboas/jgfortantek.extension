# -*- coding: utf-8 -*-

#GENERAL IMPORTS
import clr, wpf, os
clr.AddReference("System", "PresentationFramework", "WindowsBase", "PresentationCore")

#.NET IMPORTS
from System.Windows import Window, ResourceDictionary
from System.Windows.Controls import DockPanel, ListBox, Button, SelectionMode, Dock, ListBoxItem, TextBox, StackPanel, Orientation, TextBlock, CheckBox
from System.IO import StringReader
from System import EventHandler
from System.Collections.Generic import List
from System import Uri
from pyrevit import forms

class SheetSelection(Window):
    def __init__(self, wrapped_views):
        path_xaml_file = os.path.join( PATH_SCRIPT, "SheetsSelection.xaml")
        wpf.LoadComponent(self, path_xaml_file)
        self.original_views = wrapped_views
        self.checkboxes = []

        for sheet in wrapped_views:
            cb = CheckBox()
            cb.Content = sheet.sheet.Name
            cb.Tag = sheet.sheet
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

    def on_search_text_changed(self, sender, args):
        search_term = self.search_box.Text.lower()
        filtered = [item for item in self.checkboxes if search_term in str(item).lower()]
        self.listbox.ItemsSource = filtered

    def get_selected_items(self):
        return [cb.Tag for cb in self.checkboxes if cb.IsChecked]

class SheetWrapper(object):
    def __init__(self, sheet):
        self.sheet = sheet
        self.Display = "{} - {}".format(self.sheet.SheetNumber, self.sheet.Name)
        self.IsSelected = False

    def __str__(self):
        return self.Display
    
    def __repr__(self):
        return self.__str__()