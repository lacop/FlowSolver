from level import Level
from itertools import product, combinations

# encode distance to avoid loops
# maybe as separate variable, will reduce variable count and maybe clause count


def sat_var_pos(x, y, c, t):
    return "%d_%d_%d_%d" % (x, y, c, t)
def sat_var_neg(x, y, c, t):
    return "-%d_%d_%d_%d" % (x, y, c, t)
def sat_neg(c):
    return "-%s" % c

def sat_var_decode(str):
    return [int(x) for x in str.split('_')]

def directions(t):
    dirs = []
    if t in [2, 3, 6]: # top
        dirs.append((0, -1))
    if t in [1, 3, 4]: # right
        dirs.append((1, 0))
    if t in [2, 4, 5]: # bottom
        dirs.append((0, 1))
    if t in [1, 5, 6]: # left
        dirs.append((-1, 0))
    return dirs

def connects_one_way(x1, y1, t1, x2, y2):
    if t1 == 0:
        return True
    for dx,dy in directions(t1):
        if x1+dx == x2 and y1+dy == y2:
            return True
    return False

def connects(x1, y1, t1, x2, y2, t2):
    # Only 4-connectivity
    if (x1-x2)**2 + (y1-y2)**2 != 1:
        return False
    if t1 == 0 and t2 == 0:
        return False

    return connects_one_way(x1, y1, t1, x2, y2) and connects_one_way(x2, y2, t2, x1, y1)

def sat_get_clauses(level):
    xs = range(level.rows)
    ys = range(level.cols)
    cs = range(level.colors)
    ts = range(7) # 0 = dot, 1..6 = line orientations

    # At least one value for each field
    clauses = []
    for x, y in product(xs, ys):
        if level.tiles[y][x] is not None:
            continue
        clause = []
        for c, t in product(cs, ts[1:]): # Can't have dots
            clause.append(sat_var_pos(x, y, c, t))
        clauses.append(clause)

    # At most one value for each field
    for x, y in product(xs, ys):
        for (c1, t1), (c2, t2) in combinations(product(cs, ts), 2): # Distinct pair
            clauses.append([sat_var_neg(x, y, c1, t1), sat_var_neg(x, y, c2, t2)])

    # Setup board
    for x, y in product(xs, ys):
        if level.tiles[y][x] is not None:
            clauses.append([sat_var_pos(x, y, level.tiles[y][x], 0)])

    # Each dot must have exactly one line coming in
    for x, y in product(xs, ys):
        if level.tiles[y][x] is not None:
            valid = []
            # Find valid neighbor configurations that connect to this dot
            for nx, ny in level.neighbors(x, y):
                for t in ts[1:]:
                    if connects(x, y, 0, nx, ny, t):
                        valid.append(sat_var_pos(nx, ny, level.tiles[y][x], t))

            # At least one must be true
            clauses.append(valid)

            # At most one must be true
            for v1, v2 in combinations(valid, 2):
                clauses.append([sat_neg(v1), sat_neg(v2)])

    for x, y in product(xs, ys):
        if level.tiles[y][x] is not None:
            continue
        for c, t in product(cs, ts[1:]): # Can't have dots
            valid = True
            for dx, dy in directions(t):
                # Out of bounds
                if not level.valid(x+dx, y+dy):
                    valid = False
                    break
                # Touching wrong color dot
                if level.tiles[y+dy][x+dx] is not None and level.tiles[y+dy][x+dx] != c:
                    valid = False
                    break

            if not valid:
                clauses.append([sat_var_neg(x, y, c, t)])
                continue

            # Both endpoints must connect properly
            for dx, dy in directions(t):
                clause = [sat_var_neg(x, y, c, t)]
                # Ignore same-colored dots
                if level.tiles[y+dy][x+dx] is not None:
                    continue
                for t2 in ts[1:]:
                    if connects(x, y, t, x+dx, y+dy, t2):
                        clause.append(sat_var_pos(x+dx, y+dy, c, t2))
                clauses.append(clause)

    return clauses

def sat_write_clauses(clauses, path):
    lines = []
    map = {}

    for clause in clauses:
        line = ''
        for v in clause:
            neg = False
            if v[0] == '-':
                v = v[1:]
                neg = True

            if not map.has_key(v):
                map[v] = len(map) + 1 # Make sure no var has id 0

            line += '-' if neg else ''
            line += str(map[v]) + ' '
        line += '0'
        lines.append(line)

    f = open(path, 'w')
    f.write('p cnf %d %d\n' % (len(map), len(clauses)))
    for line in lines:
        f.write('%s\n' % line)
    f.close()

    return map

def sat_read_valuation(level, map, path):
    f = open(path, 'r')
    lines = f.readlines()
    f.close()

    if lines[0] != 'SAT\n':
        return None

    map = {v:k for k,v in map.items()}
    valuation = [[None for i in range(level.cols)] for j in range(level.rows)]

    f = open('dbg.txt', 'w')

    for v in lines[1].split():
        v = int(v)
        if v <= 0:
            continue

        x,y,c,t = sat_var_decode(map[v])
        f.write('%s\n'%map[v])

        if valuation[y][x] is not None:
            raise Exception('Conflict at %s %s' % (x, y))

        valuation[y][x] = (c, t)

    f.close()

    return valuation