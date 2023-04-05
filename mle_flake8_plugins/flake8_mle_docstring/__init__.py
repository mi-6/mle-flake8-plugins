import ast

import pycodestyle
from docstring_parser import Style

from .attribute_checker import AttributeChecker

__version__ = "0.1.0"


class MleDocstringChecker:
    options = None
    name = "flake8-mle-docstring"
    version = __version__

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename
        self.lines = None

    def load_file(self):
        if self.filename in ("stdin", "-", None):
            self.filename = "stdin"
            self.lines = pycodestyle.stdin_get_value().splitlines(True)
        else:
            self.lines = pycodestyle.readlines(self.filename)

        if not self.tree:
            self.tree = ast.parse("".join(self.lines))

    @classmethod
    def add_options(cls, parser):
        """Add plugin configuration option to flake8."""
        parser.add_option(
            "--docstring-sections-style",
            action="store",
            parse_from_config=True,
            default="auto",
            choices=["auto", "rest", "google", "numpy", "epy"],
            help="Docstring style.",
        )

    @classmethod
    def parse_options(cls, options):
        """Parse the configuration options given to flake8."""
        if options.docstring_sections_style == "rest":
            cls.docstring_sections_style = Style.REST
        elif options.docstring_sections_style == "google":
            cls.docstring_sections_style = Style.GOOGLE
        elif options.docstring_sections_style == "numpy":
            cls.docstring_sections_style = Style.NUMPYDOC
        elif options.docstring_sections_style == "epy":
            cls.docstring_sections_style = Style.EPYDOC
        else:
            cls.docstring_sections_style = Style.AUTO

    def run(self):
        if not self.tree or not self.lines:
            self.load_file()

        parser = AttributeChecker(self.docstring_sections_style)
        parser.visit(self.tree)
        errors = parser.errors
        errors_seen = set()

        for error in errors:
            if error in errors_seen:
                continue

            errors_seen.add(error)

            yield (error[0], error[1], error[2], AttributeChecker)
