import time 

class CYKAlgorithm:
    def __init__(self, cnf_grammar, terminals, start_symbol):
        self.cnf_grammar = cnf_grammar
        self.parse_tree = None
        self.terminals = terminals  
        self.start_symbol = start_symbol

    def tokenize_sentence(self, sentence):
        """
        Tokeniza la oración de entrada utilizando los terminales conocidos.
        """
        
        terminals_sorted = sorted(self.terminals, key=len, reverse=True)
        tokens = []
        index = 0
        sentence = sentence.strip()
        while index < len(sentence):
            match_found = False
            for terminal in terminals_sorted:
                terminal_length = len(terminal)
                if sentence[index:index+terminal_length] == terminal:
                    tokens.append(terminal)
                    index += terminal_length
                    match_found = True
                    break
            if not match_found:
                if sentence[index].isspace():
                    
                    index += 1
                else:
                    
                    unknown_symbol = sentence[index]
                    tokens.append(unknown_symbol)
                    index += 1
        return tokens

    def parse(self, sentence):
        start_time = time.time()

        
        words = self.tokenize_sentence(sentence)
        n = len(words)
        table = [[set() for _ in range(n)] for _ in range(n)]
        backpointers = [[{} for _ in range(n)] for _ in range(n)]

       
        for i, word in enumerate(words):
            for non_terminal, productions in self.cnf_grammar.items():
                for production in productions:
                    if len(production) == 1 and production[0] == word:
                        table[i][i].add(non_terminal)
                        backpointers[i][i][non_terminal] = word

        
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                for k in range(i, j):
                    for non_terminal, productions in self.cnf_grammar.items():
                        for production in productions:
                            if len(production) == 2:
                                B, C = production
                                if B in table[i][k] and C in table[k + 1][j]:
                                    table[i][j].add(non_terminal)
                                    backpointers[i][j][non_terminal] = (B, C, k)

        
        start_symbol = self.start_symbol
        accepted = start_symbol in table[0][n - 1]
        end_time = time.time()

        if accepted:
            self.parse_tree = self.build_parse_tree(backpointers, 0, n - 1, start_symbol)

        return accepted, end_time - start_time

    def build_parse_tree(self, backpointers, i, j, symbol):
        if i == j:
            return (symbol, backpointers[i][j][symbol])
        B, C, k = backpointers[i][j][symbol]
        left_tree = self.build_parse_tree(backpointers, i, k, B)
        right_tree = self.build_parse_tree(backpointers, k + 1, j, C)
        return (symbol, left_tree, right_tree)

    def print_parse_tree(self, tree, level=0):
        indent = "  " * level
        if isinstance(tree, tuple):
            symbol = tree[0]
            children = tree[1:]
            print(f"{indent}{symbol}")
            for child in children:
                self.print_parse_tree(child, level + 1)
        else:
            print(f"{indent}{tree}")


    def build_parse_tree(self, backpointers, i, j, symbol):
        if i == j:
            return (symbol, backpointers[i][j][symbol])
        B, C, k = backpointers[i][j][symbol]
        left_tree = self.build_parse_tree(backpointers, i, k, B)
        right_tree = self.build_parse_tree(backpointers, k + 1, j, C)
        return (symbol, left_tree, right_tree)

    def print_parse_tree(self, tree, level=0):
        indent = "  " * level
        if isinstance(tree, tuple):
            symbol = tree[0]
            children = tree[1:]
            print(f"{indent}{symbol}")
            for child in children:
                self.print_parse_tree(child, level + 1)
        else:
            print(f"{indent}{tree}")
