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

def get_solids(element, options):
    solids = []
    geom = element.get_Geometry(options)
    for g in geom:
        if isinstance(g, Solid) and g.Volume > 0:
            solids.append(g)
        elif isinstance(g, GeometryInstance):
            tr = g.Transform
            for sg in g.GetInstanceGeometry():
                if isinstance(sg, Solid) and sg.Volume > 0:
                    sg_transformed = SolidUtils.CreateTransformed(sg, tr)
                    solids.append(sg_transformed)
    return solids

def get_solid_bbox(solids):
    min_pt, max_pt = None, None
    for s in solids:
        bbox = s.GetBoundingBox()
        if not bbox:
            continue
        if not min_pt:
            min_pt, max_pt = bbox.Min, bbox.Max
        else:
            min_pt = XYZ(min(min_pt.X, bbox.Min.X),
                        min(min_pt.Y, bbox.Min.Y),
                        min(min_pt.Z, bbox.Min.Z))
            max_pt = XYZ(max(max_pt.X, bbox.Max.X),
                        max(max_pt.Y, bbox.Max.Y),
                        max(max_pt.Z, bbox.Max.Z))
    return (min_pt, max_pt)

def get_transformed_bbox(bbox, link_transform, offset=1):
    if not bbox:
        return None

    min_pt = link_transform.OfPoint(bbox.Min)
    max_pt = link_transform.OfPoint(bbox.Max)

    minX = min(min_pt.X, max_pt.X) - offset
    minY = min(min_pt.Y, max_pt.Y) - offset
    minZ = min(min_pt.Z, max_pt.Z) - offset
    maxX = max(min_pt.X, max_pt.X) + offset
    maxY = max(min_pt.Y, max_pt.Y) + offset
    maxZ = max(min_pt.Z, max_pt.Z) + offset

    bbox_transformed = BoundingBoxXYZ()
    bbox_transformed.Min = XYZ(minX, minY, minZ)
    bbox_transformed.Max = XYZ(maxX, maxY, maxZ)

    return bbox_transformed