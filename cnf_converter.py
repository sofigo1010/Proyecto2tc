class CNFConverter:
    def __init__(self, grammar):
        self.grammar = grammar
        self.new_symbol_count = 0
        self.terminal_cache = {}

    def get_new_symbol(self):
        self.new_symbol_count += 1
        return f"X{self.new_symbol_count}"

    def is_terminal(self, symbol):
        return not symbol.isupper()

    def convert_to_cnf(self):
        new_grammar = {}
        
        # Paso 1: Reemplazar terminales en producciones de longitud > 1
        for non_terminal, productions in self.grammar.items():
            new_productions = []
            for production in productions:
                # Si la producción es de longitud 1 y es un terminal, se deja como está
                if len(production) == 1 and self.is_terminal(production[0]):
                    new_productions.append(production)
                else:
                    new_production = []
                    for symbol in production:
                        if self.is_terminal(symbol):
                            if symbol not in self.terminal_cache:
                                new_symbol = self.get_new_symbol()
                                self.terminal_cache[symbol] = new_symbol
                                new_grammar[new_symbol] = [[symbol]]
                            new_production.append(self.terminal_cache[symbol])
                        else:
                            new_production.append(symbol)
                    new_productions.append(new_production)
            new_grammar[non_terminal] = new_productions
        
        # Paso 2: Descomponer producciones largas
        updated_grammar = new_grammar.copy()
        symbols_to_add = {}
        for non_terminal, productions in new_grammar.items():
            new_productions = []
            for production in productions:
                while len(production) > 2:
                    # Tomamos los últimos dos símbolos
                    last_two = production[-2:]
                    first_symbol, second_symbol = last_two
                    new_symbol = self.get_new_symbol()
                    # Añadimos la nueva producción al conjunto de símbolos por agregar
                    symbols_to_add[new_symbol] = [first_symbol, second_symbol]
                    # Reemplazamos los últimos dos símbolos por el nuevo símbolo
                    production = production[:-2] + [new_symbol]
                new_productions.append(production)
            updated_grammar[non_terminal] = new_productions
        # Añadimos las nuevas producciones al gramática actualizada
        for new_symbol, production in symbols_to_add.items():
            updated_grammar[new_symbol] = [production]
        return updated_grammar