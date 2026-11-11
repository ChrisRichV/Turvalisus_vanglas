#!/usr/bin/env python3
"""Ehitab data/seadused.json ja kontrollib kogu sisu.

Kasutus:
    python3 tools/ehita.py --materjal "/tee/Ruth tunnid"

Mida teeb:
  1. Loeb data/tunnid.json, kõik teemafailid ja data/terminid.json.
  2. Leiab kõik viited ([[PS § 18]], "viide": "...", "viited": [...]).
  3. Võtab iga viidatud sätte teksti SÕNA-SÕNALT algfailist (tools/seadused.py)
     ja kirjutab data/seadused.json.
  4. Kontrollib, et:
       - iga viidatud säte on algtekstis olemas;
       - iga "tsitaat" leidub algtekstis sõna-sõnalt;
       - iga {{termin}} on sõnastikus;
       - harjutuste õige vastuse indeks on olemas;
       - repos ei ole AK-märget ega AK-standarditega kattuvat teksti.
  Vea korral lõpetab koodiga 1.
"""
import argparse, json, os, re, sys, datetime, glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("--materjal", default=os.environ.get("MATERJAL", "/mnt/user-data/uploads/Ruth tunnid"))
args = ap.parse_args()
os.environ["MATERJAL"] = args.materjal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seadused as S  # noqa: E402

REF_IN_TEXT = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
TERM_IN_TEXT = re.compile(r"\{\{([^}|]+)(?:\|[^}]+)?\}\}")
REF = re.compile(r"^(?P<akt>.+?) (?P<vorm>§|art|rule) ?(?P<nr>\d+(?:\^\d+)?)(?: lg (?P<lg>\d+(?:\^\d+)?))?(?: p (?P<p>\S+))?\s*$")

vead, hoiatused = [], []

def parse_ref(r):
    m = REF.match(r.strip())
    if not m:
        return None
    return m.group("akt"), m.group("vorm"), m.group("nr"), m.group("lg")

lahkad = []   # skeemid „lahka”: osad peavad sättes sõna-sõnalt leiduma

def walk(o, path, refs, terms, quotes):
    if isinstance(o, dict):
        if o.get("tyyp") == "lahka":
            lahkad.append((o, path))
        for k, v in o.items():
            if k == "viide" and isinstance(v, str):
                refs.append((v, path))
            elif k in ("viited", "seos") and isinstance(v, list):
                refs.extend((x, path) for x in v)
            if k == "tsitaat" and isinstance(v, dict):
                quotes.append((v, path))
                continue
            walk(v, f"{path}.{k}", refs, terms, quotes)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{path}[{i}]", refs, terms, quotes)
    elif isinstance(o, str):
        refs.extend((m, path) for m in REF_IN_TEXT.findall(o))
        terms.extend((m, path) for m in TERM_IN_TEXT.findall(o))

# --- lae sisu
tunnid = json.load(open(os.path.join(REPO, "data/tunnid.json"), encoding="utf-8"))
terminid = json.load(open(os.path.join(REPO, "data/terminid.json"), encoding="utf-8"))
refs, terms, quotes = [], [], []
# --- ained ja id-de unikaalsus
aine_idd = {a["id"] for a in tunnid.get("ained", [])}
naha_tund, naha_teema = set(), set()
for t in tunnid["tunnid"]:
    if t.get("aine") not in aine_idd:
        vead.append(f"tund {t['id']}: tundmatu aine '{t.get('aine')}'")
    if t["id"] in naha_tund:
        vead.append(f"tunni id kordub: {t['id']}")
    naha_tund.add(t["id"])
    for tm in t["teemad"]:
        if tm["id"] in naha_teema:
            vead.append(f"teema id kordub: {tm['id']}")
        naha_teema.add(tm["id"])
teema_failid = []
for t in tunnid["tunnid"]:
    for tm in t["teemad"]:
        p = os.path.join(REPO, tm["fail"])
        if not os.path.exists(p):
            vead.append(f"Teemafail puudub: {tm['fail']}"); continue
        d = json.load(open(p, encoding="utf-8"))
        teema_failid.append(p)
        if d.get("id") != tm["id"]:
            vead.append(f"{tm['fail']}: id {d.get('id')} ≠ {tm['id']}")
        for i, h in enumerate(d.get("harjutused", [])):
            if h["tyyp"] == "fakt" and not (0 <= h["oige"] < len(h["valikud"])):
                vead.append(f"{tm['fail']}: harjutus {i} – vale 'oige' indeks")
        walk(d, tm["fail"], refs, terms, quotes)
walk(terminid, "data/terminid.json", refs, terms, quotes)
kiir_p = os.path.join(REPO, "data/kiirotsing.json")
if os.path.exists(kiir_p):
    kiir = json.load(open(kiir_p, encoding="utf-8"))
    teema_idd = {tm["id"] for t in tunnid["tunnid"] for tm in t["teemad"]}
    for i, r in enumerate(kiir["read"]):
        refs.extend((x, f"data/kiirotsing.json[{i}]") for x in r["pohiseadus"] + r["vangla"])
        if r.get("teema_id") and r["teema_id"] not in teema_idd:
            vead.append(f"data/kiirotsing.json[{i}]: tundmatu teema_id {r['teema_id']}")
# --- mõistekaart: viited, terminid, teemad ja seoste otsad
mk_p = os.path.join(REPO, "data/moistekaart.json")
if os.path.exists(mk_p):
    mk = json.load(open(mk_p, encoding="utf-8"))
    walk(mk, "data/moistekaart.json", refs, terms, quotes)
    mk_idd = set()
    for i, k in enumerate(mk["moisted"]):
        w = f"data/moistekaart.json moisted[{i}] ({k.get('id')})"
        if k["id"] in mk_idd: vead.append(f"{w}: id kordub")
        mk_idd.add(k["id"])
        if not k.get("teemad"): vead.append(f"{w}: teemad puuduvad")
        for tid in k.get("teemad", []):
            if tid not in naha_teema: vead.append(f"{w}: tundmatu teema {tid}")
        if k.get("termin"): terms.append((k["termin"], w))
        if not k.get("selgitus") and not k.get("termin"): vead.append(f"{w}: selgitus või termin puudub")
    for i, x in enumerate(mk["seosed"]):
        for o in ("a", "b"):
            if x[o] not in mk_idd: vead.append(f"data/moistekaart.json seosed[{i}]: tundmatu mõiste {x[o]}")

# --- terminid
for t, where in terms:
    if t not in terminid:
        vead.append(f"{where}: termin '{t}' puudub sõnastikust")

# --- sätted
MANDELA_FOOTER = re.compile(r"^(\d+/\d+|United Nations Standard Minimum Rules for the|Treatment of Prisoners \(the Nelson Mandela Rules\)|A/RES/70/175)$")

def puhasta(akt, read):
    """Ainult vormi parandus, sisu ei muutu (dokumenteeritud metaandmetes)."""
    if akt != "Mandela":
        return read
    read = [r for r in read if not MANDELA_FOOTER.match(r) and not re.match(r"^(A/RES/70/175|\d+/\d+)\b", r)]
    # lõpust ära järgmise reegli/jao pealkiri (lühike, ilma lõpumärgita)
    while len(read) > 2 and not re.search(r"[.;:]$", read[-1]) and len(read[-1]) < 70 and not read[-1].startswith("("):
        read.pop()
    # PDF-i reamurdude liitmine lõikudeks; "Rule N" jääb eraldi reaks
    out = []
    for r in read:
        algus = re.match(r"^(Rule \d+$|\d+\.|\([a-z]\))", r)
        if out and not algus and not out[-1].startswith("Rule ") and not out[-1].endswith(":"):
            out[-1] += " " + r
        elif out and re.fullmatch(r"\d+\.", out[-1]):
            out[-1] += " " + r
        else:
            out.append(r)
    return out

satted, aktid = {}, {}
for r, where in refs:
    pr = parse_ref(r)
    if not pr:
        vead.append(f"{where}: viidet ei saa parsida: '{r}'"); continue
    akt, vorm, nr, lg = pr
    if akt not in S.ACTS:
        vead.append(f"{where}: tundmatu akt '{akt}' viites '{r}'"); continue
    if S.ACTS[akt][3] != vorm:
        vead.append(f"{where}: akti '{akt}' viitevorm on '{S.ACTS[akt][3]}', mitte '{vorm}' ('{r}')"); continue
    key = f"{akt} {vorm} {nr}"
    if key in satted:
        continue
    try:
        read = S.unit_text(akt, nr)
    except KeyError as e:
        vead.append(f"{where}: {e}"); continue
    satted[key] = {"akt": akt, "nr": nr, "read": puhasta(akt, read)}
    if akt not in aktid:
        m = S.meta(akt)
        if akt == "Mandela":
            m["markus"] = "Tekst on võetud originaal-PDF-ist (paigutust säilitav väljavõte): lehekülje päised/jalused on eemaldatud ja reamurrud liidetud. Sõnu ei ole muudetud. Ametlikku eestikeelset tõlget ei ole."
            if not S.load(akt)[2].get("_pdf_layout"):
                hoiatused.append("Mandela: pdftotext puudub – kasutati tekstifaili, kus mõne loetelu sõnajärg võib olla nihkes")
        aktid[akt] = m

# lõike olemasolu kontroll (hoiatus)
for r, where in refs:
    pr = parse_ref(r)
    if not pr or not pr[3]:
        continue
    akt, vorm, nr, lg = pr
    key = f"{akt} {vorm} {nr}"
    if key not in satted:
        continue
    read = satted[key]["read"]
    leitud = any(x.startswith(f"({lg})") or x.startswith(f"{lg}. ") or x.startswith(f"{lg}.") for x in read)
    if not leitud and akt == "PS":
        leitud = int(lg.split("^")[0]) <= len(read)
    if not leitud:
        vead.append(f"{where}: lõiget {lg} ei leitud sättes {key} (viide '{r}')")

# --- normi lahkamine: iga märgitud lõik peab sättes olema sõna-sõnalt
for o, where in lahkad:
    pr = parse_ref(o["viide"])
    key = pr and f"{pr[0]} {pr[1]} {pr[2]}"
    if not key or key not in satted:
        vead.append(f"{where}: lahka – sätet ei leitud ({o.get('viide')})"); continue
    tekst = " ".join(satted[key]["read"])
    for x in o.get("osad", []):
        if x["tekst"] not in tekst:
            vead.append(f"{where}: lahka – lõiku „{x['tekst']}” ei ole sättes {o['viide']} sõna-sõnalt")

# --- tsitaadid
def norm_all(t):
    return re.sub(r"\s+", " ", t.replace(" ", " ")).strip()
for q, where in quotes:
    akt = q["viide"].split(" ")[0]
    if akt not in S.ACTS:
        vead.append(f"{where}: tsitaadi allikas tundmatu: {q['viide']}"); continue
    src = norm_all(open(S.ACTS[akt][0], encoding="utf-8").read())
    if norm_all(q["tekst"]) not in src:
        vead.append(f"{where}: tsitaati ei leitud sõna-sõnalt allikast {q['viide']}")

# --- AK kontroll
repo_tekst = ""
for p in glob.glob(os.path.join(REPO, "**/*"), recursive=True):
    if os.path.isfile(p) and p.endswith((".json", ".html", ".js", ".css", ".md")) and "/.git/" not in p:
        t = open(p, encoding="utf-8", errors="ignore").read()
        if "data/seadused.json" not in p:
            repo_tekst += "\n" + t
        if re.search(r"ASUTUSESISESEKS KASUTAMISEKS", t) and not p.endswith(("README-projekt.md", "CLAUDE.md", "ehita.py")):
            vead.append(f"AK-märge failis {os.path.relpath(p, REPO)}")

def grams(t, n=8):
    w = re.findall(r"\w+", t.lower()); return {" ".join(w[i:i+n]) for i in range(len(w)-n)}
rg = grams(repo_tekst)

# 1) Sõrmejäljed (tools/ak_sormejaljed.txt): AK-tekstide 8-sõnaliste lõikude räsid.
#    Töötab ka siis, kui AK-failid on materjalikaustast kustutatud.
import hashlib
fp_fail = os.path.join(REPO, "tools/ak_sormejaljed.txt")
if os.path.exists(fp_fail):
    fp = {l.strip() for l in open(fp_fail, encoding="utf-8") if l.strip() and not l.startswith("#")}
    kattuv = [g for g in rg if hashlib.sha256(g.encode()).hexdigest()[:16] in fp]
    if kattuv:
        vead.append(f"AK-sõrmejäljega kattuv tekst ({len(kattuv)} lõiku), nt: {sorted(kattuv)[:3]}")
else:
    hoiatused.append("tools/ak_sormejaljed.txt puudub – sõrmejälje kontroll jäi tegemata")

# 2) Materjalikaustas praegu olevad AK-märgisega tekstid (uued failid või lehed).
ak_leitud = 0
for f in glob.glob(os.path.join(args.materjal, "**/*.txt"), recursive=True) + glob.glob(os.path.join(args.materjal, "**/*.md"), recursive=True):
    if "/vastused/" in f.replace("\\", "/") or os.path.basename(f) in ("00_SISUKORD.md", "00_LOEMIND.md"):
        continue
    t = open(f, encoding="utf-8", errors="ignore").read()
    if "ASUTUSESISESEKS KASUTAMISEKS" not in t or t.startswith("ALLIKAS: Riigi Teataja"):
        continue  # seadused (nt AvTS) mainivad märget, kuid ei ole ise AK
    body = t.split("========================================", 1)[-1]
    lehed = re.split(r"--- (?:Lk|Slaid) \d+ ---", body)
    pais = "\n".join(body.splitlines()[:12])
    osad = [body] if "ASUTUSESISESEKS KASUTAMISEKS" in pais else [x for x in lehed if "ASUTUSESISESEKS KASUTAMISEKS" in x]
    for osa in osad:
        ak_leitud += 1
        k = rg & grams(osa)
        if k:
            vead.append(f"AK-märgisega tekstiga kattuv sisu ({os.path.relpath(f, args.materjal)}): {sorted(k)[:3]}")
if ak_leitud:
    hoiatused.append(f"Materjalis on {ak_leitud} AK-märgisega osa – kontrollitud, kattuvust repoga ei tohi olla")

# --- kirjuta
out = {
    "loodud": datetime.date.today().isoformat(),
    "markus": "Sätete tekstid on masinaga võetud ametlikest tekstifailidest; muudetud on ainult tühikuid ja reavahetusi.",
    "aktid": dict(sorted(aktid.items())),
    "satted": dict(sorted(satted.items())),
}
json.dump(out, open(os.path.join(REPO, "data/seadused.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"Teemasid: {len(teema_failid)} | viiteid: {len(refs)} | erinevaid sätteid: {len(satted)} | akte: {len(aktid)} | termineid: {len(set(t for t,_ in terms))} | tsitaate: {len(quotes)}")
for h in hoiatused:
    print("HOIATUS:", h)
if vead:
    print(f"\n{len(vead)} VIGA:")
    for v in vead:
        print(" -", v)
    sys.exit(1)
print("OK – kõik viited, tsitaadid ja terminid on kontrollitud.")
