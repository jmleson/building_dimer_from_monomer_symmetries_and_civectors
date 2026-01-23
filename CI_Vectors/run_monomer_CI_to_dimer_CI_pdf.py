from CI_Vectors.get_linear_combined_states import get_linear_combined_states
from CI_Vectors.get_product_terms import get_product_terms
from symmetries.PointGroups import POINTGROUP




def get_file_ci_vectors(point_group:POINTGROUP):
    content = r"""
        \documentclass{article}
        \usepackage[a4paper, left=1cm, right=1cm, top=2cm, bottom=2cm]{geometry}
        \usepackage{hyperref} % für anklickbare Bezüge 
        \usepackage{tikz} % für MO-Schemata
        \usepackage{amsmath}
        \usepackage{physics}

        \hypersetup{colorlinks=true, linkcolor=black, citecolor=black}% damit Referenzen nicht in PDF umklammert
        \setlength{\parindent}{0pt}
        
        \begin{document}

        \pagestyle{empty}
        \tableofcontents
        \newpage
        """

    content += get_product_terms(point_group=point_group)
    content += "\n" + r"\newpage" + "\n"
    content += get_linear_combined_states(point_group=point_group)

    end= r"\end{document}"
    with open(f"CI-vektoren-theoretisch_{point_group.name}.tex", "w") as file:
        file.write(content + end)




if __name__ == "__main__":
    get_file_ci_vectors(point_group=POINTGROUP.D2h)