# Font credits & licenses

Every font bundled in this folder is redistributable. Licenses were verified
against the metadata embedded in each font file, not just secondary sources.
Full license texts are in [`LICENSES/`](LICENSES/).

| Font file | Family | Author / owner | License | Source |
|---|---|---|---|---|
| `UbuntuMono.ttf` | Ubuntu Mono | Canonical Ltd. | [Ubuntu Font Licence 1.0](LICENSES/UbuntuFontLicense-1.0.txt) | https://ubuntu.com/legal/font-licence |
| `CascadiaCode-Regular.ttf` | Cascadia Code | Microsoft | [OFL-1.1](LICENSES/OFL-1.1.txt) | https://github.com/microsoft/cascadia-code |
| `CascadiaMono-Regular.ttf` | Cascadia Mono | Microsoft | [OFL-1.1](LICENSES/OFL-1.1.txt) | https://github.com/microsoft/cascadia-code |
| `FiraMono-Regular.ttf` | Fira Mono | Mozilla / Telefónica / Carrois | [OFL-1.1](LICENSES/OFL-1.1.txt) | https://github.com/mozilla/Fira |
| `MonaspaceNeon-Regular.ttf` | Monaspace Neon | GitHub, Inc. | [OFL-1.1](LICENSES/OFL-1.1.txt) | https://github.com/githubnext/monaspace |
| `Monocraft.ttc` | Monocraft | Idrees Hassan | [OFL-1.1](LICENSES/OFL-1.1.txt) | https://github.com/IdreesInc/Monocraft |
| `VT323-Regular.ttf` | VT323 | Peter Hull (The VT323 Project) | [OFL-1.1](LICENSES/OFL-1.1.txt) | https://fonts.google.com/specimen/VT323 |
| `CourierPrime-Regular.ttf` | Courier Prime | Quote-Unquote Apps | [OFL-1.1](LICENSES/OFL-1.1.txt) | https://github.com/quoteunquoteapps/CourierPrime |
| `PxPlus_IBM_VGA_8x16.ttf` | PxPlus IBM VGA 8x16 | VileR (int10h.org) | [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) | https://int10h.org/oldschool-pc-fonts/ |
| `PxPlus_IBM_CGA.ttf` | PxPlus IBM CGA | VileR (int10h.org) | [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) | https://int10h.org/oldschool-pc-fonts/ |
| `PetMe64.ttf` | Pet Me 64 | R. Bettencourt / Kreative Korp | [free use — see notice](LICENSES/PetMe64-KreativeKorp.txt) | https://www.kreativekorp.com/software/fonts/c64/ |

## Attribution notes (required by the licenses above)

- **CC BY-SA 4.0 fonts** (PxPlus IBM VGA 8x16, PxPlus IBM CGA): created by
  **VileR** as part of *The Ultimate Oldschool PC Font Pack*
  (https://int10h.org/oldschool-pc-fonts/). The files here are the unmodified
  originals. Any *derivative* of these two fonts must stay under CC BY-SA 4.0;
  this obligation does not extend to the rest of the repo.
- **OFL fonts**: "Monaspace Neon" and the "Cascadia*" names are Reserved Font
  Names — do not ship a *modified* version under those names. Unmodified
  redistribution (as here) is fully permitted.
- **Ubuntu Mono**: "Ubuntu" / "Canonical" are trademarks; the font is
  redistributed under the UFL, which grants no trademark rights.

## Fonts intentionally NOT bundled (removed for legal safety)

These were dropped from the original private bundle before this repo was made
public, because they cannot be redistributed cleanly:

- **Perfect DOS VGA 437** — no license grant embedded (its copyright field only
  points to a now-dead website); an unlicensed clone of the IBM VGA ROM font.
  The `dos` profile now uses **PxPlus IBM VGA 8x16** (CC BY-SA 4.0) instead —
  the same 8×16 IBM VGA glyphs, properly licensed.
- **pokemon-font** — its embedded copyright reads *"Copyright (c) 1996 Game
  Freak and Nintendo"* and the glyphs derive from Nintendo's Pokémon Game Boy
  games. Redistributing it would infringe Nintendo's rights. The `gameboy`
  profile now uses **VT323** (OFL-1.1) for its pixel/CRT look; the Game Boy
  green palette carries the theme.
