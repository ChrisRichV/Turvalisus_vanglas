#!/usr/bin/env python3
"""Abifunktsioonid Excalidraw'-jooniste (psühholoogia) kavandamiseks.

Iga funktsioon tagastab skeemi objekti {"tyyp": "excalidraw", "pealkiri", "alt", "elemendid": [...]},
mille saab panna sisu/psuhholoogia/T0N.md faili ```json plokki. Elemendid on Excalidraw' vormingus
(sama, mida kasutab Excalidraw' connector), nii et joonist saab connectoriga eelvaadata ja edasi muuta.
Joonised on kitsad (≈ 480 px), et need oleksid ka telefonis loetavad.

Kasutus (näide):
    python3 tools/joonis.py radiaal "Haavatav kinnipeetav" "Psühhiaatriline diagnoos" "Madal haridustase" ...
"""
import json, math, sys

VARV = {  # (täide, joon)
    "sinine": ("#a5d8ff", "#4a9eed"), "roheline": ("#b2f2bb", "#22c55e"), "oranz": ("#ffd8a8", "#f59e0b"),
    "lilla": ("#d0bfff", "#8b5cf6"), "punane": ("#ffc9c9", "#ef4444"), "kollane": ("#fff3bf", "#f59e0b"),
    "turkiis": ("#c3fae8", "#06b6d4"), "roosa": ("#eebefa", "#ec4899"),
}
_n = [0]


def _id(p):
    _n[0] += 1
    return f"{p}{_n[0]}"


def kast(x, y, w, h, tekst, varv="sinine", fs=17, kuju="rectangle"):
    t, j = VARV[varv]
    e = {"type": kuju, "id": _id("b"), "x": round(x), "y": round(y), "width": round(w), "height": round(h),
         "backgroundColor": t, "fillStyle": "solid", "strokeColor": j, "label": {"text": tekst, "fontSize": fs}}
    if kuju == "rectangle":
        e["roundness"] = {"type": 3}
    return e


def nool(x1, y1, x2, y2, varv="#1e1e1e", silt=None, katkendlik=False, ots="arrow"):
    e = {"type": "arrow", "id": _id("a"), "x": round(x1), "y": round(y1), "width": round(x2 - x1), "height": round(y2 - y1),
         "points": [[0, 0], [round(x2 - x1), round(y2 - y1)]], "strokeColor": varv, "endArrowhead": ots}
    if silt:
        e["label"] = {"text": silt, "fontSize": 14}
    if katkendlik:
        e["strokeStyle"] = "dashed"
    return e


def tekst(x, y, t, fs=16, varv="#757575"):
    return {"type": "text", "id": _id("t"), "x": round(x), "y": round(y), "text": t, "fontSize": fs, "strokeColor": varv}


def _serv(cx, cy, w, h, tx, ty):
    """punkt ristküliku (cx,cy,w,h) serval suunas (tx,ty)"""
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    s = min((w / 2) / abs(dx) if dx else 1e9, (h / 2) / abs(dy) if dy else 1e9)
    return cx + dx * s, cy + dy * s


def skeem(pealkiri, alt, el):
    return {"tyyp": "excalidraw", "pealkiri": pealkiri, "alt": alt, "elemendid": el}


def radiaal(pealkiri, kesk, osad, varv_kesk="punane", varv="oranz", alt=None, all=None, suund="sisse"):
    """keskel mõiste, ümber osad (nooled osadest keskele või keskelt osadesse)"""
    el = []
    cx, cy, R = 240, 250, 205
    el.append(kast(cx - 95, cy - 48, 190, 96, kesk, varv_kesk, 19, "ellipse"))
    n = len(osad)
    for i, o in enumerate(osad):
        a = -math.pi / 2 + 2 * math.pi * i / n
        bx, by = cx + R * math.cos(a) * 1.05, cy + R * math.sin(a) * 0.95
        w, h = 150, 64
        el.append(kast(bx - w / 2, by - h / 2, w, h, o, varv, 16))
        p1 = _serv(bx, by, w + 8, h + 8, cx, cy)
        p2 = _serv(cx, cy, 200, 104, bx, by)
        el.append(nool(*(p1 + p2)) if suund == "sisse" else nool(*(p2 + p1)))
    if all:
        el.append(tekst(40, cy + R + 60, all))
    return skeem(pealkiri, alt or f"{kesk}: " + "; ".join(osad), el)


def ring(pealkiri, osad, kesk=None, alt=None, varvid=None):
    """tsükkel: osad ringis päripäeva, nooled järgmisele"""
    el = []
    cx, cy, R = 240, 250, 190
    n = len(osad)
    if kesk:
        el.append(kast(cx - 80, cy - 40, 160, 80, kesk, "kollane", 18, "ellipse"))
    pos = []
    for i, o in enumerate(osad):
        a = -math.pi / 2 + 2 * math.pi * i / n
        pos.append((cx + R * math.cos(a), cy + R * math.sin(a) * 0.92))
    w, h = 150, 66
    for i, (o, (bx, by)) in enumerate(zip(osad, pos)):
        v = (varvid or ["sinine"])[i % len(varvid or ["sinine"])]
        el.append(kast(bx - w / 2, by - h / 2, w, h, o, v, 16))
    for i in range(n):
        (ax, ay), (bx, by) = pos[i], pos[(i + 1) % n]
        p1 = _serv(ax, ay, w + 10, h + 10, bx, by)
        p2 = _serv(bx, by, w + 10, h + 10, ax, ay)
        el.append(nool(*(p1 + p2), varv="#757575"))
    return skeem(pealkiri, alt or " → ".join(osad) + " → (uuesti)", el)


def voog(pealkiri, sammud, alt=None, varvid=None, sildid=None):
    """vertikaalne voog: kastid üksteise all, nooled vahel; sammud = [(pealkiri, tekst?)]"""
    el = []
    y = 0
    w = 420
    for i, s in enumerate(sammud):
        t = s if isinstance(s, str) else (s[0] + ("\n" + s[1] if len(s) > 1 and s[1] else ""))
        v = (varvid or ["sinine"])[i % len(varvid or ["sinine"])]
        read = max(1, len(t) // 40 + t.count("\n") + 1)
        h = 34 + read * 21
        el.append(kast(30, y, w, h, t, v, 17))
        if i < len(sammud) - 1:
            el.append(nool(30 + w / 2, y + h + 4, 30 + w / 2, y + h + 40, silt=(sildid[i] if sildid else None)))
        y += h + 44
    return skeem(pealkiri, alt or " → ".join(s if isinstance(s, str) else s[0] for s in sammud), el)


def trepp(pealkiri, astmed, alt=None, varvid=None, tipp=None):
    """astmed alt üles diagonaalis (teekond, faasid); astmed = [(pealkiri, tekst)]"""
    el = []
    n = len(astmed)
    w, h, dx = 230, 92, (480 - 230) / max(1, n - 1)
    for i, (p, t) in enumerate(astmed):
        x, y = i * dx, (n - 1 - i) * (h + 18)
        v = (varvid or ["sinine"])[i % len(varvid or ["sinine"])]
        el.append(kast(x, y, w, h, f"{p}\n{t}" if t else p, v, 16))
        if i < n - 1:
            el.append(nool(x + w * 0.75, y - 4, x + dx + w * 0.3, y - 14, varv="#757575"))
    if tipp:
        el.append(tekst(0, n * (h + 18) + 4, tipp))
    return skeem(pealkiri, alt or " → ".join(a[0] for a in astmed), el)


def kaks_poolt(pealkiri, vasak, parem, vp="Pool A", pp="Pool B", vv="roheline", pv="punane", kesk=None, alt=None):
    """kaks veergu vastamisi (nt abi ↔ risk), keskel inimene/mõiste"""
    el = []
    if kesk:
        el.append(kast(130, 0, 230, 80, kesk, "kollane", 17, "ellipse"))
    y0 = 110 if kesk else 0
    if kesk:
        el.append(nool(225, 72, 60, y0 - 6, varv=VARV[vv][1], katkendlik=True, ots="arrow"))
        el.append(nool(265, 72, 430, y0 - 6, varv=VARV[pv][1], katkendlik=True, ots="arrow"))
    el.append(tekst(10, y0, vp, 18, "#15803d" if vv == "roheline" else "#1e1e1e"))
    el.append(tekst(250, y0, pp, 18, "#ef4444" if pv == "punane" else "#1e1e1e"))
    for col, (osad, v, x) in enumerate(((vasak, vv, 0), (parem, pv, 250))):
        y = y0 + 34
        for o in osad:
            read = max(1, len(o) // 22 + 1)
            hh = 30 + read * 20
            el.append(kast(x, y, 230, hh, o, v, 16))

            y += hh + 14
    el = [e for e in el if e]
    return skeem(pealkiri, alt or f"{vp}: " + "; ".join(vasak) + f". {pp}: " + "; ".join(parem), el)


if __name__ == "__main__":
    f = globals()[sys.argv[1]]
    print(json.dumps(f(sys.argv[2], sys.argv[3], sys.argv[4:]), ensure_ascii=False))
