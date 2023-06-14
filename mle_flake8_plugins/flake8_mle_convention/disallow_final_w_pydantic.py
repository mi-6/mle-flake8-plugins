import ast
from typing import Iterator, Tuple, Type
from flake8.options.manager import OptionManager

class PydanticFinalChecker:
    name = "flake8-pydantic-final"
    version = "0.1"
    _error_tmpl = "PF001 don't use typing.Final in Pydantic models"

    def __init__(self, tree: ast.AST):
        self.tree = tree

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        pass

    @classmethod
    def parse_options(cls, options) -> None:
        pass

    def run(self) -> Iterator[Tuple[int, int, str, Type]]:
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    is_base_model = (
                        (isinstance(base, ast.Attribute) and base.attr == 'BaseModel') or
                        (isinstance(base, ast.Name) and base.id == 'BaseModel')
                    )
                    if is_base_model:
                        for body in node.body:
                            if isinstance(body, ast.AnnAssign) and isinstance(body.annotation, ast.Subscript):
                                if isinstance(body.annotation.value, ast.Name) and body.annotation.value.id == 'Final':
                                    yield (
                                        node.lineno,
                                        node.col_offset,
                                        self._error_tmpl,
                                        type(self),
                                    )
