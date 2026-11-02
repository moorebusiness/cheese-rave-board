"""Andy's race picks and display tiers for Nov. 3 (sent Nov. 2), applied on top of build_races.py's output. Idempotent.

Tiers (how often a race comes up on a tile; the weights live in board.src.html as TIER_W):
  1  Oklahoma statewide, congressional and the state questions
  2  Oklahoma Legislature and Oklahoma County
  3a other states: the races Andy named
  3b other states: the other toss-ups and battlegrounds
Usage: python3 feature_races.py races.json"""
import json, re, sys

path = sys.argv[1]
R = json.load(open(path))

GOVS = [  # governors added Nov. 2, names as civicAPI lists them for Nov. 3
    ('OH-GOV', 'OHIO GOVERNOR', 'ACTON', 'RAMASWAMY', 'R'),
    ('TX-GOV', 'TEXAS GOVERNOR', 'HINOJOSA', 'ABBOTT', 'R'),
    ('FL-GOV', 'FLORIDA GOVERNOR', 'JOLLY', 'DONALDS', 'R'),
    ('OR-GOV', 'OREGON GOVERNOR', 'KOTEK', 'DRAZAN', 'D'),
]
for id_, label, d, r, held in GOVS:
    if any(x['id'] == id_ for x in R): continue
    at = max(i for i, x in enumerate(R) if str(x.get('key', '')).startswith('G:')) + 1
    R.insert(at, dict(id=id_, label=label, cands=[dict(n=d, p='D'), dict(n=r, p='R')], share=50.0, ch=None, held=held,
                      pool=True, w=1, key='G:' + id_[:2]))
by = {x['id']: x for x in R}

NAMED = ['KY-06', 'IN-05', 'OH-GOV', 'OH-SEN', 'KS-SEN', 'SC-SEN', 'ME-SEN',          # "add these"
         'MI-SEN', 'NE-SEN', 'GA-GOV', 'KS-GOV', 'MN-SEN', 'AK-SEN']                  # "also feature"
TOSSUP_HOUSE = ['CO-05', 'PA-01', 'SC-01']   # Cook Political Report, moved to Toss Up Oct. 30
for i in NAMED + TOSSUP_HOUSE:
    by[i]['pool'] = True

for x in R:
    if x.get('ok'):
        x['tier'] = '2' if re.match(r'OK-(HD|SD)\d|OKCO', x['id']) else '1'
    elif x.get('pool'):
        x['tier'] = '3a' if x['id'] in NAMED else '3b'
    else:
        x.pop('tier', None)
json.dump(R, open(path, 'w'), separators=(',', ':'))
from collections import Counter
print(len(R), 'races; in rotation by tier:', dict(sorted(Counter(x['tier'] for x in R if x.get('pool') and x.get('tier')).items())))
