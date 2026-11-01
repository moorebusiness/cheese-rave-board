"""Compose the board pages from board.src.html + races.json.
Thin style (default) and block style (block.css overrides), each as:
  <name>.html       -> published preview (sample numbers; the preview can't reach outside sites)
  <name>-live.html  -> booth laptop file (live civicAPI results); add #rehearse for the Aug. 25 runoff, #sample for fake numbers
"""
src = open('board.src.html').read()
data = open('races.json').read()
for k in ("/*__MODE__*/'sample'", '/*__DATA__*/[]', '/*__STYLE__*/'): assert src.count(k) == 1, k
BLOCK_JS = [  # call card geometry and type sizes for the block style
    ("const CARD = {x:480, y:282, w:960, h:440};", "const CARD = {x:360, y:224, w:1200, h:560};"),
    ("fitText(card.querySelector('.cw'), 124, 64); fitText(card.querySelector('.cr'), 52, 30);",
     "fitText(card.querySelector('.cw'), 200, 96); fitText(card.querySelector('.cr'), 80, 44);"),
    ("$('flash').animate([{opacity:.16},{opacity:0}]", "$('flash').animate([{opacity:.4},{opacity:0}]"),
    ("fitText(s.lbl, 15, 10)", "fitText(s.lbl, 30, 18)"),  # inside fitLabel
]
BLOCK_FONT = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Martian+Mono:wght@300;400;500&display=swap">',
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Martian+Mono:wght@300;400;500;600&display=swap">\n'
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900&display=swap">')
import base64
def uri(f, mime): return f'data:{mime};base64,' + base64.b64encode(open(f, 'rb').read()).decode()
LAYERS = {'/*__SKYBG__*/': uri('layer-sky.jpg', 'image/jpeg'), '/*__SKYLINE__*/': uri('layer-skyline.webp', 'image/webp'),
          '/*__MOON__*/': uri('layer-moon.webp', 'image/webp'), '/*__STARS__*/[]': open('stars.json').read()}
import json
_lm = json.load(open('logos/logos.json'))   # sponsor logos (prep_logos.py), baked in so the page needs no other files
LAYERS['/*__LOGOS__*/{}'] = json.dumps({k: dict(v, src=uri(f'logos/{k}.webp', 'image/webp')) for k, v in _lm.items()}, separators=(',', ':'))
# Fonts baked in too, so the projector page looks right even if Google Fonts can't be reached from the theatre.
FACES = [('Big Shoulders Display', w, f'fonts/big-shoulders-display-latin-{w}-normal.woff2') for w in (700, 800, 900)] + \
        [('Martian Mono', w, f'fonts/martian-mono-latin-{w}-normal.woff2') for w in (300, 400, 500, 600)]
FONT_CSS = '<style>' + ''.join(f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:normal;font-display:block;'
                               f'src:url({uri(f, "font/woff2")}) format("woff2")}}' for fam, w, f in FACES) + '</style>'
def page(mode, style):
    s = src.replace("/*__MODE__*/'sample'", f"/*__MODE__*/'{mode}'").replace('/*__DATA__*/[]', data)
    for k, v in LAYERS.items():
        assert s.count(k) == 1, k
        s = s.replace(k, v)
    if style == 'block':
        s = s.replace('<title>Cheese Rave Board</title>', '<title>Cheese Rave Block Board</title>')
        s = s.replace('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Antonio:wght@200;300;400;500&display=swap">', '').replace(BLOCK_FONT[0], FONT_CSS).replace('/*__STYLE__*/', open('block.css').read())
        for a, b in BLOCK_JS:
            assert s.count(a) == 1, a; s = s.replace(a, b)
    else:
        s = s.replace('/*__STYLE__*/', '')
    return s
SKEL = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}</style>'
        '</head><body>')
for style, name in (('thin', 'cheese-rave-board'), ('block', 'cheese-rave-block')):
    open(f'{name}.html', 'w').write(page('sample', style))
    # the booth file goes straight to a projector: no side gutter, so the slide fills the screen
    live = page('live', style).replace('padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0}',
                                       'padding:0}', 1)
    open(f'{name}-live.html', 'w').write(SKEL + live + '</body></html>')
print('built thin + block, preview + live')
