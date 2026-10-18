#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
package_source="$project_dir"

if [[ $# -gt 1 ]]; then
    printf 'Usage: %s [Sublime Packages directory]\n' "$0" >&2
    exit 1
fi

if [[ $# -eq 1 ]]; then
    packages_dir="$1"
elif [[ "$(uname -s)" == "Darwin" ]]; then
    packages_dir="$HOME/Library/Application Support/Sublime Text/Packages"
    legacy_dir="$HOME/Library/Application Support/Sublime Text 3/Packages"
    if [[ ! -d "$packages_dir" && -d "$legacy_dir" ]]; then
        packages_dir="$legacy_dir"
    fi
else
    packages_dir="${XDG_CONFIG_HOME:-$HOME/.config}/sublime-text/Packages"
fi

destination="$packages_dir/Theme - Darkroom"
mkdir -p -- "$packages_dir"

if [[ -L "$destination" && "$(readlink "$destination")" == "$package_source" ]]; then
    printf 'Darkroom is already linked at %s\n' "$destination"
elif [[ -e "$destination" || -L "$destination" ]]; then
    printf 'An existing package is at %s. Move it before installing.\n' "$destination" >&2
    exit 1
else
    ln -s -- "$package_source" "$destination"
    printf 'Linked Darkroom at %s\n' "$destination"
fi

printf 'In Sublime Text, select Darkroom under both UI: Select Theme and UI: Select Color Scheme.\n'
