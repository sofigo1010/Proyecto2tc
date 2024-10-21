import time
from grammar_loader import GrammarLoader
from cnf_converter import CNFConverter
from cyk_algorithm import CYKAlgorithm
from epsilon_remover import EpsilonRemover
from unary_remover import UnaryRemover
from useless_symbols_remover import UselessSymbolsRemover

def format_production(production):
    """
    Convierte una producción que es una lista de símbolos en una cadena de texto.
    """
    if production == ['ε']:
        return 'ε'
    return ' '.join(production)

def format_grammar(grammar):
    """
    Convierte y formatea la gramática para su impresión.
    """
    formatted_grammar = []
    for non_terminal, productions in grammar.items():
        formatted_productions = [format_production(p) for p in productions]
        formatted_grammar.append(f"{non_terminal} -> {' | '.join(formatted_productions)}")
    return '\n'.join(formatted_grammar)

def main():
    # Cargar gramática desde archivo
    grammar_file = input("Ingrese el nombre del archivo de gramática (por ejemplo, 'grammar.txt'): ")
    
    try:
        loader = GrammarLoader(grammar_file)
        grammar = loader.load_grammar()
        
        # Mostrar gramática cargada
        print("\n=== Gramática original ===")
        print(format_grammar(grammar))

        # Eliminar producciones-ε
        print("\n=== Iniciando el proceso de eliminación de producciones-ε ===")
        epsilon_remover = EpsilonRemover(grammar)
        grammar_without_epsilon = epsilon_remover.remove_epsilon_productions()
        
        print("\n=== Gramática después de eliminar producciones-ε ===")
        print(format_grammar(grammar_without_epsilon))

        # Eliminar producciones unarias
        print("\n=== Iniciando el proceso de eliminación de producciones unarias ===")
        unary_remover = UnaryRemover(grammar_without_epsilon)
        grammar_without_unary = unary_remover.remove_unary_productions()

        print("\n=== Gramática después de eliminar producciones unarias ===")
        print(format_grammar(grammar_without_unary))

        # Eliminar símbolos inútiles
        print("\n=== Iniciando el proceso de eliminación de símbolos inútiles ===")
        useless_remover = UselessSymbolsRemover(grammar_without_unary)
        grammar_without_useless = useless_remover.remove_useless_symbols()

        print("\n=== Gramática después de eliminar símbolos inútiles ===")
        print(format_grammar(grammar_without_useless))

        # Convertir a CNF
        print("\n=== Iniciando la conversión a Forma Normal de Chomsky (CNF) ===")
        cnf_converter = CNFConverter(grammar_without_useless, loader.start_symbol)
        cnf_grammar, cnf_start_symbol = cnf_converter.convert_to_cnf()

        # Mostrar la gramática en CNF
        print("\n=== Gramática en Forma Normal de Chomsky (CNF) ===")
        print(format_grammar(cnf_grammar))

        # Ingresar una oración en inglés
        sentence = input("\nIngrese la oración en inglés para analizar: ")

        # Aplicar el algoritmo CYK
        print("\n=== Iniciando el algoritmo CYK ===")
        cyk = CYKAlgorithm(cnf_grammar, list(loader.terminals), cnf_start_symbol)
        print("Terminales:", loader.terminals)
        accepted, elapsed_time = cyk.parse(sentence)

        # Mostrar el resultado y el árbol de parseo
        if accepted:
            print(f"\nSÍ, la oración '{sentence}' pertenece al lenguaje.")
            print(f"Tiempo de ejecución: {elapsed_time:.6f} segundos")
            print("\nÁrbol de parseo:")
            cyk.print_parse_tree(cyk.parse_tree)
        else:
            print(f"\nNO, la oración '{sentence}' no pertenece al lenguaje.")
            print(f"Tiempo de ejecución: {elapsed_time:.6f} segundos")
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()