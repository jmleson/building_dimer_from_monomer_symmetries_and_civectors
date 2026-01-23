from symmetries.group_theory.PointGroups import POINTGROUP
from symmetries.latex.format_irred_representations import format_irred_representations
from symmetries.general_functionalities.monomer_positions import MonomerPositions

height_upper_mos = 0
height_lower_mos = height_upper_mos-0.6
x_left = 0
x_right = 1
width = 0.5
arrow_height = 0.25
arrow_x = 0.25
padding = 0.1

down_left_top = fr" \draw[<-, thick] ({x_left + arrow_x-padding}, {height_upper_mos - arrow_height}) -- ({x_left + arrow_x-padding}, {height_upper_mos+arrow_height}); "
up_left_top = fr"\draw[->, thick] ({x_left + arrow_x+padding}, {height_upper_mos - arrow_height}) -- ({x_left + arrow_x+padding}, {height_upper_mos+arrow_height}); "
down_right_top = fr" \draw[<-, thick] ({x_right + arrow_x-padding}, {height_upper_mos - arrow_height}) -- ({x_right + arrow_x-padding}, {height_upper_mos+arrow_height}); "
up_right_top = fr"\draw[->, thick] ({x_right + arrow_x+padding}, {height_upper_mos - arrow_height}) -- ({x_right + arrow_x+padding}, {height_upper_mos+arrow_height}); "

down_left_bottom = fr"\draw[<- , thick] ({x_left + arrow_x-padding}, {height_lower_mos - arrow_height}) -- ({x_left + arrow_x-padding}, {height_lower_mos+arrow_height}); "
up_left_bottom = fr"\draw[-> , thick] ({x_left + arrow_x+padding}, {height_lower_mos - arrow_height}) -- ({x_left + arrow_x+padding}, {height_lower_mos+arrow_height}); "
down_right_bottom = fr"\draw[<- , thick] ({x_right + arrow_x-padding}, {height_lower_mos - arrow_height}) -- ({x_right + arrow_x-padding}, {height_lower_mos+arrow_height}); "
up_right_bottom = fr" \draw[-> , thick] ({x_right + arrow_x+padding}, {height_lower_mos - arrow_height}) -- ({x_right + arrow_x+padding}, {height_lower_mos+arrow_height}); "

basic_tikz_element = fr"""
    % oberste MOs:
    \draw[thick] ({x_left},{height_upper_mos}) -- ({x_left + width},{height_upper_mos}); % erster Strich
    \draw[thick] ({x_right},{height_upper_mos}) -- ({x_right + width},{height_upper_mos}); % zweiter Strich
    % unterste MOs:
    \draw[thick] ({x_left},{height_lower_mos}) -- ({x_left + width},{height_lower_mos}); % dritter Strich
    \draw[thick] ({x_right},{height_lower_mos}) -- ({x_right + width},{height_lower_mos}); % vierter Strich
"""





def get_mo_schemata(point_group:POINTGROUP, occupied_mos: dict, monomer:MonomerPositions) -> str:
    """
    get benzene (HOMOs + LUMOs) MO diagramm in a latex format (tikz)
    :param occupied_mos: occupation numbers of the included orbitals, given as number per symmetry
    :param monomer: MonomerPositions.left / MonomerPositions.right; information about what data in the occupied_mos dict is needed
    :return: tikz-block of the mo scheme
    """

    if monomer.value == MonomerPositions.isolated.value:
        basic_tikz_element_isolated_monomer = fr"""
            % oberste MOs:
            \draw[thick] ({x_left},{height_upper_mos}) -- ({x_left + width},{height_upper_mos})
                node[pos=0, left] {{${format_irred_representations(point_group.label["oben_links"])}$}}
                ;
            \draw[thick] ({x_right},{height_upper_mos}) -- ({x_right + width},{height_upper_mos})
                node[pos=1, right] {{${format_irred_representations(point_group.label["oben_rechts"])}$}}
                ;
            % unterste MOs:
            \draw[thick] ({x_left},{height_lower_mos}) -- ({x_left + width},{height_lower_mos})
                node[pos=0, left] {{${format_irred_representations(point_group.label["unten_links"])}$}}
                ;
            \draw[thick] ({x_right},{height_lower_mos}) -- ({x_right + width},{height_lower_mos})
                node[pos=1, right] {{${format_irred_representations(point_group.label["unten_rechts"])}$}}
                ;
        """
        return basic_tikz_element_isolated_monomer

    electrons = []
    if point_group.label["oben_links"] in occupied_mos.keys():
        if occupied_mos[ point_group.label["oben_links"] ][monomer] > 0:
            electrons.append(up_left_top)
        if occupied_mos[ point_group.label["oben_links"] ][monomer] > 1:
            electrons.append(down_left_top)
    if point_group.label["oben_rechts"]  in occupied_mos.keys():
        if occupied_mos[ point_group.label["oben_rechts"] ][monomer] > 0:
            electrons.append(up_right_top)
        if occupied_mos[ point_group.label["oben_rechts"] ][monomer] > 1:
            electrons.append(down_right_top)
    if point_group.label["unten_links"] in occupied_mos.keys():
        if occupied_mos[ point_group.label["unten_links"] ][monomer] > 0:
            electrons.append(up_left_bottom)
        if occupied_mos[ point_group.label["unten_links"] ][monomer] > 1:
            electrons.append(down_left_bottom)
    if point_group.label["unten_rechts"] in occupied_mos.keys():
        if occupied_mos[ point_group.label["unten_rechts"] ][monomer] > 0:
            electrons.append(up_right_bottom)
        if occupied_mos[ point_group.label["unten_rechts"] ][monomer] > 1:
            electrons.append(down_right_bottom)
    if len(electrons) > 4:
        raise Exception(f"Monomer darf nur maximal 4 Elektronen haben! Hat aber {len(electrons)}.")
    return basic_tikz_element + "\n".join([e for e in electrons])+ "\n"



def get_total_mo_schemata(point_group:POINTGROUP, occupied_mos:dict) -> str:
    r"""
    get a mo diagramm for a benzene on the MonomerPositions.left and one on the MonomerPositions.right = combine two monomer mo diagramms to one dimer mo diagramm;
    :param occupied_mos: occupation numbers of the included orbitals, given as number per symmetry
    :return: equation with tikz environments representing the mo diagramms, Einzufassen in \[ und\] für Latex-Nutzung
    """
    basic_tikz_element_left = get_mo_schemata(point_group=point_group, occupied_mos=occupied_mos, monomer=MonomerPositions.left)
    basic_tikz_element_right = get_mo_schemata(point_group=point_group, occupied_mos=occupied_mos, monomer=MonomerPositions.right)

    total_tikz_object = wrap_tikzpicture(basic_tikz_element_left)
    total_tikz_object+= r"\qquad " + wrap_tikzpicture(basic_tikz_element_right)

    return total_tikz_object


def wrap_tikzpicture(tikzpicture:str) -> str:
    # complete_str = r"\begin{tikzpicture}"  + tikzpicture + "\n"+ r"\end{tikzpicture}"
    return r"\begin{tikzpicture}[baseline={(current bounding box.center)}]"  + tikzpicture.rstrip("\n") + "\n"+ r"\end{tikzpicture}"


if __name__ == '__main__':
    occupied_mos = {
        "b1u": {MonomerPositions.left: 1, MonomerPositions.right: 0},
        "b2g": {MonomerPositions.left: 2, MonomerPositions.right: 1},
        "b3g": {MonomerPositions.left: 1, MonomerPositions.right: 2},
        "au": {MonomerPositions.left: 0, MonomerPositions.right: 1},
    }
    print(r"\left\lbrace" + get_total_mo_schemata(occupied_mos=occupied_mos, point_group=POINTGROUP.D2h)+ r"\right\rbrace")