from CI_Vectors.get_linear_combined_states import get_linear_combined_states
from CI_Vectors.get_product_terms import get_product_terms
from symmetries.Molecule import Molecule




def get_file_ci_vectors(molecule:Molecule):
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

    content += get_product_terms(molecule=molecule)
    content += "\n" + r"\newpage" + "\n"
    content += get_linear_combined_states(molecule=molecule)

    end= r"\end{document}"
    with open(f"resulting_tex_files/CI-vektoren-theoretisch_{molecule.name}.tex", "w") as file:
        file.write(content + end)




if __name__ == "__main__":
    molecule = Molecule.C6H6
    get_file_ci_vectors(molecule=molecule)