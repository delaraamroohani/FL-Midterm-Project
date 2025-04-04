from collections import deque

class DFA:

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
        self.transitions.setdefault((state, symbol), next_state) # Will not add transition if one exists already
 
def nfa_to_dfa(nfa):
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
        for symbol in dfa.alphabet:
            if (state, symbol) not in dfa.transitions.keys():
                dfa.transitions.setdefault((state, symbol), "N")
                flag = True

    if flag:
        dfa.states.add("N")
        for symbol in dfa.alphabet:
            dfa.add_transition("N", symbol, "N")
    
    for (dfa_states, name) in state_names.items():
        for acc in nfa.accept_states:
            if acc in dfa_states:
                dfa.accept_states.add(name)

    return dfa

def complement(dfa):
    dfacomp = DFA()
    dfacomp.accept_states = dfa.states.copy().difference(dfa.accept_states)
    dfacomp.states = dfa.states.copy()
    dfacomp.alphabet = dfa.alphabet.copy()
    dfacomp.states = dfa.states.copy()
    dfacomp.transitions = dfa.transitions.copy()
    dfacomp.start = dfa.start
    return dfacomp

def union(dfa1, dfa2):
    dfa = DFA()
    if dfa1.alphabet != dfa2.alphabet:
        print("Alphabets aren't equal")
        return None
    dfa.alphabet = dfa1.alphabet.copy()  # both dfas have the same alphabet
    
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

        if s1 in dfa1.accept_states or s2 in dfa2.accept_states:
            dfa.accept_states.add(current_state_name)

    return dfa

# exactly the same as union - the only difference lies in the accept states
def intersection(dfa1, dfa2):
    dfa = DFA()
    
    if dfa1.alphabet != dfa2.alphabet:
        print("Alphabets aren't equal")
        return None
    dfa.alphabet = dfa1.alphabet.copy()  # both dfas have the same alphabet
    
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

        if s1 in dfa1.accept_states and s2 in dfa2.accept_states:
            dfa.accept_states.add(current_state_name)

    return dfa
