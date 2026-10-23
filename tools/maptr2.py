"""Перевод подписей на картах (v2).
Конфиг: {"src":..., "dst":..., "items":[{"box":[x0,y0,x1,y1], "text":"...", "style":"...", ...}]}
box — область английского текста (стирается). Русский текст центрируется в box (или в xy), размер подгоняется.
"""
import cv2, numpy as np, json, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

F = '/home/claude/fonts/'
STYLES = {
    # DoIP (официальные карты WotC): чёрный узкий жирный с кремовой обводкой
    'doip_title': dict(font='Oswald[wght].ttf', wght=700, fill=(28, 22, 20), stroke=0.05, stroke_fill=(238, 232, 210), hfac=1.0, sc=True, glow=0.18, thr=26, grow=3),
    'doip_label': dict(font='Oswald[wght].ttf', wght=600, fill=(28, 22, 20), stroke=0.07, stroke_fill=(238, 232, 210), hfac=0.72, upper=True, glow=0.15, thr=26, grow=3),
    'doip_white': dict(font='Oswald[wght].ttf', wght=500, fill=(248, 245, 238), stroke=0.035, stroke_fill=(40, 34, 30), hfac=0.72, upper=True),
    'doip_scale': dict(font='OpenSans[wdth,wght].ttf', wght=600, fill=(248, 246, 240), stroke=0.05, stroke_fill=(60, 52, 46), hfac=1.0),
    'doip_scale_dark': dict(font='OpenSans[wdth,wght].ttf', wght=500, fill=(30, 26, 24), stroke=0, hfac=1.0),
    # GM Binder / Beyond (EN 1–3): капитель с засечками, белая с тёмной обводкой
    'gm_title': dict(font='CormorantSC-Bold.ttf', fill=(250, 250, 248), stroke=0.04, stroke_fill=(60, 60, 64), hfac=1.15, thr=28, grow=4),
    'gm_title_dark': dict(font='CormorantSC-Bold.ttf', fill=(40, 30, 24), stroke=0.03, stroke_fill=(235, 225, 200), hfac=1.15, thr=28, grow=4),
    'gm_title_red': dict(font='CormorantSC-Bold.ttf', fill=(105, 28, 24), stroke=0.03, stroke_fill=(235, 225, 200), hfac=1.15, thr=28, grow=4),
    'gm_label': dict(font='CormorantSC-Bold.ttf', fill=(250, 250, 248), stroke=0.05, stroke_fill=(50, 50, 54), hfac=1.15, thr=28, grow=4),
    'gm_label_dark': dict(font='CormorantSC-Bold.ttf', fill=(40, 30, 24), stroke=0.04, stroke_fill=(235, 225, 200), hfac=1.15, thr=28, grow=4),
    'gm_room': dict(font='EBGaramond[wght].ttf', wght=700, fill=(250, 248, 240), stroke=0.10, stroke_fill=(40, 30, 24), hfac=1.15, thr=45, grow=2),
    'gm_scale': dict(font='EBGaramond[wght].ttf', wght=500, fill=(248, 248, 246), stroke=0.03, stroke_fill=(70, 72, 76), hfac=1.25, thr=28, grow=4),
    'gm_scale_dark': dict(font='EBGaramond[wght].ttf', wght=500, fill=(40, 30, 24), stroke=0.0, hfac=1.25, thr=28, grow=4),
}


def load(font, size, wght=None):
    f = ImageFont.truetype(F + font, size)
    if wght:
        try: f.set_variation_by_axes([wght] if 'wdth' not in font else [wght, 100])
        except Exception: pass
    return f


def mask_auto(img, box, thr=38, grow=2):
    x0, y0, x1, y1 = box
    lab = cv2.cvtColor(img[y0:y1, x0:x1], cv2.COLOR_RGB2LAB).astype(int)
    border = np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])
    bg = np.median(border, axis=0)
    d = np.sqrt(((lab - bg) ** 2).sum(2))
    m = (d > thr).astype(np.uint8)
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=grow)
    full = np.zeros(img.shape[:2], np.uint8); full[y0:y1, x0:x1] = m * 255
    return full


def scale_cfg(cfg):
    k = cfg.get('scale', 1.0)
    if k == 1.0: return cfg
    its = []
    for it in cfg['items']:
        it = dict(it)
        it['box'] = [round(v * k) for v in it['box']]
        if 'extra' in it: it['extra'] = [[round(v * k) for v in b] for b in it['extra']]
        if 'xy' in it: it['xy'] = [v * k for v in it['xy']]
        for key in ('size', 'maxw', 'lpad'):
            if key in it: it[key] = it[key] * k
        its.append(it)
    return {**cfg, 'items': its}


def render(cfg):
    cfg = scale_cfg(cfg)
    img = np.asarray(Image.open(cfg['src']).convert('RGB')).copy()
    mask = np.zeros(img.shape[:2], np.uint8)
    for it in cfg['items']:
        if it.get('keep'): continue
        st0 = STYLES[it.get('style', 'doip_label')]
        bx = list(it['box'])
        if it.get('style', '').startswith('gm_'):
            p = int((bx[3] - bx[1]) * it.get('epad', 0.3)); bx = [bx[0] - p // 2, bx[1] - p, bx[2] + p // 2, bx[3] + p]
            bx = [max(0, bx[0]), max(0, bx[1]), min(img.shape[1], bx[2]), min(img.shape[0], bx[3])]
        for b in [bx] + it.get('extra', []):
            mask |= mask_auto(img, b, it.get('thr', st0.get('thr', 38)), it.get('grow', st0.get('grow', 2)))
    out = cv2.inpaint(img, mask, 9, cv2.INPAINT_TELEA)
    im = Image.fromarray(out); d = ImageDraw.Draw(im)
    for it in cfg['items']:
        if not it.get('text'): continue
        st = {**STYLES[it.get('style', 'doip_label')], **it.get('opt', {})}
        x0, y0, x1, y1 = it['box']
        lines = it['text'].split('\n')
        if st.get('upper') and not it.get('noupper'): lines = [l.upper() for l in lines]
        bh = (y1 - y0) / len(lines)
        size = int(it.get('size') or bh * st['hfac'])
        x0, y0, x1, y1 = it['box']
        maxw = it.get('maxw', (x1 - x0) * it.get('wfac', 1.15))
        cx, cy = it.get('xy', ((x0 + x1) / 2, (y0 + y1) / 2))
        anchor = it.get('anchor', 'mm')
        sw = max(1, round(size * st['stroke'])) if st['stroke'] else 0
        n = len(lines)
        sc = it.get('sc', st.get('sc', False))
        def layout(size):
            f = load(st['font'], size, st.get('wght')); small = load(st['font'], int(size * 0.8), st.get('wght'))
            runs = []; widths = []
            for l in lines:
                if sc:
                    parts = []
                    for w_i, w in enumerate(l.split(' ')):
                        if w_i: parts.append((' ', small))
                        if w: parts.append((w[0].upper(), f))
                        if len(w) > 1: parts.append((w[1:].upper(), small))
                else:
                    parts = [(l, f)]
                runs.append(parts); widths.append(sum(ft.getlength(t) for t, ft in parts))
            return f, runs, widths
        f, runs, widths = layout(size)
        while max(widths) > maxw and size > 8:
            size -= 1; f, runs, widths = layout(size)
        sw = max(1, round(size * st['stroke'])) if st['stroke'] else 0
        lh = size * 1.05
        asc = f.getbbox('Н')[3] - f.getbbox('Н')[1]
        placed = []
        for k, (parts, tw) in enumerate(zip(runs, widths)):
            yy = cy + (k - (n - 1) / 2) * lh
            x = (x0 + it.get('lpad', 4)) if it.get('align') == 'left' else (cx - tw / 2); base = yy + asc / 2
            for t, ft in parts:
                placed.append((x, base, t, ft)); x += ft.getlength(t)
        g = st.get('glow')
        if g:
            gw = max(2, round(size * g))
            layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
            gc = tuple(st.get('glow_fill', st.get('stroke_fill', (235, 228, 205))))
            for x, base, t, ft in placed:
                ld.text((x, base), t, font=ft, anchor='ls', fill=gc + (235,), stroke_width=gw, stroke_fill=gc + (235,))
            layer = layer.filter(ImageFilter.GaussianBlur(gw * 0.6))
            im.paste(layer, (0, 0), layer); d = ImageDraw.Draw(im)
        for x, base, t, ft in placed:
            d.text((x, base), t, font=ft, anchor='ls', fill=st['fill'], stroke_width=sw, stroke_fill=st.get('stroke_fill', (0, 0, 0)))
    im.save(cfg['dst'], quality=92)
    return mask


if __name__ == '__main__':
    for p in sys.argv[1:]:
        cfgs = json.load(open(p))
        for c in (cfgs if isinstance(cfgs, list) else [cfgs]):
            render(c); print('ok', c['dst'])
