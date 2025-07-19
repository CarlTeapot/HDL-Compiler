#!/usr/bin/env python3
"""
Test runner for HDL-Parser
"""

import os
import sys
import importlib.util

def run_test(test_file):
    """Run a specific test file"""
    print(f"Running {test_file}...")
    print("=" * 60)
    
    try:
        # Import and run the test module
        test_path = os.path.join(os.path.dirname(__file__), test_file)
        spec = importlib.util.spec_from_file_location("test_module", test_path)
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)
        
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)
    print()

def main():
    """Run all tests"""
    print("HDL-Parser Test Suite")
    print("=" * 60)
    
    # Get all test files
    test_dir = os.path.dirname(__file__)
    test_files = [f for f in os.listdir(test_dir) 
                  if f.startswith('test_') and f.endswith('.py') and f != 'run_tests.py']
    
    if not test_files:
        print("No test files found!")
        return
    
    print(f"Found {len(test_files)} test(s):")
    for test_file in test_files:
        print(f"  - {test_file}")
    print()
    
    # Run each test
    for test_file in test_files:
        run_test(test_file)
    
    print("Test suite completed!")

if __name__ == '__main__':
    main() 