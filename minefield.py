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
                            nr_ = r + nr
                            nc_ = c + nc
                            if nr_ < 0 or nc_ < 0:
                                continue
                            try:
                                if self.__field[nr_][nc_] is None:
                                    self.__field[r][c] += 1
                            except IndexError:
                                continue

    def get(self, row, col):
        return self.__field[row][col]

    def zero_clusters(self):
        zeros = [(i, j) for i in range(self.rows) for j in range(self.cols)
                 if self.__field[i][j] == 0]
        zdict = {k: v for v, k in enumerate(zeros)}
        sets = []
        for i in range(len(zeros)):
            cr, cc = zeros[i]
            sets.append({zeros[i]})
            for j in zeros[i+1:]:
                if abs(cr-j[0]) < 2 and abs(cc-j[1]) < 2:
                    sets[-1].add(j)
        i = 0
        while i < len(sets):
            while True:
                s = sets[i]
                prev = len(s)
                for j in range(len(sets)-1, i, -1):
                    if not s.isdisjoint(sets[j]):
                        s.update(sets.pop(j))
                if prev == len(s):
                    break
            i += 1
        return dict(enumerate(sets))

    def max_zeros(self):
        clusts = self.zero_clusters()
        if not clusts:
            return []
        by_len = {len(v): k for k, v in clusts.items()}
        return clusts[by_len[max(by_len.keys())]]


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

    def user_mark(self, row, col):
        if self.__opened[row][col] is None:
            self.__opened[row][col] = "U"
            return True
        return False

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
