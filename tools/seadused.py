"""Seaduste ja lepingute sätete väljavõtmine ametlikest tekstifailidest.

Põhimõte: sätte tekst võetakse failist SÕNA-SÕNALT. Muudetakse ainult tühikuid
(mitu tühikut/tabulaatorit -> üks tühik, tühjad read eemaldatakse, loetelu-täht
"a)" liidetakse järgneva reaga). Sõnu, kirjavahemärke ega järjekorda ei muudeta.
"""
import re, json, os, sys, unicodedata, shutil, subprocess

ROOT = os.environ.get("MATERJAL", "/mnt/user-data/uploads/Ruth tunnid")
IM = ROOT + "/inimoigused_materjalid"
VM = ROOT + "/vangla_materjalid"

PAR = r"^§ ?(?P<n>\d+(?:\^\d+)?)\.(?:\s|$)"
ART = r"^\s*Artikkel (?P<n>\d+)\.?(?:\s|$|(?=[A-ZÕÄÖÜ]))"
ART_CAT = r"^(?P<n>\d+)\. artikkel$"
ART_EN = r"^Rule (?P<n>\d+)\s*$"
ART_EPR = r"^(?P<n>\d+(?:\.\d+)?)\s*$"

ACTS = {
  # lühend: (fail, ühiku regex, täispealkiri, viite vorm)
  "PS":    (IM+"/02_Eesti_seadused/Pohiseadus_PS.txt", PAR, "Eesti Vabariigi põhiseadus", "§"),
  "HMS":   (IM+"/02_Eesti_seadused/Haldusmenetluse_seadus_HMS.txt", PAR, "Haldusmenetluse seadus", "§"),
  "HKMS":  (IM+"/02_Eesti_seadused/Halduskohtumenetluse_seadustik_HKMS.txt", PAR, "Halduskohtumenetluse seadustik", "§"),
  "KS":    (IM+"/02_Eesti_seadused/Kohtute_seadus_KS.txt", PAR, "Kohtute seadus", "§"),
  "PSJKS": (IM+"/02_Eesti_seadused/Pohiseaduslikkuse_jarelevalve_kohtumenetluse_seadus_PSJKS.txt", PAR, "Põhiseaduslikkuse järelevalve kohtumenetluse seadus", "§"),
  "OKS":   (IM+"/02_Eesti_seadused/Oiguskantsleri_seadus_OKS.txt", PAR, "Õiguskantsleri seadus", "§"),
  "MSVS":  (IM+"/02_Eesti_seadused/Margukirjale_ja_selgitustaotlusele_vastamise_seadus_MSVS.txt", PAR, "Märgukirjale ja selgitustaotlusele vastamise ning kollektiivse pöördumise esitamise seadus", "§"),
  "VõrdKS":(IM+"/02_Eesti_seadused/Vordse_kohtlemise_seadus_VordKS.txt", PAR, "Võrdse kohtlemise seadus", "§"),
  "SoVS":  (IM+"/02_Eesti_seadused/Soolise_vordoiguslikkuse_seadus_SoVS.txt", PAR, "Soolise võrdõiguslikkuse seadus", "§"),
  "IKS":   (IM+"/02_Eesti_seadused/Isikuandmete_kaitse_seadus_IKS.txt", PAR, "Isikuandmete kaitse seadus", "§"),
  "KiKoS": (IM+"/02_Eesti_seadused/Kirikute_ja_koguduste_seadus_KiKoS.txt", PAR, "Kirikute ja koguduste seadus", "§"),
  "VRKS":  (IM+"/02_Eesti_seadused/Valismaalasele_rahvusvahelise_kaitse_andmise_seadus_VRKS.txt", PAR, "Välismaalasele rahvusvahelise kaitse andmise seadus", "§"),
  "KorS":  (IM+"/02_Eesti_seadused/Korrakaitseseadus_KorS.txt", PAR, "Korrakaitseseadus", "§"),
  "RVastS":(IM+"/02_Eesti_seadused/Riigivastutuse_seadus_RVastS.txt", PAR, "Riigivastutuse seadus", "§"),
  "KarS":  (IM+"/02_Eesti_seadused/Karistusseadustik_KarS.txt", PAR, "Karistusseadustik", "§"),
  "VangS": (VM+"/02_seadused_ja_maarused/Vangistusseadus.txt", PAR, "Vangistusseadus", "§"),
  "VSE":   (VM+"/02_seadused_ja_maarused/Vangla_sisekorraeeskiri.txt", PAR, "Vangla sisekorraeeskiri", "§"),
  "EIÕK":  (IM+"/03_Euroopa_Noukogu/Inimoiguste_ja_pohivabaduste_kaitse_konventsioon_EIOK_2021.txt", ART, "Inimõiguste ja põhivabaduste kaitse konventsioon", "art"),
  "EIÕK P6": (IM+"/03_Euroopa_Noukogu/EIOK_lisaprotokoll_nr6_surmanuhtlus.txt", ART, "EIÕK protokoll nr 6 surmanuhtluse kaotamise kohta", "art"),
  "EIÕK P13":(IM+"/03_Euroopa_Noukogu/EIOK_protokoll_nr13_surmanuhtlus.txt", ART, "EIÕK protokoll nr 13 surmanuhtluse kaotamise kohta kõikidel asjaoludel", "art"),
  "EIÕK P16":(IM+"/03_Euroopa_Noukogu/EIOK_protokoll_nr16_nouandev_arvamus.txt", ART, "EIÕK protokoll nr 16 (nõuandvad arvamused)", "art"),
  "CPT":   (IM+"/03_Euroopa_Noukogu/Piinamise_tokestamise_Euroopa_konventsioon_CPT.txt", ART, "Piinamise ja ebainimliku või alandava kohtlemise või karistamise tõkestamise Euroopa konventsioon", "art"),
  "ÜRO PK":(IM+"/04_YRO/Uhinenud_Rahvaste_Organisatsiooni_pohikiri.txt", ART, "Ühinenud Rahvaste Organisatsiooni põhikiri", "art"),
  "ÜDIÕ":  (IM+"/04_YRO/Inimoiguste_ulddeklaratsioon.txt", ART, "Inimõiguste ülddeklaratsioon", "art"),
  "KPÕRP": (IM+"/04_YRO/Kodaniku_ja_poliitiliste_oiguste_pakt.txt", ART, "Kodaniku- ja poliitiliste õiguste rahvusvaheline pakt", "art"),
  "KPÕRP FP":(IM+"/04_YRO/Kodaniku_ja_poliitiliste_oiguste_pakti_fakultatiivprotokoll.txt", ART, "Kodaniku- ja poliitiliste õiguste rahvusvahelise pakti fakultatiivprotokoll", "art"),
  "CAT":   (IM+"/04_YRO/Piinamisvastane_konventsioon_CAT.txt", ART_CAT, "Piinamise ning muu julma, ebainimliku või inimväärikust alandava kohtlemise ja karistamise vastane konventsioon", "art"),
  "OPCAT": (IM+"/04_YRO/Piinamisvastase_konventsiooni_fakultatiivprotokoll_OPCAT.txt", ART, "Piinamisvastase konventsiooni fakultatiivprotokoll", "art"),
  "PagK":  (IM+"/04_YRO/Pagulasseisundi_konventsioon_1951.txt", ART, "Pagulasseisundi konventsioon (1951)", "art"),
  "harta": (IM+"/05_Euroopa_Liit/Pohioiguste_harta_2016.txt", ART, "Euroopa Liidu põhiõiguste harta", "art"),
  "ELL":   (IM+"/05_Euroopa_Liit/Euroopa_Liidu_leping_ELL_2016.txt", ART, "Euroopa Liidu leping", "art"),
  "ELTL":  (IM+"/05_Euroopa_Liit/Euroopa_Liidu_toimimise_leping_ELTL_2016.txt", ART, "Euroopa Liidu toimimise leping", "art"),
  "Rooma": (IM+"/06_kriminaal_ja_humanitaaroigus/Rahvusvahelise_Kriminaalkohtu_Rooma_statuut.txt", ART, "Rahvusvahelise Kriminaalkohtu Rooma statuut", "art"),
  "Genf III":(IM+"/06_kriminaal_ja_humanitaaroigus/Genfi_III_konventsioon_sojavangid.txt", ART, "Genfi III konventsioon sõjavangide kohtlemise kohta", "art"),
  "Genf IV":(IM+"/06_kriminaal_ja_humanitaaroigus/Genfi_IV_konventsioon_tsiviilisikud.txt", ART, "Genfi IV konventsioon tsiviilisikute kaitse kohta sõja ajal", "art"),
  "Mandela":(IM+"/07_vanglastandardid_ingliskeelsed/Mandela_reeglid_A_RES_70_175_EN.txt", ART_EN, "ÜRO kinnipeetavate kohtlemise miinimumreeglid (Nelson Mandela reeglid), A/RES/70/175 – ingliskeelne", "rule"),
}

HEADING = re.compile(
    r"^(?:[IVXLC]+\.? ?(?:peatükk|PEATÜKK|JAOTIS|OSA)\b.*"
    r"|\d+\.? (?:peatükk|jagu|osa|jaotis)\b.*"
    r"|(?:[IVXLC]+|\d+)\.? ?JAGU\b.*"
    r"|[IVXLC]+ JAOTIS"
    r"|(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|XIV|XV)\.?$"
    r"|[A-ZÕÄÖÜŠŽ][A-ZÕÄÖÜŠŽ ,.\-–]{5,}$)"
)

def norm(line):
    line = unicodedata.normalize("NFC", line).replace("\u00a0", " ").replace("\t", " ")
    return re.sub(r"\s+", " ", line).strip()

_cache = {}
def load(act):
    if act in _cache: return _cache[act]
    path, unit_re, title, form = ACTS[act]
    raw = open(path, encoding="utf-8").read()
    head, body = raw.split("========================================", 1)
    meta = {}
    for l in head.splitlines():
        if ":" in l:
            k, v = l.split(":", 1); meta[k.strip()] = v.strip()
    for l in body.splitlines()[:25]:
        if l.startswith("Avaldamismärge:"): meta["Avaldamismärge"] = l.split(":",1)[1].strip()
    meta["_pdf_layout"] = False
    pdf = path[:-4] + ".pdf"
    if act == "Mandela" and os.path.exists(pdf) and shutil.which("pdftotext"):
        # PDF-i lihttekstis on mõne loetelu sõnade järjekord nihkes; paigutust
        # säilitav väljavõte originaal-PDF-ist annab õige järjekorra.
        body = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
        meta["_pdf_layout"] = True
    lines = [norm(l) for l in body.splitlines()]
    lines = [l for l in lines if l]
    # liida üksik loetelu-tähis ("a)", "1)") järgmise reaga
    merged = []
    for l in lines:
        if merged and re.fullmatch(r"[a-z]\)|\(?[a-z0-9]{1,3}\)", merged[-1]):
            merged[-1] = merged[-1] + " " + l
        else:
            merged.append(l)
    rx = re.compile(unit_re)
    units, order, cur = {}, [], None
    skip_title = False
    for l in merged:
        if skip_title:
            skip_title = False
            if not rx.match(l):
                continue
        if re.match(r"^(?:\d+(?:\^\d+)?|[IVXLC]+)\.? ?(?:jagu|peatükk|osa|jaotis|alljagu|JAGU|PEATÜKK|OSA|JAOTIS)$", l):
            skip_title = True
            continue
        m = rx.match(l)
        if m:
            n = m.group("n")
            if n in units:   # kordus (nt sisukord/protokoll) – jäta esimene
                cur = None; continue
            cur = n; units[n] = [l]; order.append(n); continue
        if cur is None: continue
        if HEADING.match(l):
            continue
        units[cur].append(l)
    _cache[act] = (units, order, meta, title, form)
    return _cache[act]

def unit_text(act, n):
    units, order, meta, title, form = load(act)
    if n not in units:
        raise KeyError(f"{act} {form} {n} – ei leitud failist")
    ls = units[n]
    # artiklite puhul: pealkiri eraldi
    first = ls[0]
    return ls

def meta(act):
    units, order, meta, title, form = load(act)
    path = ACTS[act][0]
    return {
        "lyhend": act, "pealkiri": title, "url": meta.get("URL", ""),
        "kehtivus": meta.get("Sõnastuse kehtivus", ""),
        "avaldamismarge": meta.get("Avaldamismärge", ""),
        "allikas": meta.get("ALLIKAS", ""),
        "mitteametlik_tolge": act in ("KPÕRP","KPÕRP FP","CAT","CPT"),
        "fail": os.path.relpath(path, ROOT).replace("\\","/"),
        "vorm": ACTS[act][3],
    }

if __name__ == "__main__":
    for a in sys.argv[1:]:
        act, n = a.rsplit(" ", 1)
        print(f"--- {act} {n}"); print("\n".join(unit_text(act, n)))
