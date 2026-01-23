import copy

from symmetries.group_theory.PointGroups import POINTGROUP


def irred_back_to_number(point_group:POINTGROUP, string:str):
    """
    Ersetze alle Vorkommnisse der irreduziblen Darstellungen im String string durch ihre Molpro-Nummer
    :param string: irreduzible representation(s)
    :return:
    """
    ordered_list = point_group.choices_irreduzible_representations_molpro_ordered
    # if point_group == POINTGROUP.C2v:# * zur Unterscheidung von Orbitalen gl. Symmetrie enthalten
    #     ordered_list = [i for i in ordered_list if "*" not in i]
    #     string = string.replace("*","")
    new_string = copy.deepcopy(string)
    replacement_dict = {rep: str(index + 1) for index, rep in enumerate(ordered_list)}
    for key, value in replacement_dict.items():
        new_string = new_string.replace(key, value)
    return new_string