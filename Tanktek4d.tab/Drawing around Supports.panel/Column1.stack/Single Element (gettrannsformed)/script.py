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

# Start transaction
transaction = Transaction(doc, "Draw bounding box outline using transform")
transaction.Start()

for element_id in selected_elements:
    element = doc.GetElement(element_id)
    element_name = Element.Name.GetValue(element)

    # Filter only structural framing elements from the specific family
    if isinstance(element, FamilyInstance) and element.Category.Id.IntegerValue == int(BuiltInCategory.OST_StructuralFraming) and "SUR_" in element.Symbol.Family.Name:
        print('ID: {}, Family Type: {}'.format(element_id, element_name))

        # Offset in feet (50 mm)
        offset = 50 / 304.8

        if "UH" in element_name:
            width_mm = int(element_name.split(".")[1])
            width_ft = width_mm / 304.8
            height_ft = 40 / 304.8

            # Get element's transformation matrix
            transform = element.GetTransform()

            # Define total width and height for the rectangle outline (in local coordinates)
            total_width = width_ft + 2 * offset
            total_height = height_ft + offset * 2 # Adjust if needed

            # Define rectangle corner points in local coordinate system
            p1_local = XYZ(-total_width/2, -total_height/2, 0)
            p2_local = XYZ( total_width/2, -total_height/2, 0)
            p3_local = XYZ( total_width/2,  total_height/2, 0)
            p4_local = XYZ(-total_width/2,  total_height/2, 0)

            # Transform local points to global coordinates using the element's transform
            p1 = transform.OfPoint(p1_local)
            p2 = transform.OfPoint(p2_local)
            p3 = transform.OfPoint(p3_local)
            p4 = transform.OfPoint(p4_local)

            # Create bounding rectangle lines
            lines = [
                Line.CreateBound(p1, p2),
                Line.CreateBound(p2, p3),
                Line.CreateBound(p3, p4),
                Line.CreateBound(p4, p1),
            ]

            # Create detail curves in the active view
            for line in lines:
                doc.Create.NewDetailCurve(view, line)

        else:
            print("Element does not follow 'UH.' naming convention")

    else:
        print('Invalid Element: {}'.format(element))

# Commit the transaction
transaction.Commit()