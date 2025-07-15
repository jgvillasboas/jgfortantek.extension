# -*- coding: utf-8 -*-

#General Imports
import os
from datetime import date
from pyrevit import forms
from collections import defaultdict

#Revit Imports
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *

#.NET Imports
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System")
from System.Collections.Generic import List

#Custom Imports
from GUI.SheetsSelection import SheetSelection, SheetWrapper
from GUI.RevisionSelection import RevisionSelection, RevisionWrapper

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
        TaskDialog("Warning! No Sheets Selected")

    else:
        all_revisions = FilteredElementCollector(doc).OfClass(Revision).ToElements()

        wrapped_revisions = [RevisionWrapper(r) for r in all_revisions]
        form2 = RevisionSelection(wrapped_revisions)
        result2 = form2.ShowDialog()

        if result2 == True:
            selected_revisions = form2.get_selected_revisions()

            t = Transaction(doc, "Set Revision on Sheets")
            t.Start()

            for wrapped_sheets in selected_sheets:
                sheet = wrapped_sheets.sheet
                
                current_ids = sheet.GetAdditionalRevisionIds()
                current_int_ids = set([elid.IntegerValue for elid in current_ids])

                for rev in selected_revisions:
                    current_int_ids.add(rev.Id.IntegerValue)

                new_elids = List[ElementId]([ElementId(i) for i in current_int_ids])
                sheet.SetAdditionalRevisionIds(new_elids)

            t.Commit()
            TaskDialog.Show("Revisions", "Revisions added in Sheets")






