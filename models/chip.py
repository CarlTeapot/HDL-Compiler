class Chip:
    def __init__(self, inputs: list[str], outputs: list[str], parts: dict[str, 'Chip']):
        self.inputs = {name: False for name in inputs}
        self.outputs = {name: False for name in outputs}
        self.parts = parts  # dict: part name -> Chip instance

    def set_input(self, name: str, value: bool):
        if name not in self.inputs:
            raise KeyError(f"Input '{name}' not found in chip inputs.")
        self.inputs[name] = value

    def get_output(self, name: str) -> bool:
        if name not in self.outputs:
            raise KeyError(f"Output '{name}' not found in chip outputs.")
        return self.outputs[name]

    def __str__(self):
        parts_str = ', '.join(self.parts.keys())
        return (
            f"Chip(\n"
            f"  Inputs: {self.inputs}\n"
            f"  Outputs: {self.outputs}\n"
            f"  Parts: {parts_str}\n"
            f")"
        )
