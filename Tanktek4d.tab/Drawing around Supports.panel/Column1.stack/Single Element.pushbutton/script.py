# -*- coding: utf-8 -*-
import os, sys, math, datetime, time
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from pyrevit import revit, forms
import clr

# Revit document and UI references
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
selection = uidoc.Selection
view = doc.ActiveView

# Get selected elements in the view
selected_elements = selection.GetElementIds()
offset = 50 / 304.8
bbox_points = []

# Start transaction
t = Transaction(doc, "Draw bounding box outline using transform")
t.Start()

for e_id in selected_elements:
    e = doc.GetElement(e_id)

    if isinstance(e, FamilyInstance) and \
       e.Category.Id.IntegerValue == int(BuiltInCategory.OST_StructuralFraming) and ("SUR_" in e.Symbol.Family.Name or "TS" in e.Symbol.Family.Name):

        bbox = e.get_BoundingBox(view)  
        if not bbox:
            continue

        min_pt = bbox.Min
        max_pt = bbox.Max

        min_x = min_pt.X - offset
        max_x = max_pt.X + offset
        min_y = min_pt.Y - offset
        max_y = max_pt.Y + offset

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