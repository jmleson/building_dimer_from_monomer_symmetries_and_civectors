from src.building_blocks.Orbital import Orbital
from src.latex.format_irred_representations import format_irred_representations
from src.mathematics.Sign import SIGN
from src.symmetries.POINTGROUP import POINTGROUP


class DimerDeterminant():

    def __init__(self, orbital_symmetry_labels:list[str], sign:SIGN, point_group:POINTGROUP):
        self.orbitals = [Orbital(sym_label=i.replace("-","").replace("+",""),
                                 occupation=1, point_group=point_group)
                         for i in orbital_symmetry_labels]
        self.point_group = point_group

        self.sign = sign
        self.prefactor = 1


    def determine_symmetry(self):
        sym = self.point_group.total_symmetric
        for i in self.orbitals:
            sym = self.point_group.product(sym, i.sym_label)
        return sym


    def determinants(self):
        eq = self.sign.value + str(abs(self.prefactor)) + r" \cdot{} \left| "
        eq += r"\underbrace{"
        inbetween = "".join(
            [format_irred_representations(i.sym_label) for i in self.orbitals ]
        )
        eq += inbetween + "_{" + format_irred_representations(self.determine_symmetry())  + r"}"
        return eq + r"\right|"


