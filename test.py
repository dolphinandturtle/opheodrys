from walks.simple import reduce

PIPICODE = """
a -> intero(10)
b -> intero(3)
somma -> a + b
stampa(somma)
"""


def parse(code, stack):
    for line in code.split('\n'):
        args = line.split(' ')
        if args[1] == '->':
            variable, value = args[0], args[2:]
            stack[variable]

def compiler(expr):
    for key, value in expr.copy().items():
        if key == "int":
            expr[key] = int(value)
        elif key == "add":
            expr['int'] = value[0]['int'] + value[1]['int']
            del expr[key]
        elif key == "print":
            print(value)


