from typing import Tuple, Any, Dict, List

from expression_compiler.operators import *
import math


class Equation:
    binary_operators = {'+': (lambda x, y: x + y, 1), '*': (lambda x, y: x * y, 2),
                        '/': (lambda x, y: x / y if y != 0 else 0, 2), '^': (lambda x, y: x ** y, 3),
                        '%': (lambda x, y: x % y, 2)}
    unary_operators = {'sqrt': (lambda x: math.sqrt(x), 4), 'sin': (lambda x: math.sin(x), 4),
                       'cos': (lambda x: math.cos(x), 4), 'tan': (lambda x: math.tan(x), 4),
                       'ln': (lambda x: math.log(x, math.e), 4), 'log': (lambda x: math.log(x, 10), 4)}
    brackets = {'(': ')', '[': ']', '{': '}'}

    def __init__(self, equation: str | Expression):
        if isinstance(equation, str):
            self.tree = self.parse_rec(self.tokenize(equation))
        elif isinstance(equation, Expression):
            self.tree = equation
        else:
            raise Exception('invalid equation')

    def calculate(self, variables: Dict[str, int] = {}) -> int:
        for key, value in variables.items():
            Expression.variables[key] = Number(value)
        return self.tree.calculate()

    # There are two ways to compile the equation, this recursive one was my first attempt
    @staticmethod
    def parse_rec(tokens: List[Expression]) -> Expression:
        if len(tokens) == 1:
            return tokens[0]
        if tokens[0] == tokens[-1]:
            return Brackets(Equation.parse_rec(tokens[1:-1]))
        min_index = find_min_priority(tokens)
        min_token = tokens[min_index]
        match type(min_token).__name__:
            case 'BinaryOperator':
                min_token.left = Equation.parse_rec(tokens[:min_index])
                min_token.right = Equation.parse_rec(tokens[min_index+1:])

            case 'UnaryOperator':
                min_token.next = Equation.parse_rec(tokens[min_index+1:])

            case 'Assign':
                variable = tokens[min_index - 1]
                value = Equation.parse_rec(tokens[min_index + 1:])
                Expression.variables[variable.name] = value
                return value

            case _:
                raise Exception('invalid token')
        return min_token

    @staticmethod
    def shunting_yard_tree(equation: str) -> Expression:
        return Equation.parse_shunting_yard(Equation.shunting_yard(Equation.tokenize(equation)))

    # we can also use the shunting yard algorithm to compile the equation
    @staticmethod
    def shunting_yard(tokens: List[Expression]) -> List[Expression]:
        output = []
        operators = []
        assignQueue = []
        for token in tokens:
            if isinstance(token, Number) or isinstance(token, Variable):
                output.append(token)
            elif isinstance(token, UnaryOperator):
                if operators and token.priority == operators[-1].priority:
                    output.append(operators.pop())
                operators.append(token)
            elif isinstance(token, BinaryOperator):
                while operators and operators[-1].priority < token.priority:
                    operators.append(operators.pop())
                operators.append(token)
            elif isinstance(token, OpenBrackets):
                operators.append(token)
            elif isinstance(token, CloseBrackets):
                while not isinstance(operators[0], OpenBrackets):
                    operators.append(operators.pop(0))
                operators.pop(0)
            elif isinstance(token, Assign):
                assignQueue.append(output.pop())
                assignQueue.append(token)
            # we can have either open brackets or assign operator
            else:
                operators.append(token)
        while operators:
            output.append(operators.pop(0))
        while assignQueue:
            output.append(assignQueue.pop(0))
        return output

    @staticmethod
    def parse_shunting_yard(tokens: List[Expression]) -> Expression:
        parse_queue = []
        while tokens:
            token = tokens.pop(0)
            if isinstance(token, Number) or isinstance(token, Variable):
                parse_queue.append(token)
            elif isinstance(token, UnaryOperator):
                token.next = parse_queue.pop(0)
                parse_queue.append(token)
            elif isinstance(token, BinaryOperator):
                token.left = parse_queue.pop(0)
                token.right = parse_queue.pop(0)
                parse_queue.append(token)
            elif isinstance(token, Assign):
                value = parse_queue.pop(0)
                variable = parse_queue.pop(0)
                Expression.variables[variable.name] = value
                return value
            else:
                raise Exception('invalid token')
        return parse_queue.pop()


    @staticmethod
    def check_balance(equation: str) -> bool:
        """
        This function is used to check if the brackets in the equation are balanced
        :param equation: equation to check
        :return: if the brackets are balanced
        """
        bracks = []
        for ch in equation:
            if ch in '([{':
                bracks.append(ch)
            if ch in ')]}':
                if not bracks or not Equation.brackets[bracks.pop()] == ch:
                    return False
        return not bracks

    @staticmethod
    def tokenize(equation: str) -> list[Expression]:
        """
        This function is used to tokenize the equation
        :param equation: string of the equation to tokenize
        :return: list of tokens
        """
        if not Equation.check_balance(equation):
            raise Exception('the equation is not balanced')
        operator_list = []
        idx = 0
        while idx < len(equation):
            ch = equation[idx]
            match ch:
                case _ if ch == '-':
                    if idx == 0 or equation[idx-1] == '=' or equation[idx-1] in "([{":
                        operator_list.append(UnaryOperator(lambda x: -x, 3))
                    else:
                        operator_list.append(BinaryOperator(lambda x, y: x - y, 1))

                case _ if ch in Equation.binary_operators:
                    operator, priority = Equation.binary_operators[ch]
                    operator_list.append(BinaryOperator(operator, priority))

                case _ if ch.isnumeric():
                    idx += 1
                    while idx < len(equation) and equation[idx].isnumeric():
                        ch += equation[idx]
                        idx += 1
                    operator_list.append(Number(int(ch)))
                    idx -= 1

                case _ if ch == "=":
                    operator_list.append(Assign())

                case _ if ch in "([{":
                    operator_list.append(OpenBrackets(Equation.brackets[ch], idx))

                case _ if ch in ")]}":
                    operator_list.append(CloseBrackets(ch))

                case _ if ch.isalpha():
                    if 0 < idx - 1 and equation[idx-1] in '0123456789':
                        op = Equation.binary_operators['*']
                        operator_list.append(BinaryOperator(op[0], op[1]))
                    idx += 1
                    while idx < len(equation) and equation[idx].isalpha():
                        ch += equation[idx]
                        idx += 1
                    operator_list.append(Equation.tokenize_word(ch))
                    idx -= 1

                case _:
                    raise Exception('invalid character')

            idx += 1
        return operator_list

    @staticmethod
    def tokenize_word(word: str) -> Expression:
        """
        Tokenizes the str
        :param word: word to tokenize
        :return: the token
        """
        match word:
            case _ if word in Expression.consts:
                return Const(word)
            case _ if word in Expression.variables:
                return Variable(word)
            case _ if word in Equation.unary_operators:
                operator, priority = Equation.unary_operators[word]
                return UnaryOperator(operator, priority)
            case _:
                raise Exception('invalid word')


def find_min_priority(lst: list[Any]) -> int:
    min_priority = 1000
    min_index = -1
    brackets = 0
    for index, token in enumerate(lst):
        if isinstance(token, OpenBrackets):
            brackets += 1
        elif isinstance(token, CloseBrackets):
            brackets -= 1
        elif brackets == 0 and min_priority > token.priority > -1:
            min_priority = token.priority
            min_index = index
    return min_index
