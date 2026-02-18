from src.symmetries.CI_ORDERING import CI_ORDERING
from src.building_blocks.Orbital import Orbital
from src.symmetries.POINTGROUP import POINTGROUP


def ordering_orbitals_by_symmetry_order(orbitals:list[Orbital], point_group:POINTGROUP, ordering:CI_ORDERING):
    if ordering == CI_ORDERING.molpro:
        ordering = point_group.choices_irreduzible_representations_molpro_ordered
    else:
        raise Exception("nyi")

    ranking = {
        **{label: i for i, label in enumerate(ordering)},
        **{label + "*": i + 0.5 for i, label in enumerate(ordering)},
    }
    orbitals.sort(key=lambda orb: ranking[orb.sym_label])
    return orbitals