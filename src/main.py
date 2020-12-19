class Nonogram:
    def __init__(self, row_vals, col_vals):
        self.row_vals = row_vals
        self.col_vals = col_vals

        self.m = len(row_vals)
        self.n = len(col_vals)

        ## Initialise grid
        self.grid = [
            [0 for _ in range(self.m)] 
            for _ in range(self.n)]

    def __str__(self):
        string = ""
        for j in range(self.m):
            for i in range(self.n):
                cell = self.grid[j][i]
                if cell == 0:
                    string += '. '
                elif cell == 1:
                    string += '  '
                elif cell == 2:
                    string += '# '
                else:
                    raise ValueError(
                        "Unrecognised value at cell ({}, {}): {}".format(i, j, cell)
                    )
            string += "\n"
        return string


N = Nonogram(
        [[2, 1], [1, 3], [1, 2], [3], [4], [1]], 
        [[1], [5], [2], [5], [2, 1], [2]]
    )

print(N)

