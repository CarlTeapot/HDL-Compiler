

def _nand_gate(a: bool, b: bool) -> bool:
    return not (a and b)

def _not_gate(a: bool, b: bool) -> bool:
    return not (a and b)

def _or_gate(a: bool, b: bool) -> bool:
    return a or b

def _and_gate(a: bool, b: bool) -> bool:
    return a and b

def built_in_chip(chip_name: str, a: bool, b: bool) -> bool :
    if chip_name == 'nand':
        return _nand_gate(a,b)
    elif chip_name == 'not':
        return _not_gate(a,b)
    elif chip_name == 'or':
        return _or_gate(a,b)
    elif chip_name == 'and':
        return _and_gate(a,b)

    return False;
