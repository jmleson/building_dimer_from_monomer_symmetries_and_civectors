from symmetries.PointGroups import POINTGROUP


def multipling_irred(product_term:dict, point_group:POINTGROUP) -> None:
    """
    multiplying all irreducible representations of an orbital determinant
       to get the total symmetry of the term
    :param product_term: determinant of dimer orbitals, given by amount, equational form, factors, forbidden
    :return: (saved in factors as one single irreducible representation)
    """
    while len(product_term["factors"]) > 1:
        new_12 = point_group.product(factor_1 = product_term["factors"][-1], factor_2 = product_term["factors"][-2])
        product_term["factors"] = product_term["factors"][:-2]+ [new_12]


if __name__ == "__main__":
    product_term = {"amount": 1, "eq": "ag b3u b2u au", "factors": ["ag", "b3u","b2u", "au"], "forbidden":False}
    x = POINTGROUP("d2h")
    print( multipling_irred(product_term, x))
    print(product_term)

    product_term = {"amount": 1, "eq": "a1 b1 b2 a1", "factors": ["a1", "b1","b2", "a1"], "forbidden":False}
    print( multipling_irred(product_term, POINTGROUP("c2v")))
    print(product_term)