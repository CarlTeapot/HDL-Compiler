from tester import run_test_from_file
from hdl_parser import HDLParser


def print_hi(name):
    print(f'Hi, {name}')

if __name__ == '__main__':
    hdl_parser = HDLParser()
    run_test_from_file("Xor.cmp", hdl_parser)

