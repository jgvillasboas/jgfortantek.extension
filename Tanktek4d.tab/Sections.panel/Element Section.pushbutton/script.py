# -*- coding: utf-8 -*-
print("Script 21/08/2025")
#Revit Imports
from Autodesk.Revit.UI.Selection import ISelectionFilter, ObjectType
from Autodesk.Revit.DB import *

#pyRevit Imports
from pyrevit import script, forms, EXEC_PARAMS

#General Imports
import traceback, math, os, sys

#Custom Imports

#Variables
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document #type: Document
selection = uidoc.Selection

selected_ids = selection.GetElementIds()
bbox_points = []
offset = 100 / 304.8  # 100mm in feet

view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
section_type = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Section][0]
viewTypeId = section_type.Id

# Transaction
t = Transaction(doc, "Transaction Start")
t.Start()  

for e_id in selected_ids:
    e = doc.GetElement(e_id)

    if isinstance(e, FamilyInstance) and \
       e.Category.Id.IntegerValue == int(BuiltInCategory.OST_StructuralFraming) and \
       "SUR_" in e.Symbol.Family.Name:
        # Get bounding box and transformation matrix
        bbox = e.get_BoundingBox(None)
        
        if not bbox:
            continue

        # Check if horizontal or vertical

        p1 = XYZ(bbox.Min.X, bbox.Min.Y, bbox.Min.Z)
        p2 = XYZ(bbox.Min.X, bbox.Max.Y, bbox.Min.Z)
        p3 = XYZ(bbox.Max.X, bbox.Min.Y, bbox.Min.Z)

        vector_x = p3 - p1
        vector_y = p2 - p1

        len_x = vector_x.GetLength()
        len_y = vector_y.GetLength()

        center_global = (bbox.Min + bbox.Max) / 2

        
        if len_x > len_y:
            basis_x = vector_x.Normalize()
            basis_y = XYZ.BasisZ
            basis_z = basis_x.CrossProduct(basis_y).Normalize()
            print("{} horizontal".format(e.Symbol.Family.Name))

            
        else:
            basis_x = vector_y.Normalize()
            basis_y = XYZ.BasisZ
            basis_z = basis_x.CrossProduct(basis_y).Normalize()
            print("{} vertical".format(e.Symbol.Family.Name))

             
             
        section_transform = Transform.Identity
        section_transform.Origin = center_global
        section_transform.BasisX = basis_x
        section_transform.BasisY = basis_y
        section_transform.BasisZ = basis_z

        bboxXYZ = BoundingBoxXYZ()
        bboxXYZ.Transform = section_transform

        local_dms = bbox.Max - bbox.Min
        width = max(local_dms.X + offset, 0.1)
        height = max(local_dms.Y + offset, 0.1)
        depth = max((bbox.Max.Z - bbox.Min.Z) + offset, 0.1)

        bboxXYZ = BoundingBoxXYZ()
        bboxXYZ.Transform = section_transform
        bboxXYZ.Min = XYZ(-width / 2, -depth / 2, -height / 2)
        bboxXYZ.Max = XYZ(width / 2, depth / 2, height / 2)

        # Create section view
        try:
            sectionView = ViewSection.CreateSection(
                doc,
                viewTypeId,
                bboxXYZ
            )

            sectionView.Name = "{}_{}".format(e.Symbol.Family.Name, e.Id.IntegerValue)
            print("Section created: {}".format(sectionView.Name))

        except Exception as ex:
            print("Error creating section for element {}: {}".format(e.Id.IntegerValue, str(ex)))

t.Commit()


        
