import ast

from docstring_parser import Style, parse

from .errors import error_codes


class AttributeChecker(ast.NodeVisitor):
    def __init__(self, style=Style.AUTO, *args, **kwargs) -> None:
        super(AttributeChecker, self).__init__(*args, **kwargs)
        self._style = style
        self.errors = []

    def docstring_attribute(self, node):
        attrs = []
        docstring = ast.get_docstring(node)
        docstring = parse(docstring, self._style)
        for param in docstring.params:
            if param.args[0] == "attribute":
                attrs.append(param.args[1].strip())
        return attrs

    def is_public(self, attr_name):
        return attr_name[0] != "_"

    def visit_ClassDef(self, node):
        if not self.is_public(node.name):
            return
        doc_attrs = self.docstring_attribute(node)

        for child in node.body:
            # dataclass, class member
            if (
                isinstance(child, ast.AnnAssign)
                and isinstance(child.target, ast.Name)
                and self.is_public(child.target.id)
                and child.target.id not in doc_attrs
            ):
                self.errors.append(
                    (
                        node.lineno,
                        node.col_offset,
                        error_codes["attribute"] % child.target.id,
                    )
                )

            # assign value in functions
            if isinstance(child, ast.FunctionDef):
                for gc in child.body:
                    if (
                        isinstance(gc, ast.Assign)
                        and gc.targets
                        and isinstance(gc.targets[0], ast.Attribute)
                        and self.is_public(gc.targets[0].attr)
                        and gc.targets[0].attr not in doc_attrs
                    ):
                        self.errors.append(
                            (
                                node.lineno,
                                node.col_offset,
                                error_codes["attribute"] % gc.targets[0].attr,
                            )
                        )
