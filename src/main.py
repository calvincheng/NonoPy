import numpy as np
from itertools import combinations

def partitions(n, k, r = None):
    '''
    https://stackoverflow.com/questions/28965734/general-bars-and-stars
    '''
    r = r or [0 for _ in range(k)]
    for c in combinations(range(n+k-1), k-1):
        yield [b-a-1+d for a,b,d in zip((-1,)+c, c+(n+k-1,), r)]

class Nonogram:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        
        self.m = len(rows)
        self.n = len(cols)

        self.grid = np.array(
            [[-1 for _ in range(self.n)] 
                 for _ in range(self.m)]
        )

        self.hash = {}
        self.hits = 0
        self.nohits = 0

    def __str__(self):
        string = ""
        for j in range(self.m):
            for i in range(self.n):
                cell = self.grid[j][i]
                if cell == -1:
                    string += '\u2895\u2895'
                elif cell == 0:
                    string += '  '
                elif cell == 1:
                    string += '\u2588\u2588'
                else:
                    raise ValueError(
                        "Unrecognised value at cell ({}, {}): {}".format(i, j, cell)
                    )
            string += "\n"
        return string

    def solve_line(self, line, rule):
        hashstring = (str(rule), str(line))
        if hashstring in self.hash:
            self.hits += 1
            return self.hash[hashstring]

        def is_valid_combo(combo):
            j = combo[0]    # solids
            k = 0           # spaces
            for i in range(len(rule)):
                if 0 in line[j:j+rule[i]] or 1 in line[k:k+combo[i]]:
                    return False
                j += (combo[i+1] + rule[i])
                k += (combo[i] + rule[i])
            if 1 in line[k:k+combo[-1]]: return False
            return True

        def generate_line_from_combo(combo):
            res = []
            num_blocks = len(rule)
            for i in range(num_blocks):
                res += [0 for _ in range(combo[i])]
                res += [1 for _ in range(rule[i])]
            res += [0 for _ in range(combo[-1])]
            return res

        k = len(rule) + 1
        n = len(line) - sum(rule) - (k - 2)
        # print("n: {} | k: {}".format(n, k))
        base = [1 if 0 < i < k-1 else 0 for i in range(k)]
        combos = list(filter(
            is_valid_combo,
            partitions(n, k, base)
        ))
        if len(combos) > 0:
            res = generate_line_from_combo(combos[0])
            for combo in combos:
                # Use value it is equal across all combos, otherwise set as unknown
                cline = generate_line_from_combo(combo)
                res = [x if not(res[i] ^ cline[i]) else -1 for i, x in enumerate(cline)]
            self.nohits += 1
            self.hash[hashstring] = res
            return res
        self.nohits += 1
        self.hash[hashstring] = line
        return line

    def solve(self):
        import cProfile, pstats
        profiler = cProfile.Profile()
        profiler.enable()

        for _ in range(5):
            for i in range(self.m):
                line = self.grid[i]
                rule = self.rows[i]
                self.grid[i] = self.solve_line(line, rule)
            for j in range(self.n):
                line = self.grid[:,j]
                rule = self.cols[j]
                self.grid[:,j] = self.solve_line(line, rule)
            # print(self)

        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('tottime')
        stats.print_stats()




col_rules = [
    [3, 3],
    [3, 5],
    [1, 5, 1],
    [1, 3],
    [4],
    [2],
    [1, 1],
    [3],
    [5],
    [1, 4, 4, 4, 4, 3],
    [3, 4, 4, 4, 4, 1],
    [3, 4, 4, 4, 4]
]
row_rules = [
    [1],
    [3],
    [2],
    [1, 1],
    [2],
    [3],
    [3],
    [2],
    [1, 1],
    [2],
    [3],
    [3],
    [2],
    [1, 1],
    [2],
    [3],
    [1, 3],
    [3, 2],
    [2, 1, 1],
    [1, 1, 2],
    [2, 3],
    [3, 3],
    [4, 1, 2],
    [3, 1, 3, 1],
    [1, 2, 5],
    [4, 3],
    [4, 1],
]

N = Nonogram(row_rules, col_rules)
N.solve()
print(N.hits, N.nohits)
print(N)


