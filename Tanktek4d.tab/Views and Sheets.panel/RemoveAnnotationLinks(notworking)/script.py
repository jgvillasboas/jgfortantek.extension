# -*- coding: utf-8 -*-

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog
import sys


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


remove_annotations_template_name = "T4D_RemoveGrids"

#Getting all Views on Project
collector = FilteredElementCollector(doc).OfClass(View)
all_views = list(collector)

#Search the view template
remove_annotations_template = None

for v in all_views:
    if v.IsTemplate and v.Name == remove_annotations_template_name:
        remove_annotations_template = v
        break

if not remove_annotations_template:
    TaskDialog.Show("View Template '{}' not found!".format(remove_annotations_template_name))
    sys.exit()

remove_annotations_id = remove_annotations_template.Id
views_updated = []
original_templates = {}

t1 = Transaction(doc, "RemoveAnnotationLinks")
t1.Start()

for view in all_views:
    if view.IsTemplate:
        continue

    current_template_id = view.ViewTemplateId
    if current_template_id is None or current_template_id == ElementId.InvalidElementId:
        continue

    original_templates[view.Id] = current_template_id

    view.ViewTemplateId = remove_annotations_id
    views_updated.append(view.Name)

t1.Commit()

t2 = Transaction (doc, "Restore Original Template")
t2.Start()

for view in all_views:
    if view.Id in original_templates:
        view.ViewTemplateId = original_templates[view.Id]

t2.Commit()

message = "{}Views updated sucefully!".format(len(views_updated))
for name in views_updated:
    message += "- {}".format(name)

TaskDialog.Show("Result", message)

