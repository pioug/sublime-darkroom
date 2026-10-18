"""Check that a Git release exports the same files as the standalone package."""

from io import BytesIO
from pathlib import Path
import subprocess
import sys
from zipfile import ZipFile


project = Path(__file__).resolve().parent.parent
revision = sys.argv[1] if len(sys.argv) == 2 else "HEAD"
if len(sys.argv) > 2:
    raise SystemExit("Usage: python3 scripts/check_release.py [git revision]")

subprocess.run([sys.executable, project / "scripts/build.py"], check=True)
export = subprocess.check_output(
    ["git", "archive", "--format=zip", revision], cwd=project
)

with ZipFile(project / "dist/Theme - Darkroom.sublime-package") as package:
    with ZipFile(BytesIO(export)) as archive:
        expected = set(package.namelist())
        actual = {entry.filename for entry in archive.infolist() if not entry.is_dir()}
        if actual != expected:
            raise SystemExit(
                "Release file mismatch.\n"
                f"Missing from Git archive: {sorted(expected - actual)}\n"
                f"Unexpected in Git archive: {sorted(actual - expected)}"
            )
        for name in sorted(expected):
            if archive.read(name) != package.read(name):
                raise SystemExit(f"Uncommitted or mismatched release file: {name}")

print(f"Release archive matches the standalone package: {len(expected)} files.")
