#!/usr/bin/env python3
"""Inventory Codex migration inputs without changing source or reading credentials."""
import argparse, collections, json, os, re, shutil, sqlite3, tempfile
from pathlib import Path

def database_inventory(path, home, available):
    # Copies are diagnostic only: concurrent writers can invalidate a raw copy.
    with tempfile.TemporaryDirectory(prefix='codex-audit-') as temp:
        local = Path(temp) / path.name
        shutil.copyfile(path, local)
        for suffix in ['-wal', '-shm']:
            sidecar = Path(str(path) + suffix)
            if sidecar.is_file():
                shutil.copyfile(sidecar, str(local) + suffix)
        connection = sqlite3.connect('file:' + local.as_posix() + '?mode=ro', uri=True)
        try:
            tables = {r[0] for r in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            report = {'quick_check': connection.execute('PRAGMA quick_check').fetchone()[0]}
            for table in ['threads', 'projects', 'thread_turns', 'thread_items']:
                if table in tables:
                    report[table] = connection.execute('SELECT count(*) FROM "' + table + '"').fetchone()[0]
            if 'threads' in tables:
                cols = {r[1] for r in connection.execute('PRAGMA table_info(threads)')}
                if 'source' in cols:
                    counts = collections.Counter()
                    for (source,) in connection.execute('SELECT source FROM threads'):
                        if source in ['cli', 'vscode', 'app']: counts['interactive_source'] += 1
                        elif 'subagent' in source: counts['subagent_source'] += 1
                        else: counts['other_source'] += 1
                    report['source_categories'] = dict(counts)
                if 'rollout_path' in cols:
                    unresolved = 0
                    for (raw,) in connection.execute('SELECT rollout_path FROM threads'):
                        normalized = raw.replace('\\', '/')
                        match = re.search(r'(?:^|/)(sessions|archived_sessions)/(.+)$', normalized)
                        if match:
                            rel = match.group(1) + '/' + match.group(2)
                            found = rel in available or rel + '.zst' in available
                        else:
                            candidate = Path(raw)
                            found = candidate.is_absolute() and candidate.is_relative_to(home) and candidate.is_file()
                        if not found: unresolved += 1
                    report['unresolved_rollout_paths'] = unresolved
            return report
        finally:
            connection.close()

def audit(home):
    if not home.is_dir(): raise ValueError('Home directory does not exist')
    formats = collections.Counter(); available = set()
    for name in ['sessions', 'archived_sessions']:
        for file in (home / name).rglob('*'):
            if not file.is_file(): continue
            if file.name.endswith('.jsonl.zst'): formats[name + ':jsonl.zst'] += 1
            elif file.name.endswith('.jsonl'): formats[name + ':jsonl'] += 1
            else: continue
            available.add(file.relative_to(home).as_posix())
    report = {'home': str(home), 'rollout_files': dict(formats), 'databases': {}, 'errors': [],
              'consistency_note': 'Temporary raw copies are preliminary; stop writers or use a verified SQLite backup API for migration-grade snapshots.'}
    index = home / 'session_index.jsonl'
    if index.is_file():
        identifiers = set(); lines = invalid = 0
        with index.open(encoding='utf-8-sig') as stream:
            for line in stream:
                if not line.strip(): continue
                lines += 1
                try:
                    row = json.loads(line)
                    if isinstance(row, dict) and row.get('id'): identifiers.add(row['id'])
                except (ValueError, TypeError): invalid += 1
        report['index'] = {'lines': lines, 'unique_ids': len(identifiers), 'invalid_lines': invalid}
    for file in sorted(home.glob('*.sqlite')):
        if not re.fullmatch(r'(state|thread_history)_\d+\.sqlite', file.name): continue
        try: report['databases'][file.name] = database_inventory(file, home, available)
        except (OSError, sqlite3.Error, ValueError) as exc: report['errors'].append({'file': file.name, 'error': str(exc)})
    if not report['databases']: report['warnings'] = ['No readable root state/history database found; check the actual source home and export scope.']
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))))
    arguments = parser.parse_args()
    try: print(json.dumps(audit(arguments.home.expanduser().resolve()), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as exc: parser.exit(1, str(exc) + '\n')
