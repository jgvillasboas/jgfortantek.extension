from Autodesk.Revit.DB import *

def create_section_view(doc, view_type_id, crop_box, name = "Section"):
    try:
        section = ViewSection.CreateSection(doc, view_type_id, crop_box)
        section.Name = name
        return section
    except Exception as ex:
        print("Error creating section view: {}".format(ex))
        return None
        