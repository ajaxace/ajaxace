#!/usr/bin/env python3
"""Wolf NEO renderer: animated futuristic demo + 15s ads. Free tools only (PIL, numpy, ffmpeg).
usage: neo.py NAME            (NAME = demo | ad1 | ad2 | ad3 | ad4)
       neo.py NAME --preview 0.5,2.0,4.0   (writes PNGs, no video)
Screens are simulated. Features shown: calendar-connected, finds options, answers questions, books nothing."""
import os, sys, math, wave, subprocess, random
import numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
CY, TL, OR, WH, GRN = (46, 197, 255), (20, 224, 192), (252, 163, 17), (255, 255, 255), (60, 255, 140)
PX, PY, PW, PHT = 110, 310, 860, 1000
SC_T, RS, BEAT = 5.2, 1.45, 5.2 / 12
INTRO_T, END_DEMO = 8 * BEAT, 12 * BEAT
LOGO = Image.open(os.path.join(HERE, "assets", "wolf_mark_v4_512.png")).convert("RGBA")

SCENES = [  # title, user text, hud?, reply bubble, chips[(label,right,color)], note
 ("Lift's cancelled?", "Lift's cancelled. How do I get home from college?", False, "College finishes 16:45. Options:",
  [("Local cab firm", "CAB", OR), ("Bus", "17:25", TL), ("Train", "17:42", CY)], "Options only. Nothing is booked."),
 ("Who's got the pick-up?", "Who's picking Sarah up today?", True, "Dan is. 3:30pm, school gate.", [], "From your family calendar."),
 ("What's on tonight?", "What time is the film tonight?", False, "Cinema times near you:",
  [("Tonight", "18:30", CY), ("Tonight", "20:15", CY), ("Tonight", "21:00", CY)], "Options only. Nothing is booked."),
 ("Forgot the shopping?", "What was the shopping I was meant to get?", True, "From your calendar: milk, eggs and bread.", [], "Anything else you need?"),
 ("Need a taxi?", "Where's the nearest taxi firm to here?", False, "Nearest options:",
  [("Local cab firm 1", "CAB", OR), ("Local cab firm 2", "CAB", OR)], "I can't book or promise a pickup."),
 ("Your week, at a glance", "What does our week look like?", True, "This week:",
  [("Mon", "Swimming 4pm", TL), ("Wed", "Dentist 3:15pm", OR), ("Fri", "Mum's birthday", CY)], "Wednesday clashes with pick-up."),
 ("Any train home?", "When's the next train home?", False, "Trains from your station:",
  [("Next", "17:42", CY), ("Then", "18:12", CY), ("Then", "18:42", CY)], "Options only. Nothing is booked."),
 ("Ask it anything", "How long do I roast a 2kg chicken?", False, "About 1 hr 45 min at 190°C (fan 170°C), then rest for 15 min.", [], "Check the juices run clear."),
]
SCENES += [
 ("Quote still to send?", "What have I got to send today?", True, "Reminder: send the Evans quote.", [], "I can remind you. I don't send anything."),
 ("Where next?", "Where do I need to be next?", True, "Next: drop Jack at Oakfield Primary, 8:50.", [], "From your family calendar."),
]
SCENES += [("From anywhere", "What time is my flight home?", True, "Saturday, 14:10. Faro to Manchester.", [], "From the family calendar.")]
ACC = [CY, TL, CY, TL, CY, TL, CY, TL, CY, TL, CY]

def fib(n):
    i = np.arange(n) + 0.5; ph = np.arccos(1 - 2 * i / n); th = np.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(th) * np.sin(ph), np.cos(ph), np.sin(th) * np.sin(ph)], 1)
GP = fib(1900)
def ll(lat, lon):
    la, lo = math.radians(lat), math.radians(lon); return np.array([math.cos(la) * math.sin(lo), math.sin(la), math.cos(la) * math.cos(lo)])
NODES = [("Home", ll(10, 0)), ("School", ll(42, -28)), ("On site", ll(-18, 30)), ("Abroad", ll(-30, -40)), ("Abroad", ll(38, 36))]

def xf(v, a, b=0.28):
    x = v[..., 0] * math.cos(a) + v[..., 2] * math.sin(a); z = -v[..., 0] * math.sin(a) + v[..., 2] * math.cos(a); y = v[..., 1]
    y2 = y * math.cos(b) - z * math.sin(b); z2 = y * math.sin(b) + z * math.cos(b); return x, y2, z2

def head(cv, text, sub, lt, size=66):
    a = eo(lt / 0.5); sp, pd_ = tsprite(text, F(BOLD, size), WH + (255,), CY, 14); paste(cv, sp, W / 2 - sp.width / 2, 150 - pd_ + (1 - a) * 30, alpha=a)
    if sub: s2, p2 = tsprite(sub, F(REG, 40), (205, 222, 250, 255)); paste(cv, s2, W / 2 - s2.width / 2, 1440 + (1 - a) * 30, alpha=eo((lt - 0.5) / 0.5))

def draw_globe(cv, lt, t):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); cx, cy, R = W / 2, 860, 400; ang = 0.32 * math.sin(lt * 0.8)
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(10, 30, 60, 90), outline=CY + (140,), width=3)
    x, y, z = xf(GP, ang); sx = cx + R * x; sy = cy - R * y
    for i in range(len(GP)):
        if z[i] > 0: d.ellipse((sx[i] - 2.2, sy[i] - 2.2, sx[i] + 2.2, sy[i] + 2.2), fill=(120, 210, 255, int(50 + 150 * z[i])))
    home = NODES[0][1]
    for k, (name, v) in enumerate(NODES):
        if k:
            pts = []
            for j in range(33):
                u = j / 32; m = (1 - u) * home + u * v; m = m / np.linalg.norm(m) * (1 + 0.28 * math.sin(math.pi * u)); xx, yy, zz = xf(m, ang); pts.append((cx + R * xx, cy - R * yy))
            d.line(pts, fill=TL + (200,), width=4)
            u = (t * 0.5 + k * 0.23) % 1; m = (1 - u) * home + u * v; m = m / np.linalg.norm(m) * (1 + 0.28 * math.sin(math.pi * u)); xx, yy, zz = xf(m, ang)
            d.ellipse((cx + R * xx - 11, cy - R * yy - 11, cx + R * xx + 11, cy - R * yy + 11), fill=(255, 255, 255, 255))
    cv.alpha_composite(ov)
    for k, (name, v) in enumerate(NODES):
        xx, yy, zz = xf(v, ang); px, py = cx + R * xx, cy - R * yy; col = OR if k == 0 else TL; r = 18 + 4 * math.sin(t * 4 + k)
        d2 = ImageDraw.Draw(cv); d2.ellipse((px - r, py - r, px + r, py + r), fill=col + (255,), outline=WH + (255,), width=3)
        sp, pd_ = tsprite(name, F(BOLD, 38), WH + (255,), col, 8); paste(cv, sp, px + 26 - pd_, py - 28 - pd_)
    head(cv, "Connected, wherever they are", "At home. At school. On site. Abroad.", lt)

@lru_cache(maxsize=None)
def tier_card(title, big, small, col, box=False):
    w, h = 900, 300; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 40, fill=(8, 16, 38, 235), outline=col + (255,), width=4)
    d.text((48, 40), title, font=F(BOLD, 50), fill=WH); d.text((48, 120), big, font=F(BOLD, 84 if not box else 70), fill=col + (255,)); d.text((48, 232), small, font=F(REG, 32), fill=(200, 215, 240))
    if box:
        d.rounded_rectangle((690, 70, 830, 200), 26, outline=col + (255,), width=4, fill=(20, 30, 50, 255)); d.ellipse((730, 110, 790, 170), outline=col + (255,), width=4); d.ellipse((752, 132, 768, 148), fill=col + (255,))
        d.text((760, 232), "Concept", font=F(REG, 28), fill=col + (255,), anchor="ma")
    return glow(im, 14, col, 0.35)

def draw_tiers(cv, lt, t):
    head(cv, "Choose how your family connects", None, lt, 54)
    for i, (spr, ti) in enumerate([(tier_card("Wolf", "£69", "per person  ·  one-off price", CY), 0.5), (tier_card("Wolf Family", "£179", "mum, dad and one child  ·  one-off price", TL), 1.2),
                                  (tier_card("Wolf Box", "COMING SOON", "Wolf at home. Details to follow.", OR, True), 1.9)]):
        a = eo((lt - ti) / 0.4); sp, pad = spr; paste(cv, sp, W / 2 - sp.width / 2 + (1 - a) * 120, 330 + i * 400 - pad, alpha=a)
    s2, p2 = tsprite("Over 18 only. Under 16s need a parent's OK.", F(REG, 32), (200, 215, 240, 255)); paste(cv, s2, W / 2 - s2.width / 2, 1600, alpha=eo((lt - 2.4) / 0.4))

def draw_trust(cv, lt, t):
    for i, (txt, col, ti) in enumerate([("Finds options.", CY, 0.3), ("Reads your calendar.", TL, 1.0), ("Books nothing.", OR, 1.7)]):
        a = eo((lt - ti) / 0.4); sp, pd_ = tsprite(txt, F(BOLD, 96), WH + (255,), col, 16); paste(cv, sp, W / 2 - sp.width / 2 + (1 - a) * 80, 640 + i * 190 - pd_, alpha=a)
    s2, p2 = tsprite("You stay in control.", F(REG, 50), (205, 222, 250, 255)); paste(cv, s2, W / 2 - s2.width / 2, 1330, alpha=eo((lt - 2.4) / 0.4))

@lru_cache(maxsize=None)
def photo_img(key):
    im = Image.open(os.path.join(HERE, "shots", key + ".png")).convert("RGB").resize((W, H), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))

@lru_cache(maxsize=None)
def photo_blur(key):
    arr = np.asarray(photo_img(key).filter(ImageFilter.GaussianBlur(22))).astype(np.float32) * 0.40 + np.array([6, 12, 28], np.float32) * 0.7
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")

@lru_cache(maxsize=None)
def pill(text):
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1))); f = F(BOLD, 62); lines = wrap(d0, text, f, 880); lh = 78
    w = int(max(d0.textlength(l, font=f) for l in lines)) + 80; h = lh * len(lines) + 40
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 34, fill=(5, 10, 26, 205), outline=CY + (255,), width=3)
    for i, l in enumerate(lines): d.text((w / 2, 20 + i * lh), l, font=f, fill=WH, anchor="ma")
    return glow(im, 14, CY, 0.4)[0], 42, w, h

@lru_cache(maxsize=None)
def ailabel():
    f = F(REG, 28); d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1))); t = "AI-generated dramatisation. Screens simulated."
    w = int(d0.textlength(t, font=f)) + 44; im = Image.new("RGBA", (w, 50), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, 49), 25, fill=(0, 0, 0, 170)); d.text((w / 2, 25), t, font=f, fill=(255, 255, 255, 225), anchor="mm"); return im

def draw_photo(cv, key, lt, dur, caption):
    z = 1.0 + 0.08 * (lt / dur); w = W / z; h = H / z; x0 = (W - w) / 2 + 18 * math.sin(lt * 0.9); y0 = (H - h) / 2
    cv.paste(photo_img(key).crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BILINEAR).convert("RGBA"), (0, 0))
    cv.alpha_composite(Image.new("RGBA", (W, H), (8, 28, 70, 46)))
    a = eo((lt - 0.25) / 0.35); sp, pad, pw, ph = pill(caption)
    paste(cv, sp, W / 2 - sp.width / 2, 1130 - pad + (1 - a) * 40, alpha=a); paste(cv, ailabel(), W / 2 - ailabel().width / 2, 1130 + ph + 14 + (1 - a) * 40, alpha=a)

@lru_cache(maxsize=None)
def F(p, s): return ImageFont.truetype(p, s)
def clamp(x): return max(0.0, min(1.0, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3

def glow(img, r, color=None, k=0.6):
    pad = r * 3; base = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0)); base.paste(img, (pad, pad), img)
    if color is None: g = base.filter(ImageFilter.GaussianBlur(r))
    else:
        a = base.getchannel("A").filter(ImageFilter.GaussianBlur(r)).point(lambda v: min(255, int(v * k * 2)))
        g = Image.new("RGBA", base.size, color + (0,)); g.putalpha(a)
    return Image.alpha_composite(g, base), pad

def tsprite(text, font, fill, gcol=None, r=14):
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1))); w = int(d0.textlength(text, font=font)) + 8; a, b = font.getmetrics()
    im = Image.new("RGBA", (max(w, 8), a + b + 6), (0, 0, 0, 0)); ImageDraw.Draw(im).text((4, 2), text, font=font, fill=fill)
    return glow(im, r, gcol, 0.7) if gcol else (im, 0)

def paste(cv, sp, x, y, alpha=1.0, cropw=None):
    if alpha <= 0.01: return
    if cropw is not None:
        cw = int(cropw)
        if cw <= 0: return
        sp = sp.crop((0, 0, min(cw, sp.width), sp.height))
    if alpha < 0.99:
        sp = sp.copy(); sp.putalpha(sp.getchannel("A").point([int(i * alpha) for i in range(256)]))
    cv.alpha_composite(sp, (int(x), int(y)))

def wrap(d, text, f, maxw):
    out = []
    for part in text.split("\n"):
        cur = ""
        for w in part.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) <= maxw: cur = t
            else: out.append(cur); cur = w
        out.append(cur)
    return out

@lru_cache(maxsize=None)
def bubble(text, kind):
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    f = F(BOLD, 40) if kind == "user" else (F(REG, 33) if kind == "note" else F(REG, 40)); lines = wrap(d0, text, f, PW - 170)
    lh = int(f.size * 1.32); w = int(max(d0.textlength(l, font=f) for l in lines)) + 62; h = lh * len(lines) + 38
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == "user": d.rounded_rectangle((0, 0, w - 1, h - 1), 36, fill=OR + (255,)); col, gc = (20, 33, 61), OR
    elif kind == "note": d.rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=(8, 40, 52, 240), outline=TL + (255,), width=3); col, gc = (170, 255, 235), TL
    else: d.rounded_rectangle((0, 0, w - 1, h - 1), 36, fill=(16, 34, 68, 245), outline=CY + (255,), width=3); col, gc = WH, CY
    for i, l in enumerate(lines): d.text((31, 19 + i * lh), l, font=f, fill=col)
    sp, pad = glow(im, 14, gc, 0.45); return sp, pad, w, h

@lru_cache(maxsize=None)
def chip(label, right, color):
    w, h = PW - 60, 84; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 28, fill=(12, 28, 58, 240), outline=color + (255,), width=3)
    d.ellipse((26, 31, 48, 53), fill=color + (255,)); d.text((70, 42), label, font=F(BOLD, 38), fill=WH, anchor="lm")
    d.text((w - 28, 42), right, font=F(MONO, 36), fill=color + (255,), anchor="rm")
    sp, pad = glow(im, 12, color, 0.35); return sp, pad, w, h

@lru_cache(maxsize=None)
def hud(text):
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1))); f = F(MONO, 28); w = int(d0.textlength(text, font=f)) + 84; h = 58
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 29, fill=(6, 30, 44, 240), outline=TL + (255,), width=2)
    d.ellipse((24, 20, 42, 38), fill=GRN + (255,)); d.text((56, 29), text, font=f, fill=(170, 255, 235), anchor="lm")
    sp, pad = glow(im, 10, TL, 0.4); return sp, pad, w, h

@lru_cache(maxsize=None)
def dots_pill():
    w, h = 190, 84; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), 38, fill=(16, 34, 68, 245), outline=CY + (255,), width=3)
    sp, pad = glow(im, 12, CY, 0.4); return sp, pad, w, h

@lru_cache(maxsize=None)
def panel(acc):
    pad = 70; w, h = PW + 2 * pad, PHT + 2 * pad
    g = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle((pad, pad, pad + PW, pad + PHT), 66, outline=acc + (255,), width=12)
    g = g.filter(ImageFilter.GaussianBlur(24))
    b = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle((pad, pad, pad + PW, pad + PHT), 66, fill=(7, 12, 30, 232))
    d.rounded_rectangle((pad, pad, pad + PW, pad + 132), 66, fill=(16, 30, 60, 240)); d.rectangle((pad, pad + 70, pad + PW, pad + 132), fill=(16, 30, 60, 240))
    d.line((pad + 30, pad + 132, pad + PW - 30, pad + 132), fill=acc + (120,), width=2)
    d.rounded_rectangle((pad + 28, pad + PHT - 116, pad + PW - 28, pad + PHT - 36), 40, fill=(18, 34, 66, 255), outline=acc + (90,), width=2)
    d.text((pad + 66, pad + PHT - 76), "Message Wolf", font=F(REG, 32), fill=(120, 140, 175), anchor="lm")
    d.ellipse((pad + PW - 98, pad + PHT - 106, pad + PW - 38, pad + PHT - 46), fill=acc + (255,))
    d.text((pad + 134, pad + 38), "Wolf", font=F(BOLD, 42), fill=WH); d.text((pad + 134, pad + 90), "Family assistant", font=F(REG, 26), fill=(150, 170, 205))
    d.ellipse((pad + 330, pad + 96, pad + 346, pad + 112), fill=GRN + (255,)); d.text((pad + 356, pad + 104), "online", font=F(REG, 24), fill=(150, 255, 190), anchor="lm")
    m = LOGO.resize((84, 84), Image.LANCZOS); b.paste(m, (pad + 28, pad + 24), m)
    d.rounded_rectangle((pad, pad, pad + PW, pad + PHT), 66, outline=acc + (255,), width=4)
    return Image.alpha_composite(g, b), pad

@lru_cache(maxsize=None)
def layout(i):
    title, user, hasud, rep, chips, note = SCENES[i]; els = []; y = PY + 172; gap = 22
    def add(kind, spr, side, t):
        nonlocal y
        sp, pad, w, h = spr; x = (PX + PW - 30 - w) if side == "r" else PX + 30
        els.append(dict(kind=kind, sp=sp, pad=pad, x=x, y=y, t=t, w=w, h=h)); y += h + gap
    add("user", bubble(user, "user"), "r", 0.30); dots_y = y; t = RS
    if hasud: add("hud", hud("CALENDAR CONNECTED"), "l", t); t += 0.35
    add("bub", bubble(rep, "wolf"), "l", t); t += 0.25
    for lab, right, col in chips: add("chip", chip(lab, right, col), "l", t); t += 0.2
    add("note", bubble(note, "note"), "l", t + 0.1)
    return els, dots_y

# ---------------- background ----------------
GX, GY = np.meshgrid(np.linspace(0, 1, 270, dtype=np.float32), np.linspace(0, 1, 480, dtype=np.float32))
rng = random.Random(7); PARTS = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(20, 90), rng.uniform(1.2, 3.4), rng.uniform(0, 6.3)) for _ in range(80)]
def background(t, photo=None):
    k = GY[..., None]; arr = (1 - k) * np.array([5, 9, 22], np.float32) + k * np.array([11, 19, 42], np.float32)
    for (bx, by, s, col, a) in [(0.25 + 0.15 * math.sin(t * .5), 0.18 + 0.1 * math.cos(t * .4), 0.30, CY, 0.50),
                                (0.82 + 0.1 * math.cos(t * .45), 0.55 + 0.12 * math.sin(t * .6), 0.34, (90, 60, 200), 0.55),
                                (0.4 + 0.2 * math.sin(t * .3), 0.92, 0.36, TL, 0.38), (0.9, 0.12 + 0.05 * math.sin(t * .7), 0.22, OR, 0.18)]:
        dx = (GX - bx) * 0.5625; dy = GY - by; arr += (a * np.exp(-(dx * dx + dy * dy) / (s * s)))[..., None] * np.array(col, np.float32) * 0.55
    im = photo_blur(photo).copy() if photo else Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); hz = 1430
    for j in range(-9, 10): d.line((W / 2 + j * 70, hz, W / 2 + j * 330, H), fill=CY + (46,), width=2)
    for i in range(14):
        z = ((i + (t * 0.7) % 1) / 14); y = hz + (H - hz) * z ** 2.1; d.line((0, y, W, y), fill=CY + (int(20 + 70 * z),), width=2)
    for (x, y0, sp, r, ph) in PARTS:
        y = (y0 - t * sp) % H; a = int(70 + 90 * (0.5 + 0.5 * math.sin(t * 2 + ph))); d.ellipse((x - r, y - r, x + r, y + r), fill=(200, 235, 255, a))
    im.alpha_composite(ov); return im

def static_overlay():
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); a = np.zeros((H, W, 4), np.uint8); a[::4, :, 3] = 16
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); v = ((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.75)) ** 2
    a[..., 3] = np.maximum(a[..., 3], np.clip(v * 150, 0, 150).astype(np.uint8)); ov = Image.fromarray(a, "RGBA"); d = ImageDraw.Draw(ov)
    for (x, y, sx, sy) in [(40, 60, 1, 1), (W - 40, 60, -1, 1)]:
        d.line((x, y, x + 60 * sx, y), fill=CY + (170,), width=3); d.line((x, y, x, y + 60 * sy), fill=CY + (170,), width=3)
    d.text((110, 62), "WOLF  //  FAMILY AI", font=F(MONO, 24), fill=CY + (170,)); return ov
STATIC = static_overlay()
LABEL = tsprite("Screens simulated", F(REG, 30), (235, 242, 255, 255))[0]

# ---------------- scene / intro / end ----------------
def draw_title(cv, title, lt):
    n = int(lt / 0.028) + 1; n = min(n, len(title)); full = F(BOLD, 72); d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1))); fw = d0.textlength(title, font=full); x0 = (W - fw) / 2
    sp, pad = tsprite(title[:n], full, WH + (255,), CY, 14); cv.alpha_composite(sp, (int(x0 - 4 - pad), 118 - pad))
    if n < len(title) or lt < 0.9:
        px = x0 + d0.textlength(title[:n], font=full) + 6; ImageDraw.Draw(cv).rectangle((px, 126, px + 8, 196), fill=CY + (255,))
    w = 180 * eo((lt - 0.1) / 0.5); ImageDraw.Draw(cv).rectangle((W / 2 - w, 236, W / 2 + w, 242), fill=OR + (255,))

def draw_scene(cv, i, lt, t):
    off = int(7 * math.sin(t * 1.7)); acc = ACC[i]; ps, pad = panel(acc)
    pulse = 0.88 + 0.12 * math.sin(t * 3); paste(cv, ps, PX - pad, PY - pad + off, alpha=min(1.0, 0.0 + eo(lt / 0.25) * pulse + 0.0) if lt < 0.25 else pulse)
    draw_title(cv, SCENES[i][0], lt); els, dots_y = layout(i); d = ImageDraw.Draw(cv)
    ring = 0.5 + 0.5 * math.sin(t * 4); lx, ly = PX + 70, PY + 66 + off
    d.ellipse((lx - 46 - 4 * ring, ly - 46 - 4 * ring, lx + 46 + 4 * ring, ly + 46 + 4 * ring), outline=acc + (int(60 + 90 * ring),), width=3)
    if 0.9 < lt < RS + 0.05:                                          # typing dots
        sp, pd_, w, h = dots_pill(); a = eo((lt - 0.9) / 0.15); paste(cv, sp, PX + 30 - pd_, dots_y + off - pd_, alpha=a)
        for k in range(3):
            b = 0.5 + 0.5 * math.sin(lt * 10 - k * 0.9); cx = PX + 30 + 52 + k * 42; cy = dots_y + off + 42 - 6 * b
            d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=(int(120 + 100 * b), int(170 + 70 * b), 255, 255))
    for e in els:
        a = eo((lt - e["t"]) / 0.28)
        if a <= 0: continue
        slide = int((1 - a) * (50 if e["kind"] != "user" else 36)); x = e["x"] - e["pad"] + (slide if e["kind"] == "chip" else 0); y = e["y"] - e["pad"] + off + (0 if e["kind"] == "chip" else slide)
        if e["kind"] == "user": paste(cv, e["sp"], x, y, alpha=min(1, a * 1.5), cropw=e["pad"] + (e["w"] + e["pad"]) * eo((lt - e["t"]) / 0.45))
        else: paste(cv, e["sp"], x, y, alpha=a)
    paste(cv, LABEL, W / 2 - LABEL.width / 2, PY + PHT + 40)

def draw_intro(cv, lt, t):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for k in range(3):
        p = (lt * 0.6 + k / 3) % 1; r = 200 + p * 520; d.ellipse((W / 2 - r, 640 - r, W / 2 + r, 640 + r), outline=CY + (int(150 * (1 - p)),), width=3)
    cv.alpha_composite(ov); s = 0.55 + 0.45 * eo(lt / 0.7); size = int(400 * s)
    gl, gp = glow(LOGO.resize((size, size), Image.LANCZOS), 30, CY, 0.8); paste(cv, gl, W / 2 - gl.width / 2, 640 - gl.height / 2, alpha=eo(lt / 0.4))
    sp, pd_ = tsprite("Wolf", F(BOLD, 190), WH + (255,), CY, 18); a = eo((lt - 0.9) / 0.4); paste(cv, sp, W / 2 - sp.width / 2, 930 - pd_ + (1 - a) * 40, alpha=a)
    sp, pd_ = tsprite("Your family's own AI assistant", F(BOLD, 50), (215, 228, 250, 255), TL, 10); a = eo((lt - 1.7) / 0.4); paste(cv, sp, W / 2 - sp.width / 2, 1190 + (1 - a) * 30, alpha=a)

@lru_cache(maxsize=None)
def end_sprites():
    L = []
    def T(text, fnt, col, y, t, g=None): sp, p = tsprite(text, fnt, col, g, 12 if g else 0); L.append((sp, y - p, t))
    T("Wolf", F(BOLD, 130), WH + (255,), 520, 0.15, CY)
    T("Your family's own AI assistant,", F(BOLD, 46), (215, 228, 250, 255), 690, 0.4)
    L.append(("PRICE", 765, 0.65))
    T("£69 per person, or £179 for mum, dad", F(REG, 36), (225, 232, 248, 255), 900, 0.95); T("and one child. One-off price.", F(REG, 36), (225, 232, 248, 255), 946, 0.95)
    T("Finds options. Books nothing.", F(BOLD, 40), WH + (255,), 1040, 1.2, TL)
    T("Over 18 only. Under 16s need a parent's OK.", F(REG, 33), (225, 232, 248, 255), 1150, 1.5)
    T("Made and shipped by a third party.", F(REG, 31), (160, 178, 208, 255), 1230, 1.7); T("Jay does not personally do the work.", F(REG, 31), (160, 178, 208, 255), 1274, 1.7)
    T("Screens simulated.", F(REG, 28), (160, 178, 208, 255), 1340, 1.9); return L

def draw_end(cv, lt, t):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for k in range(3):
        p = (lt * 0.5 + k / 3) % 1; r = 150 + p * 420; d.ellipse((W / 2 - r, 380 - r, W / 2 + r, 380 + r), outline=CY + (int(110 * (1 - p)),), width=3)
    cv.alpha_composite(ov); gl, gp = glow(LOGO.resize((290, 290), Image.LANCZOS), 24, CY, 0.7); paste(cv, gl, W / 2 - gl.width / 2, 380 - gl.height / 2, alpha=eo(lt / 0.4))
    for sp, y, ti in end_sprites():
        a = eo((lt - ti) / 0.35)
        if sp == "PRICE":
            pulse = 0.75 + 0.25 * math.sin(t * 4); s2, p2 = tsprite("from £69.", F(BOLD, 92), OR + (255,), OR, 20); paste(cv, s2, W / 2 - s2.width / 2, y - p2 + (1 - a) * 30, alpha=a * (0.8 + 0.2 * pulse))
        else: paste(cv, sp, W / 2 - sp.width / 2, y + (1 - a) * 30, alpha=a)

def glitch(rgb, lt, seed):
    k = 1 - lt / 0.2; s = int(16 * k) + 2; out = rgb.copy(); out[..., 0] = np.roll(rgb[..., 0], s, 1); out[..., 2] = np.roll(rgb[..., 2], -s, 1)
    r = np.random.RandomState(seed)
    for _ in range(6):
        y0 = r.randint(0, H - 140); hh = r.randint(16, 120); out[y0:y0 + hh] = np.roll(out[y0:y0 + hh], int(r.randint(-70, 70) * k), 1)
    return out

# ---------------- timeline + audio ----------------
def timeline(name):
    if name == "long":
        hol = os.path.exists(os.path.join(HERE, "shots", "holiday.png")); tl = [("photo", "dan", 3.2, "Forgot to send the quote?"), ("scene", 8, SC_T, "dan"), ("photo", "dan", 2.0, "Reminded. Back to work."), ("intro", None, INTRO_T, None),
            ("photo", "mirror", 2.8, "First drop-off done. What's next?"), ("photo", "dash", 2.4, "A quick check while parked."), ("scene", 9, SC_T, "dash")]
        if hol: tl.append(("photo", "holiday", 3.0, "Miles from home. Still in the loop."))
        tl += [("scene", 10, SC_T, "holiday" if hol else None), ("globe", None, 5.5, None), ("photo", "couple", 3.0, "One family calendar. Anyone can ask."), ("scene", 1, SC_T, "couple")]
        tl += [("scene", i, SC_T, None) for i in (0, 4, 2, 6, 3, 5, 7)] + [("trust", None, 5.0, None), ("tiers", None, 8.5, None), ("end", None, 6.5, None)]; return tl
    if name == "demo": return [("intro", None, INTRO_T, None)] + [("scene", i, SC_T, None) for i in range(8)] + [("end", None, END_DEMO, None)]
    if name == "dan": return [("photo", "dan", 3.2, "Forgot to send the quote?"), ("scene", 8, SC_T, "dan"), ("photo", "dan", 2.0, "Reminded. Back to work."), ("end", None, 15.0 - 3.2 - SC_T - 2.0, None)]
    if name == "mum": return [("photo", "mirror", 2.8, "First drop-off done. What's next?"), ("photo", "dash", 2.4, "A quick check while parked."), ("scene", 9, SC_T, "dash"), ("end", None, 15.0 - 5.2 - SC_T, None)]
    if name == "family": return [("photo", "couple", 3.0, "One family calendar. Anyone can ask."), ("scene", 1, SC_T, "couple"), ("end", None, 15.0 - 3.0 - SC_T, None)]
    pairs = {"ad1": (0, 1), "ad2": (2, 6), "ad3": (3, 4), "ad4": (5, 7)}[name]
    return [("scene", pairs[0], SC_T, None), ("scene", pairs[1], SC_T, None), ("end", None, 15.0 - 2 * SC_T, None)]

def synth(path, total, tl):
    sr = 44100; n = int(sr * total); t = np.arange(n) / sr; sig = np.zeros(n)
    pump = 1 - 0.55 * np.exp(-(t % BEAT) * 9)
    roots = [55.0, 43.65, 65.41, 49.0]; chords = [[220, 261.6, 329.6], [174.6, 220, 261.6], [261.6, 329.6, 392], [196, 246.9, 293.7]]
    bar = ((t // (4 * BEAT)).astype(int)) % 4
    for ci in range(4):
        m = np.convolve((bar == ci).astype(float), np.ones(3000) / 3000, mode="same")
        sig += pump * m * (np.sin(2 * np.pi * roots[ci] * t) * 0.28 + sum(np.sin(2 * np.pi * f * t) * 0.045 * (0.6 + 0.4 * np.sin(t * 0.8)) for f in chords[ci]))
    step = BEAT / 4; k = 0
    while k * step < total:                                       # 16th arp
        t0 = k * step; ch = chords[int(t0 // (4 * BEAT)) % 4]; f = ch[[0, 1, 2, 1, 0, 2, 1, 2][k % 8]] * (2 if (k // 8) % 2 else 1)
        i0 = int(sr * t0); L = int(sr * 0.2); tt = np.arange(L) / sr
        if i0 + L < n: sig[i0:i0 + L] += (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * 2 * f * tt) + 0.2 * np.sin(2 * np.pi * 3 * f * tt)) * np.exp(-tt * 18) * 0.045
        k += 1
    for b in range(int(total / BEAT) + 1):                        # kick + hats
        i0 = int(sr * b * BEAT); L = int(sr * 0.22); tt = np.arange(L) / sr
        if i0 + L < n: sig[i0:i0 + L] += np.sin(2 * np.pi * (45 * tt + 75 * (1 - np.exp(-tt * 30)) / 30 * 0 + 120 * np.exp(-tt * 25) / 25 * 6)) * np.exp(-tt * 14) * 0.45
        j0 = int(sr * (b + 0.5) * BEAT); Lh = int(sr * 0.05)
        if j0 + Lh < n: sig[j0:j0 + Lh] += np.diff(np.random.RandomState(b).randn(Lh + 1)) * np.exp(-np.arange(Lh) / sr * 90) * 0.06
    pt = np.arange(int(sr * 0.9)) / sr; ping = (np.sin(2 * np.pi * 1318.5 * pt) + 0.5 * np.sin(2 * np.pi * 1975.5 * pt) + 0.25 * np.sin(2 * np.pi * 2637 * pt)) * np.exp(-pt * 5) * 0.28
    wt = np.arange(int(sr * 0.4)) / sr; whoosh = (np.sin(2 * np.pi * (180 * wt + 2200 * wt ** 2 / 0.8)) * 0.5 + np.random.RandomState(3).randn(len(wt)) * 0.25) * np.sin(np.pi * wt / 0.4) ** 2 * 0.22
    cur = 0.0
    for kind, idx, dur, *_ in tl:
        for s_, sp in ((cur, whoosh),) + (((cur + RS, ping),) if kind == "scene" else ()):
            i0 = int(sr * s_)
            if i0 < n: sig[i0:i0 + len(sp)] += sp[:n - i0]
        cur += dur
    sig *= np.clip(np.minimum(t / 0.4, (total - t) / 1.6), 0, 1); sig = np.tanh(sig * 1.3); sig = sig / np.abs(sig).max() * 0.85
    with wave.open(path, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((sig * 32767).astype(np.int16).tobytes())

def frame(tl, t, fi):
    cur = 0.0; seg = tl[-1]; lt = t - sum(s[2] for s in tl[:-1])
    for s in tl:
        if t < cur + s[2]: seg = s; lt = t - cur; break
        cur += s[2]
    kind, idx, sdur, extra = seg; cv = background(t, extra if kind == "scene" else None)
    if kind == "intro": draw_intro(cv, lt, t)
    elif kind == "globe": draw_globe(cv, lt, t)
    elif kind == "tiers": draw_tiers(cv, lt, t)
    elif kind == "trust": draw_trust(cv, lt, t)
    elif kind == "photo": draw_photo(cv, idx, lt, sdur, extra)
    elif kind == "scene": draw_scene(cv, idx, lt, t)
    else: draw_end(cv, lt, t)
    cv.alpha_composite(STATIC); rgb = np.asarray(cv.convert("RGB"))
    if lt < 0.2 and t > 0.1: rgb = glitch(rgb, lt, fi)
    return rgb

def main():
    name = sys.argv[1]; tl = timeline(name); total = sum(s[2] for s in tl); out = os.path.join(HERE, "out_neo"); os.makedirs(out, exist_ok=True)
    if "--preview" in sys.argv:
        for ts in sys.argv[sys.argv.index("--preview") + 1].split(","):
            Image.fromarray(frame(tl, float(ts), int(float(ts) * 30))).save(os.path.join(out, f"prev_{name}_{ts}.png"))
        return
    aud = os.path.join(out, f"{name}.wav"); mp4 = os.path.join(out, f"Wolf_{name}_NEO_DRAFT.mp4"); N = int(total * FPS)
    if "--chunk" in sys.argv:
        k, n = int(sys.argv[sys.argv.index("--chunk") + 1]), int(sys.argv[sys.argv.index("--chunk") + 2]); a, b = N * k // n, N * (k + 1) // n
        p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", os.path.join(out, f"{name}_chunk{k}.mp4")], stdin=subprocess.PIPE)
        for fi in range(a, b): p.stdin.write(frame(tl, fi / FPS, fi).tobytes())
        p.stdin.close(); p.wait(); return
    if "--parallel" in sys.argv:
        synth(aud, total, tl); ps = [subprocess.Popen([sys.executable, "-I", os.path.abspath(__file__), name, "--chunk", str(k), "4"]) for k in range(4)]
        [q.wait() for q in ps]; lst = os.path.join(out, f"{name}_chunks.txt"); open(lst, "w").write("".join(f"file '{os.path.join(out, name + '_chunk' + str(k) + '.mp4')}'\n" for k in range(4)))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", aud, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total}", "-movflags", "+faststart", mp4], check=True); print("done", mp4, round(total, 1), "s"); return
    synth(aud, total, tl)
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", aud,
                          "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", f"{total}", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    for fi in range(int(total * FPS)): p.stdin.write(frame(tl, fi / FPS, fi).tobytes())
    p.stdin.close(); p.wait(); print("done", mp4, round(total, 1), "s")

if __name__ == "__main__": main()
