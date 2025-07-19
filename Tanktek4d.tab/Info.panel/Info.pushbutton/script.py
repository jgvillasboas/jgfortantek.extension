# -*- coding: utf-8 -*-

#IMPORTS
from Autodesk.Revit.DB import *
from pyrevit import forms
import wpf, os, clr

#.NET IMPORTS
clr.AddReference("System")
from System.Collections.Generic import List
from System.Windows import Window, ResourceDictionary
from System.Windows.Controls import CheckBox, Button, TextBox, ListBoxItem
from System import Uri

PATH_SCRIPT = os.path.dirname(__file__) #get directory name
doc = __revit__.ActiveUIDocument.Document #active document in Revit (revit model open)
uidoc = __revit__.ActiveUIDocument #UI document, necessary to get elements, create selections, change views, making zoom in elements, etc
app = __revit__.Application #Revit Instance, necessary to get global configurations, families information, create/open new docs, units, exportations, etc.

class AboutForm(Window):
    def __init__(self):
        path_xaml_file = os.path.join(PATH_SCRIPT, 'MainWindow.xaml')
        wpf.LoadComponent(self, path_xaml_file)

        self.ShowDialog()

    def CloseButton_Click(self, sender, e):
        self.Close()

UI = AboutForm()