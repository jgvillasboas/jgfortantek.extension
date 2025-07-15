# -*- coding: utf-8 -*-

#Revit Imports
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *

#Custom Imports
from GUI.TemplateSelector import TemplateSelector
from GUI.ViewSelection import ViewSelection, ViewWrapper


#Variables
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document #type: Document
selection = uidoc.Selection

#MAIN
#------------------------------------

view_template_elements = [v for v in FilteredElementCollector(doc).OfClass(View).ToElements() if v.IsTemplate]
template_name_list = [v.Name for v in view_template_elements]
viewtemplate_dictionary_name = {v.Name: v for v in view_template_elements}

#Select ViewTemplates

form_templates = TemplateSelector(template_name_list)
result_templates = form_templates.ShowDialog()

if result_templates == True:
    selected_template_names = form_templates.listbox.SelectedItem

    if not selected_template_names:
        TaskDialog.Show("Warning", "No View Templates were selected")

    else:
        selected_template_view = viewtemplate_dictionary_name[selected_template_names]
        TaskDialog.Show("Selected View Templates: ", "You Selected: " + str(selected_template_names))
        view_template_id = selected_template_view.Id


all_views = [view for view in FilteredElementCollector(doc).OfClass(View).ToElements() if not view.IsTemplate and not view.ViewType in [ViewType.Legend, ViewType.Schedule]]
wrapped_views = [ViewWrapper(v) for v in all_views]

form_views = ViewSelection(wrapped_views)
result_views = form_views.ShowDialog()

if result_views == True:
    selected_views = form_views.get_selected_items()

    if not selected_views:
        TaskDialog.Show("Warning", "No Views were selected")

    else:
        t = Transaction(doc, "Applying Views")
        t.Start()

        for sv in selected_views:
            sv.views.ViewTemplateId = view_template_id

        t.Commit()

None

