import ast
import unittest
from mle_flake8_plugins.flake8_mle_convention.disallow_final_w_pydantic import PydanticFinalChecker

class TestPydanticFinalChecker(unittest.TestCase):
    def test_no_error(self):
        code = "\n".join([
            "from pydantic import BaseModel",
            "",
            "class MyModel(BaseModel):",
            "    name: str",
        ])
        tree = ast.parse(code)
        checker = PydanticFinalChecker(tree)
        errors = list(checker.run())
        self.assertEqual(errors, [])

    def test_error(self):
        code = "\n".join([
            "from pydantic import BaseModel",
            "from typing import Final",
            "",
            "class MyModel(BaseModel):",
            "    name: Final[str]",
        ])
        tree = ast.parse(code)
        checker = PydanticFinalChecker(tree)
        errors = list(checker.run())
        self.assertNotEqual(errors, [])