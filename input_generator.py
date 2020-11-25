import networkx as nx
from random import seed
from random import random
from parse import write_input_file, write_output_file
from utils import calculate_stress_for_room

def graph_generator(num_vertices):
    G = nx.Graph()
    G.add_nodes_from(range(num_vertices))
    G.add_edge(0, 1, happiness=15, stress=5)
    G.add_edge(0, 2, happiness=12, stress=4.5)
    G.add_edge(0, 3, happiness=9, stress=3.5)
    G.add_edge(1, 2, happiness=0, stress=20)
    G.add_edge(1, 3, happiness=10.5, stress=4)
    G.add_edge(2, 3, happiness=11, stress=5)

    for i in range(num_vertices):
        for j in range(i+1, num_vertices):
            if i > 2 or j > 3:
                G.add_edge(i, j, happiness=round(random() * 10, 3), stress=round(random() * 5, 3))

    return G

def new_graph_generator(num_vertices):
    G = nx.Graph()
    G.add_nodes_from(range(num_vertices))

    G.add_edge(0, 1, happiness=11.329, stress=6.342)
    G.add_edge(0, 2, happiness=12.239, stress=6.495)
    G.add_edge(1, 2, happiness=13.947, stress=7.135)

    G.add_edge(2, 3, happiness=15.143, stress=7.524)

    G.add_edge(3, 4, happiness=9.837, stress=5.259)
    G.add_edge(3, 5, happiness=15.23, stress=7.784)
    G.add_edge(4, 5, happiness=13.429, stress=6.95)

    G.add_edge(5, 6, happiness=15.259, stress=7.557)

    G.add_edge(6, 7, happiness=7.294, stress=4.253)
    G.add_edge(6, 8, happiness=5.275, stress=3.293)
    G.add_edge(6, 9, happiness=9.582, stress=4.135)
    G.add_edge(7, 8, happiness=9.204, stress=5.034)
    G.add_edge(7, 9, happiness=1.9, stress=1.023)
    G.add_edge(8, 9, happiness=4.125, stress=2.234)

    for i in range(num_vertices):
        for j in range(i+1, num_vertices):
            if not G.has_edge(i, j):
                G.add_edge(i, j, happiness=round(random(), 3), stress=round(random() * 5 + 5, 3))
                # G.add_edge(i, j, happiness=0, stress=50)

    return G

def generate_cluster(G, cluster_size, v_start, ratio, room_stress): 
    total_edges = int((cluster_size * (cluster_size - 1)) / 2)
    edge_stress = [random() for i in range(total_edges)]
    stress_sum = sum(edge_stress)
    edge_stress = [(x * (room_stress + random() * -0.1)) / stress_sum for x in edge_stress] 
    k = 0
    for i in range(v_start, v_start + cluster_size):
        for j in range(i + 1, v_start + cluster_size):
            # generate stress such that 
            curr_stress = edge_stress[k]
            k += 1
            # generate random ratio less than the defining ratio
            random_ratio = ratio - random() * 0.2
            curr_happiness = curr_stress * random_ratio
            G.add_edge(i, j, happiness = round(curr_happiness, 3), stress = round(curr_stress, 3))

def generate_deceiving_edges(G, u, v, ratio):
    curr_stress = random() * 2 + 3
    random_ratio_greater = random() * 0.2 + ratio
    curr_happiness = curr_stress * random_ratio_greater
    G.add_edge(u, v, happiness = round(curr_happiness, 3), stress = round(curr_stress, 3))

def graph_generator_easier(num_vertices, ratio, clusters_sizes, starting_nodes, stress_budget):
    G = nx.Graph()
    G.add_nodes_from(range(num_vertices))

    # generate the clusters 
    for i in range(len(clusters_sizes)):
        generate_cluster(G, clusters_sizes[i], starting_nodes[i], ratio, stress_budget/len(clusters_sizes))
    
    # generate deceiving connection between clusters
    for i in range(1, len(starting_nodes)):
        generate_deceiving_edges(G, starting_nodes[i] - 1, starting_nodes[i], ratio)
    generate_deceiving_edges(G, starting_nodes[0], num_vertices - 1, ratio)

    # generate other not as effective edges 
    for i in range(num_vertices):
        for j in range(i+1, num_vertices):
            if not G.has_edge(i, j):
                low_stress = random() * 5 + 3
                low_happiness = random() * 5
                G.add_edge(i, j, happiness = round(low_happiness, 3), stress = round(low_stress, 3))
                # G.add_edge(i, j, happiness=0, stress=50)

    return G

def generate_optimal_graph(clusters_sizes):
    result = {}
    counter = 0
    for i in range(len(clusters_sizes)):
        for j in range(clusters_sizes[i]):  
            result[counter] = i
            counter += 1
    return result


graph_20 = graph_generator_easier(20, 3, clusters_sizes = [5, 4, 4, 4, 3], starting_nodes = [0, 5, 9, 13, 17], stress_budget = 75)
graph_20_out = generate_optimal_graph([5, 4, 4, 4, 3])

write_input_file(graph_20, 75, '20.in')
write_output_file(graph_20_out, '20.out')

graph_50 = graph_generator_easier(50, 3, clusters_sizes = [5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5], starting_nodes = [0, 5, 9, 14, 18, 23, 27, 32, 36, 41, 45], stress_budget = 99)
graph_50_out = generate_optimal_graph([5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5])

write_input_file(graph_50, 99, '50.in')
write_output_file(graph_50_out, '50.out')


def n_generator(num_vertices, filename):
    text_file = open(filename, "wt")
    n = text_file.write(str(num_vertices) + "\n")
    n = text_file.write(str(round(random()* 50 + 30), 3) + "\n")
    for i in range(num_vertices):
        curr_line = ""
        for j in range(i + 1, num_vertices):
            curr_line += str(i) + " " + str(j) + " " + str(round(random() * 100, 3)) + " " + str(round(random() * 100, 3)) + "\n"
        n = text_file.write(curr_line)

    text_file.close()
