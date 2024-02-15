## Description
This project is based on [**AST**](https://en.wikipedia.org/wiki/Abstract_syntax_tree)(Abstract Syntax Tree) which is mainly used for compilers.
The main idea is taking a string representing a function, tokenizing it, using the tokens to create an operator tree that makes up the function.
Then, using said tree we can compute
values for the function and graph it.

## WIP:
- Adding my own graphing tool (right now the example uses [**matplotlib**](https://github.com/matplotlib/matplotlib)).
- Simplifing adding custom functions.

## Example

to graph a simple function use:
```python
from expression_compiler.compiler import Equation
from matplotlib import pyplot as plt

upper = 100
lower = -100


y = Equation(input('Enter the equation: '))
plt.plot([i for i in range(lower, upper)],
         [y.calculate({'x': i}) for i in range(lower, upper)])
plt.show()
```
To create an Equation-tree simply use `e = Equation(string)` and to compute a speciefic value use `e.calculate()`.

for an easier time when graphing equations, it's also possible to pass a variable dictionary to `Equation.calculate()` as seen in the code above.


*You can map variables into an operator-tree and use it to create another variable as the variable does not compute the value of the tree.
```python
Equation('y=x^3+5x+sin(x)')
Equation('z=5y')
```
right now only supports function following the pattern of `y=f(x)`, to create more variables you'll need to add to the variable dictionary in the `operator.variables`.

you can easily add unary, binary operators like this:

```python
compiler.binary_operators['operator_name'=callable]
```
for a unary operator
```python
compiler.unary_operators['operator_name'=callable]
```
afterwards the tokenize function will be able to tokenize the functions correctly.
