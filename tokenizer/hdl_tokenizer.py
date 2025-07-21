from models.chip import Chip
from models.chip_parameters import ChipParameters
from models.part import Part

import os


def _load_hdl_file(full_file_name: str) -> tuple:
    if not full_file_name.endswith('.hdl'):
        raise ValueError("File name must end with .hdl")

    chip_name = full_file_name[:-4]
    print(f"Chip name detected: {chip_name}")

    filepath = os.path.join("data", full_file_name)

    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filepath}' not found.")

    return chip_name, lines


def _get_rid_of_comments(raw_lines: list) -> list:
    lines = []
    inside_block_comment = False

    for line in raw_lines:
        stripped = line.strip()
        if not stripped:
            continue

        if inside_block_comment:
            if '*/' in stripped:
                inside_block_comment = False
            continue

        if '/*' in stripped:
            start = stripped.find('/*')
            end = stripped.find('*/', start + 2)

            if end != -1:
                stripped = stripped[:start].strip()
            else:
                inside_block_comment = True
                stripped = stripped[:start].strip()

        if '//' in stripped:
            stripped = stripped.split('//')[0].strip()

        if not stripped:
            continue

        lines.append(stripped)

    return lines


def _tokenize(name: str, lines: list) -> tuple[list[str], list[str], list[str]]:
    if not lines or not lines[0].startswith("CHIP") or not lines[0].endswith('{'):
        raise SyntaxError("HDL file must start with 'CHIP ChipName {'")

    chip_name_in_file = lines[0].split()[1]
    if chip_name_in_file != name:
        raise ValueError(f"Chip name '{chip_name_in_file}' does not match file name '{name}'")

    if lines[-1] != '}':
        raise SyntaxError("HDL file must end with '}'")

    content = " ".join(lines[1:-1])

    try:
        in_start_idx = content.index("IN")
        out_start_idx = content.index("OUT")
        parts_start_idx = content.index("PARTS:")
    except ValueError:
        raise SyntaxError("A valid HDL file must contain IN, OUT, and PARTS sections.")

    in_section_str = content[in_start_idx + 2: out_start_idx].strip()
    out_section_str = content[out_start_idx + 3: parts_start_idx].strip()
    parts_section_str = content[parts_start_idx + len("PARTS:"):].strip()

    if not in_section_str.endswith(';') or not out_section_str.endswith(';'):
        raise SyntaxError("IN and OUT sections must end with a semicolon ';'")

    ins = [pin.strip() for pin in in_section_str[:-1].split(',')]
    outs = [pin.strip() for pin in out_section_str[:-1].split(',')]

    parts = [part.strip() + ';' for part in parts_section_str.split(';') if part.strip()]

    return ins, outs, parts


def _checkExistenceOfChips(directory_name: str, parts: list[str], chips: dict[str, 'ChipParameters']) -> bool:
    for part in parts:
        chip_name = part.split('(')[0].strip()
        chip_file_name = chip_name + ".hdl"
        full_path = os.path.join(directory_name, chip_file_name)
        if chip_name not in chips and not os.path.exists(full_path):
            raise ValueError(f"{chip_file_name} not found in directory '{directory_name}'")
    return True


def _tokenize_hdl(file_name: str, chips: dict[str, 'ChipParameters']):
    chip_name, lines = _load_hdl_file(file_name)
    lines = _get_rid_of_comments(lines)
    ins, outs, parts = _tokenize(chip_name, lines)

    directory = "data"

    if not _checkExistenceOfChips(directory, parts, chips):
        raise ValueError("Some chips used in PARTS are missing in the directory or built-ins.")

    for part in parts:
        sub_chip_name = part.split('(')[0].strip()
        if sub_chip_name not in chips:
            sub_file = os.path.join(directory, sub_chip_name + ".hdl")
            sub_ins, sub_outs, sub_parts_strs = _tokenize_hdl(sub_chip_name + ".hdl", chips)
            sub_parts = parse_parts(sub_parts_strs)
            chips[sub_chip_name] = ChipParameters(inputs=sub_ins, outputs=sub_outs, parts=sub_parts)
    return ins, outs, parts


def parse_parts(parts: list[str]) -> list['Part']:
    result = []
    for part in parts:
        name = part.split('(')[0].strip()
        conn_str = part.split('(')[1].split(')')[0]

        assignments = conn_str.split(',')
        connections = {}
        for assignment in assignments:
            if '=' in assignment:
                pin, wire = assignment.strip().split('=')
                connections[pin.strip()] = wire.strip()

        result.append(Part(name=name, connections=connections))

    return result


def create_chip(chip_name: str, inputs: dict[str, bool], chips: dict[str, 'ChipParameters']) -> Chip:
    if chip_name not in chips.keys():
        ins, outs, parts_strs = _tokenize_hdl(chip_name + ".hdl", chips)
        parts = parse_parts(parts_strs)
        chips[chip_name] = ChipParameters(inputs=ins, outputs=outs, parts=parts)

    return Chip(name=chip_name, inputs=inputs, chips=chips)
