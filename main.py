from tester import run_all_tests
from hdl_parser import HDLParser


def print_hi(name):
    print(f'Hi, {name}')

if __name__ == '__main__':
    hdl_parser = HDLParser('./data')
    run_all_tests(hdl_parser, './data')
