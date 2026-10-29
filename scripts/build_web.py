"""Package the unmodified MIND2 composer for the GitHub Pages browser app.

The zip is unpacked into Pyodide's virtual filesystem at runtime. It includes
only Python source files used by the generative engine, never bytecode or caches.
"""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "engine.zip"


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED) as bundle:
        for source in sorted((ROOT / "mind").rglob("*.py")):
            bundle.write(source, source.relative_to(ROOT).as_posix())
        bundle.write(ROOT / "web" / "engine_bridge.py", "engine_bridge.py")
    print(f"Built {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
