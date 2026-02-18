import re


def get_irred_with_sign_and_asterics_from_equation_part(prior_latex_ci_singles:str):
    # 1) extract (...) parts
    klammer_pattern = r'\((.*?)\)'
    klammer_matches = re.findall(klammer_pattern, prior_latex_ci_singles)

    # 2) search for irred's within (...):
    term_pattern = r'[+-][a-zA-Z0-9_]+(?:\{[^}]*\})?(?:\^\{[^}]*\})?'

    all_terms = []
    for k in klammer_matches:
        terms = re.findall(term_pattern, k)
        all_terms.extend(terms)

    return all_terms


variant1 = '}_{a_{g}^{l}}\\right| \\cdot{} \\left|\\underbrace{(-a_{g}+b_u)^{1}(-a_g^{*}+b_u^{*})^{1}(+a_{u}-b_g)^{1}(+a_u^{*}-b_g^{*})^{1}'
result1 = get_irred_with_sign_and_asterics_from_equation_part(variant1)

variant2 = '}_{a_1^{l}}\\right| \\cdot{} \\left|\\underbrace{(-a_1+b_2)^{1}(-a_1^{*}+b_2^{*})^{1}(-b_1+a_2)^{1}(-b_1^{*}+a_2^{*})^{1}'
result2 = get_irred_with_sign_and_asterics_from_equation_part(variant2)

assert result1 == ['-a_{g}', '+b_u', '-a_g^{*}', '+b_u^{*}', '+a_{u}', '-b_g', '+a_u^{*}', '-b_g^{*}']
assert result2 == ['-a_1', '+b_2', '-a_1^{*}', '+b_2^{*}', '-b_1', '+a_2', '-b_1^{*}', '+a_2^{*}']

variant3 = '}_{a_{g}^{l}}\\right| \\cdot{} \\left|\\underbrace{(-a_{g}+b_u)^{1}(-a_g^{*}+b_u^{*})^{1}(+a_{u}-b_g)^{1}(+a_u^{*}-b_g^{*})^{1}'
result3 = get_irred_with_sign_and_asterics_from_equation_part(variant3)
assert result3 == ['-a_{g}', '+b_u', '-a_g^{*}', '+b_u^{*}', '+a_{u}', '-b_g', '+a_u^{*}', '-b_g^{*}']