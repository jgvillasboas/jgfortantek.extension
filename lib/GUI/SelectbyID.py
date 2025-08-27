# -*- coding: utf-8 -*-

#GENERAL IMPORTS
import clr, wpf, os
clr.AddReference("System", "PresentationFramework", "WindowsBase", "PresentationCore")

#.NET IMPORTS
from System.Windows import Window, ResourceDictionary, WindowStartupLocation # type: ignore
from System.Windows.Controls import DockPanel, ListBox, Button, SelectionMode, Dock, ListBoxItem, TextBox, StackPanel, Orientation, TextBlock, CheckBox # type: ignore
from System.IO import StringReader # type: ignore
from System import EventHandler # type: ignore
from System.Collections.Generic import List # type: ignore
from System import Uri # type: ignore
from pyrevit import forms

PATH_SCRIPT = os.path.dirname(__file__)

class SelectID(Window):
    def __init__(self, idfromlink=None):
        path_xaml_file = os.path.join( PATH_SCRIPT, "SelectbyID.xaml")
        wpf.LoadComponent(self, path_xaml_file)
        self.idfromlink = idfromlink
        self.OkButton.IsDefault = True
        self.OkButton.IsCancel = True
        self.OkButton.Click += self.on_select_element
        self.WindowStartupLocation = WindowStartupLocation.CenterScreen

    def on_select_element(self, sender, args):
        user_input = self.ElementIDTextBox.Text.strip()
        if not user_input.isdigit():
            forms.alert("Please enter a valid integer Element ID.", title="Invalid Input")
            return

        if not user_input.isdigit():
            forms.alert("Please enter a valid integer Element ID.", title="Invalid Input")
            return

        self.idfromlink = int(user_input)
        self.DialogResult = True
        self.Close()


