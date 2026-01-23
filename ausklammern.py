from itertools import product

from symmetrie_und_orbitale.multipling_irred import multipling_irred
from symmetrie_und_orbitale.split_expression_into_sums import split_sum_into_parts
from separateAnwendungen.symmetrie_und_orbitale.split_expression_into_sums import split_expression_into_sums


### !!!!       Diese Datei ist nur zum Testen, und soll nicht von anderen Methoden importiert werden!!!!

# ausmultiplizieren
def combine_terms_separat(split_factors):
    # Verwende itertools.product, um alle Kombinationen der Teilterme zu bilden
    combinations = list(product(*split_factors))

    combined_terms = []
    for combination in combinations:
        minus_counts = sum(term.count('-') for term in combination)
        if minus_counts % 2 == 1:
            product_term= {"sign": "-"}
        else:
            product_term= {"sign": "+"}
        # filter out signs:
        product_term["eq"] = " ".join(combination).replace("-","").replace("+","")
        product_term["factors"] = [i.replace("-","").replace("+","") for i in combination]

        combined_terms.append(product_term)

    return combined_terms


# productterm = "(a+b)(c+d)(e-f)(g-h)"
productterm = "(-a+b)(-c+d)(-e+f)(-g+h)"
# productterm = "(b2g+b3u)(b3g+b2u)(au+b1g)(b1u+ag)"# Quintett links
# productterm = "(-b2g+b3u)(-b3g+b2u)(-au+b1g)(-b1u+ag)"# Quintett rechts
# # productterm = "(b3g+b2u)(b1u+ag)(b3u-b2g)(b1g-au)"# triplett 1 -triplett 3 (versch.)
# productterm = "(ag+b1u)(b1u-ag)(b2u+b3g)(b3g-b2u)"# triplett 1 -triplett 1 (gleich)
# productterm = "(b3g+b2u)(b1u+ag)(b3u-b2g)(b1g-au)"# triplett 1 -triplett 2 (versch.)
# productterm = "(b3g+b2u)(b1u+ag)(b3u-b2g)(ag-b1u)"# triplett 1 -triplett 4 (versch.)



split = split_sum_into_parts( split_expression_into_sums(productterm) )
# print(split)

########################################



combined = combine_terms_separat(split_factors=split)


###### Doppelbesetzungen rausfiltern:
for i in range(len(combined)):
    if len(set(combined[i]["factors"])) != len(combined[i]["factors"]):
        combined[i]["forbidden"] = True
    else:
        combined[i]["forbidden"] = False

print(combined)


##### Punktgruppe einsetzen  ##########


for sum in combined:
    if not sum["forbidden"]:
        print(sum["sign"], sum["eq"], end="\t=\t\t")
        # multipling_irred(sum)
        print(sum["sign"], sum["factors"][0])