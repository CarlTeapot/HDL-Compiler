from hdl_parser import HDLParser
import os


def run_all_tests(hdl_parser: HDLParser, directory_path: str):
    test_files = [f for f in os.listdir(directory_path) if f.endswith(".cmp") or f.endswith(".csv")]

    if not test_files:
        print("⚠️ No .cmp or .csv files found in the data directory.")
        return

    for test_file in test_files:
        file_path = os.path.join(directory_path, test_file)
        print(f"\n🔍 Running test: {test_file}")
        run_test_from_file(file_path, hdl_parser)


def run_test_from_file(filepath: str, hdl_parser) -> None:
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    filename = os.path.basename(filepath)
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

        try:
            input_part, output_part = line.strip().split(";")
            input_values = [bool(int(x)) for x in input_part.strip().split(",")]
            output_values = [bool(int(x)) for x in output_part.strip().split(",")]

            input_dict = dict(zip(input_names, input_values))
            raw_expected_output = dict(zip(output_names, output_values))

            chip = hdl_parser.create_chip(chip_name, input_dict)
            chip.evaluate()

            expected_output_dict = {
                k: v for k, v in raw_expected_output.items()
                if k in chip.outputs
            }

            if chip.outputs != expected_output_dict:
                print(f"❌ Test failed on line {i}:")
                print(f"   Inputs:   {input_dict}")
                print(f"   Expected: {expected_output_dict}")
                print(f"   Got:      {chip.outputs}")
            else:
                print(f"✅ Test passed on line {i}")
        except Exception as e:
            print(f"❌ Error parsing line {i}: {line}")
            print(f"   Error: {e}")


def _run_cmp_test(chip_name: str, table_lines: list[str], hdl_parser: HDLParser) -> None:
    headers = [col.strip() for col in table_lines[0].strip("|").split("|")]
    data_lines = table_lines[1:]

    for i, line in enumerate(data_lines, start=1):
        if not line.strip():
            continue

        columns = [col.strip() for col in line.strip("|").split("|")]
        input_values = [bool(int(v)) for v in columns]

        variable_dict = dict(zip(headers, input_values))

        chip = hdl_parser.create_chip(chip_name, variable_dict)
        chip.evaluate()

        expected_output_dict = {k: v for k, v in variable_dict.items() if k in chip.outputs.keys()}

        if chip.outputs != expected_output_dict:
            print(f"❌ Test failed on line {i}:")
            print(f"   Inputs: {chip.name}")
            print(f"   Expected: {expected_output_dict}")
            print(f"   Got:      {chip.outputs}")
        else:
            print(f"✅ Test passed on line {i}")
