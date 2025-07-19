def load_hdl_file() -> tuple:
    full_file_name = input('Enter file name: ').strip()

    if not full_file_name.endswith('.hdl'):
        raise ValueError("File name must end with .hdl")

    chip_name = full_file_name[:-4]
    print(f"Chip name detected: {chip_name}")

    try:
        with open(full_file_name, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{full_file_name}' not found.")

    return chip_name, lines


def get_rid_of_comments(raw_lines: list) -> list:
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


def tokenize(name: str, lines: list) -> tuple[list[str], list[str], list[str]]:
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

    in_section_str = content[in_start_idx + 2 : out_start_idx].strip()
    out_section_str = content[out_start_idx + 3 : parts_start_idx].strip()
    parts_section_str = content[parts_start_idx + len("PARTS:"):].strip()

    if not in_section_str.endswith(';') or not out_section_str.endswith(';'):
        raise SyntaxError("IN and OUT sections must end with a semicolon ';'")

    ins = [pin.strip() for pin in in_section_str[:-1].split(',')]
    outs = [pin.strip() for pin in out_section_str[:-1].split(',')]

    parts = [part.strip() + ';' for part in parts_section_str.split(';') if part.strip()]

    return ins, outs, parts
