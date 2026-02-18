from src.symmetries.CI_ORDERING import CI_ORDERING
from src.building_blocks.MonomerOccupation import MonomerOccupation
from src.mathematics.Sign import SIGN
from src.latex.wrap_tikz_picture import wrap_tikz_picture
from src.symmetries.POINTGROUP import POINTGROUP


class MonomerState:

    def __init__(self, point_group:POINTGROUP, label:str, molpro_symmetry_number:int):
        if molpro_symmetry_number >= len(point_group.choices_irreduzible_representations_molpro_ordered):
            raise Exception("wrong symmetry index")
        self.point_group = point_group
        self.label = label
        self.symmetry_index = molpro_symmetry_number

        self.always_positive_monomer_occupation = None
        self.additive_monomer_occupation = None# INFO: can be None, in case of singlet / quintet state !

        self.combination = SIGN("+")

    def get_multiplicity(self):
        if self.additive_monomer_occupation is not None:
            return 3
        if (self.always_positive_monomer_occupation.left_bottom.occupation == 1 and
                self.always_positive_monomer_occupation.left_top.occupation == 1 and
                self.always_positive_monomer_occupation.right_top.occupation == 1 and
                self.always_positive_monomer_occupation.right_bottom.occupation == 1):
            return 5
        if (self.always_positive_monomer_occupation.left_bottom.occupation == 2
                and self.always_positive_monomer_occupation.right_bottom.occupation == 2):
            return 1
        raise Exception("unknown multiplicity")

    def set_monomer_occupations(self, always_positive_monomer_occupation: MonomerOccupation,
                                additive_monomer_occupation: MonomerOccupation|None, combination:SIGN) -> None:
        if self.point_group != always_positive_monomer_occupation.point_group or (additive_monomer_occupation is not None and self.point_group != additive_monomer_occupation.point_group):
            raise Exception("wrong point group")
        self.combination = combination
        self.always_positive_monomer_occupation = always_positive_monomer_occupation
        self.additive_monomer_occupation = additive_monomer_occupation

    def to_latex(self, ordering:CI_ORDERING, multiplied_out:bool, short_version:bool):
        eq = f"{self.label} = \n " + r"\quad "
        eq += self.latex_picture(draw_label=False)
        eq += r" \quad = "
        eq += self.latex_ci_equation(ordering=ordering, multiplied_out=multiplied_out, short_version=short_version)
        return eq

    def latex_picture(self, draw_label:bool=False) -> str:
        eq = SIGN.PLUS.value + r" \left(" + wrap_tikz_picture( self.always_positive_monomer_occupation.latex_picture(draw_label=draw_label) ) + r"\right) " +"\n"
        if self.additive_monomer_occupation is not None:
            eq += self.combination.value + r" \left(" + wrap_tikz_picture( self.additive_monomer_occupation.latex_picture(draw_label=draw_label) ) + r"\right) " +"\n"
        return eq

    def latex_ci_equation(self, ordering:CI_ORDERING, multiplied_out:bool, short_version:bool):
        eq = f"{self.always_positive_monomer_occupation.latex_ci_equation(ordering=ordering, multiplied_out=multiplied_out, short_version=short_version)}"
        if self.additive_monomer_occupation is not None:
            eq += f" {self.combination.value} {self.additive_monomer_occupation.latex_ci_equation(ordering=ordering, multiplied_out=multiplied_out, short_version=short_version)}"
        return eq

    def __eq__(self, other):
        if not isinstance(other, MonomerState):
            return NotImplemented
        return (self.combination.value == other.combination.value and
                self.always_positive_monomer_occupation == other.always_positive_monomer_occupation and
                self.additive_monomer_occupation == other.additive_monomer_occupation)

