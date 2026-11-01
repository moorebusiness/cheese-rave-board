"""Build races.json for the Cheese Rave board from ElectionHub's race lists.

Real races and nominees come from ElectionHub (baseline.json, statewide/baseline.json,
initiatives/data.json, states/baseline.json). Sample vote shares are invented for the demo.
Races ElectionHub doesn't carry are marked src="gap" and use placeholder candidate names.
Usage: python3 build_races.py <electionhub_dir> <out.json>
"""
import json, random, sys

src, out_path = sys.argv[1], sys.argv[2]
b = json.load(open(f'{src}/baseline.json'))
sw = json.load(open(f'{src}/statewide_baseline.json'))
st = json.load(open(f'{src}/states_baseline.json'))
random.seed(7)

OV = {"N'Kiyla Jasmine Thomas": "Thomas", "Keisha Lance Bottoms": "Lance Bottoms", "Monica De La Cruz": "De La Cruz", "Carlos De La Cruz": "De La Cruz",
      "Kristen McDonald Rivet": "McDonald Rivet", "Marie Gluesenkamp Perez": "Gluesenkamp Perez", "María Elvira Salazar": "Salazar"}
SUF = {"Jr.", "Sr.", "II", "III", "IV"}
def sur(n):
    if n in OV: return OV[n].upper()
    t = n.split()
    return (" ".join(t[-2:]) if t[-1] in SUF else t[-1]).upper()

SH = {'Lean D': 53.5, 'Lean R': 46.5, 'Likely D': 56, 'Likely R': 44, 'Solid R': 38, 'Solid D': 62, 'Watch': 45}
def share(r):
    rt = r.get('rating')
    if rt == 'Toss Up': return round(50 + random.uniform(-3, 3), 1)
    if rt == 'Redrawn': return 42.0 if r['held'] == 'D' else 58.0
    return SH.get(rt, 50) + round(random.uniform(-2, 2), 1)

out = []
def add(**k): out.append(k)
DR = lambda d, r, dp='D': [dict(n=sur(d), p=dp), dict(n=sur(r), p='R')]

# National (pink)
for s in b['senate']:
    add(id=s['id'], label=f"{s['state'].upper()} SENATE", cands=DR(s['dem'], s['rep'], s.get('demParty', 'D')),
        share=share(s), ch='S', held=s['held'], pool=True, w=4 if s['rating'] == 'Toss Up' else 2.5, key='S:' + s['st'])
for r in b['races']:
    d = r['district']
    add(id=r['id'], label=f"{r['state'].upper()} {'AT-LARGE' if not d.isdigit() else int(d)}", cands=DR(r['dem'], r['rep']),
        share=share(r), ch='H', held=r['held'], pool=r['rating'] == 'Toss Up', w=1.5, key='H:' + r['id'])
for r in sw['races']:
    if r.get('rating') == 'Toss Up' and r['st'] != 'OK':
        add(id=r['id'], label=f"{r['state'].upper()} GOVERNOR", cands=DR(r['dem'], r['rep']), share=share(r),
            ch=None, held=r['held'], pool=True, w=2, key='G:' + r['st'])

# Oklahoma (turquoise). Statewide, federal and county candidates as civicAPI lists them for Nov. 3
# (checked Oct. 31); legislative candidates from ElectionHub. The live board rebuilds this list from civicAPI.
OKC = [  # id, label, weight, [(name, party)...] -- first candidate's sample share is the 4th field
    ('OK-GOV', 'OKLAHOMA GOVERNOR', 4, [('Cyndi Munson', 'D'), ('Mike Mazzei', 'R')], 42),
    ('OK-05', 'OKLAHOMA 5', 2, [('Jena Nelson', 'D'), ('Stephanie Bice', 'R')], 44),
    ('OK-LG', 'OK LT. GOVERNOR', 2.5, [('Kelly Forbes', 'D'), ('T. W. Shannon', 'R')], 37),
    ('OK-AG', 'OK ATTORNEY GENERAL', 2.5, [('Nick Coffey', 'D'), ('Jon Echols', 'R')], 36),
    ('OK-TREAS', 'OK TREASURER', 2, [('Cindy Byrd', 'R'), ('Kiefer Perry', 'L')], 76),
    ('OK-SUPT', 'OK SUPERINTENDENT', 2.5, [('Jennettie Marshall', 'D'), ('Robert Franklin', 'R')], 39),
    ('OK-LABOR', 'OK LABOR COMMISSIONER', 2, [('Kevin Dawson', 'D'), ('Kevin West', 'R')], 36),
    ('OK-INS', 'OK INSURANCE COMM.', 2, [('Craig MacIntyre', 'D'), ('Bob Sullivan', 'R')], 37),
    ('OK-CORP', 'OK CORPORATION COMM.', 2, [('Rhonda Eastman', 'D'), ('Brad Boles', 'R')], 36),
    ('OK-SEN', 'OK U.S. SENATE', 2.5, [("N'Kiyla Jasmine Thomas", 'D'), ('Kevin Hern', 'R')], 35),
    ('OK-01', 'OKLAHOMA 1', 2, [('John Croisant', 'D'), ('Mark Tedford', 'R')], 38),
    ('OK-02', 'OKLAHOMA 2', 2, [('Brandon Wade', 'D'), ('Josh Brecheen', 'R')], 25),
    ('OK-03', 'OKLAHOMA 3', 2, [('Suzie Byrd', 'D'), ('Frank Lucas', 'R')], 27),
    ('OK-04', 'OKLAHOMA 4', 2, [('Mitchell Jacob', 'D'), ('Tom Cole', 'R')], 33),
    ('OKCO-TREASU', 'OK COUNTY TREASURER', 1.5, [('Jessica Thompson', 'D'), ('Christie K. Miller', 'R')], 51),
    ('OKCO-ASSESS', 'OK COUNTY ASSESSOR', 1.5, [('John Gibbons', 'D'), ('Larry Stein', 'R')], 49),
    ('OKCO-C3', 'OK CO. COMMISSIONER 3', 1.5, [('Jennifer Mayo', 'D'), ('Jessica Clayton', 'R')], 40),
]
for id_, label, w, cs, sh in OKC:
    add(id=id_, label=label, cands=[dict(n=sur(n), p=p) for n, p in cs], share=round(sh + random.uniform(-2, 2), 1),
        ch=None, held='R', pool=True, w=w, ok=True)
Y = [dict(n='YES', p='Q'), dict(n='NO', p='Q')]
add(id='SQ845', label='SQ 845 · JUDICIAL PANEL', cands=Y, share=round(random.uniform(44, 56), 1), ch=None, pool=True, w=4, m=True, ok=True)
add(id='SQ847', label='SQ 847 · PROPERTY TAX', cands=Y, share=round(random.uniform(44, 56), 1), ch=None, pool=True, w=4, m=True, ok=True)
add(id='OKCO-Q', label='OK COUNTY QUESTION', cands=Y, share=round(random.uniform(44, 56), 1), ch=None, pool=True, w=1.5, m=True, ok=True)
for c in st['chambers']:
    if c['st'] != 'OK': continue
    pre = 'HD' if c['ch'] == 'lower' else 'SD'
    for d in c['districts']:
        cd = d.get('cand', {})
        if not d.get('up') or 'D' not in cd or 'R' not in cd: continue
        last = d.get('last') or {}
        if last.get('m') is not None: sh = 50 + (last['m'] / 2 if last['party'] == 'D' else -last['m'] / 2)
        else: sh = 66 if last.get('party') == 'D' else 32
        add(id=f"OK-{pre}{d['d']}", label=f"{pre} {d['d']}", cands=DR(cd['D'][0], cd['R'][0]),
            share=round(max(15, min(85, sh + random.uniform(-6, 6))), 1), ch=None, held=last.get('party'), pool=True, w=1, ok=True)

ids = [r['id'] for r in out]
assert len(ids) == len(set(ids)), 'duplicate race ids'
json.dump(out, open(out_path, 'w'), separators=(',', ':'))
pool = [r for r in out if r['pool']]
print(len(out), 'races;', len(pool), 'in rotation;', sum(1 for r in pool if r.get('ok')), 'Oklahoma;',
      'national keyed:', sum(1 for r in out if r.get('key')))
