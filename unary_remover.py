class UnaryRemover:
    def __init__(self, grammar):
        self.grammar = grammar

    def remove_unary_productions(self):
        """
        Elimina las producciones unarias de la gramática (A -> B, donde A y B son no terminales).
        """
        new_grammar = {}

        for non_terminal in self.grammar:
            
            new_productions = set()
            unaries_to_process = set()
            processed_unaries = set()

            
            productions = self.grammar[non_terminal]

            
            for production in productions:
                if len(production) == 1 and production[0].isupper():
                    unaries_to_process.add(production[0])
                else:
                    new_productions.add(tuple(production))

            
            while unaries_to_process:
                unary = unaries_to_process.pop()

                
                if unary in processed_unaries:
                    continue
                processed_unaries.add(unary)

                
                if unary in self.grammar:
                    for prod in self.grammar[unary]:
                        if len(prod) == 1 and prod[0].isupper():
                            if prod[0] != non_terminal and prod[0] not in processed_unaries:
                                unaries_to_process.add(prod[0])
                        else:
                            new_productions.add(tuple(prod))

            new_grammar[non_terminal] = [list(prod) for prod in new_productions]

        return new_grammar
