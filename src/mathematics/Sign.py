from enum import Enum
import re



class SIGN(Enum):
    PLUS = "+"
    MINUS = "-"



def split_string_into_signed_parts(s:str):
    parts = re.split(r'(?=[+-])', s)
    return [p for p in parts if p]


def build_product_from_signs_in_str(s:str):
    signs = "".join(re.findall(r"[+-]", s))
    signs = [SIGN(s) for s in signs]

    sign = SIGN.PLUS
    for s in signs:
        sign = SIGN.PLUS if sign.value == s.value else SIGN.MINUS
    return sign

