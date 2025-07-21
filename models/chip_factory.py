from models.chip_parameters import ChipParameters
from models.built_in_chips import *


class ChipFactory:
    def __init__(self, name: str, inputs: dict[str, bool], chips: dict[str, 'ChipParameters']):
        self.built_ins = {"Not", 'Or', 'And', "Nand"}
        self.name = name
        self.inputs = inputs
        self.chips = chips

        chip_params = chips[name]
        self.outputs = {name: False for name in chip_params.outputs}
        self.parts = chip_params.parts

        self.intermediaryBits: dict[str, bool] = {}

    def create(self) -> Chip:
        if self.name == 'Not':
            return NotGate(self.inputs, self.chips)
        if self.name == 'Or':
            return OrGate(self.inputs, self.chips)
        if self.name == 'And':
            return AndGate(self.inputs, self.chips)
        if self.name == 'Nand':
            return NandGate(self.inputs, self.chips)
        else:
            return Chip(self.name, self.inputs, self.chips)
