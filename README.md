# find-py-imports

I have made `find-py-imports` to detects import statements that span multiple lines, 

`find-py-imports` saerchs any given input files, selecting lines that use python import statements.
You can change the output format like grep tool, by pass a option to command-line.

```python
from datetime import (
    datetime,
    timedelta
)
# -> from datetime import datetime, timedelta

import json, \
    csv
# -> import json
#    import csv
```

## installation

```bash
git clone <this-reposity>
cd <this-reposity>

python -m pip install .
```

## command-line usage

By installing this repositoty as a python package, you can use `find_py_imports` command.

```plain
find_py_imports -h
usage: import-finder [-h] [-n] [--hide-syntax-error] [--print-file-not-found-error] [file ...]

positional arguments:
  file                  filename(s)

options:
  -h, --help            show this help message and exit
  -n, --line-number     show line number
  --hide-syntax-error   do not print syntax error print to stderr
  --print-file-not-found-error
                        print not founded files to stderr
```

`find_py_imports` provide grep-like interface.

If you give file arg(s), `find_py_imports` interpret this input arg as a filename;

```bash
find_py_imports main.py

find . -name "*.py" | xargs find_py_imports
```

If you give no file arg, `find_py_imports` interpret input from stdin as python code string;

```bash
cat main.py | find_py_imports

find_py_imports << EOF
import os
from datetime import datetime
```

`find_py_imports` detects import statements that span multiple lines,
shows output one line import statement per one package imported

```bash
echo "import os, \
    sys
from datetime import (
    datetime,
    timedelta
)" > a.py

find_py_imports a.py
# >>> import os
# >>> import sys
# >>> from datetime import datetime, timedelta
```


`find_py_imports` shows "<filename>:" prefix at output if input is given multiple files

```bash
echo import os > a.py
echo import sys > b.py

find_py_imports a.py b.py
# >>> a.py:import os
# >>> b.py:import sys
```
