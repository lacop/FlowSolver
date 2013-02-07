from itertools import permutations

class Level:
    def load_from_file(self, path):
        lines = open(path).readlines()
        matrix = [l.split() for l in lines if len(l.strip()) > 0]
        self.rows = len(matrix)
        self.cols = len(matrix[0])

        self.tiles = []
        keys = {}
        for l in matrix:
            row = []
            for r in l:
                if r == '.':
                    row.append(None)
                else:
                    if not keys.has_key(r):
                        keys[r] = len(keys)
                    row.append(keys[r])
            self.tiles.append(row)

        self.colors = len(keys)

    def valid(self, x, y):
        return x < self.cols and x >= 0 and y < self.rows and y >= 0

    def neighbors(self, x, y):
        n = []
        for dx, dy in permutations([1, 0, -1], 2):
            if dx*dx + dy*dy == 1:
                if self.valid(x+dx, y+dy):
                    n.append((x+dx, y+dy))
        return n