from parser import parse
from nfa import grammar_to_nfa

grammars = []
nfas = []
operation = ""

file = open("input.txt", 'r')
(grammars, operation) = parse(file)

for grammar in grammars:
    nfas.append(grammar_to_nfa(grammar))

for nfa in nfas:
    print(nfa)

