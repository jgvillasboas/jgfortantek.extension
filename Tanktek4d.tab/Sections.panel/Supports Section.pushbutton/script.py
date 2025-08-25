# -*- coding: utf-8 -*-
print("Creating Supports Section Views")
#Revit Imports
from Autodesk.Revit.UI.Selection import ISelectionFilter, ObjectType
from Autodesk.Revit.DB import *

#pyRevit Imports
from pyrevit import script, forms, EXEC_PARAMS

#General Imports
import traceback, math, os, sys, clr, wpf

#Custom Imports
from GUI import GetGeometry
from GUI import SectionHelper
from GUI import ViewHelper
from GUI.TemplateSelector import TemplateSelector
from GUI.DimensionHelper import DimensionHelper

#Variables
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document #type: Document
selection = uidoc.Selection

#Select Elements id for each element selected
selected_ids = selection.GetElementIds()
offset = 100 / 304.8  # 100mm in feet

#Collect View Types
view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
section_type = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Section][0]
viewTypeId = section_type.Id

#Collect View Templates
view_templates = FilteredElementCollector(doc).OfClass(View).WhereElementIsNotElementType().ToElements()
templates = [t for t in view_templates if t.IsTemplate]

if view_templates:
    win = TemplateSelector([t.Name for t in templates])
    result = win.ShowDialog()
    if not result:
        forms.alert("Operation cancelled.", exitscript=True)
        sys.exit()

    selected_name = win.listbox.SelectedItem
    selected_template = next((t for t in templates if t.Name == selected_name), None)

else:
    forms.alert("No view templates found in the document.", exitscript=True)
    sys.exit()

#Geometry Options
opt = Options()
opt.ComputeReferences = True
opt.IncludeNonVisibleObjects = False

# Transaction
t = Transaction(doc, "Create Section")
t.Start()  

#Iterate for each element selected
for e_id in selected_ids:
    e = doc.GetElement(e_id) #get Element Id
    type_name = e.Symbol.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString() #get Type Name

    #Filter if Element has "SUR_" in Family Name
    if isinstance(e, FamilyInstance) and \
       e.Category.Id.IntegerValue == int(BuiltInCategory.OST_StructuralFraming) and \
       "SUR_" in e.Symbol.Family.Name:
        
        #Get Solid
        solids = GetGeometry.get_solids(e, opt)
        if not solids:
            continue

        min_pt, max_pt = GetGeometry.get_solid_bbox(solids) #Get Solid Bounding Box
        bbox = e.get_BoundingBox(None) #Get Bouding Box
        center = (bbox.Min + bbox.Max) / 2 #Get Bounding Box Center
        
        if not bbox:
            continue

        #Get Bounding Box Points
        p1, p2, p3 = XYZ(bbox.Min.X, bbox.Min.Y, bbox.Min.Z), XYZ(bbox.Min.X, bbox.Max.Y, bbox.Min.Z), XYZ(bbox.Max.X, bbox.Min.Y, bbox.Min.Z)

        vector_x, vector_y = p3 - p1, p2 - p1 #Calculate Vectors

        len_x, len_y = vector_x.GetLength(), vector_y.GetLength()  #Get Vector Lengths
        
        basis_x = (vector_x if len_x > len_y else vector_y).Normalize() #Check if element is Horizontal

        section_transform = ViewHelper.create_transform(basis_x, center) #Create Section Transform

        #Crop View Dimensions
        width, height, depth = max(max_pt.X - min_pt.X + offset, .1), max(max_pt.Z - min_pt.Z + offset, .1), max((max_pt.Y - min_pt.Y) + offset, .1)
        
        #Crop View Position
        crop_box = ViewHelper.create_crop_box(section_transform, width, height, depth)

        # Create section view

        existing_view_name = {v.Name for v in FilteredElementCollector(doc).OfClass(View).WhereElementIsNotElementType()}
        if type_name in existing_view_name:
            print("Section view with name '{}' already exists. Skipping...".format(type_name))
            continue

        try:
            section = SectionHelper.create_section_view(doc, viewTypeId, crop_box, name = type_name)
            if section:
                print("Section created: {} \n".format(section.Name))
            if selected_template:
                section.ViewTemplateId = selected_template.Id

        except Exception as ex:
            print("Error creating section view: {}".format(ex))
            continue

            

t.Commit()


        
