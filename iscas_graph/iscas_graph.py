import sys
import pathlib
import re


def main(path):
    f = open(path, 'r', encoding='UTF-8')
    data = f.read()

    f.close()

    # データ整形
    inst_list = re.sub('//.*\n', '', data).replace('\n', '').split(';')

    # input宣言命令のリスト
    inst_input = []
    # output宣言命令のリスト
    inst_output = []
    # wire宣言命令のリスト
    inst_wire = []
    # ゲート宣言命令のリスト
    inst_gate = []

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
        else:
        

if __name__ == '__main__':
    args = sys.argv
    main(pathlib.Path(args[1]))
