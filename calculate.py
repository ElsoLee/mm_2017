from ortools.linear_solver import pywraplp
from network_building.utility import *
from network_building.build_transformation_network import build_transformation_network, initialize_network
from preprocessing.preprocessing import schedule_preprocessing, generate_sink_node
from config import config
from utils.utils import *

def solve_values(node_dictionary, arcs, delay_cost):

    # flight_list = get_flight_list(schedule_list)
    # c_value = max(delay_cost.values())

    solver = pywraplp.Solver('Q1 Solution', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    variable_dict = {}

    for a in arcs:
        variable_dict[(a.flight_id, a.source_node, a.target_node)] \
            = solver.IntVar(0, 1, '{}_{}_{}'.format(a.flight_id, a.source_node, a.target_node))

    # objective
    objective = solver.Objective()
    for v_key in variable_dict.keys():
        cost = delay_cost.get(get_cost_dictionary_key(v_key[1], v_key[2], v_key[0]), default=0)
        objective.SetCoefficient(variable_dict[v_key], cost)
    objective.SetMinimization()

    # constraint
    for node_keys in node_dictionary:
        if node_dictionary[node_keys].station_name == 'OVS':
            node_id = node_dictionary[node_keys].node_id

            constraint_to = solver.Constraint(-solver.Infinity, 5)
            for v_key in variable_dict.keys():
                source = v_key.split('_')[1]
                if source == node_id:
                    constraint_to.SetCoefficient(variable_dict[v_key], 1)

            constraint_from = solver.Constraint(-solver.Infinity, 5)
            for v_key in variable_dict.keys():
                target = v_key.split('_')[2]
                if target == node_id:
                    constraint_from.SetCoefficient(variable_dict[v_key], 1)

    result_status = solver.Solve()

    assert result_status == pywraplp.Solver.OPTIMAL

    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())


if __name__ == '__main__':

    schedule_list = schedule_preprocessing()

    marked_node_dictionary, count = initialize_network(
        schedule_list=schedule_list,
        recovery_start_time=string_to_timestamp(config.recovery_start_time),
        recovery_end_time=string_to_timestamp(config.recovery_end_time),
        station_time_band=config.station_time_band
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

    solve_values(node_dictionary, arc_list, cost_dictionary)





