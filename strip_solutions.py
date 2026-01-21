import nbformat
from pathlib import Path

MARKER = "# ---SOLUTION---"
TODO_LINE = "# TODO: Write your solution here"

def strip_cell(cell):
    if cell.cell_type != "code":
        return cell

    src = cell.source
    if MARKER in src:
        before, _ = src.split(MARKER, 1)

        # Ensure clean formatting
        before = before.rstrip()

        # Replace marker with TODO
        cell.source = f"{before}\n\n{TODO_LINE}\n"
        cell.outputs = []
        cell.execution_count = None

    return cell

def process(nb_path: Path):
    nb = nbformat.read(nb_path, as_version=4)

    for i, cell in enumerate(nb.cells):
        nb.cells[i] = strip_cell(cell)

    out_path = nb_path.with_name(nb_path.stem.replace("_solution", "") + ".ipynb")
    nbformat.write(nb, out_path)
    print(f"Written: {out_path}")

if __name__ == "__main__":
    import sys
    process(Path(sys.argv[1]))
