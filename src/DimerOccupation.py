
from src.CI_ORDERING import CI_ORDERING
from src.building_blocks.DimerDeterminant import DimerDeterminant
from src.building_blocks.MonomerOccupation import MonomerOccupation
from src.mathematics.Sign import SIGN, build_product_from_signs_in_str, split_string_into_signed_parts
from src.latex.wrap_tikz_picture import wrap_tikz_picture
from src.symmetries.POINTGROUP import POINTGROUP


class DimerOccupation:

    def __init__(self, monomer_occupation_1: MonomerOccupation, monomer_occupation_2: MonomerOccupation, sign:SIGN, point_group:POINTGROUP):
        self.monomer_occupation_1 = monomer_occupation_1
        self.monomer_occupation_2 = monomer_occupation_2
        self.point_group = point_group
        self.sign = sign
        self.prefactor = 1

    def latex_picture(self,draw_label:bool=False):
        eq = self.sign.value + r" \left(" + wrap_tikz_picture( self.monomer_occupation_1.latex_picture(draw_label=draw_label) ) + "\n"
        eq += r"\quad" + wrap_tikz_picture( self.monomer_occupation_2.latex_picture(draw_label=draw_label) ) + r"\right) " + "\n"
        return eq

    def written_in_monomer_ci_vectors(self, ordering:CI_ORDERING):
        eq = self.sign.value + str(abs(self.prefactor)) + r" \cdot{} "
        eq += self.monomer_occupation_1.latex_ci_equation(ordering=ordering)
        eq += r" \cdot{} "
        eq += self.monomer_occupation_2.latex_ci_equation(ordering=ordering)
        return eq

    def monomer_determinants(self, multiplied_out:bool ):
        eq = self.sign.value + str(abs(self.prefactor)) + r" \cdot{} \left| "
        eq += self.monomer_occupation_1.monomer_determinant_content(side = "l", multiplied_out=multiplied_out)
        eq += self.monomer_occupation_2.monomer_determinant_content(side = "r", multiplied_out=multiplied_out)
        eq += r"\right|"
        return eq

    def get_multiplied_out_determinants(self):
        self.multiply_out()
        eq = "\n".join([det.determinants_string() for det in self.determinants])
        return eq


    def multiply_out(self):
        terms = self.monomer_occupation_1.get_single_occupied_orbital_labels(side="l", multiplied_out=True)
        terms.extend(self.monomer_occupation_2.get_single_occupied_orbital_labels(side="l", multiplied_out=True))
        terms = [split_string_into_signed_parts(term) for term in terms]
        assert len(terms) == 4 # number of unpaired electrons in monomer
        ''' 4 possible cases for left * right
           Fall 1:     (l1+r1)*(l2+r2) = l1*l2 + r1*l2 + l1*r2 + r1*r2
           Fall 2:     (l1-r1)*(l2-r2) = l1*l2 - r1*l2 - l1*r2 + r1*r2
           Fall 3:     (l1+r1)*(l2-r2) = l1*l2 + r1*l2 - l1*r2 - r1*r2
           Fall 4:     (l1-r1)*(l2+r2) = l1*l2 - r1*l2 + l1*r2 - r1*r2
        '''
        self.determinants = []
        for a in terms[0]:
            for b in terms[1]:
                for c in terms[2]:
                    for d in terms[3]:
                        total_product_string = a+b+c+d
                        sign = build_product_from_signs_in_str(total_product_string)
                        det = DimerDeterminant([a,b,c,d], sign=sign, point_group=self.point_group)
                        self.determinants.append(det)
        return



