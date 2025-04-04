from parser import parse
from nfa import grammar_to_nfa
from dfa import nfa_to_dfa, union, intersection
from collections import deque

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

i = 1
for dfa in dfas:
    print(f"DFA{i}:")
    print(dfa)
    i += 1

final_dfa = None

i = 1

dfas = deque(dfas)

if operation == "Complement":
    for dfa in dfas:
        final_dfa = dfa.complement()

elif operation == "Union":
    dfa = dfas.popleft()
    while dfas:
        dfa = union(dfa, dfas.popleft())
        print(f"Union DFA{i}")
        print(dfa)
        i += 1
    final_dfa = dfa

elif operation == "Intersection":
    dfa = dfas.popleft()
    while dfas:
        dfa = intersection(dfa, dfas.popleft())
        print(f"Intersection DFA{i}")
        print(dfa)
        i += 1
    final_dfa = dfa

print("Final DFA:")
print(final_dfa)
