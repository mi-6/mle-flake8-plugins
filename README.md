# mle-flake8-plugins

## Installation

```
pip install mle-flake8-plugins
```

## Support checkers

### Docstring

#### MLE000 Attribute section checker

```py
# good
class A:
    """This is sample class A.

    Attributes:
        hoge: a member.
    """

    def __init__(self):
        self.hoge = ""

# bad
# MLE000 Missing attribute 'hoge' document in the docstring attribute section
class B:
    """This is sample class B."""

    def __init__(self):
        self.hoge = ""

```

### Coding convention

#### MLE100 Legacy type hint checker

```py
# good
def test_modern_style(a: list, b: dict) -> tuple:
    return tuple(a + list(b.keys()))

# bad
# MLE100 Consider using 'list' instead of 'List'
# MLE100 Consider using 'dict' instead of 'Dict'
# MLE100 Consider using 'tuple' instead of 'Tuple'
def test_legacy_style(a: List, b: Dict) -> Tuple:
    return tuple(a + list(b.keys()))
```

#### MLE101 No operation checker

```py
# good
def test_1_operations(a, b):
    return a + b

# bad
# MLE101 No operation in function
def test_no_operation(a, b):
    return a
```

## Related tools
* [pydocstyle](https://github.com/PyCQA/pydocstyle)
  * A tool to check document style and availability
  * It is not checked if the appropriate sections are provided.
* [darglint](https://github.com/terrencepreilly/darglint)
  * A tool to check that the appropriate sections are provided
  * This repository has been archived.
  * The "attributes" section is not checked. ([link](https://github.com/terrencepreilly/darglint/issues/25))
