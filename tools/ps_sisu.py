#!/usr/bin/env python3
"""Psühholoogia sisu: sisu/psuhholoogia/T0N.md → teemad/ps-t0N-MM-*.json + data/tunnid.json (teemad, plokid, faktid).

Kasutus:
    python3 tools/ps_sisu.py            # kõik tunnid, mille fail on olemas
    python3 tools/ps_sisu.py 7 8        # ainult tunnid 7 ja 8

Faili kuju (vt sisu/psuhholoogia/README.md):

    # TUND 7
    plokk: Tuvastamine ja eakad = 1,2,3
    plokk: Teised grupid = 4,5,6

    ## FAKTID
    ### Arvud
    - Psühhoosi esineb vangistatud noortel 10 korda rohkem → 6

    ## TEEMA 1 | slug | ikoon | lühend
    pealkiri: …
    lyhidalt: …
    ### Materjali alapealkiri
    Lõik tekst …            (tühi rida = uus lõik)
    - punkt
    1. nummerdatud punkt
    ### SKEEM
    ```json
    { "tyyp": "kaardid", … }      (üks või mitu ```json plokki)
    ```
    ### INSPEKTOR
    tekst / - punktid
    olukord: …
    mida teha: …
    ### VÄLJAST
    - tekst || allikas
    ### ERINEVUSED
    - teema || mida ütleb materjal || mida ütleb ametlik allikas || märkus (valikuline)

Harjutused võetakse vanadest teemafailidest (vt KAART_HARJUTUSED) – uusi ei lisata.
"""
import json, os, re, sys, glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SISU = os.path.join(REPO, "sisu", "psuhholoogia")

VAIKIMISI_VALJAST = {"tekst": "„Inspektor-kontaktisiku töös” osa (näide ja soovitused) on koostatud selle lehe jaoks tunnimaterjali põhjal; see ei ole õppejõu materjal.",
                     "allikas": "koostatud lehe jaoks – ei pärine tunnimaterjalist"}


def plokk_tekstist(read):
    """Read → {"sisu": [{"tekst"}|{"punktid"}|{"loend"}, …]} samas järjekorras nagu failis.
    Tühi rida = uus lõik; '- ' = punkt; '1. ' = nummerdatud punkt; taandega rida jätkab eelmist punkti."""
    sisu, praegu = [], []
    def sulge():
        if praegu:
            sisu.append({"tekst": " ".join(praegu)}); praegu.clear()
    def lisa(liik, x):
        sulge()
        if sisu and liik in sisu[-1]:
            sisu[-1][liik].append(x)
        else:
            sisu.append({liik: [x]})
    for r in read:
        s = r.rstrip()
        if not s.strip():
            sulge(); continue
        if s.startswith("- "):
            lisa("punktid", s[2:].strip()); continue
        m = re.match(r"^\d+\.\s+(.*)", s)
        if m:
            lisa("loend", m.group(1).strip()); continue
        if s.startswith("  ") and not praegu and sisu and ("punktid" in sisu[-1] or "loend" in sisu[-1]):
            k = "punktid" if "punktid" in sisu[-1] else "loend"
            sisu[-1][k][-1] += " " + s.strip(); continue
        praegu.append(s.strip())
    sulge()
    return {"sisu": sisu} if sisu else {}


def loe_tund(nr):
    p = os.path.join(SISU, f"T0{nr}.md")
    tekst = open(p, encoding="utf-8").read()
    tekst = re.sub(r"<!--.*?-->", "", tekst, flags=re.S)
    plokid, faktid, teemad = [], [], []
    osa = None
    for blk in re.split(r"^(?=## )", tekst, flags=re.M):
        if blk.startswith("# "):
            for r in blk.splitlines():
                m = re.match(r"^plokk:\s*(.+?)\s*=\s*([\d, ]+)$", r)
                if m:
                    plokid.append((m.group(1), [int(x) for x in m.group(2).split(",")]))
            continue
        if blk.startswith("## FAKTID"):
            g = None
            for r in blk.splitlines()[1:]:
                if r.startswith("### "):
                    g = {"pealkiri": r[4:].strip(), "read": []}; faktid.append(g)
                elif r.startswith("- ") and g is not None:
                    m = re.match(r"^- (.*?)\s*→\s*(\d+)\s*$", r)
                    g["read"].append({"tekst": m.group(1), "teema": int(m.group(2))} if m else {"tekst": r[2:].strip()})
            continue
        m = re.match(r"^## TEEMA (\d+) \| (\S+) \| (\S+) \| (.+)$", blk.splitlines()[0])
        if not m:
            continue
        t = {"jrk": int(m.group(1)), "slug": m.group(2), "ikoon": m.group(3), "lyhend": m.group(4).strip(),
             "materjal": [], "skeemid": [], "inspektor": {}, "valjast": [], "erinevused": []}
        alam = re.split(r"^(?=### )", blk, flags=re.M)
        for r in alam[0].splitlines()[1:]:
            if r.startswith("pealkiri:"): t["pealkiri"] = r.split(":", 1)[1].strip()
            elif r.startswith("lyhidalt:"): t["lyhidalt"] = r.split(":", 1)[1].strip()
        for a in alam[1:]:
            read = a.splitlines(); pk = read[0][4:].strip(); keha = read[1:]
            if pk == "SKEEM":
                for j in re.findall(r"```json\s*\n(.*?)\n```", "\n".join(keha), flags=re.S):
                    t["skeemid"].append(json.loads(j))
            elif pk == "INSPEKTOR":
                tav, naide = [], {}
                for r in keha:
                    if r.startswith("olukord:"): naide["olukord"] = r.split(":", 1)[1].strip()
                    elif r.startswith("mida teha:"): naide["analyys"] = r.split(":", 1)[1].strip()
                    else: tav.append(r)
                t["inspektor"] = plokk_tekstist(tav)
                if naide: t["inspektor"]["naide"] = naide
            elif pk == "ERINEVUSED":
                for r in keha:
                    if r.startswith("- ") and "||" in r:
                        osad = [x.strip() for x in r[2:].split("||")]
                        e = {"silt": "Õppematerjal", "teema": osad[0], "konspekt": osad[1], "ametlik": osad[2]}
                        if len(osad) > 3 and osad[3]: e["markus"] = osad[3]
                        if len(osad) > 4: e["silt2"] = osad[4]
                        t["erinevused"].append(e)
            elif pk == "VÄLJAST":
                for r in keha:
                    if r.startswith("- ") and "||" in r:
                        x, y = r[2:].split("||", 1)
                        t["valjast"].append({"tekst": x.strip(), "allikas": y.strip()})
            else:
                b = {"pealkiri": pk}; b.update(plokk_tekstist(keha)); t["materjal"].append(b)
        teemad.append(t)
    return plokid, faktid, teemad


def main(nrid):
    tunnid_p = os.path.join(REPO, "data", "tunnid.json")
    tunnid = json.load(open(tunnid_p, encoding="utf-8"))
    kaart_p = os.path.join(SISU, "harjutuste_kaart.json")
    kaart = json.load(open(kaart_p, encoding="utf-8")) if os.path.exists(kaart_p) else {}
    vanad_harj = {}
    for p in glob.glob(os.path.join(REPO, "teemad", "ps-*.json")):
        d = json.load(open(p, encoding="utf-8"))
        vanad_harj[d["id"]] = d.get("harjutused", [])
    vanad_harj.update(json.load(open(os.path.join(SISU, "vanad_harjutused.json"), encoding="utf-8")) if os.path.exists(os.path.join(SISU, "vanad_harjutused.json")) else {})
    for nr in nrid:
        tid = f"ps-t0{nr}"
        plokid, faktid, teemad = loe_tund(nr)
        tund = next(t for t in tunnid["tunnid"] if t["id"] == tid)
        for p in glob.glob(os.path.join(REPO, "teemad", f"{tid}-*.json")):
            os.remove(p)
        kirjed = []
        for t in teemad:
            id_ = f"{tid}-{t['jrk']:02d}"
            harj = []
            for vana in kaart.get(id_, []):
                harj += vanad_harj.get(vana, [])
            valjast = t["valjast"] or [VAIKIMISI_VALJAST]
            d = {"id": id_, "tund": tid, "jrk": t["jrk"], "mall": "psuh", "pealkiri": t["pealkiri"], "lyhend": t["lyhend"],
                 "ikoon": t["ikoon"], "lyhidalt": t["lyhidalt"], "materjal": t["materjal"], "skeemid": t["skeemid"],
                 "inspektor": t["inspektor"], "harjutused": harj, "valjast": valjast,
                 "kysimused": [], "vastus": [], "erinevused": t["erinevused"]}
            fail = f"teemad/{id_}-{t['slug']}.json"
            json.dump(d, open(os.path.join(REPO, fail), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            kirjed.append({"id": id_, "fail": fail})
        tund["teemad"] = kirjed
        if plokid:
            tund["plokid"] = [{"pealkiri": p, "teemad": [f"{tid}-{j:02d}" for j in js]} for p, js in plokid]
        else:
            tund["plokid"] = [{"pealkiri": "Peatükid", "teemad": [k["id"] for k in kirjed]}]
        for g in faktid:
            for r in g["read"]:
                if "teema" in r: r["teema"] = f"{tid}-{r['teema']:02d}"
        tund["faktid"] = faktid
        print(f"{tid}: {len(kirjed)} teemat, {sum(len(g['read']) for g in faktid)} fakti")
    json.dump(tunnid, open(tunnid_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    nrid = [int(x) for x in sys.argv[1:]] or [n for n in range(1, 9) if os.path.exists(os.path.join(SISU, f"T0{n}.md"))]
    main(nrid)
