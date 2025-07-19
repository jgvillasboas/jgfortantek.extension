# -*- coding: utf-8 -*-

#IMPORTS
from Autodesk.Revit.DB import *
from pyrevit import forms
import wpf, os, clr

#.NET IMPORTS
clr.AddReference("System")
from System.Colletions.Generic import List
from System.Windows import Window, ResourceDictionary
from System.Windows.Controls import CheckBox, Button, TextBox, ListBoxItem
from System import Uri

