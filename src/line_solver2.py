# Complete line solver using stars and bars

import numpy as np 
from itertools import combinations
from pprint import pprint

'''
Broken:   >---#--         - #    # <
      
A B C D


A: 0 to a
B: a + len(block0) to b
C: b + len(block1) to c
D: c + len(block2) to d

ALL INTERVALS CANNOT CONTAIN SPACES
'''

def partitions(n, k, r = None):
    '''
    https://stackoverflow.com/questions/28965734/general-bars-and-stars
    '''
    r = r or [0 for _ in range(k)]
    for c in combinations(range(n+k-1), k-1):
        yield [b-a-1+d for a,b,d in zip((-1,)+c, c+(n+k-1,), r)]

def is_valid_combo(line, rule, combo):
    j = combo[0]
    k = 0
    for i in range(len(rule)):
        if 0 in line[j:j+rule[i]] or 1 in line[k:k+combo[i]]:
            return False
        j += (combo[i+1] + rule[i])
        k += (combo[i] + rule[i])
    if 1 in line[k:k+combo[-1]]: return False
    return True

def generate_line_from_combo(line, rule, combo):
    res = []
    num_blocks = len(rule)
    for i in range(num_blocks):
        res += [0 for _ in range(combo[i])]
        res += [1 for _ in range(rule[i])]
    res += [0 for _ in range(combo[-1])]
    return res

def solve_line(line, rule):
    k = len(rule) + 1
    n = len(line) - sum(rule) - (k - 2)
    base = [1 if 0 < i < k-1 else 0 for i in range(k)]
    combos = list(filter(
        lambda c: is_valid_combo(line, rule, c),
        partitions(n, k, base)
    ))
    if len(combos) > 0:
        res = generate_line_from_combo(line, rule, combos[0])
        for combo in combos:
            # Use value it is equal across all combos, otherwise set as unknown
            cline = generate_line_from_combo(line, rule, combo)
            res = [x if not(res[i] ^ cline[i]) else -1 for i, x in enumerate(cline)]
        return res
    return line

def print_lines(lines):
    m = len(lines)
    n = len(lines[0])
    string = ""
    for j in range(m):
        string += "\n"
        for i in range(n):
            cell = lines[j][i]
            if cell == -1:
                string += '. '
            elif cell == 0:
                string += '  '
            elif cell == 1:
                string += '# '
            else:
                raise ValueError(
                    "Unrecognised value at cell ({}, {}): {}".format(i, j, cell)
                )
    print(string)

def main():
    # col_rules = [[1, 2], [2], [3], [2], [3]]
    # row_rules = [[3], [1, 3], [1, 1], [2], [2]]
    # # Seahorse
    # col_rules = [[1], [2, 2], [1, 4, 4], [2, 6, 1], [1, 4, 1, 1], [1, 1]]
    # row_rules = [[1], [1, 1], [5], [1], [2], [3], [2, 2], [1, 2], [2], [2], [1], [1, 1], [1, 1], [2]]
    col_rules = [[3], [3,1], [1,1,2], [1,4,2], [4,2,3], [1,1,4,3], [2,6,2], [2,1,9], [1,1,7], [2,5]]
    row_rules = [[3], [3,3], [1,1,1,1], [1,4,1], [4,3], [1,1,2], [1,6,1], [2,4,1], [5], [3], [3,3], [6], [5], [2], [2]]

    m = len(row_rules)
    n = len(col_rules)
    lines = np.array(
        [[-1 for _ in range(n)] 
             for _ in range(m)]
    )

    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()

    for _ in range(5):
        for i in range(m):
            line = lines[i]
            rule = row_rules[i]
            lines[i] = solve_line(line, rule)
        for j in range(n):
            line = lines[:,j]
            rule = col_rules[j]
            lines[:,j] = solve_line(line, rule)
    print_lines(lines)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()

main()
