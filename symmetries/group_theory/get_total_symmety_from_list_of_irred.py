from typing import List

from symmetries.group_theory.PointGroups import POINTGROUP


def get_total_symmety_from_list_of_irred(list:List, point_group: POINTGROUP)-> str:
    """
    calculating the total symmetry of a product of irreducible representations in given point group
    ( choices = ['ag', 'au', 'b1g', 'b1u', 'b2g', 'b2u', 'b3g', 'b3u'] )
    :param list: included irreducible representations
    :return: total symmetry
    """
    if len(list) == 0:
        return point_group.total_symmetric
    symmetrie = list[0]
    for i in range(1, len(list)):
        symmetrie = point_group.product(symmetrie, list[i])
    return symmetrie


if __name__ == "__main__":
    print( get_total_symmety_from_list_of_irred(["ag", "b1u", "b2g"]) )