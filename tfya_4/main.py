from collections import defaultdict #чтобы в словарях значения по умолчанию были списками

def get_next_states(states, symbol, moves): #найти все состояния, в которые можно перейти по данному символу
    result = set() #хранятся все состояния
    for state in states:
        result.update(moves.get((state, symbol), []))
    return result #множество состояний

def nfa_to_dfa(states, alph, moves, initial_states, final_states): #НКА в ДКА
    dfa_transitions = {} #переходы ДКА
    dfa_states = [] #список всех состояний ДКА
    start_states = [frozenset(initial_states)]  #начальное состояние (1)
    dfa_initial_state = start_states[0] #(1)
    while start_states:
        current = start_states.pop() #текущее состояние
        dfa_states.append(current) #добавление текущего состояния в список состояний ДКА
        for symbol in alph:
            next_states = get_next_states(current, symbol, moves) #получение след. состояния
            next_states = frozenset(next_states)
            if next_states and next_states not in dfa_states and next_states not in start_states:
                start_states.append(next_states) #если состояние новое, добавляем в список
            if next_states: #добавляем переход в список переходов
                dfa_transitions[(current, symbol)] = next_states
    dfa_final_states = [s for s in dfa_states if s.intersection(final_states)] #финальное состояние
    return dfa_states, dfa_transitions, dfa_initial_state, dfa_final_states


states = input("Enter set of states:\n").split() #набор состояний
alph = input("Enter the input alphabet:\n").split() #алфавит
moves = defaultdict(list) #словарь переходов
print("Enter state-transitions function (current state, input character, next state):")
while True: #ввод до пустой строки
    line = input()
    if not line: break #если ничего не вводится
    for transition in line.split(): #обрабатываем переходы
        current_state, input_char, next_state = transition.strip('()').split(',')
        #из текущего состояния по символу можно перейти в следующее состояние
        moves[(current_state, input_char)].append(next_state)
initial_states = set(input("Enter a set of initial states:\n").split()) #начальное состояние
final_states = set(input("Enter a set of final states:\n").split()) #конечное
#преобразование НКА в ДКА
dfa_states, dfa_transitions, dfa_initial_state, dfa_final_states = nfa_to_dfa(
    states, alph, moves, initial_states, final_states)

#вывод
print("DFA:")
print("Set of states:", ", ".join(''.join(s) for s in dfa_states))
print("Input alphabet:", ", ".join(alph))
print("State-transitions function:")
for (state, symbol), next_state in dfa_transitions.items():
    print(f"D({''.join(state)}, {symbol}) = {''.join(next_state)}")
print("Initial states:", ''.join(dfa_initial_state))
print("Final states:", ', '.join(''.join(s) for s in dfa_final_states))

# (1,a,1) (1,a,2) (1,b,3) (2,a,2) (2,b,1) (2,b,3) (3,a,3) (3,b,3)