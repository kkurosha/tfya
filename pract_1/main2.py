def operation(op1, op2, op): #для выполнения операций
    if op == '+': return op1 + op2
    elif op == '-': return op1 - op2
    elif op == '*': return op1 * op2
    elif op == '/': return op1 / op2

def to_opz(opz_expr): #вычисление выражения в опз
    stack = []
    arr_tek = opz_expr.split()
    for tek in arr_tek:
        if tek.isdigit(): stack.append(int(tek)) #если число -> в стек
        elif tek in {'+', '-', '*', '/'}: #eсли это оператор,
            op2 = stack.pop()             #извлекаем два числа
            op1 = stack.pop()
            result = operation(op1, op2, tek) #и применяем оператор
            stack.append(result)
    return stack[0] #результат вычисления в стеке

opz_expr = input("Введите выражение в обратной польской записи: ")
print("Результат выражения: ", int(to_opz(opz_expr)))





