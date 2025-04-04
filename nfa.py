"""
nfa.py

This module contains the NFA (Nondeterministic Finite Automaton) class
and a function to convert regular grammars into NFAs.

Classes:
    NFA: Represents an NFA.

Functions:
    grammar_to_nfa(grammar): Converts regular grammar to equivalent 
      NFA. 
"""

from regularGrammar import RegularGrammar

class NFA:
    """
    Represents a nondeterministic finite automaton (NFA).

    Attributes:
        states (set): Set of state names.
        transitions (dict): Mapping from (state, symbol) to the 
          set(next states).
        start (str): The start state.
        accept_states (set): Set of accepting (final) states.
        alphabet (set): Set of input symbols.

    Methods:
        add_transition(state, symbol, next_state): Adds a transition to
          the NFA.
        get_state_transitions(state): Returns all transitions from 
          state with any symbol other states in the form
          (symbol, set(next_states))
    """

    def __init__(self):
        self.states = set()
        self.transitions = {} # {(state, symbol): [next_states]}
        self.start = ""
        self.accept_states = set()
        self.alphabet = set()

    # Made for debugging purposes.
    def __str__(self):
        return f"States: {self.states}\nTransitions: {self.transitions}\nStart: {self.start}\nAccept states: {self.accept_states}"

    def add_transition(self, state, symbol, next_state):
        self.transitions.setdefault((state, symbol), []).append(next_state)

    def get_state_transitions(self, state):
        ans = {}
        for (s, symbol) in self.transitions.keys():
            if s == state:
                ans.setdefault(symbol, self.transitions.get((s, symbol)))
        return ans

def grammar_to_nfa(grammar):
    """Converts a regular grammar into an NFA."""

    nfa = NFA()
    nfa.start = grammar.start
    nfa.states = grammar.variables.copy()
    nfa.alphabet = grammar.alphabet.copy()
    
    # Left-hand side variable, right-hand side production.
    for left, right in grammar.rules.items(): 
        
        for r in right:

            if r == "Îµ": # This is supposed to be epsilon
                nfa.accept_states.add(left)

            # If RHS ends with a terminal, we have a new accept state.
            elif r[-1] in grammar.alphabet:  
                new_state = "F"
                nfa.states.add(new_state)
                nfa.add_transition(left, r, new_state)
                nfa.accept_states.add(new_state)

            else:
                nfa.add_transition(left, r[0], r[1])
    
    return nfa

