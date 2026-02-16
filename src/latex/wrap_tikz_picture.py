

def wrap_tikz_picture(tikzpicture:str) -> str:
    # complete_str = r"\begin{tikzpicture}"  + tikzpicture + "\n"+ r"\end{tikzpicture}"
    return r"\begin{tikzpicture}[baseline={(current bounding box.center)}]"  + tikzpicture.rstrip("\n").replace("; ;", ";") + "\n"+ r"\end{tikzpicture}"
