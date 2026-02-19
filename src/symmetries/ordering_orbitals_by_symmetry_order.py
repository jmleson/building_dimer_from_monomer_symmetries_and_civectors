from src.symmetries.CI_ORDERING import CI_ORDERING
from src.building_blocks.Orbital import Orbital
from src.symmetries.POINTGROUP import POINTGROUP


def ordering_orbitals_by_symmetry_order(orbitals:list[Orbital], point_group:POINTGROUP, ordering:CI_ORDERING):
    if len(orbitals) == 0:
        return
    if ordering == CI_ORDERING.molpro:
        if point_group == POINTGROUP.C2h and orbitals[0].side is not None:
            ordering = POINTGROUP.C2v.irreduzible_representations_molpro_ordered
        else:
            ordering = point_group.irreduzible_representations_molpro_ordered
    else:
        if point_group == POINTGROUP.C2h and orbitals[0].side is not None:
            ordering = POINTGROUP.C2v.irreduzible_representations_orbital_ordered
        else:
            ordering = point_group.irreduzible_representations_orbital_ordered

    ranking = {
        **{label: i for i, label in enumerate(ordering)},
        **{label + "*": i + 0.5 for i, label in enumerate(ordering)},
    }
    orbitals.sort(key=lambda orb: ranking[orb.sym_label])
    return orbitals