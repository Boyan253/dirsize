#!/usr/bin/env python3
"""Report the largest files and directories under a path."""

import argparse
import os
import sys

UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]


def human(size):
    value = float(size)
    for unit in UNITS:
        if value < 1024 or unit == UNITS[-1]:
            return "%.1f %s" % (value, unit) if unit != "B" else "%d B" % value
        value /= 1024
    return "%.1f PB" % value


def scan(root, follow_links=False):
    """Return (file_sizes, dir_sizes) for everything under root."""
    files = {}
    dirs = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=follow_links):
        total = 0
        for name in filenames:
            path = os.path.join(dirpath, name)
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            files[path] = size
            total += size
        dirs[dirpath] = dirs.get(dirpath, 0) + total
        # roll the total up into every parent we have already seen
        parent = os.path.dirname(dirpath)
        while parent and parent.startswith(root) and parent != dirpath:
            dirs[parent] = dirs.get(parent, 0) + total
            dirpath, parent = parent, os.path.dirname(parent)
    return files, dirs


def top(sizes, count, min_bytes=0):
    items = [(p, s) for p, s in sizes.items() if s >= min_bytes]
    items.sort(key=lambda kv: kv[1], reverse=True)
    return items[:count]


def parse_size(text):
    text = text.strip().upper()
    for i, unit in enumerate(UNITS):
        if unit != "B" and text.endswith(unit):
            return int(float(text[: -len(unit)]) * (1024 ** i))
    return int(float(text.rstrip("B") or 0))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("-n", "--top", type=int, default=15, help="how many entries to show")
    ap.add_argument("--min", default="0", help="ignore anything smaller, e.g. 10MB")
    ap.add_argument("--files-only", action="store_true")
    ap.add_argument("--dirs-only", action="store_true")
    ap.add_argument("--follow-links", action="store_true")
    args = ap.parse_args(argv)

    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        print("dirsize: not a directory: %s" % root, file=sys.stderr)
        return 2
    files, dirs = scan(root, args.follow_links)
    floor = parse_size(args.min)

    if not args.files_only:
        print("largest directories")
        for path, size in top(dirs, args.top, floor):
            print("  %10s  %s" % (human(size), os.path.relpath(path, root)))
    if not args.dirs_only:
        print("largest files")
        for path, size in top(files, args.top, floor):
            print("  %10s  %s" % (human(size), os.path.relpath(path, root)))
    print("total: %s across %d files" % (human(sum(files.values())), len(files)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
