class UselessSymbolsRemover:
    def __init__(self, grammar):
        self.grammar = grammar

    def remove_useless_symbols(self):
        """
        Elimina los símbolos inútiles y no terminales inalcanzables de la gramática.
        """
       
        generative = set()
        changed = True
        while changed:
            changed = False
            for non_terminal, productions in self.grammar.items():
                if non_terminal not in generative:
                    for production in productions:
                        if all(symbol in generative or symbol not in self.grammar for symbol in production):
                            generative.add(non_terminal)
                            changed = True
                            break

        
        reachable = set()
        
        initial_symbol = next(iter(self.grammar))
        to_process = [initial_symbol]

        while to_process:
            current = to_process.pop()
            if current not in reachable and current in self.grammar:
                reachable.add(current)
                for production in self.grammar[current]:
                    for symbol in production:
                        if symbol in self.grammar and symbol not in reachable:
                            to_process.append(symbol)

        
        new_grammar = {}
        for non_terminal in self.grammar:
            if non_terminal in reachable and non_terminal in generative:
                new_productions = []
                for production in self.grammar[non_terminal]:
                    if all(symbol in generative or symbol not in self.grammar for symbol in production):
                        new_productions.append(production)
                if new_productions:
                    new_grammar[non_terminal] = new_productions

        return new_grammar
