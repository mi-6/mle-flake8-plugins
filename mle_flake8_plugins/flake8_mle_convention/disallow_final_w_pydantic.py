import ast

from .errors import error_codes


class PydanticFinalChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for base in node.bases:
            is_base_model = (
                isinstance(base, ast.Attribute) and base.attr == "BaseModel"
            ) or (isinstance(base, ast.Name) and base.id == "BaseModel")
            if is_base_model:
                for body in node.body:
                    if isinstance(body, ast.AnnAssign) and isinstance(
                        body.annotation, ast.Subscript
                    ):
                        if (
                            isinstance(body.annotation.value, ast.Name)
                            and body.annotation.value.id == "Final"
                        ):
                            self.errors.append(
                                (
                                    node.lineno,
                                    node.col_offset,
                                    error_codes["disallow-pydantic-final"],
                                    type(self),
                                )
                            )
