import ast

from .disallow_final_w_pydantic import PydanticFinalChecker
from .legacy_type_hint_checker import LegacyTypeHintChecker
from .no_operation_checker import NoOperationsChecker

__version__ = "0.1.0"


class MleConventionChecker:
    name = "flake8-mle-convention"

    def __init__(self, tree: ast.AST):
        self.tree = tree

    def run(self):
        checkers = [
            LegacyTypeHintChecker(),
            NoOperationsChecker(),
            PydanticFinalChecker(),
        ]
        errors = []
        for checker in checkers:
            checker.visit(self.tree)
            errors.extend(checker.errors)

        errors_seen = set()
        for error in errors:
            if error in errors_seen:
                continue

            errors_seen.add(error)

            yield error
