from parser import parse
from nfa import grammar_to_nfa
from dfa import nfa_to_dfa, union

grammars = []
nfas = []
dfas = []
operation = ""

file = open("input.txt", 'r')
(grammars, operation) = parse(file)

for grammar in grammars:
    nfas.append(grammar_to_nfa(grammar))

for nfa in nfas:
    dfas.append(nfa_to_dfa(nfa))

for dfa in dfas:
    print("DFA:")
    print(dfa)

final_dfa = None

if operation == "Complement":
    for dfa in dfas:
        final_dfa = dfa.complement()

elif operation == "Union":
    dfa = dfas[0]
    for i in range(1, len(dfas)):
        dfa = union(dfa, dfas[i])
    final_dfa = dfa

print("Final DFA:")
print(final_dfa)
