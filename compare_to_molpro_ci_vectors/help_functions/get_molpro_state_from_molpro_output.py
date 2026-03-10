

def sign_char(x):
    return "+" if x >= 0 else "-"

def get_molpro_state_from_molpro_output(data: str, column_index: int, ci_vector_dismiss_limit:float):
    # Parse lines
    lines = data.strip().split("\n")
    patterns = []
    numbers = []

    for line in lines:
        parts = line.split()

        try:
            after_occupations = 8
            if not all(len(p) == 1 for p in parts[:after_occupations]):
                raise Exception("not Benzene-like")
            occupations = parts[:after_occupations]
        except:
            try:
                after_occupations = 4
                if not any(len(p) == 3 for p in parts[:after_occupations]):
                    raise Exception("not Chlorobenzene-like")
                occupations = [p if len(p) < 3 else p[1:] for p in parts[:after_occupations]]
            except:
                raise Exception("no pattern found")

        patterns.append("".join(occupations))
        numbers.append([float(x) for x in parts[after_occupations:]])

    variants = []
    for i in range(len(patterns)):
        x = numbers[i][column_index]
        if abs(x) > ci_vector_dismiss_limit:          # ! needs to be carefully chosen
            # in C6H5Cl molpro prints ci vectors with factor 0.12173379, that do NOT belong to the main parts according to our derivation
            # however, some parts < 0.3 need to be included
            s = sign_char(x) + patterns[i]
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
variants = get_molpro_state_from_molpro_output(data, column_index = 3, ci_vector_dismiss_limit=0.2)
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
variants = get_molpro_state_from_molpro_output(data, column_index=4, ci_vector_dismiss_limit = 0.2)
assert variants ==  variants_root_5

Cl_data_sym_3 = """
 2a0 20 22a aa     -0.34467191     -0.34424105     -0.34702251
 22a aa 2a0 20      0.34467191      0.34424105      0.34702251
 220 a0 2aa 2a     -0.34467191      0.34424105      0.34702251
 2aa 2a 220 a0      0.34467191     -0.34424105     -0.34702251
 22a 20 2a0 aa      0.34467191      0.34424191     -0.34702181
 2a0 aa 22a 20     -0.34467191     -0.34424191      0.34702181
 2aa a0 220 2a     -0.34467191      0.34424191     -0.34702181
 220 2a 2aa a0      0.34467191     -0.34424191      0.34702181
"""
variants_root_Cl = [
    "-a0202aaa",
    "+2aaaa020",
    "-20a0aa2a",
    "+aa2a20a0",
    "+2a20a0aa",
    "-a0aa2a20",
    "-aaa0202a",
    "+202aaaa0",
]
variants = get_molpro_state_from_molpro_output(Cl_data_sym_3, column_index=0, ci_vector_dismiss_limit = 0.2)
assert variants == variants_root_Cl