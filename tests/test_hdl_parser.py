import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import random
from hdl_parser import HDLParser
from tester import run_test_from_file

def shuffle_chip_order(hdl_path):
    with open(hdl_path, 'r') as f:
        lines = f.readlines()

    # Find CHIP header and footer
    chip_start = None
    chip_end = None
    for i, line in enumerate(lines):
        if line.strip().startswith('CHIP'):
            chip_start = i
        if line.strip() == '}':
            chip_end = i
            break
    if chip_start is None or chip_end is None:
        return

    # Find PARTS section
    parts_start = None
    for i in range(chip_start, chip_end):
        if 'PARTS:' in lines[i]:
            parts_start = i
            break
    if parts_start is None:
        return  # No PARTS section

    # Extract and shuffle parts
    part_lines = []
    for i in range(parts_start+1, chip_end):
        if lines[i].strip() == '':
            continue
        part_lines.append(lines[i])
    random.shuffle(part_lines)

    # Reconstruct file
    new_lines = lines[:parts_start+1] + part_lines + lines[chip_end:]
    shuffled_path = hdl_path.replace('.hdl', '_shuffled.hdl')
    with open(shuffled_path, 'w') as f:
        f.writelines(new_lines)
    return shuffled_path

def test_all():
    test_dir = os.path.dirname(__file__)
    hdl_files = [f for f in os.listdir(test_dir) if f.endswith('.hdl')]
    parser = HDLParser("./tests")
    for hdl_file in hdl_files:
        chip_name = os.path.splitext(hdl_file)[0]
        cmp_file = chip_name + '.cmp'
        hdl_path = os.path.join(test_dir, hdl_file)
        cmp_path = os.path.join(test_dir, cmp_file)
        if not os.path.exists(cmp_path):
            print(f"No .cmp file for {hdl_file}, skipping.")
            continue
        print(f"\n=== Testing {hdl_file} with {cmp_file} ===")
        run_test_from_file(cmp_path, parser)
        # Test with shuffled chip order
        shuffled_hdl = shuffle_chip_order(hdl_path)
        if shuffled_hdl:
            print(f"\n=== Testing {os.path.basename(shuffled_hdl)} with {cmp_file} (shuffled order) ===")
            run_test_from_file(cmp_path, parser)
            os.remove(shuffled_hdl)

if __name__ == '__main__':
    test_all() 