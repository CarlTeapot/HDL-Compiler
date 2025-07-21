from tester import  run_all_cmp_tests
from hdl_parser import HDLParser


def print_hi(name):
    print(f'Hi, {name}')

if __name__ == '__main__':
    hdl_parser = HDLParser()
    run_all_cmp_tests(hdl_parser)
