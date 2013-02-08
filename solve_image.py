from __future__ import print_function

from level import Level
from sat import sat_get_clauses, sat_write_clauses, sat_read_valuation
from visualization import get_solution

from PIL import Image, ImageDraw
from itertools import product
from collections import defaultdict
from pprint import pprint
from math import sin, cos, pi
from os.path import splitext
from gc import collect
from subprocess import call

SAT_PATH = 'work/MiniSat_v1.14_cygwin.exe'

def merge_buckets(buckets):
    while True:
        keys = sorted(buckets.iterkeys())
        merged = False

        # Merge left->right
        for i in range(len(keys) - 1):
            if buckets.has_key(keys[i]-1):
                continue
            if keys[i]+1 == keys[i+1]:
                buckets[keys[i+1]] += buckets[keys[i]]
                buckets[keys[i]] = 0
                merged = True

        # Merge right->left
        for i in reversed(range(len(keys))[1:]):
            if buckets.has_key(keys[i] + 1):
                continue
            if keys[i]-1 == keys[i-1]:
                buckets[keys[i-1]] += buckets[keys[i]]
                buckets[keys[i]] = 0
                merged = True

        buckets = {k:v for k,v in buckets.iteritems() if v > 0}

        if not merged:
            break

    return buckets

def avg(x):
    return sum(x) / len(x)

def color_dist2(x, y):
    return sum([(a-b)**2 for a,b in zip(x, y)])

def sample(pix, cx, cy, dist, cnt):
    colors = []
    for i in range(cnt):
        a = 2*pi*i/cnt
        x = int(cx + cos(a) * dist)
        y = int(cy + sin(a) * dist)
        colors.append(pix[x, y])
        #pix[int(x), int(y)] = (0, 255, 0)
    return colors

def avg_color(cl):
    # :/ zipwith+map
    return (avg([c[0] for c in cl]), avg([c[1] for c in cl]), avg([c[2] for c in cl]))

def parse_image(path):
    img = Image.open(path)
    pix = img.load()

    # TODO proper line detection instead of color matching
    border_color = (131, 97, 66) # brown
    #border_color = (123, 125, 66) # green
    border_threshold = 32

    xbuckets = defaultdict(int)
    ybuckets = defaultdict(int)

    # Find borders
    for pos in product(xrange(img.size[0]), xrange(img.size[1])):
        col = pix[pos]
        dist2 = color_dist2(col, border_color)
        if dist2 < border_threshold:
            xbuckets[pos[0]] += 1
            ybuckets[pos[1]] += 1

    # Throw away below average (keeps the main lines)
    xbuckets = {k:v for k,v in xbuckets.items() if v > avg(xbuckets.values())}
    ybuckets = {k:v for k,v in ybuckets.items() if v > avg(ybuckets.values())}

    # Merge neighbor buckets
    xmarks = sorted(merge_buckets(xbuckets).keys())
    ymarks = sorted(merge_buckets(ybuckets).keys())

    pprint(xmarks)
    pprint(ymarks)

    # Figure out coordinates
    minx, miny, maxx, maxy = avg([xmarks[0], xmarks[1]]), avg([ymarks[0], ymarks[1]]), avg([xmarks[-1], xmarks[-2]]), avg([ymarks[-1], ymarks[-2]])
    xsize = len(xmarks) - 1
    ysize = len(ymarks) - 1

    level = Level()
    level.cols = xsize
    level.rows = ysize
    level.tiles = [[None for i in range(xsize)] for j in range(ysize)]

    circle_ratio = 0.4
    out_ratio = 0.8
    circle_threshold = 128
    out_threshold = 1024

    color_map = {}
    map_threshold = 32

    for i, j in product(range(xsize), range(ysize)):
        x, y = avg([xmarks[i], xmarks[i+1]]), avg([ymarks[j], ymarks[j+1]])
        w = min(xmarks[i+1] - xmarks[i], ymarks[j+1] - ymarks[j])

        # Ignore empty
        if pix[x, y] == (0, 0, 0):
            continue

        center = avg_color([pix[x+a, y+b] for a,b in product([-1, 0, 1], [-1, 0, 1])])

        inside = sample(pix, x, y, w*circle_ratio/2, 8)
        inside_dist2 = avg([color_dist2(center, ic) for ic in inside])

        if inside_dist2 > circle_threshold:
            #print('IN Rejecting ', i, j)
            #print(inside)
            #print(inside_dist2)
            continue

        outside = sample(pix, x, y, w*out_ratio/2, 8)
        outside_dist2 = avg([color_dist2(center, oc) for oc in outside])

        if outside_dist2 < out_threshold:
            #print('OUT Rejecting ', i, j)
            #print(outside)
            #print(outside_dist2)
            continue

        id = None
        for k, v in color_map.items():
            if color_dist2(k, center) < map_threshold:
                id = v
                #print(x,y, 'id=', v)

        if id is None:
            id = len(color_map)
            color_map[center] = id

        level.tiles[j][i] = id

        """ImageDraw.Draw(img).ellipse((x-w/5-1, y-w/5-1, x+w/5+1, y+w/5+1), fill = 'black')
        ImageDraw.Draw(img).ellipse((x-w/5, y-w/5, x+w/5, y+w/5), fill = 'white')
        ImageDraw.Draw(img).text((x+1, y), str(id), fill = 'black')
        ImageDraw.Draw(img).text((x-1, y), str(id), fill = 'black')
        ImageDraw.Draw(img).text((x, y+1), str(id), fill = 'black')
        ImageDraw.Draw(img).text((x, y-1), str(id), fill = 'black')
        ImageDraw.Draw(img).text((x, y), str(id), fill = 'white')"""

    level.colors = len(color_map)

    img = img.crop((xmarks[0], ymarks[0], xmarks[-1], ymarks[-1]))
    img.show()

    return (level, {v:k for k,v in color_map.items()})

def solve_image(path, dist = False):
    print('Parsing image ...')
    level, color_map = parse_image(path)

    print('Generating clauses ...')
    clauses = sat_get_clauses(level, dist)
    print('Got %d clauses' % len(clauses))

    pathparts = splitext(path)
    pathin = '%s.sat_in.txt' % pathparts[0]
    pathout = '%s.sat_out.txt' % pathparts[0]
    pathsol = '%s.sol.png' % pathparts[0]

    print('Writing to file ...')
    map = sat_write_clauses(clauses, pathin)

    # Release some memory
    clauses = []
    collect()

    print('Running SAT solver ...')
    call([SAT_PATH, pathin, pathout])

    print('Reading valuation ...')
    val = sat_read_valuation(level, map, pathout)

    if not val:
        print('Unsatisfiable ...')
        return

    #pprint(val)

    print('Displaying solution ...')
    img = get_solution(level, val, dist, color_map)
    img.show()
    img.save(pathsol)

def main():
    #solve_image('screenshots/2013-02-05 17.59.29.png')
    #solve_image('screenshots/2013-02-05 18.33.40.png')
    #solve_image('screenshots/2013-02-05 18.33.46.png')
    #solve_image('screenshots/2013-02-05 18.33.50.png')
    #solve_image('screenshots/2013-02-05 18.33.53.png')
    #solve_image('screenshots/2013-02-05 19.23.25.png')
    #solve_image('screenshots/2013-02-08 19.25.35.png')
    #solve_image('screenshots/2013-02-08 19.25.46.png')
    solve_image('screenshots/2013-02-08 19.25.59.png')

if __name__ == '__main__':
    main()