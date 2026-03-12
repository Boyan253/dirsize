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
