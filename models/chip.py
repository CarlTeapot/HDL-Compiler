from models.chip_parameters import ChipParameters


class Chip:
    def __init__(self, name: str, inputs: dict[str, bool], chips: dict[str, 'ChipParameters']):
        self.name = name
        self.inputs = inputs
        self.chips = chips

        chip_params = chips[name]
        self.outputs = {name: False for name in chip_params.outputs}
        self.parts = chip_params.parts

        self.intermediaryBits: dict[str, bool] = {}

    def reset(self):
        self.inputs = {name: False for name in self.inputs}
        self.outputs = {name: False for name in self.outputs}
        self.intermediaryBits = {}

    def evaluate(self) -> str:
        from models.chip_factory import ChipFactory

        for part in self.parts:
            chip_params = self.chips[part.name]

            sub_inputs = {}
            for pin in chip_params.inputs:
                wire = part.connections[pin]
                if wire in self.inputs:
                    sub_inputs[pin] = self.inputs[wire]
                else:
                    sub_inputs[pin] = self.intermediaryBits.get(wire, False)

            chip_factory = ChipFactory(part.name, sub_inputs, self.chips)
            sub_chip = chip_factory.create()
            sub_chip.evaluate()

            for pin, value in sub_chip.outputs.items():
                wire = part.connections[pin]
                if wire in self.outputs:
                    self.outputs[wire] = value
                else:
                    self.intermediaryBits[wire] = value

        return str(self.outputs)
