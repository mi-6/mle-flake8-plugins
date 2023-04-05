import ast

from .type_hint_checker import TypeHintChecker

__version__ = "0.1.0"


class MleConventionChecker:
    name = "flake8-mle-convention"

    def __init__(self, tree: ast.AST):
        self.tree = tree

    def run(self):
        parser = TypeHintChecker()
        parser.visit(self.tree)
        errors = parser.errors
        errors_seen = set()

        for error in errors:
            if error in errors_seen:
                continue

            errors_seen.add(error)

            yield error
