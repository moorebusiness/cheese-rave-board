"""Prepare the layers for cue 9 (into the Cheese Rave) from Andy's originals (src-*.png):
turquoise sky photo, the same skyline as a cutout (so the cheese can rise from behind the buildings),
the pink moon (sized and placed to sit exactly over the home screen's moon), and the cheese logo on transparent."""
from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage as nd

# turquoise sky: full frame
Image.open('src-turquoise.png').convert('RGB').save('turq.jpg', quality=86, optimize=True, progressive=True)

# skyline cutout: everything from the tallest rooftop down
city = Image.open('src-city-cutout.png').convert('RGBA')
top = int(np.where(np.asarray(city)[..., 3].max(1) > 0)[0].min())
city.crop((0, top, 1920, 1080)).save('turq-city.webp', quality=88, method=6)
print('city cutout from y =', top)

# pink moon: feather the outer edge of its halo, then size it so its lettering matches the home screen moon (452 px)
m = np.asarray(Image.open('src-moon-pink.png').convert('RGBA')).astype(float)
h, w = m.shape[:2]
yy, xx = np.mgrid[0:h, 0:w]
a = m[..., 3]
ys, xs = np.where(a > 0)
cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
r = np.hypot(xx - cx, yy - cy)
rmax = r[a > 0].max()
m[..., 3] = a * np.clip((rmax - r) / 46, 0, 1) ** 1.5
Image.fromarray(m.round().astype(np.uint8), 'RGBA').resize((452, 452), Image.LANCZOS).save('moon-pink.webp', quality=90, method=6)

# cheese logo: white background (and the white inside the letters of FOR DEMOCRACY) to transparent, edges unmixed from white
c = np.asarray(Image.open('src-cheese.png').convert('RGB')).astype(float)
white = c.min(2) > 200
lab, n = nd.label(white)
near = nd.binary_dilation(white, iterations=3)
alpha = np.where(near, (255 - c).max(2) / 255, 1.0)
alpha = np.clip(alpha, 0, 1)
out = np.zeros((*c.shape[:2], 4))
safe = np.maximum(alpha, 1e-3)[..., None]
out[..., :3] = np.clip((c - 255 * (1 - alpha[..., None])) / safe, 0, 255)
out[..., 3] = alpha * 255
im = Image.fromarray(out.round().astype(np.uint8), 'RGBA')
bb = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
im = im.crop((bb[0] - 4, bb[1] - 4, bb[2] + 4, bb[3] + 4))
# a thin dark keyline around everything, so the yellow FOR DEMOCRACY reads on the bright turquoise sky
A = im.getchannel('A')
ring = A.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(1.2))
base = Image.new('RGBA', im.size, (3, 24, 27, 0)); base.putalpha(ring.point(lambda v: int(v * .92)))
logo = Image.alpha_composite(base, im)
H = 560
logo = logo.resize((round(logo.width * H / logo.height), H), Image.LANCZOS)
logo.save('cheese.webp', quality=92, method=6)
print('cheese logo', logo.size)
