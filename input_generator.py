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
    G.add_edge(0, 1, happiness=11, stress=6)
    G.add_edge(0, 2, happiness=13, stress=7)
    G.add_edge(1, 2, happiness=13, stress=7)

    G.add_edge(2, 3, happiness=15, stress=7)

    G.add_edge(3, 4, happiness=9, stress=5)
    G.add_edge(3, 5, happiness=15, stress=8)
    G.add_edge(4, 5, happiness=13, stress=7)

    G.add_edge(5, 6, happiness=15, stress=7)

    G.add_edge(6, 7, happiness=7, stress=4)
    G.add_edge(6, 8, happiness=5, stress=3)
    G.add_edge(6, 9, happiness=9, stress=5)
    G.add_edge(7, 8, happiness=9, stress=5)
    G.add_edge(7, 9, happiness=1, stress=1)
    G.add_edge(8, 9, happiness=3, stress=2)

    G.add_edge(9, 0, happiness=15, stress=7)

    for i in range(num_vertices):
        for j in range(i+1, num_vertices):
            if not G.has_edge(i, j):
                G.add_edge(i, j, happiness=round(random(), 3), stress=round(random() * 5 + 5, 3))

    return G

write_input_file(new_graph_generator(10), 40, '10.in')

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

