import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from tokenizer.hdl_tokenizer import _get_rid_of_comments, _tokenize


class TestHDLTokenizer(unittest.TestCase):
    def test_get_rid_of_comments(self):
        raw_lines = [
            '// This is a comment',
            'IN a, b; // inline comment',
            '/* block comment start',
            'still in comment',
            'end of comment */',
            'OUT out;',
            '',
            'PARTS:',
            'And(a=a, b=b, out=out); // part comment',
        ]
        expected = [
            'IN a, b;',
            'OUT out;',
            'PARTS:',
            'And(a=a, b=b, out=out);'
        ]
        self.assertEqual(_get_rid_of_comments(raw_lines), expected)

    def test_tokenize_success(self):
        name = 'Xor'
        lines = [
            'CHIP Xor {',
            'IN a, b;',
            'OUT out;',
            'PARTS:',
            'Nand(a=a, b=b, out=n1);',
            'And(a=a, b=b, out=n2);',
            'Or(a=n1, b=n2, out=out);',
            '}'
        ]
        ins, outs, parts = _tokenize(name, lines)
        self.assertEqual(ins, ['a', 'b'])
        self.assertEqual(outs, ['out'])
        self.assertEqual(parts, [
            'Nand(a=a, b=b, out=n1);',
            'And(a=a, b=b, out=n2);',
            'Or(a=n1, b=n2, out=out);'
        ])

    def test_tokenize_wrong_chip_name(self):
        name = 'Xor'
        lines = [
            'CHIP NotXor {',
            'IN a, b;',
            'OUT out;',
            'PARTS:',
            'Nand(a=a, b=b, out=n1);',
            '}'
        ]
        with self.assertRaises(ValueError):
            _tokenize(name, lines)

    def test_tokenize_missing_sections(self):
        name = 'Xor'
        lines = [
            'CHIP Xor {',
            'IN a, b;',
            'OUT out;',
            '}'
        ]
        with self.assertRaises(SyntaxError):
            _tokenize(name, lines)

    def test_tokenize_missing_semicolon(self):
        name = 'Xor'
        lines = [
            'CHIP Xor {',
            'IN a, b',  # missing semicolon
            'OUT out;',
            'PARTS:',
            'Nand(a=a, b=b, out=n1);',
            '}'
        ]
        with self.assertRaises(SyntaxError):
            _tokenize(name, lines)


if __name__ == '__main__':
    unittest.main()
