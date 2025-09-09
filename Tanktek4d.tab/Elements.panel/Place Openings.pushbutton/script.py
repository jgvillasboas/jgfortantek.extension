# -*- coding: utf-8 -*-
print("Placing Wall Openings in Selected Containments... ")
#Revit Imports
from Autodesk.Revit.UI.Selection import ISelectionFilter, ObjectType
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import StructuralType
from Autodesk.Revit.DB import Line, ElementTransformUtils

#pyRevit Imports
from pyrevit import script, forms, EXEC_PARAMS

#General Imports
import traceback, math, os, sys, clr, wpf

#Custom Imports
from GUI.ElementSelector import CableTraySelectionFilter, Selector

#Variables
uidoc = __revit__.ActiveUIDocument # type: ignore
doc = __revit__.ActiveUIDocument.Document # type: ignore #type: Document
selection = uidoc.Selection

bbox, bbox_center, bbox_pts = Selector.CableTraySelector()

try:
    wall_selection = selection.PickObject(ObjectType.LinkedElement, "Select Wall:")


    #Select Linked Wall and transform in host coordinates
    if wall_selection and hasattr(wall_selection, 'LinkedElementId'):
        linked_element_id = wall_selection.LinkedElementId #Link Element Id
        linked_instance_id = wall_selection.ElementId #Linked Instance Id

        link_instance = doc.GetElement(linked_instance_id) #Get Element Instance
        linked_doc = link_instance.GetLinkDocument() #Get Link Document == doc
        linked_wall = linked_doc.GetElement(linked_element_id) #Get Linked Element  (selected)
        link_transform = link_instance.GetTotalTransform()  


    #Get Wall Location and Orientation (link coords)
    loc_curve = linked_wall.Location.Curve
    wall_direction = (loc_curve.GetEndPoint(1) - loc_curve.GetEndPoint(0)).Normalize()
    wall_normal = XYZ.BasisZ.CrossProduct(wall_direction).Normalize()

    wall_cs = Transform.Identity
    wall_cs.BasisX = wall_direction 
    wall_cs.BasisY = XYZ.BasisZ
    wall_cs.BasisZ = wall_normal
    wall_cs.Origin = loc_curve.Zero

    #Transform Wall Coordinate System to Host Coordinates
    pts_in_link = [link_transform.Inverse.OfPoint(p) for p in bbox_pts]

    #Transform BBox Points to Wall Local Coordinates
    pts_local = [wall_cs.Inverse.OfPoint(p) for p in pts_in_link]

    minX = min(p.X for p in pts_local)
    maxX = max(p.X for p in pts_local)
    minY = min(p.Y for p in pts_local)
    maxY = max(p.Y for p in pts_local)
    minZ = min(p.Z for p in pts_local)
    maxZ = max(p.Z for p in pts_local)


    width = maxX - minX
    height = maxY - minY
    depth = maxZ - minZ
    center_local = XYZ((minX + maxX) / 2, (minY + maxY) / 2, (minZ + maxZ) / 2)

    #Transform Center back to Host Coordinates
    center_in_link = wall_cs.OfPoint(center_local)
    center_in_host = link_transform.OfPoint(center_in_link)

    #Place Opening Family Instance
    #Get Family Symbol
    family_name = "CCL OPE Family - 2023"
    family_symbol_name = "KGE_Ope"

    #Search for Family Symbol
    opening_collector = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()
    opening_symbol = None

    for fs in opening_collector:
        if fs.Family.Name == family_name and fs.Name == family_symbol_name:
            opening_symbol = fs
            break

    if not opening_symbol:
        forms.alert("Family Symbol {} not found in the project.".format(family_symbol_name), title="Family Symbol Not Found", warn_icon=True)
        raise Exception("Family Symbol not found")

    #Activate Family Symbol if not active
    if not opening_symbol.IsActive:
        opening_symbol.Activate()
        doc.Regenerate()

    #Place Family Instance
    t = Transaction(doc, "Place Openings in Containments")
    t.Start()

    opening_instance = doc.Create.NewFamilyInstance(center_in_host, opening_symbol, StructuralType.NonStructural)
    rotation_axis = Line.CreateBound(center_in_host, center_in_host + wall_normal)
    angle = XYZ.BasisX.AngleTo(wall_direction)
    ElementTransformUtils.RotateElement(doc, opening_instance.Id, rotation_axis, angle)


except Exception as e:
    print("Operation cancelled or failed: {}".format(e))



#Select Containment Elements

print(bbox.Min, bbox.Max)
print(bbox_center)
print(bbox_pts)
