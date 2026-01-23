from symmetrie_und_orbitale.PointGroups import POINTGROUP
from symmetrie_und_orbitale.all_products import all_products
from symmetrie_und_orbitale.linear_combinations.linear_combination_monomer_states import get_monomer_state_linear_combinations
from symmetrie_und_orbitale.linear_combinations.linear_combinations_of_combined_monomer_states import \
    linear_combinations_of_combined_monomer_states


def get_latex_file_for_d2h_symmetrie_options(content:str, point_group:POINTGROUP) -> None :
    """
    writing a latex file with all given content, that is able to compile tikz-figures as well as equations
    :param content: content of to-be latex file
    :return:
    """
    start = r"""
    \documentclass{article}
    \usepackage[a4paper, left=1cm, right=1cm, top=2cm, bottom=2cm]{geometry}
    \usepackage{hyperref} % für anklickbare Bezüge 
    \usepackage{tikz} % für MO-Schemata
    \usepackage{amsmath}
    
    \setlength{\parindent}{0pt}
    \hypersetup{colorlinks=true, linkcolor=black, citecolor=black}% damit Referenzen nicht in PDF umklammert
    \begin{document}
    
    \pagestyle{empty}
    \tableofcontents 
    \newpage 
    
    \section{Orbitale und deren Symmetrie}
    """
    if point_group == POINTGROUP.D2h:
        molecule = "C6H6"
        start += r"In der Sortierung: oben rechts $a_u$, oben links $b_{1u}$, unten links $b_{2g}$ und unten rechts $b_{3g}$ folgt: \\"
    else:
        molecule = "C6H5Cl"
        start += r"In der Sortierung: oben rechts $ $, oben links $ $, unten links $ $ und unten rechts $ $ folgt: \\"

    if molecule == "C6H6":
        filename = "DimerZOrbitalordnung-gesamt-MO-C6H6-beiWW.pdf"
    else:
        if point_group == POINTGROUP.D2h:
            filename = "DimerZOrbitalordnung-C6H5Cl-C2h-gesamt-MO-beiWW.pdf"
        elif point_group == POINTGROUP.C2v:
            filename = "DimerZOrbitalordnung-C6H5Cl-C2v-gesamt-MO-beiWW.pdf"
        elif point_group == POINTGROUP.C2h:
            filename = "DimerZOrbitalordnung-C6H5Cl-C2h-gesamt-MO-beiWW.pdf"
        else:
            raise Exception("unknown file name for get_latex_file_for_d2h_symmetrie_options")
    start += "\n" + r"\includegraphics[scale=0.125]{img/" + filename + r"}" + "\n"
    start += r"\vspace{2cm}" + "\n"
    end= r"\end{document}"
    with open("tst.tex", "w") as file:
        file.write(start + content + end)


if __name__ == "__main__":
    detailed = True
    # detailed = False
    # point_group = POINTGROUP("c2h")
    # point_group = POINTGROUP("c2v")
    point_group = POINTGROUP("d2h")

    content = all_products(point_group=point_group, monomer_combinations=True, detailed=detailed)
    content += all_products(point_group=point_group,monomer_combinations=False,detailed=detailed)
    content += get_monomer_state_linear_combinations(point_group=point_group,detailed=detailed)[0]
    content += linear_combinations_of_combined_monomer_states(point_group=point_group, detailed=detailed)
    get_latex_file_for_d2h_symmetrie_options(content, point_group=point_group)