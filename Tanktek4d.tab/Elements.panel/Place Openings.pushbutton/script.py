# -*- coding: utf-8 -*-
print("Placing Wall Openings in Selected Containments... ")
#Revit Imports
from Autodesk.Revit.UI.Selection import ISelectionFilter, ObjectType
from Autodesk.Revit.DB import *

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

bbox, bbox_center = Selector.CableTraySelector()
print(bbox.Min, bbox.Max)
print(bbox_center)


