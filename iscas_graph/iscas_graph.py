from typing import List
import sys
import pathlib
import re

from Gate import Gate

def main(path):
    f = open(path, 'r', encoding='UTF-8')
    data = f.read()

    f.close()

    # データ整形
    inst_list = re.sub('//.*\n', '', data).replace('\n', '').split(';')

    # 命令をリストに格納
    # input命令のリスト
    inst_input: List[str] = []
    # output命令のリスト
    inst_output: List[str] = []
    # wire命令のリスト
    inst_wire: List[str] = []
    # ゲート接続命令のリスト
    inst_primitive_gate: List[str] = []

    for inst in inst_list:
        # input
        if 'input ' in inst:
            inst_input.append(inst)
        # output
        elif 'output ' in inst:
            inst_output.append(inst)
        # wire
        elif 'wire ' in inst:
            inst_wire.append(inst)
        # primitive gate
        elif re.compile("and |nand |or |nor |xor |xnor |buf |not ").match(inst):
            inst_primitive_gate.append(inst)
    
    circuit_gates : List[Gate()] = []

    # 命令から必要情報の抽出
    for inst in inst_primitive_gate:
        
        # 命令部分の取り出し
        gate_def_info = inst.split('(')[0]
  
        gate_name = gate_def_info.split()[-1]
        gate_type = gate_def_info.split()[0]
              
        # 入出力指定部分の取り出し
        gate_connect_info = inst.split('(')[-1].replace(')', '').replace(' ', '').split(',')
        
        output = gate_connect_info.pop(0)
        input = gate_connect_info
        
        # ゲートの登録
        circuit_gates.append(Gate(gate_name, gate_type, output, input))
    
    for a in circuit_gates:
        print(vars(a))
        

    # グラフ作成
    # circuit_graph = nx.Graph()
    


if __name__ == '__main__':
    args = sys.argv
    main(pathlib.Path(args[1]))
