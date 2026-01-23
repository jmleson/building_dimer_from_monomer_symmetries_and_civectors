

from collections import defaultdict
from fractions import Fraction

def combine_sequences(data):
    combined = defaultdict(Fraction)

    for element in data:
        if isinstance(element, dict) and "sequence" in element:
            seq = element["sequence"]
            combined[seq] += element["factor"]
    return sorted(
        [{"sequence": seq, "factor": fac} for seq, fac in combined.items()],
        key=lambda x: abs(x["factor"]),
        reverse=True
    )