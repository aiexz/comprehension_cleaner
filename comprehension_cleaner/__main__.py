import argparse
import os

from comprehension_cleaner import ast_analyzer

parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path to the directory to analyze", type=str, default=".", nargs="?")
args = parser.parse_args()


def main():
    for x in os.walk(args.path):
        files = x[2]
        for file_path in files:
            if file_path.endswith(".py"):
                with open(os.path.join(x[0], file_path), "r") as file:
                    y = ast_analyzer.Analysis()
                    code = file.read()
                    try:
                        for k, v in y.analyze_code(code).items():
                            print(
                                f"Unnecessary list comprehension in {k} (lines {','.join([str(x.value.lineno) for x in v])}), file {file.name}")
                    except SyntaxError:
                        print(f"Syntax error in {file.name}")


if __name__ == "__main__":
    main()
