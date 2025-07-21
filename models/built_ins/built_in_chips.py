from models.chip import Chip


class NandGate(Chip):
    def __init__(self, inputs: dict[str, bool]):
        super().__init__("NAND", inputs, chips={})
        self.outputs = {"out": False}

    def evaluate(self) -> str:
        self.outputs["out"] = not (self.inputs["a"] and self.inputs["b"])
        return str(self.outputs)

class NotGate(Chip):
    def __init__(self, inputs: dict[str, bool]):
        super().__init__("NOT", inputs, chips={})
        self.outputs = {"out": False}

    def evaluate(self) -> str:
        self.outputs["out"] = not self.inputs["in"]
        return str(self.outputs)

class OrGate(Chip):
    def __init__(self, inputs: dict[str, bool]):
        super().__init__("OR", inputs, chips={})
        self.outputs = {"out": False}

    def evaluate(self) -> str:
        self.outputs["out"] = self.inputs["a"] or self.inputs["b"]
        return str(self.outputs)

class AndGate(Chip):
    def __init__(self, inputs: dict[str, bool]):
        super().__init__("AND", inputs, chips={})
        self.outputs = {"out": False}

    def evaluate(self) -> str:
        self.outputs["out"] = self.inputs["a"] and self.inputs["b"]
        return str(self.outputs)
