import ox

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
    ('ignore_COMMENT', r';[ \S]*'),
    ('ignore_SPACE', r'\s+')
])