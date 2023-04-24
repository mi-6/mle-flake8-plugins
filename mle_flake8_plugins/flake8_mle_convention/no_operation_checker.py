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
)


class NoOperationsChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []
        self._class_stack = []

    def _count_operations(self, node: ast.AST) -> int:
        count = 0
        for child in ast.iter_child_nodes(node):
            if isinstance(child, _OPERATIONS):
                count += 1
            count += self._count_operations(child)
        return count

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._class_stack.append(node)
        self.generic_visit(node)
        self._class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        current_class = self._class_stack[-1] if self._class_stack else None
        inherits_from_abc = False
        # Check if the class inherits from ABC
        if current_class:
            for base in current_class.bases:
                if isinstance(base, ast.Attribute) and base.attr == "ABC":
                    inherits_from_abc = True
                    break

        has_only_pass = len(node.body) == 1 and isinstance(node.body[0], ast.Pass)

        if not has_only_pass and not inherits_from_abc:
            operations_count = self._count_operations(node)
            if operations_count < 1:
                self.errors.append((node.lineno, node.col_offset, error_codes["no_operation"], type(self)))
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.visit_FunctionDef(node)
