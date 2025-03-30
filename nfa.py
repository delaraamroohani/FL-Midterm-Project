from regularGrammar import RegularGrammar

class NFA:

    def __init__(self):
        self.states = set()
        self.transitions = {} # {(state, symbol): [next_states]}
        self.start = ""
        self.accept_states = set()
        self.alphabet = set()

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

    nfa = NFA()
    nfa.start = grammar.start
    nfa.states = grammar.variables.copy()
    nfa.alphabet = grammar.alphabet.copy()
    
    for left, right in grammar.rules.items():
        for r in right:

            if r == "Îµ": # this is supposed to be epsilon
                nfa.accept_states.add(left)

            elif r[-1] in grammar.alphabet:  # therefore definitely a terminal
                new_state = "F"
                nfa.states.add(new_state)
                nfa.add_transition(left, r, new_state)
                nfa.accept_states.add(new_state)

            else:  # not a terminal therefore a variable
                nfa.add_transition(left, r[0], r[1])
    
    return nfa

