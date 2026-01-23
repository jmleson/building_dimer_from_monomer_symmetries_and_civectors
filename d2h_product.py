
def d2h_product(factor_1:str, factor_2:str) -> str:
    """
    multiplying irreducible representations of D2h
    :param factor_1: 1st irreducible representation
    :param factor_2: 2nd irreducible representation
    :return: factor_1 x factor_2
    """

    mix = sorted([factor_1.lower().replace(" ", ""), factor_2.lower().replace(" ", "")])
    if mix[0] == mix[1]:
        return "ag"
    if mix[0].replace("u","").replace("g","") == mix[1].replace("u","").replace("g",""):
        return "au"
    if mix[0] == "ag":
        return mix[1]
    if mix[0] == "au":
        if "g" in mix[1]:
            return mix[1].replace("g","u")
        return mix[1].replace("u","g")

    if "g" in mix[0] and "g" in mix[1] or "u" in mix[0] and "u" in mix[1]:
        form = "g"
    else:
        form = "u"
    number = [i for i in [1,2,3] if str(i) not in mix[0] and str(i) not in mix[1]]
    if len(number) != 1:
        raise Exception("wrong number")
    return "b"+str(number[0])+form



if __name__ == '__main__':
    print(d2h_product( 'b1g', 'b1u'))