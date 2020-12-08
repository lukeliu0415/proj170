import networkx as nx
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room, calculate_happiness_for_room
import sys
from os.path import basename, normpath
import glob
from random import random, randint, choice
import itertools
import copy

def partition(collection):
    if len(collection) == 1:
        yield [ collection ]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset 
        yield [ [ first ] ] + smaller

def sortOrder(e):
    if e[2].get('stress') == 0:
        return e[2].get('happiness') / 0.001
    else:
        return e[2].get('happiness') / e[2].get('stress')

def solve_naive(G, s):
    vertex_list = list(G.nodes)
    N = len(vertex_list)

    best_happiness = 0
    config = {}
    numRooms = 0

    for n, p in enumerate(partition(list(range(10))), 1):
        isValid = True
        for room in p:
            if calculate_stress_for_room(room, G) > s / len(p):
                isValid = False
                break

        if not isValid:
            continue
        
        D = {}
        for i in range(len(p)):
            for j in p[i]:
                D[j] = i

        happiness = calculate_happiness(D, G)
        if happiness > best_happiness:
            best_happiness = happiness
            config = D
            numRooms = len(p)

    return config, numRooms

def solve_greedy(G, s):
    vertex_list = list(G.nodes)
    N = len(vertex_list)

    # iterate through all possible values of number of rooms
    for k in range(1, N+1):
        solution = {}  # key:value => (vertex, room)
        room_to_vertices = {}  # key:value => (room number, vertices)

        # Assume all vertices are on their own 
        for i in range(len(vertex_list)):
            solution[i] = i
            room_to_vertices[i] = [i]
        
        edges = sorted(G.edges(data=True), key = sortOrder, reverse = True)
        # edges = sorted(G.edges(data=True), key=lambda t: t[2].get('happiness'), reverse = True) # sort by highest happiness

        for e in edges:
            # get current room numbers
            room_v = solution[e[0]]
            room_u = solution[e[1]]

            # see if the pair is already in the same room
            if room_u == room_v:
                continue
            
            # attempt to merge room
            merged_room = room_to_vertices[room_v] + room_to_vertices[room_u] 

            # if it does not satisfy stress constraints, abort
            if calculate_stress_for_room(merged_room, G) > s / k:
                continue
            
            # actually merge
            for v in room_to_vertices[room_u]:
                solution[v] = room_v
            room_to_vertices[room_v] = merged_room
            room_to_vertices.pop(room_u)

        # print(calculate_happiness(solution, G))

        # check to see if we should update if the constraint on the # of rooms is satisfied; if so, return the result
        if len(room_to_vertices) <= k:
            result = {}
            length = len(room_to_vertices)

            for i in range(length):
                vertices = room_to_vertices.pop(list(room_to_vertices.keys())[0])
                for v in vertices:
                    result[v] = i
            return result, length

def findsubsets(s):
    subsets = []
    for i in range(1, len(s) + 1):
        subsets.extend(list(itertools.combinations(s, i)))
    return subsets

def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    N = len(G.nodes())

    # another idea: get the best edges for each person, and iterate through some of them to connect together
    for k in range(5, N+1):
        G_copy = copy.deepcopy(G)
        i = 0  # room counter
        solution = {}  # key:value => (vertex, room)
        while True:
            if i == k:
                break
            v = choice(list(G_copy.nodes()))

            # if len(G_copy.nodes()) == 1:
            #     v = list(G_copy.nodes())[0]
            # else:
            #     edges = sorted(G_copy.edges(data=True), key = sortOrder, reverse = True)
            #     v = edges[0][0]

            best_ratios = sorted(G_copy.edges(v, data = True), key = sortOrder, reverse = True)[:5]
            highest_happiness = sorted(G_copy.edges(v, data=True), key=lambda t: t[2].get('happiness'), reverse = True)[:5]
            lowest_stress = sorted(G_copy.edges(v, data=True), key=lambda t: t[2].get('stress'))[:5]

            best_ratios_vertices = set([i[1] for i in best_ratios])
            highest_happiness_vertices = set([i[1] for i in highest_happiness])
            lowest_stress_vertices = set([i[1] for i in lowest_stress])

            vertices = best_ratios_vertices.union(highest_happiness_vertices).union(lowest_stress_vertices)
            subsets = findsubsets(vertices)

            best_merged_room = [v]
            largest_happiness = 0
            for subset in subsets:
                merged_room = [v]
                for vertex in subset:
                    merged_room.append(vertex)
                
                # if it does not satisfy stress constraints, abort
                if calculate_stress_for_room(merged_room, G) > s / k:
                    continue

                happiness = calculate_happiness_for_room(merged_room, G)
                if happiness > largest_happiness:
                    largest_happiness = happiness
                    best_merged_room = merged_room
            
            for v in best_merged_room:
                solution[v] = i
            i += 1
            G_copy.remove_nodes_from(best_merged_room)

            if not G_copy.nodes():
                return solution, i


# Here's an example of how to run your solver.
# Usage: python3 solver.py test.in
# if __name__ == '__main__':
#     # assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G, s = read_input_file(path + ".in")
#     if len(sys.argv) > 2 and sys.argv[2] == "g":
#         D, k = solve_greedy(G, s)
#     else:
#         D, k = solve(G, s)
#     assert is_valid_solution(D, G, s, k)
#     print(D)
#     print(k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'outputs/test.out')

#     D_staff = read_output_file(path+".out", G, s)
#     print("Staff Happiness: {}".format(calculate_happiness(D_staff, G)))


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('inputs/large-*')
    for input_path in inputs:
        output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
        G, s = read_input_file(input_path)
        D, k = solve(G, s)
        assert is_valid_solution(D, G, s, k)
        happiness = calculate_happiness(D, G)
        write_output_file(D, output_path)
        print(input_path)
