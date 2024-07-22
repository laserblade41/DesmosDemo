from expression_compiler.compiler import Equation
from matplotlib import pyplot as plt

upper = 30
lower = -30

if __name__ == '__main__':
    y = Equation(input('Enter the equation: '))
    plt.plot([i for i in range(lower, upper)],
             [y.calculate({'x': i}) for i in range(lower, upper)])
    plt.show()
