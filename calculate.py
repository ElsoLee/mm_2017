from ortools.linear_solver import pywraplp


def solve_values(nodes, arcs, delay_cost):


    solver = pywraplp.Solver('Q1 Solution', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # TODO: fix 1,2,3 with real entity number
    x = [solver.IntVar(0, 1, '{}_{}_{}'.format(1, 2, 3)) for a in arcs]

    objective = solver.Objective()

    for _x in x:
        name = _x.name().split('_')
        i = name[0]
        j = name[1]
        k = name[2]

        # TODO: use get dictionary key method
        d_key = foo(i, j, k)
        d = delay_cost[d_key]
        objective.SetCoefficient(_x, d)




    x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
    y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')

    constraint1 = solver.Constraint(-solver.infinity(), 14)
    constraint1.SetCoefficient(x, 1)
    constraint1.SetCoefficient(y, 2)

    constraint2 = solver.Constraint(0, solver.infinity())
    constraint2.SetCoefficient(x, 3)
    constraint2.SetCoefficient(y, -1)

    constraint3 = solver.Constraint(-solver.infinity(), 2)
    constraint3.SetCoefficient(x, 1)
    constraint3.SetCoefficient(y, -1)

    objective = solver.Objective()
    objective.SetCoefficient(x, 3)
    objective.SetCoefficient(y, 4)
    objective.SetMaximization()

    solver.Solve()

    opt_solution = 3 * x.solution_value() + 4 * y.solution_value()
    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())
    # The value of each variable in the solution.
    print('Solution:')
    print('x = ', x.solution_value())
    print('y = ', y.solution_value())
    # The objective value of the solution.
    print('Optimal objective value =', opt_solution)
