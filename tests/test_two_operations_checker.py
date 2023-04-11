import ast

from mle_flake8_plugins.flake8_mle_convention.two_operation_checker import TwoOperationsChecker
from mle_flake8_plugins.flake8_mle_convention.errors import error_codes

def test_use_two_operations():
    code = """
def test(a, b):
    pass
"""
    tree = ast.parse(code, '')
    visitor = TwoOperationsChecker()
    visitor.visit(tree)
    assert len(visitor.errors) == 0

    code = """
def test(a, b):
    return a + b
"""
    tree = ast.parse(code, '')
    visitor = TwoOperationsChecker()
    visitor.visit(tree)
    assert len(visitor.errors) == 1

    code = """
def test(a, b, c):
    return a + b + c
"""
    tree = ast.parse(code, '')
    visitor = TwoOperationsChecker()
    visitor.visit(tree)
    assert len(visitor.errors) == 0

    code = """
@property
def test(a, b):
    return a + b
"""
    tree = ast.parse(code, '')
    visitor = TwoOperationsChecker()
    visitor.visit(tree)
    assert len(visitor.errors) == 0
