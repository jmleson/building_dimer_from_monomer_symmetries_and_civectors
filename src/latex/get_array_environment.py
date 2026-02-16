

def get_array_environment(elements: list[str], breaking_after:int=4):
    if len(elements) < breaking_after:
        return " ".join(elements)
    else:
        rows = [
            " ".join(elements[i:i+breaking_after])
            for i in range(0, len(elements), breaking_after)
        ]

    body = r" \\[0.5cm] ".join(rows)

    return (
        r"\begin{array}{c}" + "\n"
        + body + "\n"
        + r"\end{array}"
    )
