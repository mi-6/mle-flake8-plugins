import ast

from .errors import error_codes


class LegacyTypeHintChecker(ast.NodeVisitor):
    def __init__(self, *args, **kwargs) -> None:
        super(LegacyTypeHintChecker, self).__init__(*args, **kwargs)
        self.errors = []

    def check_type_hint(self, hint: ast.AST, lineno: int, col_offset: int) -> None:
        if isinstance(hint, ast.Subscript) and isinstance(hint.value, ast.Name):
            if hint.value.id in {"List", "Dict", "Tuple"}:
                self.errors.append(
                    (
                        lineno,
                        col_offset,
                        error_codes["legacy_type_hint"]
                        % (hint.value.id.lower(), hint.value.id),
                        type(self),
                    )
                )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.returns is not None:
            self.check_type_hint(node.returns, node.lineno, node.col_offset)

        for arg in node.args.args:
            if arg.annotation is not None:
                self.check_type_hint(arg.annotation, arg.lineno, arg.col_offset)

        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self.check_type_hint(node.annotation, node.lineno, node.col_offset)
        self.generic_visit(node)
