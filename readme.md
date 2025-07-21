# 🧠 HDL Emulator

This is a Python-based HDL (Hardware Description Language) **emulator and test runner** for simulating combinational logic chips described using the Hack platform's `.hdl` files. It supports automated testing using `.cmp` and `.csv` files.

---

## 📁 Project Structure
├── data -> Contains .hdl chip definitions and .cmp/.csv test files

├── hdl_parser.py -> Main HDL parsing and chip emulation logic

├── tester.py -> Testing logic for .cmp and .csv test files

├── hdl_compiler.py -> Command-line interface for running tests



---

## ✅ Features

- Parses `.hdl` chip files with Hack HDL syntax
- Emulates **combinational** logic chips
- Supports two test formats:
  - `.cmp` (Hack style, `|` delimited)
  - `.csv` (semicolon `;` delimited input/output)
- Clear and verbose output for test results

---

## 🧪 Running Tests

Example code: 
 
 To test the entire directory:
    
    python hdl_compiler.py --dir {directory-path} 

 To test a single file:
    
    python hdl_compiler.py --file {file-path.cmp/csv}

 To test the hdl file, all the other .hdl files for the chips that it uses must be in the same folder
 

