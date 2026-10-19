#!/usr/bin/env python3
"""Read-only Hermes inventory; no credential values, message text or task execution."""
import argparse, collections, json, os, shutil, sqlite3, tempfile
from pathlib import Path

def database_inventory(path):
    with tempfile.TemporaryDirectory(prefix='hermes-audit-') as temp:
        local = Path(temp) / path.name
        shutil.copyfile(path, local)
        for suffix in ['-wal', '-shm']:
            sidecar = Path(str(path) + suffix)
            if sidecar.is_file(): shutil.copyfile(sidecar, str(local) + suffix)
        connection = sqlite3.connect('file:' + local.as_posix() + '?mode=ro', uri=True)
        try:
            tables = {r[0] for r in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            result = {'quick_check': connection.execute('PRAGMA quick_check').fetchone()[0]}
            for table in ['sessions', 'messages']:
                if table in tables:
                    result[table] = connection.execute('SELECT count(*) FROM "' + table + '"').fetchone()[0]
            return result
        finally: connection.close()

def audit(home, tools):
    if not home.is_dir(): raise ValueError('Home directory does not exist')
    report = {'home': str(home), 'skills': sum(1 for _ in (home / 'skills').rglob('SKILL.md')),
              'configuration_files_present': {name: (home / name).is_file() for name in ['config.yaml', '.env', 'auth.json']},
              'cli_discovery': {tool: shutil.which(tool) is not None for tool in tools}, 'errors': [],
              'consistency_note': 'Temporary raw copies are preliminary; use official full backup and stop target writers before restore. CLI discovery does not prove working credentials or business workflows.'}
    database = home / 'state.db'
    if database.is_file():
        try: report['state_database'] = database_inventory(database)
        except (OSError, sqlite3.Error) as exc: report['errors'].append({'file': 'state.db', 'error': str(exc)})
    else: report['warnings'] = ['state.db not found; confirm active home/profile.']
    jobs_file = home / 'cron/jobs.json'
    if jobs_file.is_file():
        try:
            data = json.loads(jobs_file.read_text(encoding='utf-8-sig'))
            jobs = data.get('jobs', data) if isinstance(data, dict) else data
            if isinstance(jobs, dict): jobs = list(jobs.values())
            if not isinstance(jobs, list): raise ValueError('Unrecognized jobs shape; inspect current version')
            states = collections.Counter()
            for job in jobs:
                if not isinstance(job, dict): states['unrecognized'] += 1; continue
                state = job.get('status')
                if state is not None: states[str(state)] += 1
                elif job.get('paused_at') is not None or job.get('paused') is True: states['paused'] += 1
                elif job.get('enabled') is False: states['disabled'] += 1
                else: states['unspecified'] += 1
            report['cron'] = {'definitions': len(jobs), 'raw_or_inferred_states': dict(states)}
        except (OSError, ValueError, TypeError) as exc: report['errors'].append({'file': 'cron/jobs.json', 'error': str(exc)})
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path(os.environ.get('HERMES_HOME', str(Path.home() / '.hermes'))))
    parser.add_argument('--check-cli', action='append', help='Repeat for business-specific CLIs; only checks discovery, never runs them.')
    arguments = parser.parse_args()
    try: print(json.dumps(audit(arguments.home.expanduser().resolve(), arguments.check_cli or ['hermes']), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as exc: parser.exit(1, str(exc) + '\n')
