import networkx as nx
from random import seed
from random import random
from parse import write_input_file

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
                G.add_edge(i, j, happiness=round(random() * 6 + 3, 3), stress=round(random() * 4.5 + 4.5, 3))

    G.add_edge(0, 9, happiness=15.329, stress=7.552)

    return G

write_input_file(new_graph_generator(10), 60, '10.in')

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
