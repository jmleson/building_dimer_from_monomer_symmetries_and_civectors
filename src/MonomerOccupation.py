from src.CI_ORDERING import CI_ORDERING
from src.Orbital import Orbital


class MonomerOccupation:

    def __init__(self, point_group):
        self.point_group = point_group

        self.left_bottom = Orbital(sym_label=point_group.label_ordering_in_monomer_occupation["left_bottom"])
        self.right_bottom = Orbital(sym_label=point_group.label_ordering_in_monomer_occupation["right_bottom"])
        self.left_top = Orbital(sym_label=point_group.label_ordering_in_monomer_occupation["left_top"])
        self.right_top = Orbital(sym_label=point_group.label_ordering_in_monomer_occupation["right_top"])

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

    def get_orbitals_in_order(self, order: CI_ORDERING):
        orbitals = self.initially_occupied_orbitals + self.initially_unoccupied_orbitals

        if order == CI_ORDERING.molpro:
            order = self.point_group.choices_irreduzible_representations_molpro_ordered
        else:
            raise Exception("nyi")

        ranking = {label: i for i, label in enumerate(order)}

        orbitals.sort(key=lambda orb: ranking[orb.sym_label])

        return orbitals

    def latex_ci_equation(self, order:CI_ORDERING):
        eq = r"\left|"
        for i in self.get_orbitals_in_order(order=order):
            eq += i.get_occupation_string()
        eq += r"\right|"
        return eq
