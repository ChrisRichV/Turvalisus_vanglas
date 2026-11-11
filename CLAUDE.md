# CLAUDE.md – Turvalisus vanglas õppeleht

Staatiline õppeleht (GitHub Pages): **aine → tund → teema** (ained: `inimoigused`, `psuhholoogia`, `oigus`). Sisu on JSON-is, seaduste tekst genereeritakse
ametlikest tekstifailidest. **Täielik arendusjuhend: [`README-projekt.md`](README-projekt.md) – loe enne muudatusi.**

## Kõvad reeglid
- Ära kirjuta ega muuda seaduse teksti käsitsi. `data/seadused.json` on genereeritud (`tools/ehita.py`).
- Iga väide teemafailis viitab sättele kujul `[[PS § 18]]` / `[[EIÕK art 8 lg 2]]`. Viide võetakse failist, mitte mälust.
- Sõna-sõnaline tsitaat ainult väljal `tsitaat` (kontrollitakse); muu tekst on selgitus.
- Väljastpoolt tunnimaterjali → `valjast` koos allikaga. Konspekt vs seadus → `erinevused`, ära vali ise.
- AK-materjal (märge „ASUTUSESISESEKS KASUTAMISEKS”) ei tohi jõuda reposse, ka ümbersõnastatuna.
- Varasemate kursuste kordamisküsimusi (`vangla_materjalid/01_kordamiskusimused`) lehele ei lisata; taktikalised detailid välja.
- Supabase: ainult publishable võti (`assets/seadistus.js`), RLS alati sees, `service_role` mitte kunagi.
- Keel: eesti. Vaikimisi tume neoonteema; igal neoonvärvil üks tähendus (kollane = seaduseviide, tsüaan = termin/õige, roosa = viga, lilla = päris näide).
- Päris näited (`naited`) on väljaspool tunnimaterjali: iga fakt kontrollitud allikast, link väljal `allikas`.

## Käsud
```bash
python3 tools/ehita.py --materjal "/mnt/user-data/uploads/Ruth tunnid"   # ehitus + kontroll, peab lõppema "OK"
python3 tools/seadused.py "VangS 29" "PS 43"                               # loe sätet algtekstist
python3 -m http.server 8000                                               # eelvaade
```
Materjal on kasutaja arvutis `Desktop\Ruth tunnid` (sisukord `00_SISUKORD.md`); too failid tööalale enne ehitust.

## Uus tund (lühidalt)
õige aine kaust (`Ruth_opetaja_tunni_failid/<Aine>/`) → teemade nimekiri → kasutaja kinnitus → `data/tunnid.json` (õige `aine`, id-d `ps-t01…`, `o-t01…`) → `teemad/tNN-MM-*.json` (+ `lyhend`, `ikoon`) → mõistekaart `tools/moistekaart.py` (mõisted + seosed varasemate tundidega) → (uus akt: `tools/seadused.py` `ACTS`)
→ `ehita.py` OK → (CSS/JS muutus: tõsta `?v=` kõigis HTML-ides) → brauseris 390 px ja 1280 px → haru + PR. Uuenda ka `Ruth tunnid/00_SISUKORD.md`.
