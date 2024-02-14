from typing import Callable
import math


class Expression:
    priority = -1
    variables = {'x': None, 'y': None, 'z': None}
    consts = {'pi': math.pi, 'e': math.e}

    def calculate(self):
        raise NotImplementedError()

    def __eq__(self, other):
        return id(self) == id(other)


class Number(Expression):
    def __init__(self, value):
        self.value = value

    def calculate(self):
        return self.value


class Const(Expression):
    def __init__(self, name):
        try:
            self.value = Expression.consts[name]
        except KeyError:
            raise Exception(f'constant {self.value} is not defined')

    def calculate(self):
        return self.value


class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def calculate(self):
        try:
            return Expression.variables[self.name].calculate()
        except KeyError:
            raise Exception(f'variable {self.name} is not defined')


class Assign(Expression):
    variable: Variable = None
    value: Expression = None
    priority = 0

    def __init__(self):
        pass

    def calculate(self):
        Expression.variables[self.variable.name] = self.value


class OpenBrackets(Expression):
    def __init__(self, bracket_type, added_priority=0):
        self.bracket_type = bracket_type
        self.priority = 1000 + added_priority

    def calculate(self):
        raise NotImplementedError()

    def __eq__(self, other):
        return isinstance(other, CloseBrackets) and self.bracket_type == other.bracket_type


class CloseBrackets(Expression):
    def __init__(self, bracket_type):
        self.bracket_type = bracket_type
        self.priority = 1000

    def calculate(self):
        raise NotImplementedError()


class Brackets(Expression):
    def __init__(self, next_exp: Expression = None):
        self.next = next_exp

    def calculate(self):
        return self.next.calculate()


class Operator(Expression):
    def __init__(self, operator: Callable, priority: int):
        self.operator = operator
        self.priority = priority

    def calculate(self):
        pass


class UnaryOperator(Operator):
    def __init__(self, operator, priority: int = 0, next_exp: Expression = None):
        operator = operator
        priority = priority
        super().__init__(operator, priority)
        self.next = next_exp

    def calculate(self):
        return self.operator(self.next.calculate())


class BinaryOperator(Operator):
    def __init__(self, operator, priority: int = 0, left: Expression = None, right: Expression = None):
        operator = operator
        priority = priority
        super().__init__(operator, priority)
        self.left = left
        self.right = right

    def calculate(self):
        if self.left and self.right:
            return self.operator(self.left.calculate(), self.right.calculate())



