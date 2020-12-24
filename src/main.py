import numpy as np
from itertools import combinations

def partitions(n, k, r = None):
    '''
    https://stackoverflow.com/questions/28965734/general-bars-and-stars
    '''
    r = r or [0 for _ in range(k)]
    for c in combinations(range(n+k-1), k-1):
        yield [b-a-1+d for a,b,d in zip((-1,)+c, c+(n+k-1,), r)]

def partitions2(n, k, r, line, rule):
    for c in combinations(range(n+k-1), k-1):
        # if any([ line[x+i] == 0 for i,x in enumerate(c) ]): continue
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

    def solve_line(self, idx, axis=0):
        line = self.grid[idx] if axis == 0 else self.grid[:,idx]
        rule = self.rows[idx] if axis == 0 else self.cols[idx]

        # Return cached solutions
        hashstring = (str(rule), str(line))
        if hashstring in self.hash:
            self.hits += 1
            return self.hash[hashstring]

        self.nohits += 1
        has_changed = False

        # Return if line already solved
        if -1 not in line:
            self.hash[hashstring] = (line, has_changed)
            return line, has_changed

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
            # partitions2(n, k, base, line, rule)
            partitions(n, k, base)
        ))

        if len(combos) > 0:
            res = generate_line_from_combo(combos[0])
            for combo in combos:
                # Use value it is equal across all combos, otherwise set as unknown
                cline = generate_line_from_combo(combo)
                res = [x if not(res[i] ^ cline[i]) else -1 for i, x in enumerate(cline)]
            has_changed = True
            self.hash[hashstring] = (res, has_changed)
            return res, has_changed

        self.hash[hashstring] = (line, has_changed)
        return line, has_changed

    def solve(self):
        import cProfile, pstats
        profiler = cProfile.Profile()
        profiler.enable()

        solved = False
        iters = 0
        while not solved:
            iters += 1
            print("Iteration: {}".format(iters))
            solved = True
            for i in range(self.m):
                solution, has_changed = self.solve_line(i, axis=0)
                if has_changed:
                    solved = False
                    self.grid[i] = solution
            for j in range(self.n):
                solution, has_changed = self.solve_line(j, axis=1)
                if has_changed:
                    solved = False
                    self.grid[:,j] = solution

        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('tottime')
        stats.print_stats()

col_rules = [
    [1],
    [1],
    [2],
    [4],
    [7],
    [9],
    [2,8],
    [1,8],
    [8],
    [1,9],
    [2,7],
    [3,4],
    [6,4],
    [8,5],
    [1,11],
    [1,7],
    [8],
    [1,4,8],
    [6,8],
    [4,7],
    [2,4],
    [1,4],
    [5],
    [1,4],
    [1,5],
    [7],
    [5],
    [3],
    [1],
    [1]
]

row_rules = [
    [8,7,5,7],
    [5,4,3,3],
    [3,3,2,3],
    [4,3,2,2],
    [3,3,2,2],
    [3,4,2,2],
    [4,5,2],
    [3,5,1],
    [4,3,2],
    [3,4,2],
    [4,4,2],
    [3,6,2],
    [3,2,3,1],
    [4,3,4,2],
    [3,2,3,2],
    [6,5],
    [4,5],
    [3,3],
    [3,3],
    [1,1] 
]

N = Nonogram(row_rules, col_rules)
N.solve()
print(N)
