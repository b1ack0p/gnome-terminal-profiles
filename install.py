#!/usr/bin/env python3
"""Offline installer for GNOME Terminal color profiles + themed fonts.

Everything is bundled (color data embedded, fonts in ./fonts/) -- NO network needed.

Usage:
  python3 install.py                 install / update all profiles (asks: themed or system font)
  python3 install.py --system-font   ... use your system monospace font for every profile
  python3 install.py --themed-fonts  ... use the matching bundled font per profile
  python3 install.py --uninstall     remove the profiles and the installed fonts

Profiles appear in GNOME Terminal > Preferences. Re-running updates in place
(deterministic UUIDs, no duplicates). Requires `dconf` and gnome-terminal.
"""
import os, re, shutil, subprocess, sys, uuid

HERE     = os.path.dirname(os.path.abspath(__file__))
FONT_SRC = os.path.join(HERE, "fonts")
FONT_DST = os.path.expanduser("~/.local/share/fonts/gnome-terminal-themes")
BASE     = "/org/gnome/terminal/legacy/profiles:/"
NS       = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

SCHEMES = {
    "batman": {
        "fg": "#6f6f6f",
        "bg": "#1b1d1e",
        "palette": [
            "#1b1d1e",
            "#e6dc44",
            "#c8be46",
            "#f4fd22",
            "#737174",
            "#747271",
            "#62605f",
            "#c6c5bf",
            "#505354",
            "#fff78e",
            "#fff27d",
            "#feed6c",
            "#919495",
            "#9a9a9d",
            "#a3a3a6",
            "#dadbd6"
        ],
        "cursor": "#fcef0c"
    },
    "blueprint": {
        "fg": "#ffffff",
        "bg": "#0e3a6b",
        "palette": [
            "#07223f",
            "#2e5680",
            "#466e96",
            "#5e86ac",
            "#3a628c",
            "#527aa2",
            "#6a92b8",
            "#c3d5e8",
            "#143f6e",
            "#426a94",
            "#5a82aa",
            "#729ac0",
            "#4e76a0",
            "#668eb6",
            "#7ea6cc",
            "#ffffff"
        ]
    },
    "c64.16color": {
        "fg": "#706deb",
        "bg": "#2e2c9b",
        "cursor": "#706deb",
        "palette": [
            "#000000",
            "#ffffff",
            "#813338",
            "#75cec8",
            "#8e3c97",
            "#56ac4d",
            "#706deb",
            "#edf171",
            "#8e5029",
            "#553800",
            "#c46c71",
            "#4a4a4a",
            "#7b7b7b",
            "#a9ff9f",
            "#706deb",
            "#b2b2b2"
        ]
    },
    "c64.8color": {
        "fg": "#706deb",
        "bg": "#2e2c9b",
        "cursor": "#706deb",
        "palette": [
            "#000000",
            "#813338",
            "#56ac4d",
            "#edf171",
            "#706deb",
            "#8e3c97",
            "#75cec8",
            "#ffffff",
            "#000000",
            "#813338",
            "#56ac4d",
            "#edf171",
            "#706deb",
            "#8e3c97",
            "#75cec8",
            "#ffffff"
        ]
    },
    "cga": {
        "fg": "#ffffff",
        "bg": "#000000",
        "palette": [
            "#000000",
            "#0000aa",
            "#00aa00",
            "#00aaaa",
            "#aa0000",
            "#aa00aa",
            "#aa5500",
            "#aaaaaa",
            "#555555",
            "#5555ff",
            "#55ff55",
            "#55ffff",
            "#ff5555",
            "#ff55ff",
            "#ffff55",
            "#ffffff"
        ]
    },
    "cmyk": {
        "fg": "#aaaaaa",
        "bg": "#000000",
        "palette": [
            "#000000",
            "#ec008c",
            "#fff200",
            "#fff200",
            "#00aeef",
            "#ec008c",
            "#00aeef",
            "#ffffff",
            "#000000",
            "#ec008c",
            "#fff200",
            "#fff200",
            "#00aeef",
            "#ec008c",
            "#00aeef",
            "#ffffff"
        ],
        "cursor": "#fff200"
    },
    "cyberpunk": {
        "fg": "#0abdc6",
        "bg": "#0d0221",
        "cursor": "#ea00d9",
        "palette": [
            "#0d0221",
            "#ff2740",
            "#00ff5f",
            "#f9f002",
            "#0a84ff",
            "#ea00d9",
            "#08f7fe",
            "#d7d7f5",
            "#3b3b6d",
            "#ff4d5e",
            "#4dff8f",
            "#fbff4d",
            "#5ca9ff",
            "#ff5ff1",
            "#62fdff",
            "#ffffff"
        ]
    },
    "dos": {
        "fg": "#aaaaaa",
        "bg": "#000000",
        "palette": [
            "#000000",
            "#0000aa",
            "#00aa00",
            "#00aaaa",
            "#aa0000",
            "#aa00aa",
            "#aa5500",
            "#aaaaaa",
            "#555555",
            "#5555ff",
            "#55ff55",
            "#55ffff",
            "#ff5555",
            "#ff55ff",
            "#ffff55",
            "#ffffff"
        ]
    },
    "firefox": {
        "fg": "#7c8fa4",
        "bg": "#0e1011",
        "palette": [
            "#002831",
            "#e63853",
            "#5eb83c",
            "#a57706",
            "#359ddf",
            "#d75cff",
            "#4b73a2",
            "#dcdcdc",
            "#26444d",
            "#e1003f",
            "#1d9000",
            "#cd9409",
            "#006fc0",
            "#a200da",
            "#005794",
            "#e2e2e2"
        ],
        "cursor": "#708284"
    },
    "gameboy": {
        "fg": "#9bbc0f",
        "bg": "#0f380f",
        "palette": [
            "#0f380f",
            "#1e481a",
            "#2d5824",
            "#4a722a",
            "#396625",
            "#5a8420",
            "#6f981a",
            "#8bac0f",
            "#306230",
            "#3c6a28",
            "#58851a",
            "#7ba512",
            "#4a7622",
            "#6f981a",
            "#8bac0f",
            "#9bbc0f"
        ],
        "cursor": "#9bbc0f"
    },
    "github.light": {
        "fg": "#1f2328",
        "bg": "#ffffff",
        "palette": [
            "#24292f",
            "#cf222e",
            "#116329",
            "#4d2d00",
            "#0969da",
            "#8250df",
            "#1b7c83",
            "#6e7781",
            "#57606a",
            "#a40e26",
            "#1a7f37",
            "#633c01",
            "#218bff",
            "#a475f9",
            "#3192aa",
            "#8c959f"
        ],
        "cursor": "#1f2328"
    },
    "github.dark": {
        "fg": "#e6edf3",
        "bg": "#0d1117",
        "palette": [
            "#484f58",
            "#ff7b72",
            "#3fb950",
            "#d29922",
            "#58a6ff",
            "#bc8cff",
            "#39c5cf",
            "#b1bac4",
            "#6e7681",
            "#ffa198",
            "#56d364",
            "#e3b341",
            "#79c0ff",
            "#d2a8ff",
            "#56d4dd",
            "#ffffff"
        ],
        "cursor": "#e6edf3"
    },
    "hulk": {
        "fg": "#b5b5b5",
        "bg": "#1b1d1e",
        "palette": [
            "#1b1d1e",
            "#269d1b",
            "#13ce30",
            "#63e457",
            "#2525f5",
            "#641f74",
            "#378ca9",
            "#d9d8d1",
            "#505354",
            "#8dff2a",
            "#48ff77",
            "#3afe16",
            "#506b95",
            "#72589d",
            "#4085a6",
            "#e5e6e1"
        ],
        "cursor": "#16b61b"
    },
    "minecraft": {
        "fg": "#aaaaaa",
        "bg": "#000000",
        "palette": [
            "#000000",
            "#0000aa",
            "#00aa00",
            "#00aaaa",
            "#aa0000",
            "#aa00aa",
            "#ffaa00",
            "#aaaaaa",
            "#555555",
            "#5555ff",
            "#55ff55",
            "#55ffff",
            "#ff5555",
            "#ff55ff",
            "#ffff55",
            "#ffffff"
        ],
        "cursor": "#aaaaaa"
    },
    "mono.black": {
        "fg": "#ffffff",
        "bg": "#000000",
        "palette": [
            "#000000",
            "#2e2e2e",
            "#4a4a4a",
            "#666666",
            "#828282",
            "#9e9e9e",
            "#bababa",
            "#d6d6d6",
            "#1c1c1c",
            "#3a3a3a",
            "#565656",
            "#727272",
            "#8e8e8e",
            "#aaaaaa",
            "#c6c6c6",
            "#ffffff"
        ]
    },
    "mono.white": {
        "fg": "#000000",
        "bg": "#ffffff",
        "palette": [
            "#000000",
            "#101010",
            "#202020",
            "#303030",
            "#404040",
            "#505050",
            "#606060",
            "#707070",
            "#181818",
            "#282828",
            "#383838",
            "#484848",
            "#585858",
            "#686868",
            "#787878",
            "#888888"
        ]
    },
    "pepsi": {
        "fg": "#ffffff",
        "bg": "#004b93",
        "cursor": "#e32934",
        "palette": [
            "#000000",
            "#e32934",
            "#ffffff",
            "#e32934",
            "#87ceeb",
            "#e32934",
            "#87ceeb",
            "#ffffff",
            "#4a76b0",
            "#ff8a91",
            "#ffffff",
            "#ff8a91",
            "#b8e2f5",
            "#ff8a91",
            "#b8e2f5",
            "#ffffff"
        ]
    },
    "phosphor.amber": {
        "fg": "#ffb000",
        "bg": "#282828",
        "palette": [
            "#664600",
            "#7f5800",
            "#cc8c00",
            "#e59e00",
            "#664600",
            "#996900",
            "#b27b00",
            "#ffb000",
            "#664600",
            "#7f5800",
            "#cc8c00",
            "#e59e00",
            "#664600",
            "#996900",
            "#b27b00",
            "#ffb000"
        ]
    },
    "phosphor.blue": {
        "fg": "#00a3dd",
        "bg": "#282828",
        "palette": [
            "#004158",
            "#00516e",
            "#0082b0",
            "#0092c6",
            "#004158",
            "#006184",
            "#00729a",
            "#00a3dd",
            "#004158",
            "#00516e",
            "#0082b0",
            "#0092c6",
            "#004158",
            "#006184",
            "#00729a",
            "#00a3dd"
        ]
    },
    "phosphor.green": {
        "fg": "#33ff33",
        "bg": "#282828",
        "palette": [
            "#146614",
            "#1a801a",
            "#29cc29",
            "#2ee62e",
            "#146614",
            "#1f991f",
            "#24b324",
            "#33ff33",
            "#146614",
            "#1a801a",
            "#29cc29",
            "#2ee62e",
            "#146614",
            "#1f991f",
            "#24b324",
            "#33ff33"
        ]
    },
    "powershell": {
        "fg": "#eeedf0",
        "bg": "#012456",
        "palette": [
            "#000000",
            "#800000",
            "#008000",
            "#808000",
            "#000080",
            "#800080",
            "#008080",
            "#c0c0c0",
            "#808080",
            "#ff0000",
            "#00ff00",
            "#ffff00",
            "#0000ff",
            "#ff00ff",
            "#00ffff",
            "#ffffff"
        ]
    },
    "solarized.dark": {
        "fg": "#657b83",
        "bg": "#002b36",
        "palette": [
            "#073642",
            "#dc322f",
            "#859900",
            "#b58900",
            "#268bd2",
            "#d33682",
            "#2aa198",
            "#eee8d5",
            "#002b36",
            "#cb4b16",
            "#586e75",
            "#657b83",
            "#839496",
            "#6c71c4",
            "#93a1a1",
            "#fdf6e3"
        ],
        "cursor": "#93a1a1"
    },
    "solarized.light": {
        "fg": "#839496",
        "bg": "#fdf6e3",
        "palette": [
            "#eee8d5",
            "#dc322f",
            "#859900",
            "#b58900",
            "#268bd2",
            "#d33682",
            "#2aa198",
            "#073642",
            "#fdf6e3",
            "#cb4b16",
            "#93a1a1",
            "#839496",
            "#657b83",
            "#6c71c4",
            "#586e75",
            "#002b36"
        ],
        "cursor": "#586e75"
    },
    "ubuntu": {
        "fg": "#ffffff",
        "bg": "#300a24",
        "palette": [
            "#171421",
            "#c01c28",
            "#26a269",
            "#a2734c",
            "#12488b",
            "#a347ba",
            "#2aa1b3",
            "#d0cfcc",
            "#5e5c64",
            "#f66151",
            "#33d17a",
            "#e9ad0c",
            "#2a7bde",
            "#c061cb",
            "#33c7de",
            "#ffffff"
        ]
    },
    "vscode": {
        "fg": "#cccccc",
        "bg": "#1e1e1e",
        "palette": [
            "#000000",
            "#cd3131",
            "#0dbc79",
            "#e5e510",
            "#2472c8",
            "#bc3fbc",
            "#11a8cd",
            "#e5e5e5",
            "#666666",
            "#f14c4c",
            "#23d18b",
            "#f5f543",
            "#3b8eea",
            "#d670d6",
            "#29b8db",
            "#e5e5e5"
        ]
    },
    "winterminal": {
        "fg": "#cccccc",
        "bg": "#0c0c0c",
        "palette": [
            "#0c0c0c",
            "#c50f1f",
            "#13a10e",
            "#c19c00",
            "#0037da",
            "#881798",
            "#3a96dd",
            "#cccccc",
            "#767676",
            "#e74856",
            "#16c60c",
            "#f9f1a5",
            "#3b78ff",
            "#b4009e",
            "#61d6d6",
            "#f2f2f2"
        ]
    }
}
FONTS   = {
    "ubuntu": [
        "Ubuntu Mono",
        13
    ],
    "winterminal": [
        "Cascadia Code",
        12
    ],
    "powershell": [
        "Cascadia Mono",
        12
    ],
    "firefox": [
        "Fira Mono",
        12
    ],
    "github.light": [
        "Monaspace Neon Frozen",
        12
    ],
    "github.dark": [
        "Monaspace Neon Frozen",
        12
    ],
    "dos": [
        "PxPlus IBM VGA 8x16",
        12
    ],
    "cga": [
        "PxPlus IBM CGA",
        12
    ],
    "c64.16color": [
        "Pet Me 64",
        12
    ],
    "c64.8color": [
        "Pet Me 64",
        12
    ],
    "gameboy": [
        "VT323",
        16
    ],
    "minecraft": [
        "Monocraft",
        13
    ],
    "phosphor.amber": [
        "VT323",
        16
    ],
    "phosphor.green": [
        "VT323",
        16
    ],
    "phosphor.blue": [
        "VT323",
        16
    ],
    "mono.black": [
        "Courier Prime",
        12
    ],
    "mono.white": [
        "Courier Prime",
        12
    ]
}

def dconf(a, **k): return subprocess.run(["dconf"]+a, capture_output=True, text=True, **k)
def read_list():   return re.findall(r"'([^']*)'", dconf(["read", BASE+"list"]).stdout)
def q(s):          return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
def pid_for(n):    return str(uuid.uuid5(NS, "gnome-terminal-theme:"+n))

SAVED_PID = pid_for("default-backup")   # a copy of the user's pre-install default, named 'default'

def snapshot_default(ids):
    """Copy the user's current default profile into a new profile named 'default' (once)."""
    if SAVED_PID in ids: return
    cur = dconf(["read", BASE + "default"]).stdout.strip().strip("'")
    if not cur or cur == SAVED_PID: return
    src  = dconf(["dump", BASE + ":" + cur + "/"]).stdout
    keys = [ln for ln in src.splitlines() if "=" in ln and not ln.startswith("visible-name=")]
    dconf(["load", BASE], input="[:%s]\nvisible-name='default'\n%s\n" % (SAVED_PID, "\n".join(keys)))
    ids.append(SAVED_PID)
    print("Saved your current default profile as a new 'default' profile.")

def install_fonts():
    os.makedirs(FONT_DST, exist_ok=True)
    n = 0
    for f in sorted(os.listdir(FONT_SRC)):
        if f.lower().endswith((".ttf", ".otf", ".ttc")):
            shutil.copy2(os.path.join(FONT_SRC, f), os.path.join(FONT_DST, f)); n += 1
    subprocess.run(["fc-cache", "-f", FONT_DST])
    return n

def choose_font_mode():
    """Themed bundled fonts, or the user's system monospace font? Flag, else prompt."""
    if "--system-font" in sys.argv:                            return "system"
    if "--themed-fonts" in sys.argv or "--themed" in sys.argv:  return "themed"
    if not sys.stdin.isatty():                                  return "themed"  # non-interactive default
    print("Font for the terminal profiles:")
    print("  [1] Themed fonts  - each profile uses its matching bundled font (default)")
    print("  [2] System font   - every profile uses your current system monospace font")
    try:
        ans = input("Choose [1/2] (default 1): ").strip().lower()
    except EOFError:
        ans = ""
    return "system" if ans in ("2", "system", "s") else "themed"

def install(font_mode):
    if not shutil.which("dconf"): sys.exit("`dconf` not found -> sudo apt install dconf-cli")
    if font_mode == "themed":
        print("Installing %d fonts (offline) -> %s" % (install_fonts(), FONT_DST))
    else:
        print("Font mode: system monospace for every profile (skipping themed-font install).")
    ids = read_list()
    dump = ""
    sysfont_pids = []
    for name, sc in SCHEMES.items():
        pid = pid_for(name)
        if pid not in ids: ids.append(pid)
        pal = "[" + ", ".join(q(c) for c in sc["palette"]) + "]"
        dump += "[:%s]\n" % pid
        dump += "visible-name=%s\n" % q(name)
        dump += "use-theme-colors=false\n"
        dump += "foreground-color=%s\n" % q(sc["fg"])
        dump += "background-color=%s\n" % q(sc["bg"])
        dump += "bold-color-same-as-fg=true\n"
        dump += "palette=%s\n" % pal
        if sc.get("cursor"):
            dump += "cursor-colors-set=true\n"
            dump += "cursor-background-color=%s\n" % q(sc["cursor"])
            dump += "cursor-foreground-color=%s\n" % q(sc["bg"])
        else:
            dump += "cursor-colors-set=false\n"
        if font_mode == "themed" and name in FONTS:
            fam, size = FONTS[name]
            dump += "use-system-font=false\n"
            dump += "font=%s\n" % q("%s %d" % (fam, size))
        else:
            dump += "use-system-font=true\n"
            sysfont_pids.append(pid)
        dump += "\n"
    # snapshot the user's current default into a 'default' profile (once), then
    # make cyberpunk the default profile
    snapshot_default(ids)
    dump += "[/]\nlist=[%s]\ndefault=%s\n" % (", ".join(q(i) for i in ids), q(pid_for("cyberpunk")))
    if subprocess.run(["dconf", "load", BASE], input=dump, text=True).returncode == 0:
        # dconf load can't unset keys, so clear any stale custom font on system-font profiles
        for pid in sysfont_pids:
            dconf(["reset", BASE + ":" + pid + "/font"])
        print("Installed/updated %d GNOME Terminal profiles (%s font); default profile = cyberpunk." % (len(SCHEMES), font_mode))
        print('Pick any from the GNOME Terminal profile menu / Preferences (default is cyberpunk).')
    else:
        sys.exit("dconf load failed (is a GNOME session / dbus available?)")

def uninstall():
    ours = {pid_for(n) for n in SCHEMES}
    ids  = [i for i in read_list() if i not in ours]
    for pid in ours: dconf(["reset", "-f", BASE+":"+pid+"/"])
    # point the default back at the saved 'default' profile (kept), else clear our default
    if SAVED_PID in ids:
        dconf(["write", BASE+"default", q(SAVED_PID)])
    elif dconf(["read", BASE+"default"]).stdout.strip().strip("'") in ours:
        dconf(["reset", BASE+"default"])
    subprocess.run(["dconf", "load", BASE], text=True, input="[/]\nlist=[%s]\n" % ", ".join(q(i) for i in ids))
    if os.path.isdir(FONT_DST):
        shutil.rmtree(FONT_DST); subprocess.run(["fc-cache", "-f"])
    print("Removed %d profiles and the installed fonts; default set back to the 'default' profile." % len(ours))

if __name__ == "__main__":
    if "--uninstall" in sys.argv:
        uninstall()
    else:
        install(choose_font_mode())
