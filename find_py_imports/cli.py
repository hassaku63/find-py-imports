import ast
import argparse
import pathlib
import sys

from typing import TypedDict, Optional

import find_py_imports.visitor as v
import find_py_imports.formatter as fmt


class _Err(TypedDict):
        filename: Optional[str]
        error: Exception


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--line-number', action='store_true', dest='show_line_number',
        help='show line number')
    parser.add_argument('--hide-syntax-error', action='store_true',dest='hide_syntax_err',
        help='do not print syntax error print to stderr')
    parser.add_argument('--print-file-not-found-error', action='store_true', dest='print_file_not_found_err',
        help='print not founded files to stderr')
    parser.add_argument('file', nargs='*', type=str, help='filename(s)')

    args = parser.parse_args()
    show_line_number: bool = args.show_line_number
    print_syntax_err: bool = not args.hide_syntax_err
    print_file_not_found_err: bool = args.print_file_not_found_err
    files: list[str] = args.file
    filenames_are_provided = True

    formatter = None
    pred = (1 < len(files), show_line_number)  # test [multiple_file?, show line_number?]
    if pred == (False, False):
        formatter = fmt.SimpleFormatter()
    elif pred == (False, True):
        formatter = fmt.LinenoFormatter()
    elif pred == (True, False):
        formatter = fmt.FilenameFormatter()
    elif pred == (True, True):
        formatter = fmt.FilenameLinenoFormatter()
    else:
        raise Exception

    # if no filename is provided then use input chars from stdin as content of a file
    if len(files) < 1:
        filenames_are_provided = False

    result: list[fmt.Record] = []
    def save_result(fn: str, stmt: v.ImportStatement):
        result.append(fmt.Record(fn, stmt))

    errs: list[_Err] = []
    if filenames_are_provided:
        # interpret input as filename
        for fn in files:
            try:
                if not pathlib.Path(fn).exists():
                    raise FileNotFoundError(fn)
                with open(fn) as fp:
                    tree = ast.parse(fp.read())
                    visitor = v.MyNodeVisitor(fn, save_result)
                    visitor.visit(tree)
            except (FileNotFoundError, SyntaxError) as e:
                errs.append({
                    'filename': fn,
                    'error': e,
                })
    else:
        # interpret input as code string
        try:
            tree = ast.parse(sys.stdin.read())
            visitor = v.MyNodeVisitor(None, save_result)
            visitor.visit(tree)
        except (FileNotFoundError, SyntaxError) as e:
            errs.append({
                'filename': None,
                'error': e,
            })

    for r in result:
        print(formatter.format(r))

    for e in errs:
        if print_syntax_err:
            s = ''
            if 1 < len(files):
                s = f' at {e["filename"]}'
            sys.stderr.write(f'syntax error{s}: {e["error"]}\n')
        if print_file_not_found_err:
            sys.stderr.write(f'no such file: {e["error"]}\n')


if __name__ == '__main__':
    main()