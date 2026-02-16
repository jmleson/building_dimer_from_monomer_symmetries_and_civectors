def format_irred_representations(latex_equation:str) -> str:
    """
    change the formatting of irreducible representations from plain strings to latex-equation compatible strings
    :param latex_equation: to-be-formatted equation
    :return: formatted latex-equation
    """
    # zuerst Ersetzen der *-markierten Werte:
    # C2h:
    latex_equation = latex_equation.replace("ag*", "a_g^{*}").replace("au*", "a_u^{*}")
    latex_equation = latex_equation.replace("bg*", "b_g^{*}").replace("bu*", "b_u^{*}")
    # C2v:
    latex_equation = latex_equation.replace("a1*^{l}", "a_1^{*l}").replace("a2*^{l}", "a_2^{*l}")
    latex_equation = latex_equation.replace("b1*^{l}", "b_1^{*l}").replace("b2*^{l}", "b_2^{*l}")
    latex_equation = latex_equation.replace("a1*^{r}", "a_1^{*r}").replace("a2*^{r}", "a_2^{*r}")
    latex_equation = latex_equation.replace("b1*^{r}", "b_1^{*r}").replace("b2*^{r}", "b_2^{*r}")
    latex_equation = latex_equation.replace("a1*", "a_1^{*}").replace("a2*", "a_2^{*}")
    latex_equation = latex_equation.replace("b1*", "b_1^{*}").replace("b2*", "b_2^{*}")

    # dann der "normalen"/unmarkierten Einträge:
    # C2h:
    latex_equation = latex_equation.replace("bg", "b_g").replace("bu", "b_u")
    # D2h:
    latex_equation = latex_equation.replace("b3g","b_{3g}").replace("ag","a_{g}")
    latex_equation = latex_equation.replace("b1u","b_{1u}").replace("au","a_{u}")
    latex_equation = latex_equation.replace("b2u","b_{2u}").replace("b1g","b_{1g}")
    latex_equation = latex_equation.replace("b2g", "b_{2g}").replace("b1g", "b_{1g}")
    latex_equation = latex_equation.replace("b3u","b_{3u}").replace("b3g","b_{3g}")
    # C2v:
    latex_equation = latex_equation.replace("a1", "a_1").replace("a2","a_2")
    latex_equation = latex_equation.replace("b1","b_1").replace("b2","b_2")


    return latex_equation
