from src.symmetries.POINTGROUP import POINTGROUP


def transform_molpro_order_into_own_ordering_D2h(ci_vector_as_occupation_sequence:str):
    if len(ci_vector_as_occupation_sequence) != 8:
        raise Exception(f"not 8 occupations in {ci_vector_as_occupation_sequence}")
    point_group = POINTGROUP.D2h

    molpro_ordered_ci = {point_group.irreduzible_representations_molpro_ordered[i]: ci_vector_as_occupation_sequence[i] for i in range(8) }
    # print(molpro_ordered_ci)

    own_ordered_ci = dict(
        sorted(
            molpro_ordered_ci.items(),
            key=lambda x: point_group.irreduzible_representations_orbital_ordered.index(x[0])
        )
    )
    # print(own_ordered_ci)

    return own_ordered_ci, "".join( own_ordered_ci.values() )





if __name__ == "__main__":
    print(transform_molpro_order_into_own_ordering_D2h("a20a")[1])