# Complete line solver using stars and bars

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
    if r is None: r = [0] * k
    for c in combinations(range(n+k-1), k-1):
        yield [b-a-1+c for a,b,c in zip((-1,)+c, c+(n+k-1,), r)]

def is_valid_combo(line, rule, combo):
    # [0, 1, 3, 13]
    # block_boundaries = [
    #     [0, 1] + 1
    #     [2, 3] + 3
    #     [6, 11] + 13
    #     [24, 24]
    # ]
    # space_boundaries = [
    #     [0, 0] + 1
    #     [1, 2] + 1
    #     [3, 6] + 5
    #     [11, 24]
    # ]
    #
    # block_boundaries = [
    #     [combo[0], combo[0]+rule[0]] + combo[1]
    #     [2, 2 + rule[1]] + combo[2]
    #     [6, 6 + rule[2]] + combo[3]
    # ]
    # space_boundaries = [
    #     [0, 0 + combo[0]] + rule[0]
    #     [1, 1 + combo[1]] + rule[1]
    #     [3, 3 + combo[2]] + rule[2]
    #     [11, 11+combo[3]]
    # ]
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
    base = [1 if i != 0 and i != k-1 else 0 for i in range(k)]
    combos = list(filter(
        lambda c: is_valid_combo(line, rule, c),
        partitions(n, k, base)
    ))
    res = generate_line_from_combo(line, rule, combos[0])
    for combo in combos:
        # Use value it is equal across all combos, otherwise set as unknown
        cline = generate_line_from_combo(line, rule, combo)
        res = [x if not(res[i] ^ cline[i]) else -1 for i, x in enumerate(cline)]
    return res

def print_lines(lines):
    m = len(lines)
    n = len(lines[0])
    string = ""
    for j in range(m):
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
        string += "\n"
    print(string)

def main():
    row_rules = [[2, 1], [1, 3], [1, 2], [3], [4], [1]]
    col_rules = [[1], [5], [2], [5], [2, 1], [2]]
    m = len(row_rules)
    n = len(col_rules)
    lines = [[-1 for _ in range(m)] 
                for _ in range(n)]

    print_lines(lines)

    # string = "---#--         -      # "
    # line = [-1] * len(string)
    # for i, c in enumerate(string):
    #     if c == '-': line[i] = 0
    #     elif c == '#': line[i] = 1
    # rule = [1, 1, 5]
    # solve_line(line, rule)

main()
