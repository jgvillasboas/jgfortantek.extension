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

#Select Elements id for each element selected
selected_ids = selection.GetElementIds()
offset = 100 / 304.8  # 100mm in feet

#Collect View Types
view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
section_type = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Section][0]
viewTypeId = section_type.Id

#Geometry Options
opt = Options()
opt.ComputeReferences = True
opt.IncludeNonVisibleObjects = False

# Transaction
t = Transaction(doc, "Transaction Start")
t.Start()  

#Iterate for each element selected
for e_id in selected_ids:
    e = doc.GetElement(e_id) #get Element Id
    type_name = e.Symbol.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString() #get Type Name
    Rod_length_mm = e.LookupParameter("Rod 2 Length - 30 mm").AsDouble() #Get Rod Lenght in mm
    Rod_length_ft = (Rod_length_mm + 75) / 304.8 #Transform to feet

    #Filter if Element has "SUR_" in Family Name
    if isinstance(e, FamilyInstance) and \
       e.Category.Id.IntegerValue == int(BuiltInCategory.OST_StructuralFraming) and \
       "SUR_" in e.Symbol.Family.Name:
        
        #Get Solid
        geom = e.get_Geometry(opt)
        min_pt, max_pt = None, None

        for g in geom:
            solids = []
            if isinstance(g, Solid) and g.Volume > 0:
                solids.append(g)
            elif isinstance(g, GeometryInstance):
                tr = g.Transform
                for sg in g.GetInstanceGeometry():
                    if isinstance(sg, Solid) and sg.Volume > 0:
                        sg_transformed = SolidUtils.CreateTransformed(sg, tr)
                        solids.append(sg_transformed)

            for s in solids:
                bbox_solid = s.GetBoundingBox()
                if not bbox_solid:
                    continue
                if not min_pt:
                    min_pt, max_pt = bbox_solid.Min, bbox_solid.Max
                else:
                    min_pt = XYZ(min(min_pt.X, bbox_solid.Min.X),
                                min(min_pt.Y, bbox_solid.Min.Y),
                                min(min_pt.Z, bbox_solid.Min.Z))
                    max_pt = XYZ(max(max_pt.X, bbox_solid.Max.X),
                                max(max_pt.Y, bbox_solid.Max.Y),
                                max(max_pt.Z, bbox_solid.Max.Z))

            center = (min_pt + max_pt) / 2

        # Get Bounding Box
        bbox = e.get_BoundingBox(None)
        center_bbox = (bbox.Min + bbox.Max) / 2 #Get Bounding Box Center
        
        if not bbox:
            continue

        #Get Bounding Box Points
        p1 = XYZ(bbox.Min.X, bbox.Min.Y, bbox.Min.Z)
        p2 = XYZ(bbox.Min.X, bbox.Max.Y, bbox.Min.Z)
        p3 = XYZ(bbox.Max.X, bbox.Min.Y, bbox.Min.Z)
        p4 = XYZ(bbox.Max.X, bbox.Max.Y, bbox.Min.Z)
        p5 = XYZ(bbox.Min.X, bbox.Min.Y, bbox.Max.Z)

        #Calculate Vectors
        vector_x = p3 - p1
        vector_y = p2 - p1

        #Get Vector Lengths
        len_x = vector_x.GetLength()
        len_y = vector_y.GetLength()

        #Check if element is Horizontal
        if len_x > len_y:
            basis_x = vector_x.Normalize() #Width Vector (Horizontal)
        else: 
            basis_x = vector_y.Normalize() #Width Vector (Vertical)

        basis_y = XYZ.BasisZ #Height Vector
        basis_z = basis_x.CrossProduct(basis_y).Normalize() #Depth Vector
        
        # Create section position
        section_transform = Transform.Identity #Transforming Coordinates
        section_transform.BasisX = basis_x
        section_transform.BasisY = basis_y
        section_transform.BasisZ = basis_z
        section_transform.Origin = center_bbox

        #Crop View Dimensions
        width = max(max_pt.X - min_pt.X + offset, .1)
        height = max(max_pt.Z - min_pt.Z + offset, .1)
        depth = max((max_pt.Y - min_pt.Y) + offset, .1)
        print("Width: {}, Height: {}, Depth: {}".format(width, height, depth))
        
        #Crop View Position
        CropView = BoundingBoxXYZ()
        CropView.Transform = section_transform
        CropView.Min = XYZ(-width / 2, -height / 2, -depth / 2)
        CropView.Max = XYZ(width / 2, height / 2, depth / 2)

        # Create section view
        try:
            sectionView = ViewSection.CreateSection(
                doc,
                viewTypeId,
                CropView
            )

            sectionView.Name = "{}".format(type_name)
            print("Section created: {} \n".format(sectionView.Name))

        except Exception as ex:
            print("Error creating section for element {}: {}".format(type_name, str(ex)))

t.Commit()


        
