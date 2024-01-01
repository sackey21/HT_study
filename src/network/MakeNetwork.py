import re
import networkx as nx  # python3に直インストールしてます
import sys
import pathlib
from typing import List


class MakeNetwork:
    def create_graph_GL(data, circuit_graph=nx.Graph()) -> nx.Graph:
        """
        ゲートレベル記述に対応してる回路生成プログラム
        """
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
                circuit_graph.add_edge(
                    primary_input, input, label=wire, weight=1)

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

    def create_graph_RTL(data, circuit_di_graph=nx.Graph()) -> nx.Graph:
        """
        RTLレべル記述に対応してる回路生成プログラム
        """
        # データの整形
        # 各行のデータを区切る
        # always文どうしようかな
        insts_list = re.sub('//.*\n', '', data).replace('\n', '')
        insts_list = re.split('(?<=;)',insts_list)
        # print(insts_list)
        # 各命令に対して細かく調整

        insts_input: List[str] = []
        insts_output: List[str] = []
        insts_reg: List[str] = []
        insts_wire: List[str] = []
        insts_parameter: List[str] = []
        insts_assign: List[str] = []
        insts_function: List[str] = []
        insts_always: List[str] = []
        insts_module: List[str] = []
        insts_under_module: List[str] = []
        for i in insts_list:
            # always文の配列化
            if 'always' in i:
                insts_always.append(i)
                # endのところ辺りまでの判定をどうにかしたい
                # ;がないのがダルすぎる
                continue
            # input命令の配列化
            if 'input' in i:
                if '`include' in i:
                    i = re.split("(?=input)", i)[1]
                insts_input.append(i)
                continue
            # output命令の配列化
            if 'output' in i:
                insts_output.append(i)
                continue
            # reg命令の配列化
            if 'reg' in i:
                insts_reg.append(i)
                continue
            # wire命令の配列化
            if 'wire' in i:
                insts_wire.append(i)
                continue
            if 'parameter' in i:
                insts_parameter.append(i)
                continue
            # module宣言を配列化する
            if 'module' in i:
                if '`' in i:
                    i = re.split("(?=module)", i)[1]
                insts_module.append(i)
                continue
            # aassignの配列化
            if 'assign' in i:
                insts_assign.append(i)
                continue
            # function文の配列化
            if 'always' in i:
                insts_function.append(i)
                continue

            if (re.findall('[a-zA-Z_]+ *[a-zA-Z_]+ *\( *', i) and re.findall('\.[a-zA-Z_]+\([a-zA-Z_]+\),?', i) and re.findall('\);', i)):
                insts_under_module.append(i)
        
        # input命令の配列化
        # inputをエッジに設定
        
        # outputを配列化
        # outputをエッジに設定
        
        # wireを配列化
        # wireをエッジに設定
        
        # regを配列化
        # regをエッジに設定
        
        # 下位モジュールをノード化
        # inputとかoutputをどうするか決める

if __name__ == '__main__':
    args = sys.argv
    f = open(args[1], 'r', encoding='UTF-8')
    data = f.read()
    f.close()
    MakeNetwork.create_graph_RTL(data)
