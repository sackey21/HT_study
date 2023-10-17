from typing import List

# 各ゲートのゲート、入出力等の情報を管理するクラス


class Gate:
    _name: str = None
    _type: str = None
    _input: List[str] = []
    _output: str = None

    def __init__(self, name: str, type: str, output: str, input: List[str]):
        self._name = name
        self._type = type
        self._output = output
        self._input = input

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def input(self):
        return self._input

    @property
    def output(self):
        return self._output

    # and_gates = []
    # nand_gates = []
    # or_gates = []
    # nor_gates = []
    # xor_gates = []
    # xnor_gates = []
    # buf_gates = []
    # not_gates = []
