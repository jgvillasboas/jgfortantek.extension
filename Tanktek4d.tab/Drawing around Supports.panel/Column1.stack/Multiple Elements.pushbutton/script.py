# -*- coding: utf-8 -*-
import os, sys, math, datetime, time
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from pyrevit import revit, forms
import clr

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView
selection = uidoc.Selection

offset = 50 / 304.8  # 50mm em pés
selected_ids = selection.GetElementIds()
bbox_points = []

t = Transaction(doc, "Contorno planar sem transform")
t.Start()

for e_id in selected_ids:
    e = doc.GetElement(e_id)

    if isinstance(e, FamilyInstance) and \
       e.Category.Id.IntegerValue == int(BuiltInCategory.OST_StructuralFraming) and \
       "SUR_" in e.Symbol.Family.Name:

        bbox = e.get_BoundingBox(view)
        if not bbox:
            continue

        # Add Bbox points to the list
        bbox_points.append(bbox.Min)
        bbox_points.append(bbox.Max)

if bbox_points:
    min_x = min(p.X for p in bbox_points) - offset
    max_x = max(p.X for p in bbox_points) + offset
    min_y = min(p.Y for p in bbox_points) - offset
    max_y = max(p.Y for p in bbox_points) + offset

    # Create points according bounding box (Z Axis = 0 // Plan View)
    p1 = XYZ(min_x, min_y, 0)
    p2 = XYZ(max_x, min_y, 0)
    p3 = XYZ(max_x, max_y, 0)
    p4 = XYZ(min_x, max_y, 0)

    lines = [
        Line.CreateBound(p1, p2),
        Line.CreateBound(p2, p3),
        Line.CreateBound(p3, p4),
        Line.CreateBound(p4, p1),
    ]

    for line in lines:
        doc.Create.NewDetailCurve(view, line)

t.Commit()