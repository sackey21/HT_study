from typing import List
import sys
import pathlib
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from Gate import Gate
from network_centrality.calc_centrality import calc_centrality
from network.MakeNetwork import MakeNetwork

# メイン


def main(path):
    data = load_file(path)

    circuit_graph: nx.Graph = MakeNetwork.create_graph_GL(data)
    circuit_di_graph: nx.DiGraph = MakeNetwork.create_graph_GL(
        data, nx.DiGraph())

    # アルゴリズム実行
    # minimum_spanning_tree(circuit_graph)
    # dijkstras(circuit_graph, "input5", "output1")

    calc_centrality.calc_group_centrality(circuit_di_graph, circuit_graph)

    draw_network(circuit_graph, './../result/result3')
    draw_network(circuit_di_graph, './../result/result4')


def load_file(path):
    f = open(path, 'r', encoding='UTF-8')
    data = f.read()
    f.close()
    return data


def draw_network(G, output_file: str):
    # グラフ描写部。
    # エッジのラベルを取得
    edge_labels = {edge: G[edge[0]][edge[1]]
                   ["label"] for edge in G.edges()}
    print(edge_labels)

    # ネットワーク図出力
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500,
            node_color="skyblue", font_size=10, font_color="black")
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_color="red")

    plt.savefig(output_file)

# 最少全域木


def minimum_spanning_tree(G):
    print('size of G:', G.size(weight='weight'))
    T = nx.minimum_spanning_tree(G)

    print('size of MST:', T.size(weight='weight'))
    print('spanning edges:')
    for i in sorted(T.edges(data=True)):
        print(i)

# ダイクストラ法


def dijkstras(G, start, goal):
    DG = nx.Graph(G)
    shortest_path = nx.dijkstra_path(DG, start, goal)
    shortest_path_weight = nx.dijkstra_path_length(DG, start, goal)

    print("Shortest Path:", shortest_path)
    print("Weight:", shortest_path_weight)


if __name__ == '__main__':
    args = sys.argv
    main(pathlib.Path(args[1]))
