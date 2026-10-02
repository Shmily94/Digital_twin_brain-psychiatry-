"""Retarget the absolute paths hard-coded in the figure scripts to THIS package.

Every figure script in 04_figures/ was written with two absolute constants:

    FIGDIR = "<author figure tree>"
    HERE   = os.path.join(FIGDIR, "<figure subdirectory>")

and the five scripts recovered from the analysis session additionally carry the
absolute path of that session's working directory.  The scripts in this package
are BYTE-IDENTICAL COPIES of the ones that produced the submitted figures, so
those constants still point at the author's machine.  This tool rewrites them
to the location of this package, and nothing else: it touches only the path
literals, never a statistic, a parameter or a plotting instruction.

Default is a dry run.  Nothing is written until you pass --apply.

    python tools/retarget_paths.py            # report what would change
    python tools/retarget_paths.py --apply    # rewrite in place (idempotent)
    python tools/retarget_paths.py --restore  # undo, from the .orig backups

Each modified file is backed up once as <name>.orig before its first rewrite,
so --restore always returns the tree to the byte-identical state.

Two implementation notes, both of which were bugs found in testing:

1.  The replacement paths live INSIDE the old revision directory, so replacing
    the three literals in sequence would rewrite the substring just inserted.
    Substitution therefore goes through sentinels and is expanded afterwards.
2.  This file itself contains the literals as constants, so it must exclude
    its own directory from both --apply and --restore, or it rewrites itself
    and the next --restore reverts the tool rather than the figure scripts.
"""
import os
import sys
import shutil

HERE_DIR = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE_DIR)
FIGDIR_NEW = os.path.join(PKG, "04_figures")
RECOVERED_NEW = os.path.join(FIGDIR_NEW, "_recovered_session_b194cd74")
NEW_REVISION = os.path.join(PKG, "06_upstream_inputs")

# The literals as they appear in the shipped copies.  Assembled from fragments
# so that this file is not itself a match for the patterns it rewrites.
_HOME = "/Users/" + "yunman/Desktop/submission"
OLD_REVISION = _HOME + "/revision"
OLD_FIGDIR = OLD_REVISION + "/text/figures"
OLD_RECOVERED = ("/Users/" + "yunman/.claude-science/orgs"
                 "/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/workspaces"
                 "/b194cd74-5255-435a-9c1e-206638f9adae")

# longest first; OLD_REVISION is a prefix of OLD_FIGDIR
SUBS = [(OLD_RECOVERED, RECOVERED_NEW),
        (OLD_FIGDIR, FIGDIR_NEW),
        (OLD_REVISION, NEW_REVISION)]

SKIP_DIRS = {"__pycache__", ".ipynb_checkpoints", "tools"}


def walk_package():
    for root, dirs, files in os.walk(PKG):
        dirs[:] = [d for d in dirs
                   if d not in SKIP_DIRS and os.path.join(root, d) != HERE_DIR]
        if root == HERE_DIR:
            continue
        yield root, files


def iter_scripts():
    for root, files in walk_package():
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(root, f)


def retarget(src):
    """Return (new_source, {literal: count}).  Sentinel-based, see note 1."""
    out = src
    hits = {}
    for i, (old, _new) in enumerate(SUBS):
        if old in out:
            hits[old] = out.count(old)
            out = out.replace(old, "\x00RETARGET%d\x00" % i)
    for i, (_old, new) in enumerate(SUBS):
        out = out.replace("\x00RETARGET%d\x00" % i, new)
    return out, hits


def main(argv):
    apply_ = "--apply" in argv
    restore = "--restore" in argv

    if restore:
        n = 0
        for root, files in walk_package():
            for f in files:
                if f.endswith(".orig"):
                    shutil.copy2(os.path.join(root, f), os.path.join(root, f[:-5]))
                    n += 1
        print("restored %d file(s) from .orig backups" % n)
        return 0

    changed = []
    for p in iter_scripts():
        try:
            src = open(p, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        out, hits = retarget(src)
        if not hits or out == src:
            continue
        changed.append((os.path.relpath(p, PKG), hits))
        if apply_:
            bak = p + ".orig"
            if not os.path.exists(bak):
                shutil.copy2(p, bak)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(out)

    verb = "rewrote" if apply_ else "would rewrite"
    print("%s %d script(s)" % (verb, len(changed)))
    for rel, hits in changed[:12]:
        print("  %s" % rel)
    if len(changed) > 12:
        print("  ... and %d more" % (len(changed) - 12))
    if not apply_ and changed:
        print("\nnothing written. re-run with --apply to perform the rewrite.")
    print("\nFIGDIR    -> %s" % FIGDIR_NEW)
    print("recovered -> %s" % RECOVERED_NEW)
    print("upstream  -> %s" % NEW_REVISION)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
