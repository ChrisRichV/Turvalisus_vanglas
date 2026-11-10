# Turvalisus vanglas – õppeleht (tehniline kirjeldus)

Avalik õppeleht Sisekaitseakadeemia kursuse teemade kordamiseks tundide kaupa.
Hostitud GitHub Pagesis, ainult staatilised failid. Sisu on JSON-failides, et lehte
oleks lihtne täiendada ilma HTML-i muutmata.

## Põhimõtted

1. **Seaduse tekst ei muutu.** Kõik hüpikaknas näidatavad sätted on masinaga välja
   võetud Riigi Teataja / EUR-Lexi / ÜRO ametlikest tekstidest (`data/seadused.json`).
   Neid ei kirjutata käsitsi. Ümbersõnastused on teemafailides selgelt eraldatud
   selgitustena.
2. **Iga väide viitab allikale.** Viide kujul `[[PS § 18]]`, `[[EIÕK art 8 lg 2]]`
   muutub lehel klikitavaks ja näitab sätte täpset teksti, akti versiooni ja linki.
3. **Väljastpoolt tunnimaterjali** lisatud info on märgitud (`valjast` / allikas).
4. **Konspekti ja ametliku teksti erinevused** on iga teema juures välja toodud.
5. **Reposse ei lähe** asutusesiseseks kasutamiseks (AK) märgitud materjal ega sellest
   tuletatud tekst. Varasemate kursuste kordamisküsimusi (~280) lehele ei lisata.
6. **Supabase**: ainult publishable/anon võti, RLS alati sees. `service_role` võtit ei
   ole ega tohi reposse panna.

## Struktuur

```
index.html            – avaleht: tunnid → teemad, otsing, kaasuse lahendamise skeem
teema.html?id=…       – üks teema: 5 osa + skeem + tunni küsimuse vastus + harjutused
kordamine.html        – kordamine: tunni küsimused + segatud harjutused (5–10 tk)
assets/
  stiil.css           – kujundus (hele/tume teema)
  app.js              – andmete laadimine, märgistuse renderdamine, hüpikaknad
  skeemid.js          – skeemitüübid (voog, tasandid, puu, võrdlus, kaalud)
  seadistus.js        – Supabase URL + publishable võti (avalik)
data/
  tunnid.json         – tundide nimekiri, kuupäevad, tunni kordamisküsimused, teemad
  terminid.json       – sõnastik (termin → selgitus + viited)
  seadused.json       – GENEREERITUD: viidatud sätete tekstid + aktide metaandmed
teemad/
  t01-01-uro.json …   – üks fail teema kohta
tools/
  ehita.py            – loeb teemad/terminid, võtab viidatud sätted algtekstidest,
                        kirjutab data/seadused.json, kontrollib kõik viited
  seadused.py         – algtekstide parser (aktide loetelu, failiteed)
supabase/
  001_tagasiside.sql  – tabel parandusettepanekutele + RLS
```

## Märgistus teemafailides

| Kirjutad | Lehel |
|---|---|
| `[[PS § 18]]`, `[[VangS § 4^1 lg 2]]`, `[[EIÕK art 8 lg 2]]`, `[[Mandela rule 58]]` | klikitav viide, hüpikaknas sätte tekst (lõige esile tõstetud) |
| `[[PS § 18\|esimene lause]]` | sama, aga lehel kuvatakse tekst pärast `\|` |
| `{{proportsionaalsus}}` või `{{proportsionaalsus\|proportsionaalne}}` | klikitav termin sõnastikust |
| `**paks**` | paks kiri |

Ülaindeks kirjutatakse `^`-ga nagu Riigi Teatajas: `§ 41^1` = § 41¹.

## Teemafaili kuju (`teemad/*.json`)

```json
{
  "id": "t01-08", "tund": "t01", "jrk": 8,
  "pealkiri": "Inimväärikus", "kysimused": [10],
  "lyhidalt": "Üks lause, mis jääb meelde.",
  "osad": {
    "pohimote":  { "tekst": "…" },
    "alus":      { "read": [ { "tase": "Eesti", "viited": ["PS § 18"], "tekst": "…" } ] },
    "piiramine": { "tekst": "…", "punktid": ["…"] },
    "vangla":    { "tekst": "…", "naide": { "olukord": "…", "analyys": "…" } },
    "tyypviga":  { "punktid": ["…"] }
  },
  "skeem": { "tyyp": "voog|tasandid|puu|vordlus|kaalud", "…": "…" },
  "vastus": [ { "nr": 10, "punktid": ["…"] } ],
  "harjutused": [
    { "tyyp": "fakt", "kysimus": "…", "valikud": ["…"], "oige": 0, "selgitus": "…" },
    { "tyyp": "kaasus", "kysimus": "…", "vastus": ["kaitseala …", "riive …"] }
  ],
  "erinevused": [ { "teema": "…", "konspekt": "…", "ametlik": "…", "viide": "…" } ],
  "valjast":    [ { "tekst": "…", "allikas": "…" } ]
}
```

## Uue tunni lisamine

1. Pane tunni materjal kohalikku kausta (`Ruth tunnid/...`) koos tekstiversiooniga.
2. Lisa tund faili `data/tunnid.json` (kuupäev, kordamisküsimused, teemade id-d).
3. Loo iga teema jaoks `teemad/tNN-MM-nimi.json`.
4. Kui vaja uut akti, lisa see `tools/seadused.py` loetellu `ACTS`.
5. Käivita `python3 tools/ehita.py --materjal "<Ruth tunnid kausta tee>"` – see
   ehitab `data/seadused.json` ja peatub vea korral (nt viide sättele, mida pole).
6. Kontrolli lehte kohapeal: `python3 -m http.server` ja ava `http://localhost:8000`.

## Supabase

Tabel `public.oppeleht_tagasiside` (vt `supabase/001_tagasiside.sql`):
lehe kasutaja saab teema juures saata parandusettepaneku („Teata veast“).
RLS: anonüümne kasutaja saab ainult lisada (INSERT), mitte lugeda ega muuta.
Ettepanekuid loeb omanik Supabase'i töölaualt. Kui Supabase pole saadaval,
töötab leht edasi, ainult tagasiside nupp annab teada, et saatmine ebaõnnestus.

## Avaldamine

Repo peab olema **avalik**, et GitHub Pages töötaks tasuta kontoga.
Settings → Pages → Source: *Deploy from a branch* → `main` / `(root)`.
