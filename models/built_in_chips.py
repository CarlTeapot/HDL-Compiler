from models.chip import Chip
from models.chip_parameters import ChipParameters

class NandGate(Chip):
    def __init__(self, inputs: dict[str, bool], chips: dict[str, 'ChipParameters']):
        super().__init__("Nand", inputs, chips)
        self.outputs = {"out": False}

    def evaluate(self) -> str:
        self.outputs["out"] = not (self.inputs["a"] and self.inputs["b"])
        return str(self.outputs)

class NotGate(Chip):
    def __init__(self, inputs: dict[str, bool], chips: dict[str, 'ChipParameters']):
        super().__init__("Not", inputs, chips)
        self.outputs = {"out": False}

    def evaluate(self) -> str:
        self.outputs["out"] = not self.inputs["in"]
        return str(self.outputs)

class OrGate(Chip):
    def __init__(self, inputs: dict[str, bool], chips: dict[str, 'ChipParameters']):
        super().__init__("Or", inputs, chips)
        self.outputs = {"out": False}

    def evaluate(self) -> str:
        self.outputs["out"] = self.inputs["a"] or self.inputs["b"]
        return str(self.outputs)

class AndGate(Chip):
    def __init__(self, inputs: dict[str, bool], chips: dict[str, 'ChipParameters']):
        super().__init__("And", inputs, chips)
        self.outputs = {"out": False}

    def evaluate(self) -> str:
        self.outputs["out"] = self.inputs["a"] and self.inputs["b"]
        return str(self.outputs)
