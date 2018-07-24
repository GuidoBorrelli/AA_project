import time
import networkx as nx
import pandas as pd
import alg1 as tarjan
import alg2 as nuutila
import alg3 as pearce
import performance
import test

SIZE_BENCHMARK = 10000
TEST = False
TEST_NODE_SIZE = 0
TEST_EDGE_PROBABILITY = 0
DEBUG = False


# Density variable can assume indicative values: 0(sparse graph), 1(normal graph), 2(dense graph)
# Nodes dimensional variable are set to: 50, 100, 200, 600
# Saves performance of the density/dimensional combination
def create_test_set():
    dimension_list = [50, 100, 200, 600]
    density_list = [0, 1, 2]
    # Create a dataframe to save performance for each algorithm
    df1 = pd.DataFrame(columns={'Sparse', 'Medium', 'Dense'}, index=dimension_list)
    df2 = pd.DataFrame(columns={'Sparse', 'Medium', 'Dense'}, index=dimension_list)
    df3 = pd.DataFrame(columns={'Sparse', 'Medium', 'Dense'}, index=dimension_list)
    performance_dict = {'Tarjan': df1, 'Nuutila': df2, 'Pearce': df3}
    for graph_density in density_list:
        column_1 = []
        column_2 = []
        column_3 = []
        for nodes_dimension in dimension_list:
            column_performance = create_benchmark(nodes_dimension, graph_density)
            column_1.append(column_performance['Tarjan'])
            column_2.append(column_performance['Nuutila'])
            column_3.append(column_performance['Pearce'])
        # Based on graph_density, I fill the right column
        if graph_density == 0:
            df1['Sparse'] = column_1
            df2['Sparse'] = column_2
            df3['Sparse'] = column_3
        elif graph_density == 1:
            df1['Medium'] = column_1
            df2['Medium'] = column_2
            df3['Medium'] = column_3
        elif graph_density == 2:
            df1['Dense'] = column_1
            df2['Dense'] = column_2
            df3['Dense'] = column_3
    return performance_dict


# Creates the set of graph to generate given a specified couple of node dimension and density of graphs
# Manipulate performance of every graph and aggregate them according to the algorithm
def create_benchmark(nodes_dimension, graph_density):
    print("Create benchmark : Nodes {}  -  Density type {}".format(nodes_dimension, graph_density))
    # List containing time records for each algorithm
    times1_list = []
    times2_list = []
    times3_list = []
    dict_times = {}
    for _ in range(0, SIZE_BENCHMARK):
        # print(i, end="\r")
        times1, times2, times3 = create_direct_graph(nodes_dimension, graph_density)
        times1_list.append(times1)
        times2_list.append(times2)
        times3_list.append(times3)
    dict_times['Pearce'] = times1_list
    dict_times['Nuutila'] = times2_list
    dict_times['Tarjan'] = times3_list
    return dict_times


# Deprecated - Initially idea was to adapt size of test set on different cases
# Given characteristics of set of graphs to generate, set the graph cardinality of the benchmark
def set_quantity(nodes_dimension, graph_density):
    if graph_density <= 10 ** 2:
        card = nodes_dimension
    elif 1 == graph_density:
        card = 2 * (10 ** 2)
    else:
        card = 10 ** 2
    return card


# A random graph is created with the given characteristics
# Based on density of graph, different functions are used due to complexity gains
# Performance on algorithms are evaluated for each graph after creation
def create_direct_graph(n, d):
    # An heuristic to build valid edge probabilities
    def switch_density(argument):
        switcher = {
            0: 1 / n,
            1: 3 / n,
            2: 1 / (n ** 0.1),
        }
        value = switcher.get(argument, False)
        if value is False:
            raise "Invalid Density: " + argument
        return switcher[argument]

    p = switch_density(d)
    if d == 0:
        graph = nx.fast_gnp_random_graph(n, p, seed=None, directed=True)
    else:
        graph = nx.gnp_random_graph(n, p, seed=None, directed=True)
    return apply_alg(graph)


# Call algorithms to be applied on the graph
def apply_alg(graph):
    # Keep track of time of each algorithm executed
    t0 = time.time()
    pearce.apply_alg(graph)
    duration0 = time.time() - t0
    t1 = time.time()
    nuutila.apply_alg(graph)
    duration1 = time.time() - t1
    t2 = time.time()
    tarjan.apply_alg(graph)
    duration2 = time.time() - t2
    return duration0, duration1, duration2


def main():
    if not TEST:
        print("Start")
        dict_performance = create_test_set()
        if DEBUG:
            print("Tarjan performance: {}".format(dict_performance['Tarjan']))
            print("Nuutila performance: {}".format(dict_performance['Nuutila']))
            print("Pearce performance: {}".format(dict_performance['Pearce']))
        performance.plot_result(dict_performance)
        print("End")
    else:
        test.test_algorithms(TEST_NODE_SIZE, TEST_EDGE_PROBABILITY)
    return 0


if __name__ == "__main__":
    main()
