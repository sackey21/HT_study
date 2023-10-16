import sys
import pathlib
import re
import networkx as nx


def main(path):
    f = open(path, 'r', encoding='UTF-8')
    data = f.read()

    f.close()

    # データ整形
    inst_list = re.sub('//.*\n', '', data).replace('\n', '').split(';')

    # 命令をリストに格納
    # input命令のリスト
    inst_input = []
    # output命令のリスト
    inst_output = []
    # wire命令のリスト
    inst_wire = []
    # ゲート接続命令のリスト
    inst_primitive_gate = []

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

    # print(inst_input)
    # print(inst_output)
    # print(inst_wire)
    # print(inst_primitive_gate)

if __name__ == '__main__':
    args = sys.argv
    main(pathlib.Path(args[1]))
