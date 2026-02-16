
def c2h_product(factor_1:str, factor_2:str) -> str:
    """
    multiplying irreducible representations of D2h
    :param factor_1: 1st irreducible representation
    :param factor_2: 2nd irreducible representation
    :return: factor_1 x factor_2
    """
    if factor_1 == "ag":
        return factor_2
    if factor_2 == "ag":
        return factor_1
    if factor_1 == factor_2:
        return "ag"

    # print("sorted:", [factor_1,factor_2].sort())
    combination = [factor_1,factor_2]
    combination.sort()
    if combination == ["au", "bg"]:
        return "bu"
    if combination == ["au", "bu"]:
        return "bg"
    if combination == ["bg", "bu"]:
        return "au"
    else:
        print(factor_1, factor_2)



if __name__ == "__main__":
    print( c2h_product("bu","bg") )