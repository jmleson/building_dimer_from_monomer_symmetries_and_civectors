from src.latex.format_irred_representations import format_irred_representations


class Orbital():

    def __init__(self, sym_label:str, occupation:int=0):
        if occupation not in [0, 1, 2]:
            raise Exception("Invalid occupation")

        self.occupation = occupation
        self.sym_label = sym_label

    def get_occupation_string(self):
        if self.occupation == 1:
            return "a"
        return str(self.occupation)

    def latex_picture(self, x_left, height, node_position:str, draw_label:bool=False):
        if node_position not in ["left", "right"]:
            raise Exception("Invalid node position")
        width = 0.5
        padding = 0.1
        arrow_height = 0.25
        arrow_x = 0.25

        basic_tikz_element =  fr"""\draw[thick] ({x_left},{height}) -- ({x_left + width},{height})"""
        if node_position == "left":
            if not draw_label:
                basic_tikz_element += "%"
            basic_tikz_element += fr"""node[pos=0, left] {{${format_irred_representations(self.sym_label)}$}}""" + "\n"

        if node_position == "right":
            if not draw_label:
                basic_tikz_element += "%"
            basic_tikz_element += fr"""node[pos=1, right] {{${format_irred_representations(self.sym_label)}$}}""" + "\n"

        basic_tikz_element += ";"
        electrons = []
        if self.occupation > 0:
            up_left_top = fr"\draw[->, thick] ({x_left + arrow_x + padding}, {height - arrow_height}) -- ({x_left + arrow_x + padding}, {height + arrow_height}) ; "
            electrons.append(up_left_top)
        if self.occupation > 1:
            down_left_top = fr" \draw[<-, thick] ({x_left + arrow_x - padding}, {height - arrow_height}) -- ({x_left + arrow_x - padding}, {height + arrow_height}) ; "
            electrons.append(down_left_top)
        return basic_tikz_element + "\n".join([e for e in electrons]) + ";"

