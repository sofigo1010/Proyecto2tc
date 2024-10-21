class CNFConverter:
    def __init__(self, grammar, start_symbol):
        self.grammar = grammar
        self.new_symbol_count = 0
        self.terminal_cache = {}
        self.start_symbol = start_symbol 

    def get_new_symbol(self):
        self.new_symbol_count += 1
        return f"X{self.new_symbol_count}"

    def is_terminal(self, symbol):
        return not symbol.isupper()

    def convert_to_cnf(self):
        new_grammar = {}
        new_start_symbol = self.start_symbol
        
        
        for non_terminal, productions in self.grammar.items():
            new_productions = []
            for production in productions:
                
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
        
        
        updated_grammar = new_grammar.copy()
        symbols_to_add = {}
        for non_terminal, productions in new_grammar.items():
            new_productions = []
            for production in productions:
                while len(production) > 2:
                    
                    last_two = production[-2:]
                    first_symbol, second_symbol = last_two
                    new_symbol = self.get_new_symbol()
                   
                    symbols_to_add[new_symbol] = [first_symbol, second_symbol]
                    
                    production = production[:-2] + [new_symbol]
                new_productions.append(production)
            updated_grammar[non_terminal] = new_productions
        
        for new_symbol, production in symbols_to_add.items():
            updated_grammar[new_symbol] = [production]
        return updated_grammar, new_start_symbol
