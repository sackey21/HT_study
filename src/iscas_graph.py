from typing import List
import sys
import pathlib
import re
import networkx as nx  # python3に直インストールしてます
import matplotlib.pyplot as plt
import pandas as pd
from Gate import Gate
from network_centrality.calc_centrality import calc_centrality


# メイン
def main(path):
    data = load_file(path)

    circuit_graph: nx.Graph = create_graph(data)
    circuit_di_graph: nx.DiGraph = create_graph(data, nx.DiGraph())

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

# グラフの作成


def create_graph(data, circuit_graph=nx.Graph()) -> nx.Graph:
    # データ整形
    insts_list = re.sub('//.*\n', '', data).replace('\n', '').split(';')

    # 命令をリストに格納
    # input命令のリスト
    insts_input: List[str] = []
    # output命令のリスト
    insts_output: List[str] = []
    # wire命令のリスト
    insts_wire: List[str] = []
    # ゲート接続命令のリスト
    insts_primitive_gate: List[str] = []

    for inst in insts_list:
        # input
        if 'input ' in inst:
            insts_input.append(inst)
        # output
        elif 'output ' in inst:
            insts_output.append(inst)
        # wire
        elif 'wire ' in inst:
            insts_wire.append(inst)
        # primitive gate
        elif re.compile("and |nand |or |nor |xor |xnor |buf |not ").match(inst):
            insts_primitive_gate.append(inst)

    # 入力信号線抽出
    primary_input_wire: List[str] = []
    for inst in insts_input:
        for input_wire in inst.replace('input ', '').split(','):
            primary_input_wire.append(input_wire)

    # 出力信号線抽出
    primary_output_wire: List[str] = []
    for inst in insts_output:
        for output_wire in inst.replace('output ', '').split(','):
            primary_output_wire.append(output_wire)

    # ゲート関連の命令から必要情報の抽出
    for inst in insts_primitive_gate:

        # 命令部分の取り出し
        gate_def_info = inst.split('(')[0]
        gate_name = gate_def_info.split()[-1]
        gate_type = gate_def_info.split()[0]

        # 入出力指定部分の取り出し
        gate_connect_info = inst.split(
            '(')[-1].replace(')', '').replace(' ', '').split(',')

        output = gate_connect_info.pop(0)
        input = gate_connect_info
        # ゲートの登録
        circuit_graph.add_node(gate_name, type=gate_type,
                               input=input, output=output)

    # 外からの入力線を表すエッジとノードの設定、入力先ゲートと接続
    input_num: int = 0
    for wire in primary_input_wire:
        input_num += 1
        primary_input: str = "input" + str(input_num)
        circuit_graph.add_node(primary_input)
        for input in [i for i, value in dict(
                nx.get_node_attributes(circuit_graph, 'input')).items() if wire in value]:
            circuit_graph.add_edge(primary_input, input, label=wire, weight=1)

    # 外へ出力する信号線を表すエッジとノードの設定、出力元ゲートと接続
    output_num: int = 0
    for wire in primary_output_wire:
        output_num += 1
        primary_output: str = "output" + str(output_num)
        circuit_graph.add_node(primary_output)
        for output in [i for i, value in dict(
                nx.get_node_attributes(circuit_graph, 'output')).items() if wire in value]:
            circuit_graph.add_edge(
                primary_output, output, label=wire, weight=1)

    # ワイヤの抽出
    wires: List[str] = []
    for inst in insts_wire:
        for wire in inst.replace('wire', '').replace(' ', '').split(','):
            wires.append(wire)

    # ワイヤをエッジとして追加
    for wire in wires:
        input_gate: List[str] = [i for i, value in dict(
            nx.get_node_attributes(circuit_graph, 'input')).items() if wire in value]
        output_gate: List[str] = [i for i, value in dict(
            nx.get_node_attributes(circuit_graph, 'output')).items() if wire in value]
        for input in input_gate:
            for output in output_gate:
                circuit_graph.add_edge(input, output, label=wire, weight=1)

    return circuit_graph

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
