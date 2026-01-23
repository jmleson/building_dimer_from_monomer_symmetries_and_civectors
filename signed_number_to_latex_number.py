def signed_number_to_latex_number(signed_number:int) -> str:
    """
    get a reasonable formatted number from a python number
    :param signed_number: amount of something
    :return: formatted number
    """
    if signed_number == 1:
        return "+"
    if signed_number == -1:
        return "-"
    if signed_number >= 0:
        return "+" + str(signed_number)
    return str(signed_number)
