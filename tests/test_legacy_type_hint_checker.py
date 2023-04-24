import ast

from mle_flake8_plugins.flake8_mle_convention.errors import error_codes
from mle_flake8_plugins.flake8_mle_convention.legacy_type_hint_checker import (
    LegacyTypeHintChecker,
)


def test_use_legacy_type_hint():
    code = """
from typing import List, Dict, Tuple

def test(a: List[int], b: Dict[str, int], c: Tuple[int, str]):
    pass
"""
    tree = ast.parse(code, "")
    visitor = LegacyTypeHintChecker()
    visitor.visit(tree)
    assert len(visitor.errors) == 3
    assert visitor.errors[0][2] == error_codes["legacy_type_hint"] % ("list", "List")
    assert visitor.errors[1][2] == error_codes["legacy_type_hint"] % ("dict", "Dict")
    assert visitor.errors[2][2] == error_codes["legacy_type_hint"] % ("tuple", "Tuple")
