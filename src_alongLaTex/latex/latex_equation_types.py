from enum import Enum


class latex_equation_types(Enum):
    """ kinds of latex environments, that induce an equation """
    INLINE = {"start":"$", "end": "$"}
    DISPLAYED = {"start": "$$", "end": "$$"}
    MULTLINE = {"start":  r"\begin{multline*}" , "end": r"\end{multline*}"}
    BASIC = {"start": r"\[", "end": r"\]"}



def get_expression_as_latex_formula(term:str, kind: latex_equation_types) -> str:
    """
    convert equation content into total latex equation environment
    :param term: content of equation
    :param kind: latex-format for the equation
    :return:
    """
    if len(term.replace(" ","")) == 0:
        return ""
    return f"{kind.value['start']}{term}{kind.value['end']}"
