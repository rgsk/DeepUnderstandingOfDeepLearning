#!/usr/bin/env python3

import json
import sys
from pathlib import Path


def normalize_notebook(path: Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"failed to read {path}: {exc}") from exc

    changed = False

    for cell in data.get("cells", []):
        if cell.get("cell_type") == "code":
            if cell.get("execution_count") is not None:
                cell["execution_count"] = None
                changed = True

            for output in cell.get("outputs", []):
                if output.get("execution_count") is not None:
                    output["execution_count"] = None
                    changed = True

    if changed:
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )

    return changed


def iter_notebooks(root: Path):
    if root.is_file() and root.suffix == ".ipynb":
        yield root
        return

    if root.is_dir():
        yield from sorted(root.rglob("*.ipynb"))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: normalize_notebooks.py <path> [<path> ...]", file=sys.stderr)
        return 2

    changed_paths = []

    for arg in argv[1:]:
        root = Path(arg)
        for notebook in iter_notebooks(root):
            if normalize_notebook(notebook):
                changed_paths.append(notebook)

    for notebook in changed_paths:
        print(f"normalized {notebook}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
