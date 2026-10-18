// Darkroom — pure black, neutral text, and colorful syntax.

type Palette = {
  name: string;
  background: string;
  foreground: string;
  accents: readonly string[];
};

const palette: Palette = {
  name: "Darkroom",
  background: "#000000",
  foreground: "#EEEEEE",
  accents: ["yellow", "blue", "iris", "peach", "rose", "red"],
};

export async function loadPalette(source: Promise<string>) {
  const theme = JSON.parse(await source) as Palette;

  if (!theme.name || theme.accents.length === 0) {
    throw new Error("A palette needs a name and an accent.");
  }

  return { ...palette, ...theme };
}

export function describe({ name, accents }: Palette): string {
  return `${name} pairs black with ${accents.join(", ")}.`;
}

console.log(describe(palette));
