def get_table(number_of_columns: int, content_lines: list[str]) -> str:

    if number_of_columns <= 0:
        raise ValueError("number_of_columns must be positive")

    column_format = "c" * number_of_columns

    processed_lines = []
    for line in content_lines:
        stripped = line.rstrip()
        if not stripped.endswith(r"\\"):
            stripped += r" \\[0.1cm] "
        processed_lines.append(stripped)

    table = [
        r"\begin{table}[ht]",
        r"\centering",
        rf"\begin{{tabular}}{{{column_format}}}",
        r"\hline",
        processed_lines[0],
        r"\hline",
        *processed_lines[1:],
        r"\hline",
        r"\end{tabular}",
        r"\end{table}",
    ]

    return "\n".join(table)
