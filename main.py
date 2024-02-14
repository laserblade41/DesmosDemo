from expression_compiler.compiler import *
from matplotlib import pyplot as plt

upper = 100
lower = -100


y = Equation(input('Enter the equation: '))
plt.plot([i for i in range(lower, upper)],
         [y.calculate({'x': i}) for i in range(lower, upper)])
plt.show()
