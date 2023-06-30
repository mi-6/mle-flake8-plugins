import ast

from mle_flake8_plugins.flake8_mle_docstring.attribute_checker import \
    AttributeChecker
from mle_flake8_plugins.flake8_mle_docstring.errors import error_codes


def test_no_attribute_docs():
    code = """
from dataclasses import dataclass

@dataclass
class Test:
    a: int = 10

    def __init__(self):
        self.b = 1
"""
    tree = ast.parse(code, "")
    visitor = AttributeChecker()
    visitor.visit(tree)
    assert len(visitor.errors) == 2
    assert visitor.errors[0][2] == error_codes["attribute"] % "a"
    assert visitor.errors[1][2] == error_codes["attribute"] % "b"


def test_provided_attribute_docs():
    code = """
from dataclasses import dataclass

@dataclass
class Test:
    '''Test

    Attributes:
      a: hoge
      b: fuga
    '''
    a: int = 10

    def __init__(self):
        self.b = 1
"""
    tree = ast.parse(code, "")
    visitor = AttributeChecker()
    visitor.visit(tree)
    assert len(visitor.errors) == 0
