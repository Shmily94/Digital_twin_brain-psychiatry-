"""Check that the analysis/figure environment can run this package.

    python 00_environment/check_environment.py

Reports the version of every package the figure and analysis scripts import,
flags anything missing, and confirms that the figure data tree is present.
Exits non-zero if a required package is missing.
"""
import importlib
import os
import sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED = {"numpy": "2.4.6", "scipy": "1.17.1", "pandas": "2.3.3",
            "matplotlib": "3.11.1", "statsmodels": "0.14.6",
            "sklearn": "1.9.0", "PIL": "12.3.0", "pptx": "1.0.2",
            "openpyxl": "3.1.5"}
OPTIONAL = {"h5py": "3.16.0 (only for scripts that read simulation output)"}


def check(name, expected, required):
    try:
        mod = importlib.import_module(name)
    except ImportError:
        state = "MISSING" if required else "missing (optional)"
        print("  %-14s %-12s %s" % (name, "-", state))
        return required
    got = getattr(mod, "__version__", "unknown")
    flag = "" if got == expected.split()[0] else "  <- verification used %s" % expected
    print("  %-14s %-12s ok%s" % (name, got, flag))
    return False


def main():
    print("python        %s" % sys.version.split()[0])
    print("\npackages:")
    missing = False
    for n, v in REQUIRED.items():
        missing |= check(n, v, True)
    for n, v in OPTIONAL.items():
        check(n, v, False)

    print("\nfigure tree:")
    figdir = os.path.join(PKG, "04_figures")
    n_data = sum(len([f for f in files if f.endswith((".csv", ".xlsx", ".mat", ".npz"))])
                 for _, _, files in os.walk(figdir))
    n_py = sum(len([f for f in files if f.endswith(".py")])
               for _, _, files in os.walk(figdir))
    print("  %s" % figdir)
    print("  %d data files, %d scripts" % (n_data, n_py))
    if n_data == 0:
        print("  the figure data tree is empty - the package is incomplete")
        missing = True

    print("\npaths:")
    marker = os.path.join(figdir, "fig.4", "fig4_main_A4.py")
    if os.path.exists(marker):
        src = open(marker, encoding="utf-8").read()
        if figdir in src:
            print("  scripts are retargeted to this package")
        else:
            print("  scripts still carry the author's absolute paths")
            print("  run:  python tools/retarget_paths.py --apply")

    print("\n%s" % ("environment incomplete" if missing else "environment ok"))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
