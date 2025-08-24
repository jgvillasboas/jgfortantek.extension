from Autodesk.Revit.DB import *

def get_section_type(doc):
    views_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
    return [vt for vt in views_types if vt.ViewFamily == ViewFamily.Section][0]

def create_transform(basis_x, center):
    basis_y = XYZ.BasisZ
    basis_z = basis_x.CrossProduct(basis_y).Normalize()

    t = Transform.Identity
    t.BasisX = basis_x
    t.BasisY = basis_y
    t.BasisZ = basis_z
    t.Origin = center
    return t

def create_crop_box(transform, width, height, depth):
    crop = BoundingBoxXYZ()
    crop.Transform = transform
    crop.Min = XYZ(-width / 2, -height / 2, -depth / 2)
    crop.Max = XYZ(width / 2, height / 2, depth / 2)
    return crop