from __future__ import print_function
from solve_image import solve_image
from subprocess import call
from datetime import datetime

def solve_monkey():
    path = 'screenshots/%s.png' % datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print('Taking screenshot')
    call(['monkeyrunner', 'monkeyscreen.py', path])
    print('Rotating')
    call(['convert', '-rotate',  '90', path, path])
    
    print('Starting image solver')
    solve_image(path, dist=False)
    
if __name__ == '__main__':
    solve_monkey()