"""Pure black surfaces, neutral text, and colorful accents."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    name: str
    background: str = "#000000"
    foreground: str = "#EEEEEE"
    accents: tuple[str, ...] = ("yellow", "blue", "iris", "peach", "rose", "red")

    def describe(self, *, include_background: bool = True) -> str:
        # Comments stay quiet without disappearing into the background.
        accents = ", ".join(self.accents)
        description = f"{self.name}: {accents}"
        if include_background:
            return f"{description} on {self.background}"
        return description


def make_palette(name: str | None = None) -> Palette:
    return Palette(name=name or "Darkroom")


if __name__ == "__main__":
    palette = make_palette()
    print(palette.describe(include_background=True))
