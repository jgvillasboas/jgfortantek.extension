# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ObjectType

from GUI.NewNameHelper import NewNameHelper

uidoc = __revit__.ActiveUIDocument # type: ignore
doc = __revit__.ActiveUIDocument.Document # type: ignore #type: Document
selection = uidoc.Selection
name_manager = NewNameHelper(doc)
new_view_name = name_manager.get_unique_name("My_3D_View")
active_view = uidoc.ActiveView

try:
    # Select Linked File
    reference = selection.PickObject(ObjectType.LinkedElement, "Select a Revit Link File:")

    if reference and hasattr(reference, 'LinkedElementId'):
        linked_element_id = reference.LinkedElementId #Link Element Id
        linked_instance_id = reference.ElementId #Linked Instance Id

        link_instance = doc.GetElement(linked_instance_id) #Get Element Instance
        linked_doc = link_instance.GetLinkDocument() #Get Link Document == doc
        linked_element = linked_doc.GetElement(linked_element_id) #Get Linked Element  (selected)
        link_transform = link_instance.GetTotalTransform()

        # Get the bounding box of the linked element in its own coordinate system
        bbox = linked_element.get_BoundingBox(None)

        offset = 1
        pt_min = link_transform.OfPoint(bbox.Min)
        pt_max = link_transform.OfPoint(bbox.Max)

        minX = min(pt_min.X, pt_max.X) - offset
        minY = min(pt_min.Y, pt_max.Y) - offset
        minZ = min(pt_min.Z, pt_max.Z) - offset
        maxX = max(pt_min.X, pt_max.X) + offset
        maxY = max(pt_min.Y, pt_max.Y) + offset
        maxZ = max(pt_min.Z, pt_max.Z) + offset

        bbox_transformed = BoundingBoxXYZ()
        bbox_transformed.Min = XYZ(minX, minY, minZ)
        bbox_transformed.Max = XYZ(maxX, maxY, maxZ)

        view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
        view_3d_type = [vt for vt in view_types if vt.ViewFamily == ViewFamily.ThreeDimensional][0]

        t = Transaction(doc, "Create 3D View")

        t.Start()

        view_3d = View3D.CreateIsometric(doc, view_3d_type.Id)
        view_3d.Name = new_view_name
        view_3d.SetSectionBox(bbox_transformed)
        view_3d.ViewTemplateId = active_view.ViewTemplateId

        t.Commit()

        uidoc.ActiveView = view_3d

except Exception as e:
    print("Operation cancelled or failed: {}".format(e))