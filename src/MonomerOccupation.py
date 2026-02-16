from src.Orbital import Orbital


class MonomerOccupation:

    def __init__(self, point_group):

        self.left_bottom = Orbital(sym_label=point_group.label_ordering_in_monomer_occupation["left_bottom"])
        self.right_bottom = Orbital(sym_label=point_group.label_ordering_in_monomer_occupation["right_bottom"])
        self.left_top = Orbital(sym_label=point_group.label_ordering_in_monomer_occupation["left_top"])
        self.right_top = Orbital(sym_label=point_group.label_ordering_in_monomer_occupation["right_top"])

        self.initially_occupied_orbitals = [self.left_bottom, self.right_bottom]
        self.initially_unoccupied_orbitals = [self.left_top, self.right_top]



    def latex_picture(self, draw_label:bool = False ):
        height_upper_mos = 0
        height_lower_mos = height_upper_mos - 0.6

        tikz = "% lower MOs:\n"
        tikz += self.left_bottom.latex_picture(x_left=0, height=height_lower_mos, node_position="left", draw_label=draw_label)
        tikz += self.right_bottom.latex_picture(x_left=1, height=height_lower_mos, node_position="right", draw_label=draw_label)
        tikz += "% upper MOs:\n"
        tikz += self.left_top.latex_picture(x_left=0, height=height_upper_mos, node_position="left", draw_label=draw_label)
        tikz += self.right_top.latex_picture(x_left=1, height=height_upper_mos, node_position="right", draw_label=draw_label)

        return tikz
