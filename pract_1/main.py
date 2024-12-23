def prioritet_op(op): #приоритет операторов
    if op == '+' or op == '-': return 1
    elif op == '*' or op == '/': return 2
    return 0

def obr_pz(expr): #преобразование выражения в опз
    output = []  #для хранения опз
    stack = []  #для хранения операторов
    i = 0
    while i < len(expr):
        tek = expr[i] #текущий элемент
        if tek == ' ': #пробел пропускаем
            i += 1
            continue
        if tek.isdigit(): #если число, добавляем его в рез-т
            num = []
            while i < len(expr) and expr[i].isdigit(): #для полноценного числа
                num.append(expr[i])
                i += 1
            output.append(''.join(num))
            continue
        if tek == '(': #если (, добавляем в стек операторов
            stack.append(tek)
        elif tek == ')': #если ), выталкиваем из стека операторы до открывающей скобки
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  #удаляем открывающую скобку
        elif tek in {'+', '-', '*', '/'}: #если оператор
            while (stack and stack[-1] != '(' and
                   prioritet_op(stack[-1]) >= prioritet_op(tek)):
                output.append(stack.pop())
            stack.append(tek)
        i += 1
    while stack: #выталкиваем оставшиеся операторы из стека
        output.append(stack.pop())
    return ' '.join(output)

expr = input("Введите математическое выражение: ")
print("Обратная польская запись: ", obr_pz(expr))




