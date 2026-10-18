# Releasing Darkroom

Package name: **Theme - Darkroom**

Repository: [pioug/sublime-darkroom](https://github.com/pioug/sublime-darkroom)

The package files live at the repository root. Keep resource paths under
`Theme - Darkroom/`, regardless of the repository's name. Do not add
`package-metadata.json`; Package Control generates it during installation.

The first submission targets macOS and Sublime Text build 4197 or newer.
Darkroom has been checked in build 4214. Windows and Linux need a native visual
check before broadening the `platforms` field in the registry entry.

## Prepare a release

1. Review the changes and update `CHANGELOG.md`. For the first release, change
   `Unreleased` to `1.0.0` and add the release date.
   Run `python3 scripts/render_assets.py` after changing the palette or screenshots.
   The editor preview uses Darkroom P3. Preserve the capture’s embedded color
   profile; the viewports exclude the OS title bar.
2. Run `python3 scripts/build.py`.
3. Test the built archive in Sublime Text. Use either the development link or
   the archive for a given installation, since an unpacked development package
   can hide problems in the archive. Select another theme and color scheme
   before switching between the two installations, then reselect Darkroom.
4. Check tabs, folder expansion, the command palette, Find/Where/Replace,
   autocomplete, split views, and the syntax samples in `examples/` with both
   Darkroom and Darkroom P3. Check the UI with IBM Plex Sans installed and check
   font fallback separately. Review Darkroom P3 on a Display P3 Mac; its RGB
   values are tuned for that display, since Sublime does not tag color schemes
   with a color profile.
5. Commit the release files, then run `python3 scripts/check_release.py`.
   This compares the committed Git export with the current standalone package
   and catches missing files, development files, and uncommitted changes.
6. Create a semantic version tag such as `1.0.0` and push the commit and tag to
   the public repository. Publish the built `.sublime-package` as a release
   asset for manual installation if desired.

The validation workflow repeats the build and Git-export check on pushes and
pull requests. `.gitattributes` excludes development material from Git exports;
`scripts/build.py` uses an explicit list for standalone archives.

## Submit to Package Control

1. Confirm the repository is public and the version tag exists.
2. Fork [sublimehq/package_control_channel](https://github.com/sublimehq/package_control_channel).
3. Copy the object in `.github/package-control.json` into `repository/t.json`,
   in alphabetical order. The local JSON file is a draft entry, not a
   self-hosted `packages.json` file.
4. Run the channel repository's tests and address its pull request checklist.
   Explain that Darkroom combines pure black surfaces, neutral text, colorful
   syntax, and IBM Plex Sans interface typography.
5. Submit the pull request as the package maintainer. After acceptance, update
   the README with the Package Control installation instructions.

Future compatible releases are discovered from semantic version tags. Change
the channel entry when repository details or compatibility requirements change.

References: [submission guide](https://docs.sublimetext.io/guide/package-control/submitting.html)
and [channel pull request checklist](https://github.com/sublimehq/package_control_channel/blob/master/.github/PULL_REQUEST_TEMPLATE.md).
