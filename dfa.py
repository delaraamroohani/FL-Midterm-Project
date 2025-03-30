from collections import deque

class DFA:

    def __init__(self):
        self.states = set()
        self.transitions = {}  # {(state, symbol): next_state} 
        self.start = ""                           # notice there is only one next state
        self.accept_states = set()

    def __str__(self):
        return f"States: {self.states}\nTransitions: {self.transitions}\nStart: {self.start}\nAccept states: {self.accept_states}"

    def add_transition(self, state, symbol, next_state):
        self.transitions.setdefault((state, symbol), next_state) # Will not add transition if one exists already

def nfa_to_dfa(nfa):
    dfa = DFA()
    dfa.start = "q0"
    
    state_names = {} # {symbol: set(states)}
    state_num = 1

    states_queue = deque()
    states_queue.append(frozenset(nfa.start))
    state_names.setdefault(frozenset(nfa.start), "q0")
    checked = set()

    while states_queue:

        states_set = states_queue.popleft()
        checked.add(states_set)
        # print("States set: " + str(states_set))
        transitions = {}

        for s in states_set:
            temp_transitions = nfa.get_state_transitions(s)
            # print("Temp transitions: " + str(temp_transitions))
            for symbol, next_states in temp_transitions.items():
                transitions.setdefault(symbol, set()).update(next_states)

        # print("Transitions: " + str(transitions))

        for (symbol, next_states) in transitions.items():
            next_states = frozenset(next_states)
            # print(f"Symbol: {symbol}, Next states: {next_states}")
            state_names.setdefault(next_states, f"q{state_num}")
            if state_names.get(next_states) == f"q{state_num}":
                state_num += 1
            dfa.add_transition(state_names.get(states_set), symbol, state_names.get(next_states))
            # print("States names keys: " + str(state_names.keys()))
            if next_states not in checked:
                states_queue.append(next_states) 
            dfa.transitions.setdefault((state_names.get(states_set), symbol), state_names.get(next_states)) 

    dfa.states.update(state_names.values())

    flag = False
    for state in dfa.states:
        for symbol in nfa.alphabet:
            if (state, symbol) not in dfa.transitions.keys():
                dfa.transitions.setdefault((state, symbol), "N")
                flag = True

    if flag:
        dfa.states.add("N")
    
    for (dfa_states, name) in state_names.items():
        for acc in nfa.accept_states:
            if acc in dfa_states:
                dfa.accept_states.add(name)

    return dfa


    

    

