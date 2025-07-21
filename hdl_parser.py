import os

from models.chip import Chip
from models.chip_parameters import ChipParameters
from tokenizer.hdl_tokenizer import create_chip


class HDLParser:

    def __init__(self, directory_name: str):
        self.directory_name = directory_name
        self.chips: dict[str, ChipParameters] = {
            "Nand": ChipParameters(
                inputs=["a", "b"],
                outputs=["out"],
                parts=[]
            ),
            "Not": ChipParameters(
                inputs=["in"],
                outputs=["out"],
                parts=[]
            ),
            "Or": ChipParameters(
                inputs=["a", "b"],
                outputs=["out"],
                parts=[]
            ),
            "And": ChipParameters(
                inputs=["a", "b"],
                outputs=["out"],
                parts=[]
            ),
        }

    def create_chip(self, chip_name: str, variables: dict[str, bool]) -> Chip:
        return create_chip(chip_name, variables, self.chips, self.directory_name)
