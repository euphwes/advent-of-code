from collections import Counter

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 1
YEAR = 2024

PART_ONE_DESCRIPTION = "distance between lists"
PART_ONE_ANSWER = 1110981

PART_TWO_DESCRIPTION = "similarity score"
PART_TWO_ANSWER = 24869388


def _parse_lists(raw_input: list[str]) -> tuple[list[int], list[int]]:
    left_column: list[int] = []
    right_column: list[int] = []

    for line in raw_input:
        left, right = (int(n) for n in line.split())
        left_column.append(left)
        right_column.append(right)

    return left_column, right_column


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    left_column, right_column = _parse_lists(raw_input)

    # Sort both columns of integers, and return the sum of the differences between each
    # pair of values from the left and right columns
    left_column.sort()
    right_column.sort()
    return sum(abs(left - right) for left, right in zip(left_column, right_column, strict=True))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    left_column, right_column = _parse_lists(raw_input)

    # The "similarity score" is the sum of the products of the values in the left column,
    # and how often those values appear in the right column.
    right_column_counts = Counter(right_column)
    return sum(a * right_column_counts[a] for a in left_column)


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))


"""
{
    "python.venvFolders": [
        "venvs"
    ],

    // Configure glob patterns for excluding files and folders. For example, the files
    // explorer decides which files and folders to show or hide based on this setting.
    // Read more about glob patterns
    // [here](https://code.visualstudio.com/docs/editor/codebasics#_advanced-search-options).
	"files.exclude": {
        "**/.git": true,
        "**/.svn": true,
        "**/.hg": true,
        "**/CVS": true,
        "**/.DS_Store": true,
        "**/__pycache__": true,
        "**/.vscode": true,
        "**/.classpath": true,
        "**/.project": true,
        "**/.settings": true,
        "**/.factorypath": true
    },
    "editor.rulers": [

        {
          "column": 96,
          "color": "#a3a3a32c"
        },
      ],
    // "explorer.autoReveal": true,
    "editor.suggestSelection": "first",
    "vsintellicode.modify.editor.suggestSelection": "automaticallyOverrodeDefaultValue",
    "[typescriptreact]": {
      "editor.defaultFormatter": "esbenp.prettier-vscode",
      "editor.formatOnSave": true,
    },
    "[typescript]": {
      "editor.defaultFormatter": "esbenp.prettier-vscode",
      "editor.formatOnSave": true,
    },
    "[python]": {
      "editor.formatOnType": true,
      "editor.formatOnSave": true,
      "editor.defaultFormatter": "charliermarsh.ruff",
      "editor.codeActionsOnSave": {
        "source.fixAll": "explicit",
        "source.organizeImports": "explicit",
      }
    },
    "rewrap.autoWrap.enabled": true,
    "python.analysis.autoImportCompletions": true,
    "python.analysis.indexing": true,
    "python.analysis.pythonVersion": "3.13",
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.diagnosticSeverityOverrides": {
        "reportUnboundVariable": "warning",
      },
    "workbench.colorTheme": "Default Dark+",
    "colorize.languages": [
      "typescript",
      "javascript",
      "css",
      "scss",
      "typescriptreact"
    ],
}
"""
extensions = """
colorize
python
pylance
python debugger
ruff
"""
