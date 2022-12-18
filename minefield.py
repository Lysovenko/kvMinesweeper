from random import randint


class MineField:
    def __init__(self, rows=10, cols=10, mines=20):
        indices = list(range(rows * cols))
        rinds = [indices.pop(randint(0, len(indices) - 1))
                 for i in range(mines)]
        self.__field = [[0 for j in range(cols)] for i in range(rows)]
        self.rows = rows
        self.cols = cols
        for i in rinds:
            row = i // cols
            col = i % cols
            self.__field[row][col] = None
        for r in range(rows):
            for c in range(cols):
                if self.__field[r][c] is None:
                    continue
                for nr in (-1, 0, 1):
                    for nc in (-1, 0, 1):
                        if any((nr != 0, nc != 0)):
                            try:
                                if self.__field[r + nr][c + nc] is None:
                                    self.__field[r][c] += 1
                            except IndexError:
                                continue

    def get(self, row, col):
        return self.__field[row][col]


class Opener:
    def __init__(self, field):
        self.__mined = field
        self.rows = field.rows
        self.cols = field.cols
        self.__opened = [[None for j in range(self.cols)]
                         for i in range(self.rows)]

    def pick(self, row, col):
        v = self.__mined.get(row, col)
        if v is None:
            self.__opened[row][col] = "B"
        else:
            self.__opened[row][col] = v
        return v

    def _around_zeros(self):
        neibours = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.__opened[r][c] == 0:
                    for rr in (-1, 0, 1):
                        for rc in (-1, 0, 1):
                            if all((rr == 0, rc == 0)):
                                continue
                            if any((rr + r < 0, rc + c < 0)):
                                continue
                            try:
                                if self.__opened[r + rr][c + rc] is None:
                                    v = self.__mined.get(r + rr, c + rc)
                                    if v is None:
                                        v = "B"
                                    self.__opened[r + rr][c + rc] = v
                                    neibours.append((r + rr, c + rc, v))
                            except IndexError:
                                continue
        return neibours

    def around_zeros(self):
        neibours = []
        while True:
            neibs = self._around_zeros()
            if not neibs:
                break
            neibours.extend(neibs)
        return neibours
