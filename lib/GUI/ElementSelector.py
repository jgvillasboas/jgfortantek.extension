from Autodesk.Revit.UI.Selection import ISelectionFilter, ObjectType
from Autodesk.Revit.DB import *

from pyrevit import forms
import traceback

uidoc = __revit__.ActiveUIDocument # type: ignore
doc = __revit__.ActiveUIDocument.Document # type: ignore #type: Document
selection = uidoc.Selection


class CableTraySelectionFilter(ISelectionFilter):
    def AllowElement(self, element):
        try:
            return element.Category.Id.IntegerValue == int(BuiltInCategory.OST_CableTray) or element.Category.Id.IntegerValue == int(BuiltInCategory.OST_DuctCurves)
        except:
            return False

    def AllowReference(self, reference, position):
        return False
    

class Selector():
    @staticmethod
    def CableTraySelector(containment_elements=None):
        print("Select Containments:")
        containment_elements = selection.PickObjects(ObjectType.Element, CableTraySelectionFilter(), "Select Containment Elements to Place Openings:")
        count = len(containment_elements)
        try:
            while len(containment_elements) == 0:
                try: 
                    #Get Containment Elements:
                    containment_elements = selection.PickObjects(ObjectType.Element, "Select Containment Elements to Place Openings:", CableTraySelectionFilter())

                    count = len(containment_elements)

                    if count == 0:
                        forms.alert("No containment elements selected. Please select at least one containment", title="No Selection", warn_icon=True)

                except Exception as e:
                    print("Error occurred while selecting containment elements: {}".format(e))
                    traceback.print_exc()
                    containment_elements = []

            if count == 1:
                el = doc.GetElement(containment_elements[0].ElementId)
                overall_bbox = el.get_BoundingBox(None)

            else:
                minX_overall, minY_overall, minZ_overall = 1e9, 1e9, 1e9
                maxX_overall, maxY_overall, maxZ_overall = -1e9, -1e9, -1e9

                for e in containment_elements:
                    el = doc.GetElement(e)
                    bbox = el.get_BoundingBox(None)

                    if not bbox:
                        continue

                    min_pt = bbox.Min
                    max_pt = bbox.Max

                    if minX_overall is None:
                        minX_overall = min(minX_overall, min_pt.X)
                        minY_overall = min(minY_overall, min_pt.Y)
                        minZ_overall = min(minZ_overall, min_pt.Z)

                        maxX_overall = max(maxX_overall, max_pt.X)
                        maxY_overall = max(maxY_overall, max_pt.Y)
                        maxZ_overall = max(maxZ_overall, max_pt.Z)

                    else:
                        minX_overall = min(minX_overall, min_pt.X)
                        minY_overall = min(minY_overall, min_pt.Y)
                        minZ_overall = min(minZ_overall, min_pt.Z)

                        maxX_overall = max(maxX_overall, max_pt.X)
                        maxY_overall = max(maxY_overall, max_pt.Y)
                        maxZ_overall = max(maxZ_overall, max_pt.Z)

                overall_bbox = BoundingBoxXYZ()
                overall_bbox.Min = XYZ(minX_overall, minY_overall, minZ_overall)
                overall_bbox.Max = XYZ(maxX_overall, maxY_overall, maxZ_overall)
                overall_bbox_center = XYZ((overall_bbox.Min.X + overall_bbox.Max.X) / 2,
                                        (overall_bbox.Min.Y + overall_bbox.Max.Y) / 2,
                                        (overall_bbox.Min.Z + overall_bbox.Max.Z) / 2)
                bbox_pts = [
                    XYZ(overall_bbox.Min.X, overall_bbox.Min.Y, overall_bbox.Min.Z),
                    XYZ(overall_bbox.Min.X, overall_bbox.Min.Y, overall_bbox.Max.Z),
                    XYZ(overall_bbox.Min.X, overall_bbox.Max.Y, overall_bbox.Min.Z),
                    XYZ(overall_bbox.Min.X, overall_bbox.Max.Y, overall_bbox.Max.Z),
                    XYZ(overall_bbox.Max.X, overall_bbox.Min.Y, overall_bbox.Min.Z),
                    XYZ(overall_bbox.Max.X, overall_bbox.Min.Y, overall_bbox.Max.Z),
                    XYZ(overall_bbox.Max.X, overall_bbox.Max.Y, overall_bbox.Min.Z),
                    XYZ(overall_bbox.Max.X, overall_bbox.Max.Y, overall_bbox.Max.Z)
                    ]
                
        except Exception as e:
            print("Error occurred while placing openings: {}".format(e))
            traceback.print_exc()

        return overall_bbox, overall_bbox_center, bbox_pts

class FamilySymbolName:
    @staticmethod
    def get_family_symbol(doc, family_name, family_symbol_name):
        collector = FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_GenericModel)

        for fs in collector:
            fam_name = fs.Family.Name
            type_name = fs.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()

            if fam_name.strip() == family_name.strip() and type_name.strip() == family_symbol_name.strip():
                return fs
            
        return None