"""
dfa.py

This module contains the DFA (Deterministic Finite Automaton) class
and contains functions for converting NFAs to DFAs, and for computing
operations such as union, intersection, and complement on DFAs.

Classes:
    DFA: Represents a DFA.

Functions:
    complement(dfa): Returns the complement of a given DFA.
    nfa_to_dfa(nfa): Converts an NFA to an equivalent DFA.
    union(dfa1, dfa2): Returns the DFA that accepts the union of two 
      input DFAs.
    intersection(dfa1, dfa2): Returns the DFA that accepts the 
      intersection of two input DFAs.
"""
from collections import deque

class DFA:
    """
    Represents a deterministic finite automaton (DFA).

    Attributes:
        states (set): Set of state names.
        transitions (dict): Mapping from (state, symbol) to the next state.
        start (str): The start state.
        accept_states (set): Set of accepting (final) states.
        alphabet (set): Set of input symbols.

    Methods:
        add_transition(state, symbol, next_state): Adds a transition to the DFA.
    """

    def __init__(self):
        self.states = set()
        self.transitions = {}  # {(state, symbol): next_state} 
        self.start = ""                           # notice there is only one next state
        self.accept_states = set()
        self.alphabet = set()

    def __str__(self):
        s = "# States\n"
        s += " ".join(map(str, self.states))
        s += "\n# Alphabet\n"
        s += " ".join(map(str, self.alphabet))
        s += "\n# Start State\n"
        s += self.start
        s += "\n# Final States\n"
        s += " ".join(map(str, self.accept_states))
        s += "\n# Transitions\n"
        
        for ((state, symbol), next_state) in self.transitions.items():
            s += f"{state} {symbol} {next_state}\n"

        return s

    def add_transition(self, state, symbol, next_state):
        # Will not add transition if one with same state and symbol exists already.
        self.transitions.setdefault((state, symbol), next_state)
 
def nfa_to_dfa(nfa):
    """Converts an NFA to an equivalent DFA."""

    dfa = DFA()
    dfa.start = "q0"
    dfa.alphabet = nfa.alphabet
    
    state_names = {} # {set(states): symbol}
    state_num = 1

    states_queue = deque()
    states_queue.append(frozenset(nfa.start))
    state_names.setdefault(frozenset(nfa.start), "q0")
    checked = set()

    while states_queue:

        states_set = states_queue.popleft()
        checked.add(states_set)
        transitions = {}

        # Get all transitions from the states that have been popped.
        for s in states_set:
            temp_transitions = nfa.get_state_transitions(s)
            for symbol, next_states in temp_transitions.items():
                transitions.setdefault(symbol, set()).update(next_states)

        # Create states for each set of states and add them to the queue
        # to be checked if they haven't been checked already. 
        for (symbol, next_states) in transitions.items():
            next_states = frozenset(next_states)
            state_names.setdefault(next_states, f"q{state_num}")
            if state_names.get(next_states) == f"q{state_num}":
                state_num += 1
            dfa.add_transition(state_names.get(states_set), symbol, state_names.get(next_states))
            if next_states not in checked:
                states_queue.append(next_states) 
            dfa.transitions.setdefault((state_names.get(states_set), symbol), state_names.get(next_states))

    dfa.states.update(state_names.values())

    # Check if there are states that don't have a transition for all of
    # the alphabet and transition them to "N".
    flag = False
    for state in dfa.states:
        for symbol in dfa.alphabet:
            if (state, symbol) not in dfa.transitions.keys():
                dfa.transitions.setdefault((state, symbol), "N")
                flag = True

    if flag:
        dfa.states.add("N")
        for symbol in dfa.alphabet:
            dfa.add_transition("N", symbol, "N")
    
    # Update accept states based on those of equivalent NFA.
    for (dfa_states, name) in state_names.items():
        for acc in nfa.accept_states:
            if acc in dfa_states:
                dfa.accept_states.add(name)

    return dfa

def complement(dfa):
    """Returns the complement of a given DFA."""

    dfacomp = DFA()
    # Switch accept states and normal states.
    dfacomp.accept_states = dfa.states.copy().difference(dfa.accept_states)
    dfacomp.states = dfa.states.copy()
    dfacomp.alphabet = dfa.alphabet.copy()
    dfacomp.states = dfa.states.copy()
    dfacomp.transitions = dfa.transitions.copy()
    dfacomp.start = dfa.start
    return dfacomp

def union(dfa1, dfa2):
    """Computes the union of two DFAs."""

    dfa = DFA()
    if dfa1.alphabet != dfa2.alphabet:
        print("Alphabets aren't equal")
        return None
    dfa.alphabet = dfa1.alphabet.copy()  # Both dfas have the same alphabet.
    
    # Each state in dfa1 * dfa2 is a tuple consisting of a state
    # from dfa1 and a state from dfa2.
    start_state = (dfa1.start, dfa2.start)
    dfa.start = "q0"

    states_queue = deque([start_state])
    checked = set()
    state_mapping = {start_state: "q0"}
    dfa.states.add("q0")
    
    state_count = 1

    while states_queue:
        (s1, s2) = states_queue.popleft()
        checked.add((s1, s2))
        current_state_name = state_mapping[(s1, s2)]

        # Get next state by checking next state for each state in each
        # respective dfa and add them to queue if they haven't been 
        # checked already.
        for symbol in dfa.alphabet:
            next_s1 = dfa1.transitions.get((s1, symbol))
            next_s2 = dfa2.transitions.get((s2, symbol))
            next_state = (next_s1, next_s2)

            if next_state not in state_mapping and next_state not in checked:
                new_state_name = f"q{state_count}"
                state_mapping[next_state] = new_state_name
                state_count += 1
                dfa.states.add(new_state_name)
                states_queue.append(next_state)

            dfa.add_transition(current_state_name, symbol, state_mapping[next_state])

        # For union, if either states are accept states in each 
        # respective dfa, the state will be an accept state.
        if s1 in dfa1.accept_states or s2 in dfa2.accept_states:
            dfa.accept_states.add(current_state_name)

    return dfa

def intersection(dfa1, dfa2):
    """Computes the intersection of two DFAs."""
    # Exactly the same as union - the only difference lies in the accept states.

    dfa = DFA()
    
    if dfa1.alphabet != dfa2.alphabet:
        print("Alphabets aren't equal")
        return None
    dfa.alphabet = dfa1.alphabet.copy()
    
    start_state = (dfa1.start, dfa2.start)
    dfa.start = "q0"

    states_queue = deque([start_state])
    checked = set()
    state_mapping = {start_state: "q0"}
    dfa.states.add("q0")
    
    state_count = 1

    while states_queue:
        (s1, s2) = states_queue.popleft()
        checked.add((s1, s2))
        current_state_name = state_mapping[(s1, s2)]

        for symbol in dfa.alphabet:
            next_s1 = dfa1.transitions.get((s1, symbol))
            next_s2 = dfa2.transitions.get((s2, symbol))
            next_state = (next_s1, next_s2)

            if next_state not in state_mapping and next_state not in checked:
                new_state_name = f"q{state_count}"
                state_mapping[next_state] = new_state_name
                state_count += 1
                dfa.states.add(new_state_name)
                states_queue.append(next_state)

            dfa.add_transition(current_state_name, symbol, state_mapping[next_state])

        # For intersection, if both states are accept states in each 
        # respective dfa, the state will be an accept state.
        if s1 in dfa1.accept_states and s2 in dfa2.accept_states:
            dfa.accept_states.add(current_state_name)

    return dfa
