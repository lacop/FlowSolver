from __future__ import print_function

from level import Level
from sat import sat_get_clauses, sat_write_clauses, sat_read_valuation
from visualization import get_solution

from subprocess import call
from pprint import pprint
from os.path import splitext

from pprint import pprint

SAT_PATH = 'work/MiniSat_v1.14_cygwin.exe'

def solve_file(path):
    print('Reading level from', path)
    level = Level()
    level.load_from_file(path)

    print('Generating clauses ...')
    clauses = sat_get_clauses(level)
    print('Got %d clauses' % len(clauses))

    pathparts = splitext(path)
    pathin = '%s.sat_in%s' % pathparts
    pathout = '%s.sat_out%s' % pathparts
    pathsol = '%s.sol.png' % pathparts[0]

    print('Writing to file ...')
    map = sat_write_clauses(clauses, pathin)

    print('Running SAT solver ...')
    call([SAT_PATH, pathin, pathout])

    print('Reading valuation ...')
    val = sat_read_valuation(level, map, pathout)

    if not val:
        print('Unsatisfiable ...')
        return

    print('Displaying solution ...')
    img = get_solution(level, val)
    img.show()
    img.save(pathsol)

def main():
    #solve_file('levels/flow_free_8_8_150.txt')
    #solve_file('levels/flow_free_14_14_1.txt')
    #solve_file('levels/flow_free_14_14_2.txt')
    solve_file('levels/flow_free_14_14_30.txt')

if __name__ == '__main__':
    main()