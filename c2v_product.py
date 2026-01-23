
def c2v_product(factor_1:str, factor_2:str) -> str:
    """
    multiplying irreducible representations of C2v
    :param factor_1: 1st irreducible representation
    :param factor_2: 2nd irreducible representation
    :return: factor_1 * factor_2
    """
    if factor_1 == "a1":
        return factor_2
    if factor_2 == "a1":
        return factor_1
    if factor_1 == factor_2:
        return "a1"

    # print("sorted:", [factor_1,factor_2].sort())
    combination = [factor_1,factor_2]
    combination.sort()
    if combination == ["a2", "b1"]:
        return "b2"
    if combination == ["a2", "b2"]:
        return "b1"
    if combination == ["b1", "b2"]:
        return "a2"
    else:
        raise Exception(f"unknown factors in c2v_product {factor_1}, {factor_2}")



if __name__ == "__main__":
    print( c2v_product("b2","b1") )