import ast
from subprocess import call
from typing import (
    Callable,
    NamedTuple,
    Literal,
    Optional,
    Union,
)


class ImportStatement(NamedTuple):
    type: Union[Literal['Import'], Literal['FromImport']]
    module: str
    symbols: Optional[list[str]]
    lineno: int


VisitCallback = Callable[[str, ImportStatement], None]


class MyNodeVisitor(ast.NodeVisitor):
    def __init__(self, filename: str, callback: VisitCallback) -> None:
        super().__init__()
        self._callback = callback
        self._filename = filename

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self._callback(self._filename, ImportStatement(
                type='Import',
                module=alias.name,
                lineno=alias.lineno,
                symbols=None,
            ))

    def visit_ImportFrom(self, node: ast.ImportFrom):
        self._callback(self._filename, ImportStatement(
            type='FromImport',
            module=node.module,
            lineno=node.lineno,
            symbols=[n.name for n in node.names]
        ))
