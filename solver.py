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

    # TODO: your code here!
    vertex_list = list(G.nodes)
    N = len(vertex_list)

    solution_list = []
    happiness_list = []

    # result_k = 0
    k = 1
    while (k < N):
        # Keep track of the best solution 
        # best_happiness_so_far = 0
        solution = {}   # key:value => (vertex, room)
        total_stress_left = 0
        room_to_vertices = {}      # key:value => (room number, vertices)

        # Assume all vertices are on their own 
        for i in range(len(vertex_list)):
            solution[i] = i
            room_to_vertices[i] = [i]
        
        # print(type(G.edges))
        edges = sorted(G.edges(data=True), key=lambda t: t[2].get('happiness', 0)/t[2].get('stress', 1), reverse = True)
        # print(edges)    
        for e in edges: 
            # temp_solution = {} 
            # temp_happiness = 0
            v = e[0]
            u = e[1]
            curr_stress = e[2].get('stress', 0)
            
            # try to make the best choice 
            room_v = solution[e[0]]
            room_u = solution[e[1]]
            if room_u == room_v:
                continue
            
            #attempt merge room
            merged_room = room_to_vertices[room_v] + room_to_vertices[room_u]   
            room_num = len(room_to_vertices) - 1   

            #see if it satisfy stress constraints
            if calculate_stress_for_room(merged_room, G) > s / k:
                continue
            
            # actually merge 
            for v in room_to_vertices[room_u]:
                solution[v] = room_v
            room_to_vertices[room_v] = merged_room
            room_to_vertices.pop(room_u)

            # check to see if we should update 
            # calculate_happiness(solution, G)
        if len(room_to_vertices) <= k:
            result = solution
            break
        # if temp_happines > best_happiness_so_far:
        #     best_solution_so_far = temp_solution

        # if is_valid_solution(solution, G, s, k):
        #     result = solution
        #     result_k = k
        #     break
        k += 1

    return result, k


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
    # write_output_file(D, 'out/test.out')

    # D_staff = read_output_file("samples/10.out", G, s)
    # print("Staff Happiness: {}".format(calculate_happiness(D_staff, G)))


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
