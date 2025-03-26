class RegularGrammar:

    alphabet = set()
    variables = set()
    start = ''
    rules = {}
    
    def __init__(self, alphabet, variables, start, rules):
        self.alphabet = alphabet
        self.variables = variables
        self.start = start
        self.rules = rules

    def __str__(self):
        return f"Alphabet: {self.alphabet}\nVariables: {self.variables}\nSatrt: {self.start}\nRules: {self.rules}"

