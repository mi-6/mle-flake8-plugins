import ast

from mle_flake8_plugins.flake8_mle_convention.type_hint_checker import TypeHintChecker
from mle_flake8_plugins.flake8_mle_convention.errors import error_codes

def test_use_legacy_type_hint():
    code = """
from typing import List, Dict, Tuple

def test(a: List[int], b: Dict[str, int], c: Tuple[int, str]):
    pass
"""
    tree = ast.parse(code, '')
    visitor = TypeHintChecker()
    visitor.visit(tree)
    assert len(visitor.errors) == 3
    assert visitor.errors[0][2] == error_codes["type_hint"] % ("list", "List")
    assert visitor.errors[1][2] == error_codes["type_hint"] % ("dict", "Dict")
    assert visitor.errors[2][2] == error_codes["type_hint"] % ("tuple", "Tuple")
