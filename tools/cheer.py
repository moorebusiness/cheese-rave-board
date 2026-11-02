#!/usr/bin/env python3
"""Celebrate a result on every Cheese Rave board.

Writes cheer.json at the site root, commits it and pushes. Every open board checks cheer.json every 20 seconds and
GitHub Pages publishes in about a minute, so the celebration appears one to two minutes after this runs.

  python3 tools/cheer.py "SQ 845 DEFEATED" --kicker "OKLAHOMA VOTERS SAY NO" --sub "THE JUDICIAL PANEL STAYS AS IT IS" --race SQ845
  python3 tools/cheer.py "TEST" --kicker "THIS IS ONLY A TEST" --secs 10      # a rehearsal
  python3 tools/cheer.py ... --dry-run                                         # write cheer.json, don't commit

--race takes a board race id (SQ845, SQ847, OK-05, GA-SEN, NC-SEN ...; see src/races.json). The board then shows that
race's current split under the headline, from its own live numbers. --secs is how long it holds (8-90, default 25).
"""
import argparse, json, subprocess, sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
p = argparse.ArgumentParser()
p.add_argument('headline')
p.add_argument('--kicker', default='')
p.add_argument('--sub', default='')
p.add_argument('--race', default='')
p.add_argument('--secs', type=int, default=25)
p.add_argument('--dry-run', action='store_true')
a = p.parse_args()

races = {r['id'] for r in json.loads((ROOT / 'src' / 'races.json').read_text())}
if a.race and a.race not in races:
    print(f'note: {a.race} is not in src/races.json; the board will show no numbers unless it loads that id live', file=sys.stderr)
now = datetime.now(ZoneInfo('America/Chicago'))
cheer = {'id': 'c' + now.strftime('%Y%m%d-%H%M%S'), 'at': now.isoformat(timespec='seconds'), 'kicker': a.kicker,
         'headline': a.headline, 'sub': a.sub, 'race': a.race, 'secs': max(8, min(90, a.secs))}
(ROOT / 'cheer.json').write_text(json.dumps(cheer, indent=2) + '\n')
print(json.dumps(cheer, indent=2))
if a.dry_run:
    sys.exit(0)
git = lambda *args: subprocess.run(['git', '-C', str(ROOT), *args], check=True)
git('add', 'cheer.json')
git('commit', '-q', '-m', f'Celebrate: {a.headline}')
git('pull', '-q', '--rebase', 'origin', 'main')
git('push', '-q', 'origin', 'main')
print(f'pushed at {now:%I:%M:%S %p} Central; boards show it in about 1-2 minutes')
