# -*- coding: utf-8 -*-

#Revit Imports
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *

#.NET Imports
import os
import clr
clr.AddReference("System")
clr.AddReference("System.Windows.Forms")
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
from System.Windows.Forms import FolderBrowserDialog, DialogResult

#PyRevit Imports
from pyrevit import Forms    
from GUI.SheetsSelection import SheetSelection, SheetWrapper
from GUI.PDFConfig import PDFConfig

#Variables
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document #type: Document
selection = uidoc.Selection

all_sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()

wrapped_sheets = [SheetWrapper(s) for s in all_sheets]
form = SheetSelection(wrapped_sheets)
result = form.ShowDialog()

if result == True:
    selected_sheets = form.get_selected_items()

    if not selected_sheets:
        TaskDialog("No Sheets Selected")

else: 
    script.exit()

viewset = ViewSet()

for sheet in selected_sheets:
    viewset.Insert(sheet.sheet)


form1 = PDFConfig()
result1 = form1.ShowDialog()







