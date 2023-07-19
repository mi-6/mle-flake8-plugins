import ast

from .errors import error_codes

_OPERATIONS = (
    ast.Call,
    ast.Attribute,
    ast.Subscript,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitAnd,
    ast.BitXor,
    ast.And,
    ast.Or,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.If,
    ast.For,
    ast.While,
    ast.With,
)


class NoOperationsChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []
        self._class_stack = []

    def _count_operations(self, node: ast.AST) -> int:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return sum(self._count_operations(child) for child in node.body)
        elif isinstance(node, (ast.arguments, ast.arg, ast.expr_context, ast.keyword)):
            return 0
        else:
            return int(isinstance(node, _OPERATIONS)) + sum(
                self._count_operations(child) for child in ast.iter_child_nodes(node)
            )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        has_only_pass = len(node.body) == 1 and isinstance(node.body[0], ast.Pass)
        has_decorator = bool(node.decorator_list)

        if not has_only_pass and not has_decorator:
            operations_count = self._count_operations(node)
            if operations_count < 1:
                self.errors.append(
                    (
                        node.lineno,
                        node.col_offset,
                        error_codes["no_operation"],
                        type(self),
                    )
                )
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.visit_FunctionDef(node)
