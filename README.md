# GNOME Terminal color profiles (offline bundle)

A self-contained installer that adds a set of **GNOME Terminal** color profiles,
each with a matching themed **font**. Everything is bundled — the color data is
embedded in `install.py` and every font ships in `fonts/` — so it works **fully
offline**. No downloads, no network.

## Contents
```
install.py       offline installer (no network required)
fonts/           bundled themed fonts (.ttf / .ttc)
fonts/CREDITS.md per-font author + license + source
fonts/LICENSES/  full license texts for the bundled fonts
LICENSE          MIT license for the installer code + palettes
README.md        this file
```

## Usage
```bash
python3 install.py             # install / update all profiles + fonts
python3 install.py --uninstall # remove the profiles and the installed fonts
```
- Re-running updates in place — deterministic IDs, no duplicates.
- Fonts are copied to `~/.local/share/fonts/gnome-terminal-themes/` and
  registered with `fc-cache`.
- 26 profiles are created; pick one from GNOME Terminal's profile menu /
  title-bar picker, or set a default in **Preferences**.
- Requirements: `dconf` (`sudo apt install dconf-cli` if missing) and
  `gnome-terminal`, run inside a GNOME session.

## Themed fonts and their licenses

Every bundled font is redistributable. Licenses were verified against the
metadata **embedded in each font file**. Full texts live in
[`fonts/LICENSES/`](fonts/LICENSES/); a complete table is in
[`fonts/CREDITS.md`](fonts/CREDITS.md).

| Profile(s) | Font | License |
|---|---|---|
| ubuntu | Ubuntu Mono | Ubuntu Font Licence 1.0 |
| winterminal | Cascadia Code | OFL-1.1 |
| powershell | Cascadia Mono | OFL-1.1 |
| firefox | Fira Mono | OFL-1.1 |
| github.light, github.dark | Monaspace Neon | OFL-1.1 |
| dos | PxPlus IBM VGA 8x16 | CC BY-SA 4.0 |
| cga | PxPlus IBM CGA | CC BY-SA 4.0 |
| c64.16color, c64.8color | Pet Me 64 | Kreative Korp free-use |
| gameboy | VT323 | OFL-1.1 |
| minecraft | Monocraft | OFL-1.1 |
| phosphor.amber/green/blue | VT323 | OFL-1.1 |
| mono.black, mono.white | Courier Prime | OFL-1.1 |

Profiles left on the **system font** (no terminal-suitable thematic font):
vscode, solarized.dark, solarized.light, batman, hulk, blueprint, cmyk, pepsi,
cyberpunk.

> **Attribution:** the two `PxPlus IBM …` fonts (used by `dos` and `cga`) are
> CC BY-SA 4.0 by **VileR** — *The Ultimate Oldschool PC Font Pack*,
> https://int10h.org/oldschool-pc-fonts/ . Any derivative of *those font files*
> must stay CC BY-SA 4.0; the rest of this repo is MIT.

## Trademarks & names

Profile names such as `ubuntu`, `github.light`, `firefox`, `pepsi`, `batman`, `hulk`,
`gameboy`, `minecraft`, and `cyberpunk` refer to trademarks owned by their
respective companies. They are used here **only to identify** the color scheme a
profile approximates. This project is unofficial, is not affiliated with or
endorsed by any of those owners, and claims no rights in their marks. Color
palette **values** are factual data and are not claimed as copyrighted.

If you are a rights holder and want a name changed, open an issue.

## License

- Installer code (`install.py`), documentation, and palette data: **MIT** (see
  [`LICENSE`](LICENSE)) — free to use, copy, modify, and share.
- Bundled fonts: each under its own license — see
  [`fonts/CREDITS.md`](fonts/CREDITS.md) and [`fonts/LICENSES/`](fonts/LICENSES/).

## Notes
- Adjust any point size in GNOME Terminal **Preferences → profile → Text** after
  install.
- The palettes are authentic/verified reference colors (VS Code Dark+, Campbell,
  Yaru, Solarized, Colodore C64, GitHub Primer, Minecraft §-codes, classic Pepsi
  globe, etc.).
- The bundle is portable: move the whole folder anywhere and `install.py` still
  works (it locates `fonts/` relative to itself).
