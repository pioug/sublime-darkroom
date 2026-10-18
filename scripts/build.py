"""Package the theme without development files or examples."""

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


project = Path(__file__).resolve().parent.parent
package_name = "Theme - Darkroom"
destination = project / "dist" / f"{package_name}.sublime-package"
documents = [
    project / "Darkroom.sublime-theme",
    project / "Darkroom.sublime-color-scheme",
    project / "Darkroom P3.sublime-color-scheme",
    project / "Widget - Darkroom.sublime-settings",
    project / "Widget - Darkroom.hidden-color-scheme",
]
sources = [
    *documents,
    project / "README.md",
    project / "LICENSE",
    project / "CHANGELOG.md",
    *sorted((project / "textures").glob("*.png")),
]

for source in sources:
    if not source.is_file():
        raise FileNotFoundError(source)

definitions = {
    document.name: json.loads(document.read_text(encoding="utf-8"))
    for document in documents
}
for rule in definitions["Darkroom.sublime-theme"]["rules"]:
    for property_name, value in rule.items():
        if property_name.endswith(".texture") and value.startswith(f"{package_name}/"):
            texture = project / Path(value).relative_to(package_name)
            for scale in ("", "@2x", "@3x"):
                variant = texture.with_name(f"{texture.stem}{scale}{texture.suffix}")
                if not variant.is_file():
                    raise FileNotFoundError(variant)

destination.parent.mkdir(exist_ok=True)
with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
    for source in sources:
        archive.write(source, source.relative_to(project).as_posix())

print(destination)
