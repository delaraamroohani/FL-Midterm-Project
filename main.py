from parser import parse
from nfa import grammar_to_nfa
from dfa import nfa_to_dfa

grammars = []
nfas = []
dfas = []
operation = ""

file = open("input.txt", 'r')
(grammars, operation) = parse(file)

for grammar in grammars:
    nfas.append(grammar_to_nfa(grammar))

for nfa in nfas:
    print("NFA:")
    print(nfa)
    dfas.append(nfa_to_dfa(nfa))

for dfa in dfas:
    print("DFA:")
    print(dfa)



