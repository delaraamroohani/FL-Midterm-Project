from parser import parse
from nfa import grammar_to_nfa
from dfa import nfa_to_dfa, union, intersection, complement
from collections import deque

grammars = []
nfas = []
dfas = []
operation = ""

file = open("input.txt", 'r')
(grammars, operation) = parse(file)
file.close()

for grammar in grammars:
    nfas.append(grammar_to_nfa(grammar))

for nfa in nfas:
    dfas.append(nfa_to_dfa(nfa))

final_dfa = None

dfas = deque(dfas)

if operation == "Complement":
    dfa = dfas.popleft()
    final_dfa = complement(dfa)

elif operation == "Union":
    dfa = dfas.popleft()
    while dfas:
        dfa = union(dfa, dfas.popleft())
    final_dfa = dfa

elif operation == "Intersection":
    dfa = dfas.popleft()
    while dfas:
        dfa = intersection(dfa, dfas.popleft())
    final_dfa = dfa

file = open("output.txt", "w")
file.write(str(final_dfa))
file.close()
