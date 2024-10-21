def generate_combinations(symbols, nullable_symbols):
    from itertools import product

    options = []
    for symbol in symbols:
        if symbol in nullable_symbols:
            options.append([symbol, None])  # None representa omisión
        else:
            options.append([symbol])

    all_combinations = set()
    for combination in product(*options):
        # Remover valores None (símbolos omitidos)
        new_combination = tuple(s for s in combination if s is not None)
        if new_combination:
            all_combinations.add(new_combination)
    return all_combinations


def display_grammar(grammar):
    """
    Muestra la gramática en un formato legible.

    Args:
        grammar (dict): Diccionario que representa la gramática.
    """
    for non_terminal, productions in grammar.items():
        productions_str = []
        for prod in productions:
            if prod == ['ε']:
                productions_str.append('ε')
            else:
                productions_str.append(' '.join(prod))
        productions_line = ' | '.join(productions_str)
        print(f"{non_terminal} -> {productions_line}")
