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
                minX_overall, minY_overall, minZ_overall = None, None, None
                maxX_overall, maxY_overall, maxZ_overall = None, None, None

                for e in containment_elements:
                    el = doc.GetElement(e)
                    bbox = el.get_BoundingBox(None)

                    min_pt = bbox.Min
                    max_pt = bbox.Max

                    if minX_overall is None:
                        minX_overall, minY_overall, minZ_overall = min(min_pt.X, min_pt.Y, min_pt.Z)
                        maxX_overall, maxY_overall, maxZ_overall = max(max_pt.X, max_pt.Y, max_pt.Z)
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
        except Exception as e:
            print("Error occurred while placing openings: {}".format(e))
            traceback.print_exc()

        return overall_bbox, overall_bbox_center