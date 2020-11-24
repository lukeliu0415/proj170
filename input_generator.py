# import networkx as nx
from random import seed
from random import random

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

n_generator(20, "input_20.txt")
n_generator(50, "input_50.txt")