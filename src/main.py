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


