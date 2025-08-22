from Autodesk.Revit.DB import XYZ, BoundingBoxXYZ

def make_section_bbox(bbox, section_transform, offset):
    """Create a bounding box aligned with section transform"""
    corners = [
        XYZ(bbox.Min.X, bbox.Min.Y, bbox.Min.Z),
        XYZ(bbox.Min.X, bbox.Min.Y, bbox.Max.Z),
        XYZ(bbox.Min.X, bbox.Max.Y, bbox.Min.Z),
        XYZ(bbox.Min.X, bbox.Max.Y, bbox.Max.Z),
        XYZ(bbox.Max.X, bbox.Min.Y, bbox.Min.Z),
        XYZ(bbox.Max.X, bbox.Min.Y, bbox.Max.Z),
        XYZ(bbox.Max.X, bbox.Max.Y, bbox.Min.Z),
        XYZ(bbox.Max.X, bbox.Max.Y, bbox.Max.Z),
    ]

    local_pts = [section_transform.OfPoint(corner) for corner in corners]

    local_min = XYZ(min(pt.X for pt in local_pts), min(pt.Y for pt in local_pts), min(pt.Z for pt in local_pts))
    local_max = XYZ(max(pt.X for pt in local_pts), max(pt.Y for pt in local_pts), max(pt.Z for pt in local_pts))

    bboxXYZ = BoundingBoxXYZ()
    bboxXYZ.Transform = section_transform
    bboxXYZ.Min = local_min
    bboxXYZ.Max = local_max

    return bboxXYZ
