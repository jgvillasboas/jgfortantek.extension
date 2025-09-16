# -*- coding: utf-8 -*-

#REVIT/GENERAL IMPORTS
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from pyrevit import forms, script
import wpf, os, clr

#.NET IMPORTS
clr.AddReference("System")
from System.Collections.Generic import List
from System.Windows import Window, ResourceDictionary
from System.Windows.Controls import CheckBox, Button, TextBox, ListBoxItem
from System import Uri

#Custom Imports
from GUI.TemplateSelector import TemplateSelector
from GUI.ViewSelection import ViewSelection, ViewWrapper
from GUI.SheetsSelection import SheetSelection, SheetWrapper


#VARIABLES
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document #type: Document
selection = uidoc.Selection

#MAIN
#------------------------------------

#Get views      
all_views = [view for view in FilteredElementCollector(doc).OfClass(View).ToElements() if not view.IsTemplate and not view.ViewType in [ViewType.Legend, ViewType.Schedule]]
wrapped_views = [ViewWrapper(v) for v in all_views]
form_views = ViewSelection(wrapped_views)

#Asking User to Select Views
if form_views.ShowDialog():
    selected_wrappers, selected_views, selected_names = form_views.get_selected_items()
    selected_views = sorted(selected_views, key=lambda v: ViewWrapper.alphanum_key(v.Name))
        
    if not selected_views:
        TaskDialog.Show("Warning", "No Views were selected")
        script.exit()
    
    #Get Sheets
    all_sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()
    wrapped_sheets = [SheetWrapper(s) for s in all_sheets]
    form_sheets = SheetSelection(wrapped_sheets)

    #Check if views are already placed in any sheet
    check_all_views = FilteredElementCollector(doc).OfClass(Viewport).ToElements()
    views_already_on_sheets = {vp.ViewId.IntegerValue: vp.SheetId.IntegerValue for vp in check_all_views}   

    #Asking user to Select Sheet (only works for the first sheet)
    if form_sheets.ShowDialog():
        selected_sheets = form_sheets.get_selected_items()
        sheet_id = selected_sheets[0].Id

        #Collect Title Block Position
        sheet_elements = FilteredElementCollector(doc, sheet_id).ToElements()
        titleblocks = [t for t in sheet_elements if isinstance (t, FamilyInstance) and t.Category.Id.IntegerValue == int(BuiltInCategory.OST_TitleBlocks)]

        if titleblocks:
            tb = titleblocks[0]
            tb_pos = tb.Location.Point

        else:
            tb_pos = XYZ (0, 0, 0)

        if not selected_sheets:
            TaskDialog.Show("Warning", "No Sheets were selected")
            script.exit()

    if not form_sheets.DialogResult:
        script.exit()

    #Layout Configuration
    t = Transaction(doc, "Placing Views in Selected Sheets")
    t.Start()

    #Starting Position Reference
    x_offset = -2.45
    y_offset = 1.65
    spacing_x = 0.4
    spacing_y = 0.5
    max_per_row = 5
    count = 0

    #Position each view whitin the sheet
    for view in selected_views:
        if view.Id.IntegerValue in views_already_on_sheets:
            sheet_name = doc.GetElement(ElementId(views_already_on_sheets[view.Id.IntegerValue])).Name
            TaskDialog.Show("Warning", "View '{}' is already placed in Sheet '{}'".format(view.Name, sheet_name))
            continue

        position = XYZ(tb_pos.X + x_offset, tb_pos.Y + y_offset, 0)
        Viewport.Create(doc, sheet_id, view.Id, position)
        count += 1
        x_offset += spacing_x
        
        if count % max_per_row == 0:
            x_offset = -2.45
            y_offset -= spacing_y


    TaskDialog.Show("Success","Views Placed Successfully")
    t.Commit()


