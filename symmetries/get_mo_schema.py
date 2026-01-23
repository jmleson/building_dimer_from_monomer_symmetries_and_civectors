from symmetries.PointGroups import POINTGROUP

height_upper_mos = 0
height_lower_mos = height_upper_mos-0.6
x_left = 0
x_right = 1
width = 0.5
arrow_height = 0.25
arrow_x = 0.25
padding = 0.1

down_left_top = f" \draw[<-, thick] ({x_left + arrow_x-padding}, {height_upper_mos - arrow_height}) -- ({x_left + arrow_x-padding}, {height_upper_mos+arrow_height}); "
up_left_top = f"\draw[->, thick] ({x_left + arrow_x+padding}, {height_upper_mos - arrow_height}) -- ({x_left + arrow_x+padding}, {height_upper_mos+arrow_height}); "
down_right_top = f" \draw[<-, thick] ({x_right + arrow_x-padding}, {height_upper_mos - arrow_height}) -- ({x_right + arrow_x-padding}, {height_upper_mos+arrow_height}); "
up_right_top = f"\draw[->, thick] ({x_right + arrow_x+padding}, {height_upper_mos - arrow_height}) -- ({x_right + arrow_x+padding}, {height_upper_mos+arrow_height}); "

down_left_bottom = f"\draw[<- , thick] ({x_left + arrow_x-padding}, {height_lower_mos - arrow_height}) -- ({x_left + arrow_x-padding}, {height_lower_mos+arrow_height}); "
up_left_bottom = f"\draw[-> , thick] ({x_left + arrow_x+padding}, {height_lower_mos - arrow_height}) -- ({x_left + arrow_x+padding}, {height_lower_mos+arrow_height}); "
down_right_bottom = f"\draw[<- , thick] ({x_right + arrow_x-padding}, {height_lower_mos - arrow_height}) -- ({x_right + arrow_x-padding}, {height_lower_mos+arrow_height}); "
up_right_bottom = f" \draw[-> , thick] ({x_right + arrow_x+padding}, {height_lower_mos - arrow_height}) -- ({x_right + arrow_x+padding}, {height_lower_mos+arrow_height}); "

basic_tikz_element = f"""
    % oberste MOs:
    \draw[thick] ({x_left},{height_upper_mos}) -- ({x_left + width},{height_upper_mos}); % erster Strich
    \draw[thick] ({x_right},{height_upper_mos}) -- ({x_right + width},{height_upper_mos}); % zweiter Strich
    % unterste MOs:
    \draw[thick] ({x_left},{height_lower_mos}) -- ({x_left + width},{height_lower_mos}); % dritter Strich
    \draw[thick] ({x_right},{height_lower_mos}) -- ({x_right + width},{height_lower_mos}); % vierter Strich
"""



def get_mo_schemata(point_group:POINTGROUP, occupied_mos: dict, monomer:str) -> str:
    """
    get benzene (HOMOs + LUMOs) MO diagramm in a latex format (tikz)
    :param occupied_mos: occupation numbers of the included orbitals, given as number per symmetry
    :param monomer: "left" / "right"; information about what data in the occupied_mos dict is needed
    :return: tikz-block of the mo scheme
    """
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
    """
    get a mo diagramm for a benzene on the "left" and one on the "right" = combine two monomer mo diagramms to one dimer mo diagramm;
    :param occupied_mos: occupation numbers of the included orbitals, given as number per symmetry
    :return: equation with tikz environments representing the mo diagramms, Einzufassen in \[ und\] für Latex-Nutzung
    """
    basic_tikz_element_left = get_mo_schemata(point_group=point_group, occupied_mos=occupied_mos, monomer="left")
    basic_tikz_element_right = get_mo_schemata(point_group=point_group, occupied_mos=occupied_mos, monomer="right")

    total_tikz_object = r"\begin{tikzpicture}" + basic_tikz_element_left
    total_tikz_object+= r"\end{tikzpicture} \qquad \begin{tikzpicture}" + basic_tikz_element_right
    total_tikz_object+= r"\end{tikzpicture}"

    return total_tikz_object



if __name__ == '__main__':
    occupied_mos = {
        "b1u": {"left": 1, "right": 0},
        "au": {"left": 0, "right": 1},
        "b2g": {"left": 1, "right": 2},
        "b3g": {"left": 2, "right": 1},
    }
    print(r"\left\lbrace" + get_total_mo_schemata(occupied_mos=occupied_mos)+ r"\right\rbrace")