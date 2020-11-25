import networkx as nx
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room
import sys


def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """

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
        
        edges = sorted(G.edges(data=True), key=lambda e: e[2].get('happiness') / e[2].get('stress'), reverse = True)
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
            room_num = len(room_to_vertices) - 1   

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


# Here's an example of how to run your solver.
# Usage: python3 solver.py test.in
if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print(D)
    print(k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, 'out/test.out')

    D_staff = read_output_file("20.out", G, s)
    print("Staff Happiness: {}".format(calculate_happiness(D_staff, G)))


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
