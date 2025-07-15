# -*- coding: utf-8 -*-

#Revit Imports
from Autodesk.Revit.UI.Selection import ISelectionFilter, ObjectType
from Autodesk.Revit.DB import *

#pyRevit Imports
from pyrevit import script, forms, EXEC_PARAMS

#General Imports
import traceback, math, os, sys

#Custom Imports
from GUI.SelectFromDict import select_from_dict
from Snippets._vectors import rotate_vector
from Snippets._views import SectionGenerator

#Variables
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document #type: Document
selection = uidoc.Selection

output = script.get_output()

#FUNCTIONS
def place_views_on_sheet (doc, views, new_sheet):
    positions = [
        XYZ(-0.85, 0.65, 0),
        XYZ(-0.5, 0.65, 0),
        XYZ(-0.85, 0.35, 0)
    ]

    for n, view in enumerate(views):
        if Viewport.CannAddViewToSheet(doc, new_sheet.Id, view.Id):
            pt = positions [n]
            viewport = Viewport.Create(doc, new_sheet.Id, view.Id, pt)

def __init__(self, el):
    self.el = el

def get_generic_properties(self):
    
    el_type = doc.GetElement(self.el.GetTypeId()) if isinstance(self.el, Element) else None
    BB = self.el.get_BoundingBox(None)
    BB_typ = el_type.get_BoundingBox(None)
    self.origin = (BB.Max + BB.Min) / 2

    el_fam = el_type.Family
    el_placement = el_fam.FamilyPlacementType
    fpt = FamilyPlacementType

    self.width = (BB_typ.Max.X - BB_typ.Min.X)
    self.height = (BB_typ.Max.Z - BB_typ.Min.Z)
    self.depth = (BB_typ.Max.Y - BB_typ.Min.Z)

    pt_start = XYZ(BB_typ.Min.X, (BB_typ.Min.Y + BB_typ.Max.Y) / 2, BB_typ.Min.Z)
    pt_end = XYZ(BB_typ.Max.X, (BB_typ.Min.Y + BB_typ.Max.Y) / 2, BB_typ.Max.Z)

    self.vector = pt_end - pt_start

    try:
        rotation_rad = self.el.Location.Rotation
        self.vector = rotate_vector(self.vector, rotation_rad)
    except:
        if EXEC_PARAMS.debug_mode:
            import traceback
            print(traceback.format_exc())
    return

#CLASSES
class ElementProperties():
     origin = None
     vector = None
     width = None
     height = None

     offset = 1.0
     depth = 1.0
     depth_offset = 1.0

     valid = False


#MAIN
bic = BuiltInCategory
select_opts = {'Walls'  :bic.OST_Walls,
               'Supports' : [bic.OST_StructuralFraming, bic.OST_StructuralFramingOther]
               }

selected_opts = select_from_dict(select_opts, 
                                 title = 'Title',
                                 label = 'Select Categories to Pick Elements',
                                 version = 'Version 1.0',
                                 SelectMultiple = False
                                 )

def flatten_list(lst):
        new_lst = []
        for i in lst:
            if isinstance(i, list):
                new_lst += 1
            else:
                new_lst.append(i)
        return new_lst

selected_opts = flatten_list(selected_opts)

if not selected_opts:
        forms.alert('No Category was selected. Please Try Again', title='Title', exitscript=True)

#----------------------------------------------------------

class EF_SelectionFilter(ISelectionFilter):
    def __init__(self, list_types_or_cats):
        """ISelection Filter made fo filter with types
        :param allowed_types: list of allowed Types"""

        self.list_types_or_cats = [ElementId(i) if type(i) == BuiltInCategory else i for i in list_types_or_cats]
    
    def AllowElement(self, elem):
        if elem.ViewSpecific:
            return False
        
        if type(elem) in self.list_types_or_cats:
            return True
        
        elif elem.Category.ID in self.list_types_or_cats:
            return True
        
selected_elems = []

try: 
    ISF = EF_SelectionFilter(selected_opts)
    with forms.WarningBar(title='Select Elements and click Finish'):
        ref_selected_elems = uidoc.Selection.PickObjects(ObjectType.Element, ISF)
    
    selected_elems = [doc.GetElement(ref) for ref in ref_selected_elems]

except: 
    if EXEC_PARAMS.debug_mode:
        import traceback

        print(traceback.format_exc())   

if not selected_elems:
    error_msg = "No Elements were selected .\nPlease Try Again"
    forms.alert(error_msg, title="Selection has Failed", exitscript=True)
         
views = FilteredElementCollector(doc).OfClass(View).ToElements()
dict_view_templates = {v.Name:v for v in views if v.IsTemplate}
dict_view_templates['None'] = None
  
    #Select ViewTemplate
sel_view_template = select_from_dict(dict_view_templates,
                                    title = 'View',
                                    label = 'Select ViewTemplate for Sections',
                                    version = 'Version: 1.0',
                                    SelectMultiple = False)

if sel_view_template:
    sel_view_template = sel_view_template[0]
    
#Transaction
t = Transaction(doc, 'Section Generator')
t.Start()

table_data = []
new_view = []

from pyrevit.forms import ProgressBar

counter = 0
max_value = len(selected_ids)
with ProgressBar(cancellabel=True) as pb:
    for el in selected_ids:
        if pb.cancelled:
            break

        counter  += 1
        pb.update_progress(counter, max_value)

        
        E = ElementProperties()

        gen = SectionGenerator(doc,
                                origin = E.origin,
                                vector = E.vector,
                                width = E.width,
                                height = E.height,
                                offset = E.offset,
                                depth = E.depth,
                                depth_offset = E.depth_offset)
        
        el_type = doc.GetElement(el.GetTypeId())
        type_name = Element.Name.GetValue(el_type)
        cat_name = el.Category.Name

        view_name_base = '{}_{}'.format(type_name, el.Id)
        elev, cross, plan = gen.create_sections(view_name_base=view_name_base)

        if sel_view_template:
            elev.ViewTemplateId = sel_view_template.Id
            cross.ViewTemplateId = sel_view_template.Id
            plan.ViewTemplateId = sel_view_template.Id

        
t.Commit()

try:
    #👀 DISPLAY TABLE
    output.print_table(table_data=table_data,
                       title="New Sections",
                       columns=["Category","TypeName","Element", "Sheet", "Elevation", "Cross", "Plan"])
except:
    if EXEC_PARAMS.debug_mode:
        import traceback

        print(traceback.format_exc())
    # output.log_error(traceback.format_exc())