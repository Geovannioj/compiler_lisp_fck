import ox
import click
import pprint

lexer = ox.make_lexer([
    ('LOOP', r'loop'),
    ('DEC', r'dec'),
    ('INC', r'inc'),
    ('OPEN_PARENTHESIS', r'\('),
    ('CLOSE_PARENTHESIS', r'\)'),
    ('RIGHT', r'right'),
    ('LEFT', r'left'),
    ('PRINT', r'print'),
    ('READ', r'read'),
    ('DO', r'do'),
    ('DO_AFTER', r'do-after'),
    ('DO_BEFORE', r'do-before'),
    ('ADD', r'add'),
    ('SUB', r'sub'),
    ('NUMBER', r'[0-9]+'),
    ('DEF', r'def'),
    ('FUCTION', r'(?!loop)(?!dec)(?!inc)(?!right)(?!left)(?!print)(?!read)(?!do)(?!do)(?!do)(?!add)(?!sub)(?!def)(?!\d)[a-zA-Z0-9-\+_]+'),
    ('ignore_COMMENT', r';[ \S]*'),
    ('ignore_SPACE', r'\s+')
])

tokens_list = ['LOOP',
          'DEC',
          'INC',
          'OPEN_PARENTHESIS',
          'CLOSE_PARENTHESIS',
          'RIGHT',
          'LEFT',
          'PRINT',
          'READ',
          'DO',
          'DO_AFTER',
          'DO_BEFORE',
          'ADD',
          'SUB',
          'NUMBER',
          'DEF',
          'FUCTION']

parser = ox.make_parser([
    ('expr : OPEN_PARENTHESIS CLOSE_PARENTHESIS', lambda x,y: '()'),
    ('expr : OPEN_PARENTHESIS term CLOSE_PARENTHESIS', lambda x,y,z: y),
    ('term : atom term', lambda x,y: (x,) + y),
    ('term : atom', lambda x: (x,)),
    ('atom : expr', lambda x: x),
    ('atom : DEC', lambda x: x),
    ('atom : INC', lambda x: x),
    ('atom : LOOP', lambda x: x),
    ('atom : RIGHT', lambda x: x),
    ('atom : LEFT', lambda x: x),
    ('atom : PRINT', lambda x: x),
    ('atom : READ', lambda x: x),
    ('atom : DO', lambda x: x),
    ('atom : DO_AFTER', lambda x: x),
    ('atom : DO_BEFORE', lambda x: x),
    ('atom : ADD', lambda x: x),
    ('atom : SUB', lambda x: x),
    ('atom : NUMBER', int),
    ('atom : DEF', lambda x: x),
     ('atom : FUCTION', lambda x: x)
], tokens_list)

# definition of functions

def do_before(command, array):
    new_array = []
    iterator = 0
    while iterator < len(array):
        new_array.append(array[iterator])
        new_array.append(command)
        if array[iterator] == 'add' or array[iterator] == 'sub':
            iterator += 1
            new_array.append(array[iterator])
        iterator += 1

    return new_array

def do_after(command, array):
    new_array = []
    iterator = 0
    while iterator < len(array):
        if array[iterator] == 'add' or array[iterator] == 'sub':
            new_array.append(array[iterator])
            iterator += 1
        new_array.append(array[iterator])
        new_array.append(command)
        iterator += 1

    return new_array


def add_sub(char, number, list_out):
    iterator = 0
    while iterator < number:
        list_out.append(char)
        iterator += 1

    return list_out

def compiler(tree, output_list):

    interactor = 0
    while interactor < len(tree):
        if isinstance(tree[interactor], tuple):
            output_list = compiler(tree[interactor], output_list)
        elif tree[interactor] == 'inc':
            output_list.append('+')
        elif tree[interactor] == 'dec':
            output_list.append('-')
        elif tree[interactor] == 'right':
            output_list.append('>')
        elif tree[interactor] == 'left':
            output_list.append('<')
        elif tree[interactor] == 'add':
            interactor += 1
            output_list = add_sub('+', tree[interactor], output_list)
        elif tree[interactor] == 'sub':
            interactor += 1
            output_list = add_sub('-', tree[interactor], output_list)
        elif tree[interactor] == 'print':
            output_list.append('.')
        elif tree[interactor] == 'read':
            output_list.append(',')
        elif tree[interactor] == 'do-after':
            interactor += 1 
            command = tree[interactor]
            interactor += 1 
            array = do_after(command, list(tree[interactor]))
            output_list = compiler(array, output_list)
        elif tree[interactor] == 'do-before':
            interactor += 1 
            command = tree[interactor]
            interactor += 1 
            array = do_before(command, list(tree[interactor]))
            output_list = compiler(array, output_list)
        elif tree[interactor] == 'loop':
            output_list.append('[')
            output_list = compiler(tree[interactor], output_list)
            output_list.append(']')
        elif tree[interactor] == 'def':
            pass
        interactor += 1

    return output_list

def treatOutputFile(tree):
    file_output = open('outputFile.bf', 'w')
    output = []
    output = compiler(tree, output)
    file_output.write(''.join(output))
    file_output.close()
    print('\nOutput file saved sucessfully!')

@click.command()
@click.argument('input_file', type=click.File('r'))

def print_tree(input_file):
    input_code = input_file.read()
    tokens = lexer(input_code)
    print('Tokens:\n', tokens)
    syntatic_tree = parser(tokens)
    print("\nTree:")
    pprint.pprint(syntatic_tree)
    treatOutputFile(syntatic_tree)

if __name__ == '__main__':
    print_tree()