from src.CI_ORDERING import CI_ORDERING
from src.building_blocks.Orbital import Orbital
from src.latex.format_irred_representations import format_irred_representations
from src.symmetries.POINTGROUP import POINTGROUP
from src.symmetries.ordering_orbitals_by_symmetry_order import ordering_orbitals_by_symmetry_order


class MonomerOccupation:

    def __init__(self, point_group:POINTGROUP):
        self.point_group = point_group

        self.left_bottom = Orbital(sym_label=point_group.label_ordering_in_monomer_occupation["left_bottom"], point_group=point_group)
        self.right_bottom = Orbital(sym_label=point_group.label_ordering_in_monomer_occupation["right_bottom"], point_group=point_group)
        self.left_top = Orbital(sym_label=point_group.label_ordering_in_monomer_occupation["left_top"], point_group=point_group)
        self.right_top = Orbital(sym_label=point_group.label_ordering_in_monomer_occupation["right_top"], point_group=point_group)

        self.initially_occupied_orbitals = [self.left_bottom, self.right_bottom]
        self.initially_unoccupied_orbitals = [self.left_top, self.right_top]


    def set_occupation(self, occupation:dict):
        if "left_bottom" in occupation:
            self.left_bottom.occupation = occupation["left_bottom"]
        if "right_bottom" in occupation:
            self.right_bottom.occupation = occupation["right_bottom"]
        if "left_top" in occupation:
            self.left_top.occupation = occupation["left_top"]
        if "right_top" in occupation:
            self.right_top.occupation = occupation["right_top"]

        if self.left_bottom.sym_label in occupation:
            self.left_bottom.occupation = occupation[self.left_bottom.sym_label]
        if self.right_bottom.sym_label in occupation:
            self.right_bottom.occupation = occupation[self.right_bottom.sym_label]
        if self.left_top.sym_label in occupation:
            self.left_top.occupation = occupation[self.left_top.sym_label]
        if self.right_top.sym_label in occupation:
            self.right_top.occupation = occupation[self.right_top.sym_label]

    def latex_picture(self, draw_label:bool = False ):
        height_upper_mos = 0
        height_lower_mos = height_upper_mos - 0.6

        tikz = "\n% lower MOs:\n"
        tikz += self.left_bottom.latex_picture(x_left=0, height=height_lower_mos, node_position="left", draw_label=draw_label)
        tikz += self.right_bottom.latex_picture(x_left=1, height=height_lower_mos, node_position="right", draw_label=draw_label)
        tikz += "\n% upper MOs:\n"
        tikz += self.left_top.latex_picture(x_left=0, height=height_upper_mos, node_position="left", draw_label=draw_label)
        tikz += self.right_top.latex_picture(x_left=1, height=height_upper_mos, node_position="right", draw_label=draw_label)

        return tikz

    def get_orbitals_in_order(self, ordering: CI_ORDERING):
        orbitals = self.initially_occupied_orbitals + self.initially_unoccupied_orbitals
        return ordering_orbitals_by_symmetry_order(orbitals=orbitals, ordering=ordering, point_group=self.point_group)

    def latex_ci_equation(self, ordering:CI_ORDERING):
        eq = r"\left|"
        for i in self.get_orbitals_in_order(ordering=ordering):
            eq += i.get_occupation_string()
        eq += r"\right|"
        return eq


    def get_single_occupied_orbital_labels(self, side:str, multiplied_out:bool) -> list[str]:
        orbitals = []
        for i in self.get_orbitals_in_order(ordering = CI_ORDERING.molpro):
            if i.occupation == 1:
                orbitals.append( i.get_sym_string(side, multiplied_out=multiplied_out) )
        return orbitals

    def monomer_determinant_content(self, side:str, multiplied_out:bool):
        eq = "".join(
                      [r"\left(" + format_irred_representations(i) + r"\right)"
                       for i in self.get_single_occupied_orbital_labels(side, multiplied_out)
                      ]
                  )
        return eq


    def __eq__(self, other):
        if not isinstance(other, MonomerOccupation):
            return NotImplemented
        return (self.right_bottom == other.right_bottom
                and self.left_bottom == other.left_bottom
                and self.right_top == other.right_top
                and self.left_top == other.left_top)


