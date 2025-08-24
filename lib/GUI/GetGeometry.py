from Autodesk.Revit.DB import *

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
