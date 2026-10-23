"""Перевод подписей на картах: стираем английский текст (inpaint) и пишем русский тем же стилем."""
import cv2, numpy as np, sys, json
from PIL import Image, ImageDraw, ImageFont

FONTS = {
    'title': '/home/claude/fonts/CormorantSC-Bold.ttf',
    'sc': '/home/claude/fonts/AlegreyaSC-Bold.ttf',
    'scm': '/home/claude/fonts/AlegreyaSC-Medium.ttf',
    'serif': '/home/claude/fonts/EBGaramond[wght].ttf',
}


def text_mask(img, box, mode='light', thr=None, grow=3):
    x0, y0, x1, y1 = box
    sub = cv2.cvtColor(img[y0:y1, x0:x1], cv2.COLOR_RGB2LAB)[..., 0].astype(int)
    if mode == 'light':
        t = thr or 175
        m = (sub > t).astype(np.uint8)
    else:
        t = thr or 70
        m = (sub < t).astype(np.uint8)
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=grow)
    full = np.zeros(img.shape[:2], np.uint8)
    full[y0:y1, x0:x1] = m * 255
    return full


def erase(img, boxes):
    mask = np.zeros(img.shape[:2], np.uint8)
    for b in boxes:
        mask |= text_mask(img, b['box'], b.get('mode', 'light'), b.get('thr'), b.get('grow', 3))
    return cv2.inpaint(img, mask, 7, cv2.INPAINT_TELEA), mask


cfg_scale = [1.0]
def draw(im, labels):
    d = ImageDraw.Draw(im)
    for L in labels:
        f = ImageFont.truetype(FONTS[L.get('font', 'title')], L['size'])
        if L.get('wght'):
            try: f.set_variation_by_axes([L['wght']])
            except Exception: pass
        if L.get('maxw'):
            while f.getlength(L['text']) > L['maxw'] * cfg_scale[0] and f.size > 8:
                f = ImageFont.truetype(f.path, f.size - 1)
                if L.get('wght'): f.set_variation_by_axes([L['wght']])
        kw = dict(font=f, fill=tuple(L.get('fill', (245, 240, 230))), anchor=L.get('anchor', 'mm'),
                  stroke_width=L.get('stroke', 0), stroke_fill=tuple(L.get('stroke_fill', (40, 40, 45))))
        if L.get('shadow'):
            sx, sy = L['shadow']
            d.text((L['xy'][0] + sx, L['xy'][1] + sy), L['text'], **{**kw, 'fill': (20, 20, 25), 'stroke_fill': (20, 20, 25)})
        d.text(tuple(L['xy']), L['text'], **kw)
    return im


def run(src, dst, cfg):
    img = np.asarray(Image.open(src).convert('RGB')).copy()
    sc = cfg.get('scale', 1.0); cfg_scale[0] = sc
    def S(v): return [int(round(x * sc)) for x in v]
    boxes = [{**b, 'box': S(b['box'])} for b in cfg['erase']]
    out, mask = erase(img, boxes)
    im = Image.fromarray(out)
    labels = [{**L, 'xy': S(L['xy']), 'size': int(L['size'] * sc), 'stroke': int(round(L.get('stroke', 0) * sc)),
               'shadow': [v * sc for v in L['shadow']] if L.get('shadow') else None} for L in cfg['labels']]
    draw(im, labels)
    im.save(dst, quality=92)
    return mask


if __name__ == '__main__':
    cfg = json.load(open(sys.argv[3]))
    run(sys.argv[1], sys.argv[2], cfg)
