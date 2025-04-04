""""
main.py

This is the main module of the project. It reads the regular grammars
from the input.txt file, turns them into NFAs, turns the NFAs to DFAs, 
does the specified operation on the DFAs, and writes the final DFA into
the a file named output.txt.
"""

from parser import parse
from nfa import grammar_to_nfa
from dfa import nfa_to_dfa, union, intersection, complement
from collections import deque

grammars = []
nfas = []
dfas = []
operation = ""

# Read and parse input.txt
file = open("input.txt", 'r')
(grammars, operation) = parse(file)
file.close()

# Turn grammars into NFAs
for grammar in grammars:
    nfas.append(grammar_to_nfa(grammar))

# Turn NFAs to DFAs
for nfa in nfas:
    dfas.append(nfa_to_dfa(nfa))

final_dfa = None

dfas = deque(dfas)

# Do specified operation on DFAs
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

# Write final DFA in output.txt
file = open("output.txt", "w")
file.write(str(final_dfa))
file.close()
