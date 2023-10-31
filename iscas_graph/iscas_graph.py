from typing import List
import sys
import pathlib
import re
import networkx as nx  # 直置きpython3に直インストールしてます
import matplotlib.pyplot as plt

from Gate import Gate


def main(path):
    f = open(path, 'r', encoding='UTF-8')
    data = f.read()

    f.close()

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

    circuit_graph = nx.Graph()

    # 命令から必要情報の抽出
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

    print(circuit_graph.nodes)

    # ワイヤの抽出
    wires: List[str] = []
    for inst in insts_wire:
        for wire in inst.replace('wire', '').replace(' ', '').split(','):
            wires.append(wire)

    # print(wires)

    # エッジ追加
    for wire in wires:
        print(wire)
        input_gate: List[str] = [i for i, value in dict(
            nx.get_node_attributes(circuit_graph, 'input')).items() if wire in value]
        output_gate: List[str] = [i for i, value in dict(
            nx.get_node_attributes(circuit_graph, 'output')).items() if wire in value]
        for input in input_gate:
            for output in output_gate:
                circuit_graph.add_edge(input, output, label=wire)

    # エッジのラベルを取得
    edge_labels = {edge: circuit_graph[edge[0]][edge[1]]
                   ["label"] for edge in circuit_graph.edges()}
    print(edge_labels)

    # ネットワーク図出力# ネットワーク図の描画
    pos = nx.spring_layout(circuit_graph)
    nx.draw(circuit_graph, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_color="black")
    nx.draw_networkx_edge_labels(circuit_graph, pos, edge_labels=edge_labels, font_color="red")

    plt.savefig('test')


if __name__ == '__main__':
    args = sys.argv
    main(pathlib.Path(args[1]))
