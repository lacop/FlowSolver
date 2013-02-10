from __future__ import print_function

from solve_image import solve_image, avg
from sat import connects
from level import Level

from subprocess import call
from datetime import datetime
from sys import argv
from itertools import product
from pprint import pprint
from os.path import splitext

def solve_monkey(dist = False):
    path = 'screenshots/%s.png' % datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print('Taking screenshot')
    call(['monkeyrunner', 'monkeyscreen.py', path])
    print('Rotating')
    call(['convert', '-rotate',  '90', path, path])
    
    print('Starting image solver')
    val, xmarks, ymarks = solve_image(path, dist)
    
    print('Generating solution path')
    pathparts = splitext(path)
    pathsol = '%s.sol_path.txt' % pathparts[0]
    solfile = open(pathsol, 'w')
    
    level = Level()
    level.rows = len(val)
    level.cols = len(val[0]) 
    for x, y in product(range(level.cols), range(level.rows)):
        c, t = val[y][x][0]
        if t != 0:
            continue
        #print('Tracing color', c)
        # Found a dot, start
        cx, cy, ct = x, y, 0
        while True:
            # Print current
            #print(cx, cy, ct)
            solfile.write('%d %d\n' % (avg([xmarks[cx], xmarks[cx+1]]), avg([ymarks[cy], ymarks[cy+1]])))
            # Find next
            cx2, cy2, ct2 = -1, -1, -1
            for nx, ny in level.neighbors(cx, cy):
                nc, nt = val[ny][nx][0]
                if nc >= 0 and connects(cx, cy, ct, nx, ny, nt):
                    cx2 = nx
                    cy2 = ny
                    ct2 = nt
                    break
            # Found nothing - done
            if cx2 == -1:
                break
            # Delete current and replace with next
            val[cy][cx][0] = -1, -1
            cx = cx2
            cy = cy2
            ct = ct2
        # Delete last
        val[cy][cx][0] = -1, -1
        solfile.write('0 0\n')
    solfile.close()
    
    print('Solving on device')
    call(['monkeyrunner', 'monkeypath.py', pathsol])
    
    print('DONE')
    
if __name__ == '__main__':
    d = False
    if len(argv) > 1:
        if argv[1] == 'dist':
            d = True
    solve_monkey(dist = d)