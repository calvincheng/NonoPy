import numpy as np
import itertools
from obj.PriorityQueue import PriorityQueue

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
        # 0 - column, 1 - row
        line = self.grid[:,idx] if axis == 0 else self.grid[idx]
        rule = self.cols[idx] if axis == 0 else self.rows[idx]

        # Return cached solutions
        hashstring = (str(rule), str(line))
        if hashstring in self.hash:
            self.hits += 1
            return self.hash[hashstring]

        self.nohits += 1
        changed_idxs = []

        # Return if line already solved
        if -1 not in line:
            self.hash[hashstring] = (line, changed_idxs)
            return line, changed_idxs

        def partitions(n, k, r = None):
            '''
            https://stackoverflow.com/questions/28965734/general-bars-and-stars
            '''
            r = r or [0 for _ in range(k)]
            for c in itertools.combinations(range(n+k-1), k-1):
                if line[c[0]] == 0: continue
                yield [b-a-1+d for a,b,d in zip((-1,)+c, c+(n+k-1,), r)]


        def is_valid_combo(combo):
            j = combo[0]    # solids
            k = 0           # spaces
            for i in range(len(rule)):
                if (
                    not all(line[j:j+rule[i]])      # Space covered by solid
                    or any(line[k:k+combo[i]] == 1)  # Solid covered by space
                ):
                    return False
                j += (combo[i+1] + rule[i])
                k += (combo[i] + rule[i])
            if any(line[k:k+combo[-1]] == 1): return False
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

            changed_idxs = [i for i,x in enumerate(res) if x != line[i]]
            self.hash[hashstring] = (res, changed_idxs)
            return res, changed_idxs

        self.hash[hashstring] = (line, changed_idxs)
        return line, changed_idxs

    def solve(self):
        import cProfile, pstats
        profiler = cProfile.Profile()
        profiler.enable()

        # Populate priority queue
        priority_queue = PriorityQueue()
        for i in range(self.m):
            priority = -sum(self.rows[i])
            priority_queue.add_item((i, 1), priority)
        for j in range(self.n):
            priority = -sum(self.cols[j])
            priority_queue.add_item((j, 0), priority)

        while len(priority_queue.items) > 0:
            try: idx, axis = priority_queue.pop_item()
            except KeyError: break
            solution, changed_idxs = self.solve_line(idx, axis)

            for changed_idx in changed_idxs:
                priority = -100 # TODO: Calculate priority using a function
                priority_queue.add_item(
                    (changed_idx, (axis+1)%2), 
                    priority
                )

            if len(changed_idxs) > 0:
                if axis == 0:
                    self.grid[:,idx] = solution
                else:
                    self.grid[idx] = solution

        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('tottime')
        stats.print_stats(10)


# from examples.candy_cane import row_rules, col_rules
# from examples.seahorse import row_rules, col_rules
from examples.wikipedia_w import row_rules, col_rules

N = Nonogram(row_rules, col_rules)
N.solve()
print(N)
print("Hashtable hitrate: {:.2f}%".format(N.hits / (N.hits + N.nohits) * 100))
