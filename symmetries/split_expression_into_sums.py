from typing import List


def split_expression_into_sums(expression:str)->List[str]:
    """
    split up an equation/expression into its separate summands - by ()
    :param expression: sum of determinants/...; we are interested in its different parts
    :return: list of the different parts of the expressions
    """
    expression = expression.replace(" ","").replace(r"\cdot","")
    factors = expression.split(')(')

    # Remove outer parentheses if present
    if expression.startswith('(') and expression.endswith(')'):
        factors[0] = factors[0][1:]
        factors[-1] = factors[-1][:-1]
    return factors


def split_sum_into_parts(factors):
    """
    split up expressions in a list into summands by +/-
    :param factors: list of combinations of irreducible representations/...
    :return: list of individual summands as list
    """
    split_factors = []

    for factor in factors:
        terms = []
        current_term = ""

        for char in factor:
            if char in ['+', '-']:
                if current_term:
                    terms.append(current_term)
                current_term = char
            else:
                current_term += char
        if current_term:# letzter Term
            terms.append(current_term)

        split_factors.append(terms)
    return split_factors
