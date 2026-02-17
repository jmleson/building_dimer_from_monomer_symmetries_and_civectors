

def underbrace(s:str, info:str=None):
    return r"\underbrace{" + s + r"}" if info is None else r"\underbrace{" + s + r"}_{" + info + r"}"