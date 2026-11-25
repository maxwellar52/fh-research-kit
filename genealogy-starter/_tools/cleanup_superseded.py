"""cleanup_superseded.py — delete every Superseded folder in the Genealogy folder,
except Genealogy/_tools/Superseded (old script versions are kept).

Works on Mac and Windows. By default the Genealogy
folder is the one this script sits in (_tools/..), so it cleans whichever copy
you run it from.

Usage:
    python3 cleanup_superseded.py              # dry run: list what would be deleted
    python3 cleanup_superseded.py --apply      # delete them
    python3 cleanup_superseded.py --root "E:\\Genealogy" --apply   # another copy

On Windows use "py" or "python" in place of "python3".
"""
import argparse
import os
import shutil
import sys

KEEP = os.path.join('_tools', 'Superseded')


def folder_size(path):
    total, count = 0, 0
    for dirpath, _dirs, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(dirpath, f))
                if not f.startswith('._'):
                    count += 1
            except OSError:
                pass
    return total, count


def human(n):
    for unit in ('bytes', 'KB', 'MB', 'GB'):
        if n < 1024 or unit == 'GB':
            return f'{n:.0f} {unit}' if unit == 'bytes' else f'{n:.1f} {unit}'
        n /= 1024


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description='Delete Superseded folders (except _tools/Superseded).')
    ap.add_argument('--root', default=os.path.dirname(here),
                    help='Genealogy folder to clean (default: the folder above _tools)')
    ap.add_argument('--apply', action='store_true', help='actually delete (default is a dry run)')
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    # Safety: only run on a Genealogy folder that has _tools and the tracker in it.
    if not (os.path.isdir(os.path.join(root, '_tools'))
            and os.path.isfile(os.path.join(root, '_AAResearch_Tracker.xlsx'))):
        sys.exit(f'Stopped: {root} has no _tools folder or _AAResearch_Tracker.xlsx, '
                 'so it does not look like the Genealogy folder.')

    keep = os.path.normcase(os.path.join(root, KEEP))
    found = []
    for dirpath, dirs, _files in os.walk(root):
        for d in list(dirs):
            if d == 'Superseded':
                full = os.path.join(dirpath, d)
                dirs.remove(d)          # don't walk inside it
                if os.path.normcase(full) != keep:
                    found.append(full)

    if not found:
        print(f'No Superseded folders to delete in {root} (kept {KEEP}).')
        return

    grand, files = 0, 0
    print(('Deleting' if args.apply else 'DRY RUN — would delete') + f' {len(found)} Superseded folder(s) in {root}:\n')
    for path in sorted(found):
        size, n = folder_size(path)
        grand += size; files += n
        print(f'  {os.path.relpath(path, root)}   ({n} files, {human(size)})')
        if args.apply:
            try:
                shutil.rmtree(path)
            except OSError as e:
                print(f'    !! could not delete: {e}')
    print(f'\nTotal: {files} files, {human(grand)}. Kept: {KEEP}')
    if not args.apply:
        print('Nothing was deleted. Run again with --apply to delete.')


if __name__ == '__main__':
    main()
