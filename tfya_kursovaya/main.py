class Lexer:
    RESERVED_WORDS = {  # ключевые слова
        "if": "IF",
        "then": "THEN",
        "else": "ELSE",
        "for": "FOR",
        "to": "TO",
        "do": "DO",
        "while": "WHILE",
        "read": "READ",
        "write": "WRITE",
        "as": "ASSIGN",
        "true": "TRUE",
        "false": "FALSE",
        "and": "AND",
        "or": "OR",
        "not": "NOT",
        "dim": "DIM",
    }

    SYMBOLS = {  # разделители
        "{": "LBRACE",
        "}": "RBRACE",
        "[": "LBRACKET",
        "]": "RBRACKET",
        ";": "SEMICOLON",
        ",": "COMMA",
        "(": "LPAREN",
        ")": "RPAREN",
        ":": "COLON",
    }

    TYPE = {  # типы данных
        "%": "INT",
        "!": "REAL",
        "$": "BOOL",
    }

    OPERATORS = {  # операторы
        "+": "ADD_OP",
        "-": "ADD_OP",
        "*": "MUL_OP",
        "/": "MUL_OP",
        "=": "REL_OP",
        "<>": "REL_OP",
        ">=": "REL_OP",
        "<=": "REL_OP",
        "<": "REL_OP",
        ">": "REL_OP",
    }

    def __init__(self, program_text):
        self.program_lines = program_text.splitlines() # текст разбивается на строки
        self.lexemes = []  # список лексем
        self.column_number = 0  # текущая колонка
        self.line_number = 0  # текущая строка

    def analyze_line(self, line):  # анализ одной строки
        accumulator = ""   # символы лексемы
        current_state = "START"  # начальное состояние
        for idx, char in enumerate(line, start=1):
            self.column_number = idx  # номер колонки

            if current_state == "START":
                if char.isspace():  # пропуск пробелов
                    continue
                elif char.isalpha():
                    accumulator += char
                    current_state = "IDENTIFIER"  # обработка идентификаторов
                elif char.isdigit() or (char == '.' and accumulator):
                    accumulator += char
                    current_state = "NUMBER"  # обработка чисел
                elif char in self.SYMBOLS:
                    self.add_lexeme(self.SYMBOLS[char], char)  # добавление символа
                elif char in "<>=":
                    accumulator += char
                    current_state = "REL_OPERATOR"  # операторы сравнения
                elif char in self.OPERATORS:  # добавление оператора
                    self.add_lexeme(self.OPERATORS[char], char)
                elif char in self.TYPE:  # добавление типа данных
                    self.add_lexeme(self.TYPE[char], char)
                else:
                    print(f"Ошибка: Неизвестный символ '{char}' в строке {self.line_number}, колонке {self.column_number}.")

            elif current_state == "IDENTIFIER":  # обработка идентификаторов
                if char.isalnum():
                    accumulator += char
                else:
                    if accumulator in self.RESERVED_WORDS:
                        self.add_lexeme(self.RESERVED_WORDS[accumulator], accumulator)
                    else:
                        self.add_lexeme("IDENTIFIER", accumulator)
                    accumulator = ""
                    current_state = "START"
                    self.analyze_line(char)  # повторный вызов для текущего символа

            # аналогично для других состояний:
            elif current_state == "NUMBER":
                if char.isdigit():
                    accumulator += char  # собираем цифры числа
                elif char == "." and '.' not in accumulator:  # Проверяем на точку
                    accumulator += char
                elif char.lower() in 'bosh':  # проверяем на возможные суффиксы для систем счисления
                    if char.lower() == 'b':  # двоичная система
                        if accumulator and all(c in '01' for c in accumulator):  # проверка на допустимые цифры
                            self.add_lexeme("NUMBER", accumulator + 'b')  # добавляем лексему
                            accumulator = ""
                            current_state = "START"
                    elif char.lower() == 'o':  # восьмеричная система
                        if accumulator and all(c in '01234567' for c in accumulator):  # проверка на допустимые цифры
                            self.add_lexeme("NUMBER", accumulator + 'o')  # добавляем лексему
                            accumulator = ""
                            current_state = "START"
                            self.add_lexeme("SEMICOLON", ";")  # добавляем точку с запятой
                        else:
                            print(f"Ошибка: некорректное восьмеричное число '{accumulator}'")
                            accumulator = ""
                            current_state = "START"
                    elif char.lower() == 'd':  # десятичная система
                        if accumulator and accumulator.isdigit():  # проверка на допустимые цифры
                            self.add_lexeme("NUMBER", accumulator + 'd')  # добавляем лексему
                            accumulator = ""
                            current_state = "START"
                            self.add_lexeme("SEMICOLON", ";")  # Добавляем точку с запятой
                        else:
                            print(f"Ошибка: некорректное десятичное число '{accumulator}'")
                            accumulator = ""
                            current_state = "START"
                    elif char.lower() == 'h':  # шестнадцатеричная система
                        if accumulator and all(c in '0123456789abcdefABCDEF' for c in accumulator):  # проверка на допустимые цифры
                            self.add_lexeme("NUMBER", accumulator + 'h')  # добавляем лексему
                            accumulator = ""
                            current_state = "START"
                else:
                    self.add_lexeme("NUMBER", accumulator)  # если это обычное число
                    accumulator = ""
                    current_state = "START"
                    self.analyze_line(char)  # повторно анализируем текущий символ

            elif current_state == "REL_OPERATOR":
                if char in "=>":
                    accumulator += char
                    if accumulator in self.OPERATORS:
                        self.add_lexeme(self.OPERATORS[accumulator], accumulator)
                        accumulator = ""
                        current_state = "START"
                else:
                    if accumulator in self.OPERATORS:
                        self.add_lexeme(self.OPERATORS[accumulator], accumulator)
                    accumulator = ""
                    current_state = "START"
                    self.analyze_line(char)

        # завершаем обработку строки, если что-то осталось еще
        if current_state == "IDENTIFIER" and accumulator:
            if accumulator in self.RESERVED_WORDS:
                self.add_lexeme(self.RESERVED_WORDS[accumulator], accumulator)
            else:
                self.add_lexeme("IDENTIFIER", accumulator)

    def add_lexeme(self, lexeme_type, lexeme_value):  # сохраняет лексемы в список
        self.lexemes.append((lexeme_type, lexeme_value))

    def display_lexemes(self):  # вывод лексем
        for lexeme in self.lexemes:
            print(lexeme)

    def execute(self):  # запуск анализа строк
        for line_idx, line in enumerate(self.program_lines, start=1):
            self.line_number = line_idx  # обновление номера строки
            self.analyze_line(line)  # анализ строки

    def retrieve_lexemes(self):
        return self.lexemes  # список лексем


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0  # текущая позиция в списке токенов
        self.declared_variables = set()

    def parse(self):
        self.program()

    def current_token(self):  # текущий токен
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def eat(self, token_type):  # соответствует ли текущий токен ожидаемому типу.
        token = self.current_token()
        if token and token[0] == token_type:
            self.position += 1
        else:
            self.raise_syntax_error(token_type)

    def raise_syntax_error(self, expected):
        token = self.current_token()
        position = self.position + 1
        if token:
            raise SyntaxError(f"Синтаксическая ошибка в позиции {position}: ожидался '{expected}', но найден '{token[0]}' ('{token[1]}').")
        else:
            raise SyntaxError(f"Синтаксическая ошибка в позиции {position}: ожидался '{expected}', но достигнут конец программы.")

    def program(self):
        self.eat('LBRACE')
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            self.declaration_or_statement()
        self.eat('RBRACE')

    def declaration_or_statement(self):  # пропуск комментариев
        while self.current_token() and self.current_token()[0] == 'COMMENT':
            self.eat('COMMENT')
        if self.current_token()[0] == 'DIM':
            self.declaration()
        else:
            self.statement()

    def declaration(self):  # объявление переменной
        self.eat('DIM')
        identifiers = self.identifier_list()  # список идентификаторов
        self.declared_variables.update(identifiers)  # добавляем их в список объявленных переменных
        self.eat('COLON')  # ожидаем ":"

        if self.current_token()[0] in ('INT', 'REAL', 'BOOL'):
            self.eat(self.current_token()[0])
        else:
            self.raise_syntax_error('тип переменной')  # Если тип не найден, вызываем ошибку

        self.optional_semicolon(mandatory=True)  # Ожидаем или не ожидаем точки с запятой

    def identifier_list(self):  # обрабатывает список идентификаторов
        identifiers = []
        identifiers.append(self.current_token()[1])  # Добавляем первый идентификатор
        self.eat('IDENTIFIER')  # Переходим к следующему токену
        while self.current_token() and self.current_token()[0] == 'COMMA':  # Если есть запятая
            self.eat('COMMA')  # Пропускаем запятую
            identifiers.append(self.current_token()[1])  # Добавляем следующий идентификатор
            self.eat('IDENTIFIER')  # Переходим к следующему токену
        return identifiers

    def statement(self):
        while self.current_token() and self.current_token()[0] == 'COMMENT':
            self.eat('COMMENT')
        token = self.current_token()
        if token[0] == 'IF':
            self.if_statement()
        elif token[0] == 'FOR':
            self.for_statement()
        elif token[0] == 'WHILE':
            self.while_statement()
        elif token[0] == 'READ':
            self.read_statement()
            self.optional_semicolon(mandatory=True)
        elif token[0] == 'WRITE':
            self.write_statement()
            self.optional_semicolon(mandatory=True)
        elif token[0] == 'LBRACKET':
            self.composite_statement()
        elif token[0] == 'IDENTIFIER':
            self.assignment_statement()
            self.optional_semicolon(mandatory=True)
        else:
            self.raise_syntax_error("оператор или ключевое слово")

    def if_statement(self):
        self.eat('IF')  # Съедаем ключевое слово 'IF'
        self.expression()  # Обрабатываем условие
        self.eat('THEN')  # Съедаем ключевое слово 'THEN'

        # Проверяем, есть ли начало блока
        if self.current_token() and self.current_token()[0] == 'LBRACE':
            self.composite_statement()  # Обрабатываем блок инструкций
        else:
            self.statement()  # Обрабатываем одиночный оператор

        # Обрабатываем конструкцию 'else'
        if self.current_token() and self.current_token()[0] == 'ELSE':
            self.eat('ELSE')  # Съедаем ключевое слово 'ELSE'
            if self.current_token() and self.current_token()[0] == 'LBRACE':
                self.composite_statement()  # Обрабатываем блок инструкций в else
            else:
                self.statement()  # Обрабатываем одиночный оператор в else

    def for_statement(self):
        self.eat('FOR')  # Съедаем ключевое слово 'FOR'

        identifier = self.current_token()[1]
        if identifier not in self.declared_variables:
            self.raise_syntax_error(f"Переменная '{identifier}' не была объявлена.")
        self.eat('IDENTIFIER')  # Съедаем идентификатор переменной цикла

        self.eat('ASSIGN')  # Ожидаем оператора присваивания 'as'

        # Обрабатываем начальное значение
        self.expression()  # Ожидаем выражение, например, 0

        # Ожидаем 'TO' после выражения
        if self.current_token()[0] != 'TO':
            self.raise_syntax_error(
                f"Ожидается 'TO' после присваивания переменной '{identifier}', найдено {self.current_token()[0]}.")

        self.eat('TO')  # Съедаем 'TO'

        # Ожидаем выражение для конца диапазона (например, 10)
        self.expression()  # Обрабатываем число или выражение

        self.eat('DO')  # Съедаем ключевое слово 'DO'

        if self.current_token() and self.current_token()[0] == 'LBRACE':
            self.composite_statement()  # Обрабатываем блок инструкций
        else:
            self.statement()  # Если нет блока, обрабатываем один оператор

    def while_statement(self):
        self.eat('WHILE')
        self.expression()  # обрабатываем условие цикла
        self.eat('DO')

        # есть ли начало блока
        if self.current_token() and self.current_token()[0] == 'LBRACE':
            self.composite_statement()  # блок инструкций
        else:
            # если нет блока, то обрабатываем одиночный оператор
            self.statement()

    def read_statement(self):
        self.eat('READ')
        self.eat('LPAREN')
        identifiers = self.identifier_list()
        self.check_identifiers_declared(identifiers)
        self.eat('RPAREN')

    def write_statement(self):
        self.eat('WRITE')
        self.eat('LPAREN')
        self.expression_list()
        self.eat('RPAREN')

    def composite_statement(self):
        self.eat('LBRACE')
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            self.statement()
        self.eat('RBRACE')

    def assignment_statement(self):
        identifier = self.current_token()[1]
        if identifier not in self.declared_variables:
            self.raise_syntax_error(f"Переменная '{identifier}' не была объявлена.")
        self.eat('IDENTIFIER')  # Съедаем идентификатор
        self.eat('ASSIGN')  # Ожидаем 'as'
        self.expression()  # Присваиваем значение

    def expression_list(self):
        self.expression()
        while self.current_token() and self.current_token()[0] == 'COMMA':
            self.eat('COMMA')
            self.expression()

    def expression(self):
        self.logical_expression()

    def logical_expression(self):
        self.relational_expression()
        while self.current_token() and self.current_token()[0] in ('AND', 'OR'):
            self.eat(self.current_token()[0])
            self.relational_expression()

    def relational_expression(self):
        self.additive_expression()
        while self.current_token() and self.current_token()[0] == 'REL_OP':
            self.eat('REL_OP')
            self.additive_expression()

    def additive_expression(self):
        self.multiplicative_expression()
        while self.current_token() and self.current_token()[0] == 'ADD_OP':
            self.eat('ADD_OP')
            self.multiplicative_expression()

    def multiplicative_expression(self):
        self.operand()
        while self.current_token() and self.current_token()[0] == 'MUL_OP':
            self.eat('MUL_OP')
            self.operand()

    def operand(self):
        token = self.current_token()
        if token[0] == 'IDENTIFIER':  # Это идентификатор
            self.check_identifiers_declared([token[1]])
            self.eat('IDENTIFIER')
        elif token[0] == 'NUMBER':  # если число, то обрабатываем как число
            # Здесь проверяем, является ли число целым или с плавающей точкой
            number_value = token[1]
            if '.' in number_value or 'e' in number_value or 'E' in number_value:
                # Это вещественное число (FLOAT)
                self.eat('NUMBER')
            else:
                # Целое число
                self.eat('NUMBER')
        elif token[0] in ('TRUE', 'FALSE'):
            self.eat(token[0])
        elif token[0] == 'NOT':  # лог отрицание
            self.eat('NOT')
            self.operand()
        elif token[0] == 'LPAREN':  # если скобки, то рекурсивно обрабатываем выражение
            self.eat('LPAREN')
            self.expression()
            self.eat('RPAREN')
        else:
            self.raise_syntax_error("идентификатор, число или выражение")

    def optional_semicolon(self, mandatory=False):
        if self.current_token() and self.current_token()[0] == 'SEMICOLON':
            self.eat('SEMICOLON')
        elif mandatory:
            self.raise_syntax_error("';'")

    def check_identifiers_declared(self, identifiers):
        for identifier in identifiers:
            if identifier not in self.declared_variables:
                raise SyntaxError(f"Семантическая ошибка: переменная '{identifier}' не объявлена.")


if __name__ == '__main__':
    try:
        with open('test.txt', 'r') as file:
            code = file.read()

        lexer = Lexer(code)
        lexer.execute()

        print("Токены:")
        lexer.display_lexemes()

        tokens = lexer.retrieve_lexemes()

        parser = Parser(tokens)
        try:
            parser.parse()
        except SyntaxError as e:
            print(f"Ошибка синтаксического анализа: {e}")
        else:
            print("\nСинтаксический и семантический анализы успешны")

    except FileNotFoundError:
        print("Ошибка: файл 'test.txt' не найден.")
    except Exception as e:
        print(f'Непредвиденная ошибка: {e}')

