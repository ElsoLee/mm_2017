from ortools.linear_solver import pywraplp
from network_building.utility import *
from network_building.build_transformation_network import build_transformation_network, initialize_network
from preprocessing.preprocessing import schedule_preprocessing, generate_sink_node
from config import config
from utils.utils import *

def solve_values(node_dictionary, arcs, delay_cost, schedule_list):

    flight_list = get_flight_list(schedule_list)
    # c_value = max(delay_cost.values())

    solver = pywraplp.Solver('Q1 Solution', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    variable_dict = {}

    for a in arcs:
        variable_dict[(a.flight_id, a.source_node.node_id, a.target_node.node_id)] \
            = solver.IntVar(0, 1, '{}_{}_{}'.format(a.flight_id, a.source_node.node_id, a.target_node.node_id))

    # objective
    objective = solver.Objective()
    for v_key in variable_dict.keys():
        cost = delay_cost.get((v_key[1], v_key[2], v_key[0]), 0)
        objective.SetCoefficient(variable_dict[v_key], cost)
    objective.SetMinimization()

    # constraint
    # for node_keys in node_dictionary:
    #     if node_dictionary[node_keys].station_name == 'OVS':
    #         node_id = node_dictionary[node_keys].node_id
    #
    #         constraint_to = solver.Constraint(-solver.infinity(), 5)
    #         for v_key in variable_dict.keys():
    #             source = v_key[1]
    #             if source == node_id:
    #                 constraint_to.SetCoefficient(variable_dict[v_key], 1)
    #
    #         constraint_from = solver.Constraint(-solver.infinity(), 5)
    #         for v_key in variable_dict.keys():
    #             target = v_key[2]
    #             if target == node_id:
    #                 constraint_from.SetCoefficient(variable_dict[v_key], 1)

    for flight in flight_list:
        cons = None
        for var_key in variable_dict.keys():
            if var_key[0] == flight:
                cons = solver.Constraint(-solver.infinity(), 1)
                break
        if not cons:
            continue
        for var_key in variable_dict.keys():
            if var_key[0] == flight:
                cons.SetCoefficient(variable_dict[var_key], 1)

    for flight in flight_list:
        cons_low = None
        for var_key in variable_dict.keys():
            if var_key[0] == flight:
                cons_low = solver.Constraint(-solver.infinity(), -1)
                break
        if not cons_low:
            continue
        for var_key in variable_dict.keys():
            if var_key[0] == flight:
                cons_low.SetCoefficient(variable_dict[var_key], -1)

    graph_flights = get_flight_count(arc_list)

    constraint_flight_count = solver.Constraint(-solver.infinity(), len(graph_flights))
    for var_key in variable_dict.keys():
        constraint_flight_count.SetCoefficient(variable_dict[var_key], 1)

    constraint_flight_count_less = solver.Constraint(-solver.infinity(), -len(graph_flights))
    for var_key in variable_dict.keys():
        constraint_flight_count_less.SetCoefficient(variable_dict[var_key], -1)

    result_status = solver.Solve()

    assert result_status == pywraplp.Solver.OPTIMAL

    print 'Number of variables =', solver.NumVariables()
    print 'Number of constraints =', solver.NumConstraints()

    print('Optimal objective value = %d' % solver.Objective().Value())

    for keys in variable_dict.keys():
        print '%s = %d' % (variable_dict[keys].name(), variable_dict[keys].solution_value())


if __name__ == '__main__':

    schedule_list = schedule_preprocessing()

    marked_node_dictionary, count = initialize_network(
        schedule_list=schedule_list,
        recovery_start_time=string_to_timestamp(config.recovery_start_time),
        recovery_end_time=string_to_timestamp(config.recovery_end_time),
        station_time_band=config.station_time_band,
        turnaround_time=config.turnaround_time
    )

    node_dictionary, arc_list, cost_dictionary = build_transformation_network(
        previous_count=count,
        schedule_list=schedule_list,
        sink_node_information_dictionary=generate_sink_node(),
        marked_node_dictionary=marked_node_dictionary,
        turnaround_time=config.turnaround_time,
        cost_function=lambda x: x,
        station_time_band=config.station_time_band
    )

    print cost_dictionary
    solve_values(node_dictionary, arc_list, cost_dictionary, schedule_list)





