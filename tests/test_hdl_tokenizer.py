import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tokenizer.hdl_tokenizer import get_rid_of_comments, tokenize

def load_hdl_file_direct(file_path: str) -> tuple:
    """Load HDL file directly without user input"""
    if not file_path.endswith('.hdl'):
        raise ValueError("File name must end with .hdl")

    # Extract chip name
    chip_name = file_path[:-4].split('/')[-1]  # Get just the filename without path
    print(f"Chip name detected: {chip_name}")

    # Open file and read lines
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")

    return chip_name, lines

def test_hdl_tokenizer():
    """Test the HDL tokenizer on CPU.hdl file"""
    try:
        # Test with CPU.hdl file
        file_path = "test_files/CPU.hdl"
        print("Testing HDL tokenizer on test_files/CPU.hdl")
        print("=" * 50)
        
        # Load the file
        chip_name, raw_lines = load_hdl_file_direct(file_path)
        print(f"Loaded file: {chip_name}")
        print(f"Number of raw lines: {len(raw_lines)}")
        
        # Remove comments
        clean_lines = get_rid_of_comments(raw_lines)
        print(f"Number of clean lines: {len(clean_lines)}")
        print("Clean lines:")
        for i, line in enumerate(clean_lines):
            print(f"  {i+1}: {line}")
        
        # Tokenize
        ins, outs, parts = tokenize(chip_name, clean_lines)
        
        print("\n" + "=" * 50)
        print("TOKENIZATION RESULTS:")
        print("=" * 50)
        
        print(f"\nINPUT PINS ({len(ins)}):")
        for i, pin in enumerate(ins):
            print(f"  {i+1}: {pin}")
            
        print(f"\nOUTPUT PINS ({len(outs)}):")
        for i, pin in enumerate(outs):
            print(f"  {i+1}: {pin}")
            
        print(f"\nPARTS ({len(parts)}):")
        for i, part in enumerate(parts):
            print(f"  {i+1}: {part}")
            
        print("\n" + "=" * 50)
        print("Tokenization completed successfully!")
        
    except Exception as e:
        print(f"Error during tokenization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_hdl_tokenizer() 