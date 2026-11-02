"""Andy's national picks for Nov. 3 (sent Nov. 2), applied on top of build_races.py's output:
adds Ohio governor, puts every named race in rotation at the top weight, and adds the House races Cook
moved to Toss Up on Oct. 30 (CO-05, PA-01, SC-01). Idempotent.
Usage: python3 feature_races.py races.json"""
import json, sys

path = sys.argv[1]
R = json.load(open(path))
by = {r['id']: r for r in R}

if 'OH-GOV' not in by:   # civicAPI: Amy Acton (D), Vivek Ramaswamy (R), plus a Libertarian and write-ins
    at = max(i for i, r in enumerate(R) if str(r.get('key', '')).startswith('G:')) + 1
    R.insert(at, dict(id='OH-GOV', label='OHIO GOVERNOR', cands=[dict(n='ACTON', p='D'), dict(n='RAMASWAMY', p='R')],
                      share=50.4, ch=None, held='R', pool=True, w=5, key='G:OH'))
    by = {r['id']: r for r in R}

FEATURED = ['KY-06', 'IN-05', 'OH-GOV', 'OH-SEN', 'KS-SEN', 'SC-SEN', 'ME-SEN',          # "add these"
            'MI-SEN', 'NE-SEN', 'GA-GOV', 'KS-GOV', 'MN-SEN', 'AK-SEN']                  # "also feature"
TOSSUP_HOUSE = ['CO-05', 'PA-01', 'SC-01']   # Cook Political Report, moved to Toss Up Oct. 30

for i in FEATURED:
    by[i].update(pool=True, w=5)
for i in TOSSUP_HOUSE:
    by[i].update(pool=True)
json.dump(R, open(path, 'w'), separators=(',', ':'))
nat = [r for r in R if r.get('pool') and not r.get('ok')]
print(len(R), 'races;', len(nat), 'national in rotation;', sum(1 for r in nat if r['w'] >= 5), 'featured')
