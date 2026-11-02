"""Trim the sponsor logos Andy sent (Nov. 1) to their visible edges and save them as webp for the sponsor slides.
Usage: python3 prep_logos.py <attachments_dir>"""
import json, os, sys
from PIL import Image
src = sys.argv[1].rstrip('/') + '/'
# file prefix -> (key, name shown to screen readers, max box). Slide 1 logos display larger.
L = {'dfde2996': ('gazette', 'Oklahoma Gazette and UBS', (900, 600)), '0a0d362d': ('infocus', 'InFocus Campaigns', (900, 600)),
     '2c8ded12': ('cfo', 'Communities Foundation of Oklahoma', (640, 420)), '6a2cf4d9': ('kpg', 'Kirkpatrick Policy Group', (640, 420)),
     '30f5c478': ('mitchelltalks', 'MitchellTalks', (640, 420)), 'c695d4c8': ('vox', 'Vox Audio Visual', (640, 420)),
     '5409d0f1': ('sawyer', 'Greg and Marti Sawyer', (640, 420)), 'd6036982': ('focus', 'Focus Workplace Furniture + Design', (640, 420)),
     '41d4af68': ('konjo', 'Konjo Concepts', (640, 420)), '1a6723fc': ('boomtown', 'Boomtown Creamery', (640, 420)),
     '68ac2b96': ('fuzzys', 'Fuzzy’s Taco Shop', (640, 420)), '848ba4e4': ('tacoempire', 'Taco Empire', (640, 420)),
     'cac0847d': ('eastside', 'Eastside Pizza House', (640, 420)), '99039978': ('stonehorse', 'Stonehorse Café & Market', (640, 420)),
     'f20618a9': ('empireslice', 'Empire Slice House', (640, 420)),
     'c1a1de12': ('shortle', 'Allyson Shortle', (640, 420))}   # added Nov. 2
meta = {}
for f, (key, alt, box) in L.items():
    im = Image.open(src + f + '-image.png').convert('RGBA')
    im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 12 else 0).getbbox())
    im.thumbnail(box, Image.LANCZOS)
    im.save(f'logos/{key}.webp', 'WEBP', quality=90, method=6)
    meta[key] = {'alt': alt, 'w': im.size[0], 'h': im.size[1]}
json.dump(meta, open('logos/logos.json', 'w'), indent=1)
print(len(meta), 'logos,', round(sum(os.path.getsize('logos/' + k + '.webp') for k in meta) / 1024), 'KB')
