    # -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ObjectType
from pyrevit import forms, script
import wpf, os, clr

from GUI.SelectbyID import SelectID
from GUI import ViewHelper

uidoc = __revit__.ActiveUIDocument # type: ignore
doc = __revit__.ActiveUIDocument.Document # type: ignore #type: Document
selection = uidoc.Selection
name_manager = ViewHelper.NewNameHelper(doc)
new_view_name = name_manager.get_unique_name("My_3D_View")
active_view = uidoc.ActiveView

linked_element_id_value = None

while linked_element_id_value is None:
    window = SelectID()

    if window.ShowDialog() == True:
        linked_element_id_value = window.idfromlink

if linked_element_id_value:

    linked_element = None
    linked_instance = None

    for link in FilteredElementCollector(doc).OfClass(RevitLinkInstance):
        link_doc = link.GetLinkDocument()
        elem_id = ElementId(linked_element_id_value)
        e = link_doc.GetElement(elem_id)

        if e:
            linked_element = e
            linked_instance = link
            break

    if not linked_element:
        print("Element ID not found in any Linked File")

    try:
        if linked_instance:
            linked_doc = linked_instance.GetLinkDocument() #Get Link Document == doc
            link_transform = linked_instance.GetTotalTransform()

            if linked_doc is not None:

                # Get the bounding box of the linked element
                bbox = linked_element.get_BoundingBox(None)

                # Transform the bounding box to the host document's coordinate system
                bbox_transformed = ViewHelper.get_transformed_bbox(bbox, link_transform, offset=1)

                # Get the 3D view types
                view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
                view_3d_type = [vt for vt in view_types if vt.ViewFamily == ViewFamily.ThreeDimensional][0]

                t = Transaction(doc, "Create 3D View")
                t.Start()
                # Create the 3D view
                view_3d = View3D.CreateIsometric(doc, view_3d_type.Id)
                view_3d.Name = new_view_name
                view_3d.SetSectionBox(bbox_transformed)
                view_3d.ViewTemplateId = active_view.ViewTemplateId

                t.Commit()
                uidoc.ActiveView = view_3d
            else:
                raise Exception("Failed to get the linked document.")

    except Exception as e:
        print("Operation cancelled or failed: {}".format(e))
