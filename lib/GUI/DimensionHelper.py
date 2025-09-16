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
    def get_family_reference_planes(family_instance):
        """
        Retorna os Reference Planes da família que correspondem aos nomes ALWAYS_DIM e CONDITIONAL_DIM
        """
        planes = []
        for rp in family_instance.Symbol.Family.GetFamilySymbolIds():
            # rp pode ser FamilyElementId, precisa converter para Element
            elem = family_instance.Document.GetElement(rp)
            if isinstance(elem, ReferencePlane) and elem.Name in DimensionHelper.ALWAYS_DIM + list(DimensionHelper.CONDITIONAL_DIM.keys()):
                planes.append(elem)
        return planes

    @staticmethod
    def create_dimensions_from_planes(doc, section_view, family_instance):
        """
        Cria cotas na Section View a partir dos Reference Planes da família
        """
        planes = DimensionHelper.get_family_reference_planes(family_instance)
        if not planes:
            print("No reference planes found for dimensioning.")
            return None

        # transforma os pontos da família para o espaço do projeto
        transform = family_instance.GetTransform()
        points_project = []
        for rp in planes:
            if hasattr(rp, "Curve") and rp.Curve is not None:
                loc_point = rp.Curve.Evaluate(0.5, True)  # ponto central da linha
                points_project.append(transform.OfPoint(loc_point))
            else:
                # caso seja plano sem curva
                try:
                    points_project.append(transform.OfPoint(rp.GetPlane().Origin))
                except:
                    continue

        if len(points_project) < 2:
            print("Not enough points for dimensioning.")
            return None

        # criar ReferenceArray e linhas de dimensão
        ref_array = ReferenceArray()
        # Transformação: usamos referência indireta, criando pequenas linhas para referência
        # No caso de planos nomeados, podemos criar dimension entre pontos
        for i in range(len(points_project)):
            ref_array.Append(XYZ(points_project[i].X, points_project[i].Y, points_project[i].Z))

        # Dimensão vertical (UpDirection da Section)
        line_v = Line.CreateBound(points_project[0], points_project[-1])
        dim_v = doc.Create.NewDimension(section_view, line_v, ref_array)

        # Dimensão horizontal (RightDirection da Section)
        line_h = Line.CreateBound(points_project[0], points_project[-1])
        dim_h = doc.Create.NewDimension(section_view, line_h, ref_array)

        return [dim_v, dim_h]
