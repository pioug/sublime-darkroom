"""Render the README montage from native screenshots and both Darkroom palettes."""

import base64
import json
import mimetypes
from pathlib import Path


project = Path(__file__).resolve().parent.parent
assets = project / "assets"
font = "IBM Plex Sans, sans-serif"

# IBM/plex: packages/plex-sans/fonts/complete/woff2. License: assets/fonts/LICENSE.txt.
font_faces = []
for weight, name in [(400, "Regular"), (500, "Medium")]:
    encoded = base64.b64encode(
        (assets / "fonts" / f"IBMPlexSans-{name}.woff2").read_bytes()
    ).decode("ascii")
    font_faces.append(
        f'@font-face {{ font-family: "IBM Plex Sans"; font-weight: {weight}; '
        f'src: url(data:font/woff2;base64,{encoded}) format("woff2"); }}'
    )
font_style = '<style>' + "\n".join(font_faces) + '</style>'


def screenshot_frame(name, key, x, y, width, height, crop, background="#000000"):
    """Clip a native screenshot to a flat frame without changing its pixels."""
    encoded = base64.b64encode((assets / name).read_bytes()).decode("ascii")
    media_type = mimetypes.guess_type(name)[0]
    view_box = " ".join(str(value) for value in crop)
    image_height = width * crop[3] / crop[2]
    image_y = y + (height - image_height) / 2
    return f'''
  <defs><clipPath id="{key}"><rect x="{x}" y="{y}" width="{width}" height="{height}" rx="10"/></clipPath></defs>
  <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="10" fill="{background}"/>
  <g clip-path="url(#{key})">
    <svg x="{x}" y="{image_y}" width="{width}" height="{image_height}" viewBox="{view_box}">
      <image width="1744" height="1132" href="data:{media_type};base64,{encoded}"/>
    </svg>
  </g>
  <rect x="{x + 0.5}" y="{y + 0.5}" width="{width - 1}" height="{height - 1}" rx="9.5" fill="none" stroke="#292929"/>
'''


montage = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1848" viewBox="0 0 1600 1848" role="img" aria-labelledby="title description">
  <title id="title">Darkroom P3 in Sublime Text 4</title>
  <desc id="description">Native screenshots of the Darkroom P3 editor, Go to Anything, command palette, and Find in Files, with the Darkroom and Darkroom P3 color palettes.</desc>
  {font_style}
  <rect x="0.5" y="0.5" width="1599" height="1847" rx="16" fill="#000000" stroke="#242424"/>
  <g font-family="{font}">
    <text x="40" y="65" fill="#969696" font-size="21">Sublime Text 4</text>
    <g fill="#969696" font-size="21">
      <text x="40" y="1007">Go to Anything</text>
      <text x="816" y="1007">Command palette</text>
      <text x="40" y="1350">Find / Where / Replace</text>
    </g>
  </g>
'''
# Exclude the OS title bar and its screen-sharing badge from every viewport.
montage += screenshot_frame(
    "preview.png", "editor", 40, 104, 1520, 854, (0, 64, 1744, 980)
)
montage += screenshot_frame(
    "goto-anything.jpg", "goto", 40, 1028, 744, 272, (500, 136, 1106, 358),
    background="#111111"
)
montage += screenshot_frame(
    "command-palette.jpg", "commands", 816, 1028, 744, 272, (500, 136, 1106, 404),
    background="#111111"
)
montage += screenshot_frame(
    "find-in-files.jpg", "find", 40, 1372, 1520, 216, (16, 880, 1712, 244)
)
for name, y in [("Darkroom", 1656), ("Darkroom P3", 1768)]:
    syntax = json.loads((project / f"{name}.sublime-color-scheme").read_text())["variables"]
    montage += (
        f'  <g transform="translate(40 {y})" font-family="{font}">\n'
        f'    <text y="-22" fill="#969696" font-size="21">{name} palette</text>\n'
    )
    for index, accent in enumerate(
        ("string", "amber", "red", "coral", "mauve", "blue", "teal", "sage")
    ):
        color = syntax[accent]
        x = index * 191
        fill = f'fill="{color}"'
        if name == "Darkroom P3":
            # Match the P3 screenshot; retain a fallback for older SVG viewers.
            channels = " ".join(
                f"{int(color[start:start + 2], 16) / 255:.6f}"
                for start in (1, 3, 5)
            )
            fill += f' style="fill: color(display-p3 {channels})"'
        montage += (
            f'    <rect x="{x}" width="183" height="40" rx="3" {fill}/>\n'
            f'    <text x="{x + 12}" y="27" fill="#191919" font-size="18" '
            f'font-weight="500">{color}</text>\n'
        )
    montage += '  </g>\n'
montage += '</svg>\n'

(assets / "montage.svg").write_text(montage, encoding="utf-8")
print("Rendered assets/montage.svg")
