import re

from src.CI_ORDERING import CI_ORDERING
from src.building_blocks.DimerDeterminant import DimerDeterminant
from src.building_blocks.MonomerOccupation import MonomerOccupation
from src.mathematics.Sign import SIGN, build_product_from_signs_in_str, split_string_into_signed_parts
from src.latex.wrap_tikz_picture import wrap_tikz_picture
from src.symmetries.POINTGROUP import POINTGROUP
from src.mathematics.get_all_combinations import get_all_combinations


class DimerOccupation:

    def __init__(self, monomer_occupation_1: MonomerOccupation, monomer_occupation_2: MonomerOccupation, sign:SIGN, point_group:POINTGROUP):
        self.monomer_occupation_1 = monomer_occupation_1
        self.monomer_occupation_2 = monomer_occupation_2
        self.monomer_occupation_1.set_side("l")
        self.monomer_occupation_2.set_side("r")

        self.determinants = []

        self.point_group = point_group
        self.sign = sign
        self.prefactor = 1

    def latex_picture(self,draw_label:bool=False):
        eq = self.sign.value + r" \left(" + wrap_tikz_picture( self.monomer_occupation_1.latex_picture(draw_label=draw_label) ) + "\n"
        eq += r"\quad" + wrap_tikz_picture( self.monomer_occupation_2.latex_picture(draw_label=draw_label) ) + r"\right) " + "\n"
        return eq

    def written_in_monomer_ci_vectors(self, ordering:CI_ORDERING, multiplied_out:bool):
        eq = self.sign.value
        if abs(self.prefactor) != 1:
            eq += str(abs(self.prefactor)) + r" \cdot{} "
        eq += self.monomer_occupation_1.latex_ci_equation(ordering=ordering, multiplied_out=multiplied_out)
        eq += r" \cdot{} "
        eq += self.monomer_occupation_2.latex_ci_equation(ordering=ordering, multiplied_out=multiplied_out)
        return eq

    def monomer_determinants(self, multiplied_out:bool ):
        eq = self.sign.value + str(abs(self.prefactor)) + r" \cdot{} \left| "
        eq += self.monomer_occupation_1.monomer_determinant_content(side = "l", multiplied_out=multiplied_out)
        eq += self.monomer_occupation_2.monomer_determinant_content(side = "r", multiplied_out=multiplied_out)
        eq += r"\right|"
        return eq

    def _get_orbital_occ_list(self, values:list[str]):
        orbitals = []
        for s in values:
            orbital_LC = re.search(r'\((.*?)\)', s).group(1)
            occupation = int( re.search(r'\{(.*?)\}', s).group(1) )
            included_orbitals = split_string_into_signed_parts(orbital_LC)
            for orbital_sym_label in included_orbitals:
                sign = "".join([i for i in orbital_sym_label if i in [SIGN.PLUS.value, SIGN.MINUS.value]])
                if len(sign) == 0:
                    sign = SIGN.PLUS
                irred = "".join([i for i in orbital_sym_label if i not in [SIGN.PLUS.value, SIGN.MINUS.value]])
                paired_label = [i for i in included_orbitals if i != orbital_sym_label]
                if len(paired_label) != 1:
                    raise Exception("should have a pair")
                orbitals.append({"sym_label": irred, "sign": SIGN(sign), "occupation": int(occupation),
                                 "paired_label": paired_label[0].replace("+","").replace("-","")})
        return orbitals


    def multiply_out(self, ordering:CI_ORDERING):
        if len(self.determinants) > 0:
            return
        # print("$$", self.monomer_occupation_1.latex_ci_equation(ordering=ordering, multiplied_out=False),
        #       self.monomer_occupation_2.latex_ci_equation(ordering=ordering, multiplied_out=False), "$$"
        #       )
        # print("$$",
        #       self.monomer_occupation_1.latex_ci_equation(ordering=ordering, multiplied_out=True),
        #       self.monomer_occupation_2.latex_ci_equation(ordering=ordering, multiplied_out=True), "$$"
        #       )

        monomer_LC_and_OCC_1 = [i.get_occupation_string(multiplied_out=True) for i in self.monomer_occupation_1.get_orbitals_in_order(ordering=ordering)]
        monomer_LC_and_OCC_2 = [i.get_occupation_string(multiplied_out=True) for i in self.monomer_occupation_2.get_orbitals_in_order(ordering=ordering)]

        monomer_LC_and_OCC_1 = [i.replace(SIGN.MINUS.value, SIGN.PLUS.value) for i in monomer_LC_and_OCC_1]
        monomer_LC_and_OCC_2 = [i.replace(SIGN.MINUS.value, SIGN.PLUS.value) for i in monomer_LC_and_OCC_2]
        common_values = list(set(monomer_LC_and_OCC_1) & set(monomer_LC_and_OCC_2))
        definite_orbitals = self._get_orbital_occ_list(common_values)
        sign_of_definite_orbitals = SIGN.PLUS

        choices_1 = self._get_orbital_occ_list([i for i in monomer_LC_and_OCC_1 if i not in common_values])
        choices_2 = self._get_orbital_occ_list([i for i in monomer_LC_and_OCC_2 if i not in common_values])

        possibilities = get_all_combinations(choices_1, choices_2)

        for possibility in possibilities:
            signs = [i["sign"] for i in possibility]+[self.sign, sign_of_definite_orbitals]
            sign = build_product_from_signs_in_str("".join([s.value for s in signs]))
            orbital_symmetry_labels_occ0 = [i["sym_label"] for i in possibility if i["occupation"] == 0]
            orbital_symmetry_labels_occ1 = [i["sym_label"] for i in possibility if i["occupation"] == 1]
            orbital_symmetry_labels_occ2 = [i["sym_label"] for i in possibility if i["occupation"] == 2]

            # add definite parts:
            orbital_symmetry_labels_occ0.extend([o["sym_label"] for o in definite_orbitals if o["occupation"] == 0])
            orbital_symmetry_labels_occ1.extend([o["sym_label"] for o in definite_orbitals if o["occupation"] == 1])
            orbital_symmetry_labels_occ2.extend([o["sym_label"] for o in definite_orbitals if o["occupation"] == 2])


            if not len(orbital_symmetry_labels_occ1) == 4:
                continue
            if not len(orbital_symmetry_labels_occ1) + 2 * len(orbital_symmetry_labels_occ2) == 8:
                continue
            assert len(orbital_symmetry_labels_occ0 + orbital_symmetry_labels_occ1 + orbital_symmetry_labels_occ2) == len(set(orbital_symmetry_labels_occ0 + orbital_symmetry_labels_occ1 + orbital_symmetry_labels_occ2))

            det = DimerDeterminant(orbital_symmetry_labels_occ1=orbital_symmetry_labels_occ1,
                                    orbital_symmetry_labels_occ0=orbital_symmetry_labels_occ0,
                                    sign=sign, point_group=self.point_group, ordering=ordering)
            self.determinants.append(det)

        if len(self.determinants) > 2**4:
            raise Exception(f"Too many determinants ({len(self.determinants)}): run test_get_determinants()")


        # grouped = defaultdict(lambda: {"occupations": [], "signs": []})
        # for d in possibilities_1 + possibilities_2:
        #     sym = d['sym_label']
        #     grouped[sym]["occupations"].append(d['occupation'])
        #     grouped[sym]["signs"].append(d['sign'])
        #
        # orbitals = []
        # for sym, info in grouped.items():
        #     for i in range(len(info["occupations"])):
        #         sign = info["signs"][i]
        #         occupation = info["occupations"][i]
        #         orbital = Orbital(sym_label =sym, occupation=occupation, point_group=self.point_group)
        #         orbital.sign = sign
        #         orbitals.append(orbital)

        pass

        # terms = self.monomer_occupation_1.get_single_occupied_orbital_labels(side="l", multiplied_out=True)
        # terms.extend(self.monomer_occupation_2.get_single_occupied_orbital_labels(side="r", multiplied_out=True))
        # terms = [split_string_into_signed_parts(term) for term in terms]
        # assert len(terms) == 4 # number of unpaired electrons in monomer
        # ''' 4 possible cases for left * right
        #    Fall 1:     (l1+r1)*(l2+r2) = l1*l2 + r1*l2 + l1*r2 + r1*r2
        #    Fall 2:     (l1-r1)*(l2-r2) = l1*l2 - r1*l2 - l1*r2 + r1*r2
        #    Fall 3:     (l1+r1)*(l2-r2) = l1*l2 + r1*l2 - l1*r2 - r1*r2
        #    Fall 4:     (l1-r1)*(l2+r2) = l1*l2 - r1*l2 + l1*r2 - r1*r2
        # '''
        # self.determinants = []
        # for a in terms[0]:
        #     for b in terms[1]:
        #         for c in terms[2]:
        #             for d in terms[3]:
        #                 total_product_string = a+b+c+d
        #                 sign = build_product_from_signs_in_str(total_product_string)
        #                 sign = sign.PLUS if sign == self.sign else sign.MINUS
        #
        #                 orbitals_flat = [item for row in terms for item in row]
        #                 orbitals_occ_0 = [i for i in orbitals_flat if i not in [a,b,c,d]]
        #
        #                 det = DimerDeterminant(orbital_symmetry_labels_occ1=[a, b, c, d],
        #                                        orbital_symmetry_labels_occ0=orbitals_occ_0,
        #                                        sign=sign, point_group=self.point_group, ordering=ordering)
        #                 self.determinants.append(det)
        return



