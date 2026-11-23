"""Architecture test.

Vérifie que tous les appels à `to_csv` faits dans le package
`formation_mlops_2` sont bien appelés avec l'argument `index=False`.

Cela évite d'écrire l'index du DataFrame dans les fichiers CSV générés
(données, prédictions, etc.).
"""

import ast
from pathlib import Path

PACKAGE_ROOT = Path(__file__).parents[2] / "formation_mlops_2"



def test_to_csv_called_with_index_false():
    # Collect all Python files in the package
    python_files = list(PACKAGE_ROOT.rglob("*.py"))

    violations = []

    for file_path in python_files:
        with open(file_path, encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read(), filename=str(file_path))
            except SyntaxError:
                continue

        for node in ast.walk(tree):
            # Look for method calls (df.to_csv(...))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "to_csv":
                # Check if index=False is present in the arguments
                index_arg = None
                for keyword in node.keywords:
                    if keyword.arg == "index":
                        index_arg = keyword.value
                        break

                    # If index argument is not present or is not False
                    if index_arg is None or not isinstance(index_arg, ast.Constant) or index_arg.value is not False:
                        violations.append(str(file_path))

    assert not violations, (
        f"Found to_csv() calls without index=False in: {', '.join(violations)}"
    )
