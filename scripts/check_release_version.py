#!/usr/bin/env python3
"""Check VERSION, its package mirror, dated changelog and source-change bump.

Run without arguments for consistency; --base <git-ref> also enforces a bump
for source changes. Docs and CI-only changes do not require a bump.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*))?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?')


def parse(value):
    match = SEMVER.fullmatch(value)
    if not match:
        raise ValueError(f'Invalid bare SemVer: {value!r}')
    return tuple(map(int, match.group(1, 2, 3))), match.group(4)


def newer(current, previous):
    core, pre = parse(current)
    oldcore, oldpre = parse(previous)
    if core != oldcore:
        return core > oldcore
    if pre is None or oldpre is None:
        return pre is None and oldpre is not None
    for a, b in zip(pre.split('.'), oldpre.split('.')):
        if a == b:
            continue
        if a.isdigit() and b.isdigit():
            return int(a) > int(b)
        if a.isdigit() != b.isdigit():
            return not a.isdigit()
        return a > b
    return len(pre.split('.')) > len(oldpre.split('.'))


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('--base')
    base = args.parse_args().base
    version = (ROOT / 'VERSION').read_text().strip()
    parse(version)
    package = ROOT / 'package.json'
    if package.exists() and json.loads(package.read_text()).get('version') != version:
        raise ValueError('package.json version must match VERSION')
    lock = ROOT / 'package-lock.json'
    if lock.exists():
        data = json.loads(lock.read_text())
        if data.get('version') != version or data.get('packages', {}).get('', {}).get('version', version) != version:
            raise ValueError('package-lock.json version must match VERSION')
    changelog = (ROOT / 'CHANGELOG.md').read_text()
    if not re.search(r'^## \[Unreleased\]\s*$', changelog, re.M):
        raise ValueError('CHANGELOG.md needs an Unreleased section')
    if not re.search(r'^## \[' + re.escape(version) + r'\] - \d{4}-\d{2}-\d{2}\s*$', changelog, re.M):
        raise ValueError(f'CHANGELOG.md needs a dated [{version}] section')
    if base:
        files = git('diff', '--name-only', '--no-renames', f'{base}...HEAD').splitlines()
        source = [p for p in files if not (p.endswith(('.md', '.txt')) or p.startswith(('docs/', '.github/')))]
        had_version = subprocess.run(['git', 'cat-file', '-e', f'{base}:VERSION'], cwd=ROOT, capture_output=True).returncode == 0
        if had_version:
            previous = git('show', f'{base}:VERSION')
            if version != previous and not newer(version, previous):
                raise ValueError('VERSION must increase; build metadata alone is not a bump')
            if source and not newer(version, previous):
                raise ValueError('Source changed without a VERSION bump')
    print(f'Version check OK: {version}')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(f'Version check FAILED: {error}')
