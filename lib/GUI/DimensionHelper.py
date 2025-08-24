# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *

class DimensionHelper:

    ALWAYS_DIM = [
        "Bottom",
        "Tier1_Bottom",
        "Tier1_Top",
        "2ndTop",
        "1st Top"
    ]

    CONDITIONAL_DIM = {
        "Tier2_Bottom": "Tier 2",
        "Tier2_Top": "Tier 2",
        "Tier3_Bottom": "Tier 3",
        "Tier3_Top": "Tier 3",
        "Tier4_Bottom": "Tier 4",
        "Tier4_Top": "Tier 4",
        "Tier5_Bottom": "Tier 5",
        "Tier5_Top": "Tier 5",
        "Tier6_Bottom": "Tier 6",
        "Tier6_Top": "Tier 6",
    }

    @staticmethod
    def create_vertical_chain_dimension(doc, sectionView, familyInstance):
        """
        Cria uma cadeia de cotas verticais entre os reference planes da família.
        """
        try:
            refs = []
            geom_opts = Options()
            geom = familyInstance.get_Geometry(geom_opts)

            for g in geom:
                if isinstance(g, GeometryInstance):
                    inst_geom = g.GetSymbolGeometry()
                    for sg in inst_geom:
                        if isinstance(sg, ReferencePlane):
                            name = sg.Name

                            # Sempre cotar
                            if name in DimensionHelper.ALWAYS_DIM:
                                refs.append((sg.Reference, sg.BubbleEnd))

                            # Condicionais
                            elif name in DimensionHelper.CONDITIONAL_DIM:
                                param_name = DimensionHelper.CONDITIONAL_DIM[name]
                                param = familyInstance.LookupParameter(param_name)
                                if param and param.AsInteger() == 1:
                                    refs.append((sg.Reference, sg.BubbleEnd))

            if len(refs) < 2:
                return None

            # Ordenar pelo Z (altura)
            refs_sorted = sorted(refs, key=lambda x: x[1].Z)

            # Criar ReferenceArray
            refArray = ReferenceArray()
            for r, _ in refs_sorted:
                refArray.Append(r)

            # Criar linha vertical passando pelo X/Y do primeiro ponto
            base_pt = refs_sorted[0][1]
            top_pt = refs_sorted[-1][1]
            offset = 1.0 / 304.8  # 1mm em pés, só para afastar da geometria
            line = Line.CreateBound(
                XYZ(base_pt.X + offset, base_pt.Y, base_pt.Z),
                XYZ(top_pt.X + offset, top_pt.Y, top_pt.Z)
            )

            # Criar dimensão em cadeia
            dim = doc.Create.NewDimension(sectionView, line, refArray)
            return dim

        except Exception as ex:
            print("Erro ao criar dimensões: {}".format(ex))
            return None
