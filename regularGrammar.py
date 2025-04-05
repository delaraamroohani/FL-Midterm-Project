"""
regularGrammar.py

A module that contains the class RegularGrammar.
"""

class RegularGrammar:
    """Represents a regular grammar.
    
    Attributes:
        alphabet (set): Set of alphabet.
        variables (set): Set of variables.
        start (str): The start variable.
        rules (dict): Mapping from variable to production.
    """

    alphabet = set()
    variables = set()
    start = ""
    rules = {}
    
    def __init__(self, alphabet, variables, start, rules):
        self.alphabet = alphabet
        self.variables = variables
        self.start = start
        self.rules = rules

    def __str__(self):
        # Made for debugging purposes.
        return f"Alphabet: {self.alphabet}\nVariables: {self.variables}\nStart: {self.start}\nRules: {self.rules}"

