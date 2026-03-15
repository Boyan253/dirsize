# dirsize

> Find what is eating your disk: the biggest files and folders under a path, human readable.

## Why

Your disk is full and the GUI tools all want to install something. `dirsize` is
one stdlib-only file that tells you where the space went.

## Usage

```
python dirsize.py                       # current directory
python dirsize.py D:/ --top 20          # top 20 directories and files
python dirsize.py . --min 100MB         # ignore small fry
python dirsize.py . --files-only
```

## Output

```
largest directories
     12.4 GB  node_modules
      3.1 GB  .git
largest files
      880 MB  build/app.iso
       41 MB  .git/objects/pack/pack-9f2.pack
total: 16.9 GB across 48210 files
```

Directory totals are cumulative: a parent includes everything beneath it, so
the list reads top-down like a treemap.

## Notes

- Symlinks are not followed unless you pass `--follow-links`, so a loop cannot
  hang the scan.
- Unreadable files are skipped rather than aborting the run.
- `--min` accepts `500KB`, `10MB`, `1.5GB`.

## Tests

```
pip install pytest
pytest
```
