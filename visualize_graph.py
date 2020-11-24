import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(G):
    plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
G = nx.petersen_graph()