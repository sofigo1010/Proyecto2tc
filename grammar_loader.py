import os
import re

class GrammarLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.non_terminals = set()
        self.terminals = set()
        self.start_symbol = None  

    def load_grammar(self):
        """
        Carga una gramática desde un archivo de texto y valida su formato.

        Returns:
            dict: Diccionario que representa la gramática cargada.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"El archivo '{self.file_path}' no existe.")

        grammar = {}
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        
        for line in lines:
            line = line.strip()
            if not line or '->' not in line:
                continue
            left_side, _ = map(str.strip, line.split('->'))
            if self.start_symbol is None:
                self.start_symbol = left_side  
            self.non_terminals.add(left_side)

        
        for line in lines:
            line = line.strip()
            if not line or '->' not in line:
                continue
            _, right_side = map(str.strip, line.split('->'))
            productions = [prod.strip() for prod in right_side.split('|')]

            for prod in productions:
                if prod != 'ε':
                    
                    symbols = re.findall(r'\b\w+\b|\S', prod)
                    for symbol in symbols:
                        if symbol not in self.non_terminals and not symbol.isupper():
                            self.terminals.add(symbol)

        
        for line in lines:
            line = line.strip()
            if not line or '->' not in line:
                continue

            
            left_side, right_side = map(str.strip, line.split('->'))

            
            productions = [prod.strip() for prod in right_side.split('|')]

            
            processed_productions = []
            for prod in productions:
                if prod != 'ε':
                    symbols = self.tokenize_production(prod)
                    processed_productions.append(symbols)
                else:
                    processed_productions.append(['ε'])  # Representamos ε como una lista con 'ε'

            
            if left_side in grammar:
                grammar[left_side].extend(processed_productions)
            else:
                grammar[left_side] = processed_productions

        return grammar

    def tokenize_production(self, production):
        """
        Tokeniza una producción en símbolos, utilizando los símbolos conocidos.
        """
       
        all_symbols = list(self.non_terminals) + list(self.terminals)
        
        all_symbols.sort(key=len, reverse=True)

        tokens = []
        index = 0
        production = production.strip()
        while index < len(production):
            match_found = False
            for symbol in all_symbols:
                symbol_length = len(symbol)
                if production[index:index+symbol_length] == symbol:
                    tokens.append(symbol)
                    index += symbol_length
                    match_found = True
                    break
            if not match_found:
                if production[index].isspace():
                    
                    index += 1
                else:
                    
                    
                    unknown_symbol = production[index]
                    tokens.append(unknown_symbol)
                    index += 1
        return tokens