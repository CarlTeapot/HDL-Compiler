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

        remaining_parts = self.parts.copy()
        evaluated_parts = set()

        while remaining_parts:
            progress_made = False
            for part in remaining_parts[:]:
                chip_params = self.chips[part.name]

                sub_inputs = {}
                inputs_ready = True

                for pin in chip_params.inputs:
                    wire = part.connections[pin]
                    if wire in self.inputs:
                        sub_inputs[pin] = self.inputs[wire]
                    elif wire in self.intermediaryBits:
                        sub_inputs[pin] = self.intermediaryBits[wire]
                    else:
                        inputs_ready = False
                        break

                if not inputs_ready:
                    continue

                chip_factory = ChipFactory(part.name, sub_inputs, self.chips)
                sub_chip = chip_factory.create()
                sub_chip.evaluate()

                for pin, value in sub_chip.outputs.items():
                    wire = part.connections[pin]
                    if wire in self.outputs:
                        self.outputs[wire] = value
                    else:
                        self.intermediaryBits[wire] = value

                remaining_parts.remove(part)
                progress_made = True
                evaluated_parts.add(part)

            if not progress_made:
                raise RuntimeError("Unable to resolve all parts; possible combinational loop or missing wire.")

        return str(self.outputs)

