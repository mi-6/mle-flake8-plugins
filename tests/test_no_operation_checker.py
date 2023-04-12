import ast

from mle_flake8_plugins.flake8_mle_convention.no_operation_checker import NoOperationsChecker
from mle_flake8_plugins.flake8_mle_convention.errors import error_codes

def test_use_no_operations():
    code = """
def test(a, b):
    pass
"""
    tree = ast.parse(code, '')
    visitor = NoOperationsChecker()
    visitor.visit(tree)
    assert len(visitor.errors) == 0

    code = """
def test(a, b):
    return a
"""
    tree = ast.parse(code, '')
    visitor = NoOperationsChecker()
    visitor.visit(tree)
    assert len(visitor.errors) == 1

    code = """
def test(a, b):
    return a + b
"""
    tree = ast.parse(code, '')
    visitor = NoOperationsChecker()
    visitor.visit(tree)
    assert len(visitor.errors) == 0
