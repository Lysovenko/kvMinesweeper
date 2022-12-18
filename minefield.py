from random import randint


class MineField:
    def __init__(self, rows=10, cols=10, mines=20):
        indices = list(range(rows * cols))
        rinds = [indices.pop(randint(0, len(indices) - 1))
                 for i in range(mines)]
        self.field = [[0 for j in range(cols)] for i in range(rows)]
        self.rows = rows
        self.cols = cols
        for i in rinds:
            row = i // cols
            col = i % cols
            self.field[row][col] = None
        for r in range(rows):
            for c in range(cols):
                if self.field[r][c] is None:
                    continue
                for nr in (-1, 0, 1):
                    for nc in (-1, 0, 1):
                        if any((nr != 0, nc != 0)):
                            try:
                                if self.field[r + nr][c + nc] is None:
                                    self.field[r][c] += 1
                            except IndexError:
                                continue

    def get(self, row, col):
        return self.field[row][col]
