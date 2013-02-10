FlowSolver
==========

Using SAT solvers to generate solutions for [Flow](https://play.google.com/store/apps/details?id=com.bigduckgames.flow&hl=en) levels. Can solve selected level on device automatically using [MonkeyRunner](http://developer.android.com/tools/help/monkeyrunner_concepts.html).

The code is quite messy and slow, but it works.

Example run
===========

For a fully autonomous solving of a level on screen run

    python solve_monkey.py

This will perform the following steps:

- Use MonkeyRunner to take a [screenshot](https://raw.github.com/lacop/FlowSolver/master/screenshots/2013-02-10_16-18-48.png).
- Extract the level from the screenshot.
- Setup SAT clauses and write them to file.
- Run a SAT solver on the file to generate a solution.
- Display the [solution](https://raw.github.com/lacop/FlowSolver/master/screenshots/2013-02-10_16-18-48.sol.png).
- Finally, use MonkeyRunner to send a [series of drag events](https://raw.github.com/lacop/FlowSolver/master/screenshots/2013-02-10_16-18-48.sol_path.txt) to execute the solution on the device.

![solution](https://raw.github.com/lacop/FlowSolver/master/screenshots/2013-02-10_16-18-48.sol.png)

Old examples
============

These are old examples using [MiniSAT](http://minisat.se/). By using [glucose](http://www.lri.fr/~simon/?page=glucose) you can achieve much better speeds.

![level_8_150](https://raw.github.com/lacop/FlowSolver/master/levels/flow_free_8_8_150.sol.png)

**Level 8x8, #150** 2,688 variables, 58,603 clauses, solved instantaneously

![level_14_1](https://raw.github.com/lacop/FlowSolver/master/levels/flow_free_14_14_1.sol.png)

**Level 14x14, #1** 20,580 variables, 1,095,960 clauses, approx. 3 minutes to solve

![level_14_30](https://raw.github.com/lacop/FlowSolver/master/levels/flow_free_14_14_30.sol_dist.png)

**Level 14x14, #30,** _with cycle breaking_ 59,388 variables, 12,256,516 clauses, approx. 4 minutes to solve

![level_14_30](https://raw.github.com/lacop/FlowSolver/master/levels/flow_free_14_14_30.sol_nodist.png)

**Level 14x14, #30,** _without cycle breaking_ 20,580 variables, 1,096,306 clauses, approx. 1 minutes to solve
