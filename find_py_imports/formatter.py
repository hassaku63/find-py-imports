from typing import NamedTuple

from find_py_imports.visitor import ImportStatement


class Record(NamedTuple):
    filename: str
    stmt: ImportStatement


class Formatter():
    def format(self, record: Record) -> str:
        if record.stmt.type == 'Import':
            return self.format_Import(record)
        elif record.stmt.type == 'FromImport':
            return self.format_FromImport(record)

    def format_Import(self, record: Record) -> str:
        raise NotImplementedError

    def format_FromImport(self, record: Record) -> str:
        raise NotImplementedError


class SimpleFormatter(Formatter):
    def format_Import(self, record: Record) -> str:
        return f'import {record.stmt.module}'

    def format_FromImport(self, record: Record) -> str:
        return f'from {record.stmt.module} import {", ".join(record.stmt.symbols)}'


class LinenoFormatter(Formatter):
    def format_Import(self, record: Record) -> str:
        return f'{record.stmt.lineno}:import {record.stmt.module}'

    def format_FromImport(self, record: Record) -> str:
        return f'{record.stmt.lineno}:from {record.stmt.module} import {", ".join(record.stmt.symbols)}'


class FilenameFormatter(Formatter):
    def format_Import(self, record: Record) -> str:
        return f'{record.filename}:import {record.stmt.module}'

    def format_FromImport(self, record: Record) -> str:
        return f'{record.filename}:from {record.stmt.module} import {", ".join(record.stmt.symbols)}'


class FilenameLinenoFormatter(Formatter):
    def format_Import(self, record: Record) -> str:
        return f'{record.filename}:{record.stmt.lineno}:import {record.stmt.module}'

    def format_FromImport(self, record: Record) -> str:
        return f'{record.filename}:{record.stmt.lineno}:from {record.stmt.module} import {", ".join(record.stmt.symbols)}'
