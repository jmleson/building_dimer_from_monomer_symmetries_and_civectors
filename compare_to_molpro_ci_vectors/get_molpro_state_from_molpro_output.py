

def sign_char(x):
    return "+" if x >= 0 else "-"

def get_molpro_state_from_molpro_output(data: str, column_index: int):
    # Parse lines
    lines = data.strip().split("\n")
    patterns = []
    numbers = []

    for line in lines:
        parts = line.split()
        patterns.append(parts[:8])
        numbers.append([float(x) for x in parts[8:]])

    variants = []
    for i in range(len(patterns)):
        x = numbers[i][column_index]
        if abs(x) > 0.01:          # Filter: nur wenn Betrag > 0.01
            s = sign_char(x) + "".join(patterns[i])
            variants.append(s)

    return variants




### INCLUDED TESTS: 
data = """
     0 2 a a 0 2 a a      0.00000000     -0.00000022      0.00000155      0.34701928      0.35836745     -0.70190036      0.49380170
     a a 2 0 a a 2 0     -0.00000000     -0.00000022     -0.00000155      0.34701931      0.35836748      0.70190036      0.49380166
     a 2 a 0 a 2 a 0      0.00000000      0.48562677      0.69607076      0.35836784     -0.34702824      0.00000153      0.00000641
     0 a 2 a 0 a 2 a      0.00000000      0.48562663     -0.69607076      0.35836794     -0.34702833     -0.00000153      0.00000641
     a 2 2 a 0 a a 0      0.34495841     -0.24281368      0.00000005      0.35270229      0.00566973     -0.00000002     -0.24689123
     a a a a 0 2 2 0      0.34495841      0.24281368     -0.00000005     -0.35270229     -0.00566973      0.00000002      0.24689123
     0 a a 0 a 2 2 a      0.34495841     -0.24281368      0.00000005      0.35270229      0.00566973     -0.00000002     -0.24689123
     0 2 2 0 a a a a      0.34495841      0.24281368     -0.00000005     -0.35270229     -0.00566973      0.00000002      0.24689123
     a a 2 0 0 2 a a      0.34495841     -0.24281346      0.00000005      0.00566500     -0.35269802      0.00000002      0.24689764
     a 2 a 0 0 a 2 a     -0.34495841     -0.24281346      0.00000005      0.00566500     -0.35269802      0.00000002      0.24689764
     0 a 2 a a 2 a 0     -0.34495841     -0.24281346      0.00000005      0.00566500     -0.35269802      0.00000002      0.24689764
     0 2 a a a a 2 0      0.34495841     -0.24281346      0.00000005      0.00566500     -0.35269802      0.00000002      0.24689764
"""
variants = get_molpro_state_from_molpro_output(data, column_index = 3)
variants_root_4 = [
        "+02aa02aa",
        "+aa20aa20",
        "+a2a0a2a0",
        "+0a2a0a2a",
        "+a22a0aa0",
        "-aaaa0220",
        "+0aa0a22a",
        "-0220aaaa"]
assert variants == variants_root_4

variants_root_5 = [
        "+02aa02aa"    ,
        "+aa20aa20"    ,
        "-a2a0a2a0" ,
        "-0a2a0a2a" ,
        "-aa2002aa" ,
        "-a2a00a2a" ,
        "-0a2aa2a0" ,
        "-02aaaa20" ,
]
variants = get_molpro_state_from_molpro_output(data, column_index=4)
assert variants ==  variants_root_5
