# Turvalisus vanglas – arendusjuhend

See fail kirjeldab, kuidas leht on ehitatud ja kuidas seda edasi arendada. Loe see läbi enne
iga muudatust. Lühike reeglite kokkuvõte on failis [`CLAUDE.md`](CLAUDE.md).

- **Repo:** `ChrisRichV/Turvalisus_vanglas` → GitHub Pages (`main`, juurkaust)
- **Andmebaas:** Supabase, projekt „ChrisRichV's Project” (`oxjzdlqycqipfelomrnv`), tabel `oppeleht_tagasiside`
- **Materjal:** kohalik kaust `Ruth tunnid` (ei ole repos), sisukord `Ruth tunnid/00_SISUKORD.md`
- **Seis:** tund 1 (10.11.2026), seadused seisuga 10.11.2026

---

## 1. Põhimõtted (mittekaubeldavad)

1. **Seaduse tekst ei muutu.** Hüpikaknas näidatav sätte tekst võetakse masinaga ametlikust
   tekstifailist (`tools/seadused.py` → `data/seadused.json`). Seda ei kirjutata ega parandata käsitsi.
2. **Tsitaat ja selgitus on eraldi.** Teemafailis on selgitus omas sõnastuses, sätte tekst on
   viite taga. Sõna-sõnaline tsitaat läheb välja `tsitaat` ja ehitusskript kontrollib, et see leidub allikas.
3. **Iga väide viitab sättele** (`[[PS § 18]]`). Viide, mida algtekstis ei ole, peatab ehituse.
4. **Väljastpoolt tunnimaterjali** (õigusteaduse mõisted, kohtupraktika, välisallikad) → väli `valjast`, allikaga.
5. **Konspekt vs ametlik tekst** – lahknevus väljale `erinevused`, ise ei vali.
6. **AK-materjal ei jõua reposse** – ei tsitaadina ega ümbersõnastatuna. Kontroll on automaatne (vt p 7).
7. **Varasemate kursuste kordamisküsimusi (~280, `vangla_materjalid/01_kordamiskusimused`) lehele ei lisata.**
   Neid võib kasutada ainult taustainfona ja alati seadusega kontrollides. Taktikalised detailid jäetakse välja.
8. **Supabase:** repos ainult publishable/anon võti, RLS alati sees, `service_role` mitte kunagi.

---

## 2. Arhitektuur

Staatiline leht, ilma raamistiku ja ehitussammuta brauseri jaoks.

**Hierarhia: aine → tund → teema.** Ained on eraldi (eraldi leht, kordamine, sisukorra haru), kuid
seaduste tekstid on ühised (`data/seadused.json`) ja **seaduste register** näitab, millistes ainetes
ja teemades iga säte esineb. Ained praegu: `inimoigused` (KS240), `psuhholoogia` (vangla psühholoogia),
`oigus` (õiguse õpetus). Uus aine = uus kirje `data/tunnid.json` → `ained` + kaust `Ruth tunnid`-is. Kõik sisu on JSON-is, HTML-failid
ainult renderdavad. Ainus „ehitus” on Pythoni skript, mis genereerib seaduste andmefaili ja
kontrollib sisu.

```
 Ruth tunnid/ (kohalik)                 repo
 ├─ inimoigused_materjalid/*.txt ──┐
 ├─ vangla_materjalid/*.txt ───────┼─► tools/seadused.py ─► tools/ehita.py ─► data/seadused.json
 │                                 │        (parser)          (kontroll)        (genereeritud)
 └─ Ruth_opetaja_tunni_failid/ ────┘                              ▲
    Ruth_kordamiskusimused/   ─── Claude kirjutab ──► teemad/*.json, data/*.json ┘
                                                              │
                                    index.html / teema.html / kordamine.html  ◄── assets/*.js
                                                              │
                                     „Teata veast” ──► Supabase oppeleht_tagasiside (INSERT)
```

### Failid

| Fail | Roll | Muuda käsitsi? |
|---|---|---|
| `index.html` | Töölaud: ainekaardid, „jätka” (viimati vaadatud), otsing kõigist ainetest, kaasuse skeem, sõnastik | harva |
| `aine.html?id=inimoigused` | Aine leht: tunnid → plokid → teemad, otsing aines, kiirotsing (kui `aine.kiirotsing`) | harva |
| `seadused.html` | Seaduste register: akt → säte → teemad (ainefiltriga); arvutatakse brauseris teemafailidest | harva |
| `teema.html?id=t01-08` | Teema: 5 osa + skeem + tunni küsimus + harjutused + allikamärkused + tagasiside | harva |
| `kordamine.html?aine=…&tund=…&teema=…` | Segatud harjutused (5/8/10) aine/tunni/teema kaupa ja tunni küsimused vastustega | harva |
| `assets/app.js` | Andmed, märgistus (`md`), **ühine päis + sisukorra sahtel** (`A.kaivita({leht, aine, tund, teema})`), hüpikaknad, näiteaken, harjutused, tagasiside | harva |
| `assets/skeemid.js` | Skeemitüübid: `voog`, `puu`, `tasandid`, `vordlus`, `kaalud` | uue tüübi korral |
| `assets/stiil.css` | Kujundus, hele/tume teema | harva |
| `assets/seadistus.js` | Supabase URL + **publishable** võti | ei |
| `data/tunnid.json` | Tundide nimekiri, kordamisküsimused, plokid, teemafailid, allikafailid | **iga uus tund** |
| `teemad/tNN-MM-nimi.json` | Üks teema | **iga uus teema** |
| `data/terminid.json` | Sõnastik | uue termini korral |
| `data/kiirotsing.json` | Tabel „põhiõigus → vangla õigusakt” | vajadusel |
| `data/seadused.json` | **Genereeritud** – viidatud sätete tekstid + aktide metaandmed | **ei kunagi** |
| `tools/seadused.py` | Aktide loetelu `ACTS` ja parser | uue akti korral |
| `tools/ehita.py` | Ehitus ja kontroll | ei |
| `tools/ak_sormejaljed.txt` | AK-tekstide räsitud 8-sõnalised lõigud (tekst ise pole taastatav) | ei |
| `supabase/001_tagasiside.sql` | Tabel + RLS | uue tabeli korral uus fail `002_…` |

---

## 3. Andmemudel

### `data/tunnid.json`
```json
{ "ained": [ { "id": "inimoigused", "nimi": "…", "lyhend": "Inimõigused", "kood": "KS240", "kirjeldus": "…", "kiirotsing": true } ],
  "tunnid": [ {
    "id": "t01", "aine": "inimoigused", "nr": 1, "pealkiri": "…", "kuupaev": "2026-11-10", "olek": "valmis | tulemas",
    "kirjeldus": "…", "materjal": ["avalik materjali kirjeldus"],
    "kysimused": ["õppejõu küsimus 1", "…"],          // järjekord = number
    "plokid": [ { "pealkiri": "…", "teemad": ["t01-01", "…"] } ],
    "teemad": [ { "id": "t01-01", "fail": "teemad/t01-01-uro.json" } ],
    "allikafailid": { "opetaja": [], "kysimused": [], "tekstiversioonid": [], "markus": "" }
} ] }
```

**Id-de kuju:** inimõigused `t01`, `t01-01`; psühholoogia `ps-t01`, `ps-t01-01`; õigus `o-t01`, `o-t01-01`.
Teemafail: `teemad/<teema-id>-<nimi>.json`. Id-d peavad olema unikaalsed (ehitus kontrollib).

### `teemad/*.json`
```json
{
  "id": "t01-08", "tund": "t01", "jrk": 8, "pealkiri": "…", "kysimused": [10],
  "lyhidalt": "1–2 lauset lihtsas keeles",
  "osad": {
    "pohimote":  { "pealkiri?": "…", "tekst": "…", "tsitaat?": { "viide": "EIÕK preambul", "tekst": "sõna-sõnalt" }, "punktid?": [] },
    "alus":      { "read": [ { "tase": "Eesti | Vangla | Euroopa Nõukogu | Euroopa Liit | ÜRO | …", "viited": ["PS § 18"], "tekst": "…" } ] },
    "piiramine": { "pealkiri?": "…", "tekst?": "…", "punktid": [] },
    "vangla":    { "tekst": "…", "naide": { "olukord": "…", "analyys": "kaitseala → riive → … → järeldus" } },
    "tyypviga":  { "punktid": [] }
  },
  "skeem": { "tyyp": "…" } ,                      // või massiiv mitmest skeemist
  "vastus": [ { "nr": 10, "punktid": [] } ],      // iga tunni küsimuse kohta, mida teema katab
  "harjutused": [
    { "tyyp": "fakt", "kysimus": "…", "valikud": ["…"], "oige": 1, "selgitus": "[[viide]]" },
    { "tyyp": "kaasus", "kysimus": "…", "vastus": ["**Kaitseala:** …", "**Riive:** …", "…", "**Järeldus:** …"] }
  ],
  "erinevused": [ { "teema": "…", "konspekt": "…", "ametlik": "…", "viide": "…", "markus?": "…" } ],
  "valjast":    [ { "tekst": "…", "allikas": "… – ei pärine tunnimaterjalist" } ],
  "naited?": [ {                                   // päris juhtum, nupp „Päris näide”
      "pealkiri": "Tali vs Eesti", "kohus": "Euroopa Inimõiguste Kohus", "aeg": "13. veebruar 2014",
      "lugu": "mis juhtus", "tulemus": "mida kohus otsustas", "oppetund": "mida meelde jätta + [[viide]]",
      "seos": ["EIÕK art 3"], "allikas": { "nimi": "…", "url": "https://…" } } ]
}
```
**Päris näited** on alati väljaspool tunnimaterjali: iga fakt (kuupäev, otsus, hüvitis) peab olema
kontrollitud allikast, mille link on väljal `allikas`. Kui detaili ei õnnestu kinnitada, jäta see välja.
Ilma näiteta teemal nuppu ei kuvata.

Tunni kordamisküsimused (`vastus[]` + `tunnid.json` küsimused) ilmuvad kordamise lehel ka segatud
harjutuses tüübina `tunnikys` („Ainult tunni küsimused” filter).
Viis osa vastavad õppimise skeemile: 1) mis õigus/põhimõte, 2) õiguslik alus, 3) piiramise alused
ja proportsionaalsus, 4) näide vanglast, 5) tüüpviga eksamil.

### Skeemid (`skeem.tyyp`)
| Tüüp | Kuju | Väljad |
|---|---|---|
| `voog` | nummerdatud sammud (ainult kui sisu on päriselt järjestus) | `sammud[{pealkiri, tekst, viide?}]` |
| `puu` | juur + harud | `juur{…}`, `harud[{pealkiri, toon: a/b/c, lapsed[…]}]` |
| `tasandid` | read sildiga vasakul | `tasandid[{pealkiri, toon, kastid[…]}]` |
| `vordlus` | tabel; mobiilis kaardid | `veerud[]`, `read[{silt, lahtrid[]}]` |
| `kaalud` | kaks vaagnat + tingimused | `vasak{…, silt}`, `parem{…, silt}`, `all[]` |

### Märgistus tekstis
| Kirjutad | Tulemus |
|---|---|
| `[[PS § 18]]`, `[[VangS § 4^1 lg 2]]`, `[[EIÕK art 8 lg 2]]`, `[[Mandela rule 58]]` | klikitav viide; aken näitab sätet, lõige esile tõstetud |
| `[[PS § 18\|kuvatav tekst]]` | sama, teise kuvatekstiga |
| `{{termin-id}}`, `{{termin-id\|kuvatav}}` | klikitav termin (`data/terminid.json`) |
| `**paks**`, `` `kood` `` | vorming |

Viite kuju: `<AKT> <§|art|rule> <nr>[ lg <nr>][ p <nr>]`. Akti lühend peab olema `tools/seadused.py` →
`ACTS` võtmete hulgas. Punkti (`p`) aken esile ei tõsta, lõiget tõstab.

---

## 4. Ehitus ja kontroll

```bash
python3 tools/ehita.py --materjal "/tee/Ruth tunnid"
```
Väljund: `data/seadused.json`. Skript lõpetab **veaga**, kui:
- teemafail puudub või `id` ei klapi; harjutuse `oige` indeks on vale;
- viidet ei saa parsida, akt on tundmatu, säte või lõige puudub algtekstis;
- `tsitaat` ei leidu sõna-sõnalt allikas;
- `{{termin}}` puudub sõnastikust; kiirotsingu `teema_id` on tundmatu;
- repos on AK-märge, **AK-sõrmejäljega** kattuv tekst või kattuvus materjalis praegu oleva AK-märgisega lõiguga.

Viimane eduka ehituse seis: 15 teemat, 818 viidet, 168 sätet, 33 akti.

### Kohalik eelvaade
```bash
python3 -m http.server 8000     # ava http://localhost:8000 (failina avades fetch ei tööta)
```
Kontrolli: 390 px laiusel horisontaalset kerimist ei tohi olla; konsoolis vigu ei tohi olla; ava mõni
viide ja termin; tume režiim.

---

## 5. Uue tunni lisamine (töövoog)

1. **Materjal kausta** (kasutaja): õppejõu failid → `Ruth tunnid/Ruth_opetaja_tunni_failid/<Aine>/`,
   kordamisküsimused → `Ruth tunnid/Ruth_kordamiskusimused/<Aine>/` (`Inim_ja_pohioigused`,
   `Vangla_psuhholoogia`, `Oigus`). Failinimi `AAAA-KK-PP_tunni_teema.<laiend>`.
2. **Tekstiversioon** iga originaali kõrvale (`.txt`/`.md`, sama nimi, päis `ALLIKAS / TÜÜP / TEISENDUS`).
3. **Uuenda `Ruth tunnid/00_SISUKORD.md`** (uued failid, märgised, AK).
4. **Teemade nimekiri** (≤ ~15) → näita kasutajale ja oota kinnitust.
5. **`data/tunnid.json`**: õiges aines muuda tund `olek: "valmis"`, lisa küsimused, plokid, teemad,
   `allikafailid`; lisa sama aine alla uus `tulemas`-kirje järgmise tunni jaoks.
   Psühholoogias ei ole alati seadusesätteid – siis võib `alus.read[].viited` olla tühi ja väited
   viitavad õppejõu materjalile (`valjast` ei ole vaja, kui allikas on tunnimaterjal).
6. **`teemad/tNN-MM-nimi.json`** iga teema kohta. Enne kirjutamist **loe sätted algtekstist**
   (`python3 tools/seadused.py "VangS 29" "PS 43"`). Vangla näide → kaasuse skeem.
7. **Uus akt?** Lisa `tools/seadused.py` → `ACTS` (lühend, fail, ühiku regex, pealkiri, vorm).
   Kontrolli parserit: `python3 -c "import seadused as s; u,o,*_=s.load('AKT'); print(len(o), o[:5])"`.
8. **`python3 tools/ehita.py`** kuni vigu pole.
9. **Võrdle konspekti tsitaate ametliku tekstiga** (sõnatasemel diff) → `erinevused`.
10. Eelvaade brauseris (telefoni ja arvuti laius), siis haru + PR.

### Uue akti lisamine – parseri mustrid
| Muster | Kasutus |
|---|---|
| `PAR` `^§ N.` | Riigi Teataja seadused ja määrused |
| `ART` `^Artikkel N` | lepingud (EIÕK, harta, ÜRO, Rooma jne) |
| `ART_CAT` `^N. artikkel$` | piinamisvastane konventsioon |
| `ART_EN` `^Rule N$` | Mandela reeglid (võetakse originaal-PDF-ist `pdftotext -layout`, kui olemas) |

Parser eemaldab jao/peatüki pealkirjad, liidab üksikud loetelutähised („a)”) järgmise reaga ja jätab
esimese esinemise, kui number kordub (sisukord, protokollid).

---

## 6. Teadaolevad eripärad ja õppetunnid

- **Harta numbrid:** konspekt kasutab jõustumata Euroopa põhiseaduse lepingu numbreid (II-61 …).
  Kehtiv: art 1, 3, 4, 6, 7, 21, 47. Alati `harta art N`.
- **EIÕK art 35:** failis kaks lg 1 sõnastust (6 kuud kuni 1.02.2022 / 4 kuud alates). Mõlemad kuvatakse.
- **CAT, CPT, KPÕRP (+FP):** mitteametlik tõlge – aken näitab silti automaatselt.
- **KPÕRP art 16 ja 46:** RT failis valesti märgitud („Artikkel l6”) – parser ei leia; ära viita.
- **Rooma statuut art 12 lg 2:** RT tõlkes „art 13 lõigetes a ja b”, originaalis (a) ja (c).
- **Mandela reeglid:** lihttekstis oli rule 58 sõnajärg nihkes; seetõttu kasutatakse PDF-i paigutusega väljavõtet.
- **VRKS** ei defineeri pagulast ise, vaid viitab EL-i määrustele (§ 2).
- **RT muudatusmärked** (`[RT I, …]`) jäävad teksti, kuvatakse halli väikese kirjana.
- **AK:** standardid kustutati kasutaja kaustast 10.11.2026; kontroll toimub `tools/ak_sormejaljed.txt` kaudu.
  Tallinna Vangla kodukorra **lisa 11** on AK – ülejäänud kodukord mitte.

---

## 7. AK-kontroll

`tools/ak_sormejaljed.txt` sisaldab AK-dokumentide iga 8-sõnalise lõigu SHA-256 räsi esimest 16 märki
(avalikes seadustes esinevad lõigud välja arvatud). Ehitus räsib repo teksti samamoodi ja
peatub kattuvuse korral. Lisaks skannitakse materjalikausta: iga fail, kus on märge
„ASUTUSESISESEKS KASUTAMISEKS” (v.a Riigi Teataja seadused), võrreldakse repoga.
**Uue AK-faili ilmumisel** lisa selle sõrmejäljed (vt skripti `tools/ehita.py` funktsioon `grams`) ja
teavita kasutajat.

---

## 8. Supabase

`supabase/001_tagasiside.sql` – `public.oppeleht_tagasiside`:
`id, loodud, teema, osa, tekst (5–2000), nimi (≤80), olek ('uus'|'parandatud'|'tagasi_lykatud')`.
RLS: `anon`/`authenticated` ainult `INSERT (teema, osa, tekst, nimi)`; SELECT/UPDATE/DELETE puudub.
Kontrollitud: anon INSERT õnnestub, SELECT → `permission denied`.
Ettepanekuid loeb omanik Supabase'i töölaualt. Samas projektis on teise lehe tabelid
(`parandused`, `kasutajad`, `haaled`, `kysimuste_stat`) – neid ei puuduta.

Uus tabel: uus migratsioonifail `supabase/00N_….sql`, RLS sees, käivita `get_advisors(security)`.

---

## 9. Kujundus

Vaikimisi **tume teema neoonaktsentidega**; hele teema lülitiga (`data-theme="light"`, valik
salvestatakse brauserisse). Sära (`text-shadow`/`box-shadow`) ainult tähtsal – mitte kõigel.

| Token | Tume (vaikimisi) | Hele | Tähendus |
|---|---|---|---|
| `--paber` | `#0d1117` | `#ecEEea` | taust |
| `--tint` | `#e6eaee` | `#1c2733` | tekst |
| `--marker` | `#ffe14a` neoonkollane | `#f2c230` | **ainult** seaduseviited, võtmelause, peamine nupp |
| `--vask` | `#2ef5d6` neoontsüaan | `#2f6f6a` | **ainult** terminid, õige vastus, tunni küsimuse vastus |
| `--rooste` | `#ff4fa0` neoonroosa | `#a8432c` | **ainult** tüüpvead, vale vastus, erinevused |
| `--lilla` | `#b388ff` neoonlilla | `#6b3fd1` | **ainult** päris näited (nupp ja aken) |

Kirjad: Archivo (pealkirjad, liides; laius 110–125 %) ja Source Serif 4 (sisu, seadusetekst).
Vasakule joondatud, tekstiveerg ≤ 42rem. Nummerdus (1–5, voo sammud) ainult päris järjestuse puhul.
Neooni reeglid on `stiil.css` lõpus plokis „NEOON”; uus tähtis element saab sära ainult siis, kui see kannab ühte neist neljast tähendusest.

---

## 10. Avaldamine

1. Muudatus haru peale → PR → liida `main`.
2. Repo peab olema **avalik** (tasuta kontol Pages privaatsest repost ei tööta).
3. Settings → Pages → *Deploy from a branch* → `main` / `(root)`. `.nojekyll` on olemas.
4. Pärast 01.01.2027: uued redaktsioonid (VangS, ATS, KarS, KrMS, HKMS) → uuenda tekstifailid,
   käivita `ehita.py`, kontrolli muutunud sätete viiteid.
