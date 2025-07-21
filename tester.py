from hdl_parser import HDLParser

import os


def run_test_from_file(filename: str, hdl_parser) -> None:
    filepath = os.path.join("data", filename)
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    chip_name = os.path.splitext(filename)[0]
    if filename.endswith(".csv") or ";" in lines[0]:
        _run_csv_test(chip_name, lines, hdl_parser)
    elif "|" in lines[0]:
        _run_cmp_test(chip_name, lines, hdl_parser)
    else:
        print("❌ Unknown format. File must be .csv or contain | or ; to indicate format.")


def _run_csv_test(chip_name: str, csv_lines: list[str], hdl_parser: HDLParser) -> None:
    header = csv_lines[0].strip()
    input_part, output_part = header.split(";")
    input_names = [name.strip() for name in input_part.split(",")]
    output_names = [name.strip() for name in output_part.split(",")]

    for i, line in enumerate(csv_lines[1:], start=1):
        if not line.strip():
            continue

        input_part, output_part = line.strip().split(";")
        input_values = [bool(int(x)) for x in input_part.strip().split(",")]
        output_values = [bool(int(x)) for x in output_part.strip().split(",")]

        input_dict = dict(zip(input_names, input_values))
        expected_output_dict = dict(zip(output_names, output_values))

        chip = hdl_parser.create_chip(chip_name, input_dict)
        chip.evaluate()

        if chip.outputs != expected_output_dict:
            print(f"❌ Test failed on line {i}:")
            print(f"   Inputs: {input_dict}")
            print(f"   Expected: {expected_output_dict}")
            print(f"   Got:      {chip.outputs}")
        else:
            print(f"✅ Test passed on line {i}")


def _run_cmp_test(chip_name: str, table_lines: list[str], hdl_parser: HDLParser) -> None:
    headers = [col.strip() for col in table_lines[0].strip("|").split("|")]
    data_lines = table_lines[1:]

    input_names = [name for name in headers if name != "out"]
    output_names = ["out"]

    for i, line in enumerate(data_lines, start=1):
        if not line.strip():
            continue  # Skip empty lines

        columns = [col.strip() for col in line.strip("|").split("|")]
        values = [bool(int(v)) for v in columns]

        input_values = values[:-1]
        output_values = values[-1:]

        input_dict = dict(zip(input_names, input_values))
        expected_output_dict = dict(zip(output_names, output_values))

        chip = hdl_parser.create_chip(chip_name, input_dict)
        chip.evaluate()

        if chip.outputs != expected_output_dict:
            print(f"❌ Test failed on line {i}:")
            print(f"   Inputs: {input_dict}")
            print(f"   Expected: {expected_output_dict}")
            print(f"   Got:      {chip.outputs}")
        else:
            print(f"✅ Test passed on line {i}")
