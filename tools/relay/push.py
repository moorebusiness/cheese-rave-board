"""Publish one relay snapshot: python3 push.py SNAPSHOT.json  (the object extract.js returns in the State Election Board page).
Writes okrelay.json at the site root, commits, and pushes. Boards apply it within about 30 s of GitHub Pages publishing."""
import json, subprocess, sys
REPO = '/home/claude/cheese-rave-board'
snap = json.load(open(sys.argv[1]))
if 'r' in snap:   # the compact form the browser hands back: [id, rep, [[name, party, votes], ...]]
    snap = {'at': snap['at'], 'asOf': snap.get('asOf'), 'src': 'Oklahoma State Election Board, unofficial',
            'races': [{'id': i, 'rep': rep, 'cands': [{'name': n, 'party': p, 'votes': v} for n, p, v in cs]} for i, rep, cs in snap['r']]}
assert snap.get('at') and snap.get('races'), 'not a relay snapshot'
json.dump(snap, open(f'{REPO}/okrelay.json', 'w'), separators=(',', ':'), ensure_ascii=False)
run = lambda *a: subprocess.run(a, cwd=REPO, check=True, capture_output=True, text=True)
run('git', 'add', 'okrelay.json')
if subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=REPO).returncode == 0:
    print('no change'); sys.exit(0)
run('git', 'commit', '-q', '-m', f"Relay: Oklahoma results as of {snap.get('asOf') or snap['at']}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01JFjUzy5dKmAWyr9kgnnQXE")
run('git', 'pull', '-q', '--rebase', 'origin', 'main'); run('git', 'push', '-q', 'origin', 'main')
print('pushed', snap.get('asOf'), len(snap['races']), 'races')
