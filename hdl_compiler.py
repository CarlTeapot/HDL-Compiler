import argparse
import os
from tester import run_all_tests, run_test_from_file
from hdl_parser import HDLParser

def main():
    parser = argparse.ArgumentParser(description="HDL Chip Tester")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--dir",
        type=str,
        help="Directory containing test vector (.cmp or .csv) files"
    )

    group.add_argument(
        "--file",
        type=str,
        help="Path to a single .cmp or .csv test file"
    )

    args = parser.parse_args()

    if args.file:
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            return

        print(f"🔍 Running test: {args.file}")

        file_dir = os.path.dirname(args.file) or "."
        hdl_parser = HDLParser(file_dir)
        run_test_from_file(args.file, hdl_parser)

    elif args.dir:
        if not os.path.isdir(args.dir):
            print(f"❌ Directory not found: {args.dir}")
            return
        hdl_parser = HDLParser(args.dir)
        run_all_tests(hdl_parser, args.dir)

if __name__ == '__main__':
    main()
