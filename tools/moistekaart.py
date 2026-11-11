"""Mõistekaardi sisu (data/moistekaart.json). Muuda siin ja käivita: python3 tools/moistekaart.py, siis tools/ehita.py.

Reeglid: selgitus lihtsas keeles, iga väide viitab sättele [[...]] (kontrollib ehita.py); teemad = teema id-d;
seosed a → b sildiga (lühike tegusõna). Mõiste, mille silt = teema lühinimi, liidetakse kaardil teemaga üheks sõlmeks.
"""
import json
K = []
def m(id, silt, teemad, viited=(), selgitus=None, termin=None):
    K.append({k: v for k, v in dict(id=id, silt=silt, teemad=list(teemad), viited=list(viited), selgitus=selgitus, termin=termin).items() if v not in (None, [])})

# ---------- Õiguse alused: põhiseadus (tund 10)
m("pohiseadus", "Põhiseadus", ["o-t10-01", "o-t10-04"], ["PS § 3 lg 1", "PS § 152"],
  "Riigi kõige tähtsam seadus. Riigivõimu teostatakse ainult põhiseaduse ja sellega kooskõlas olevate seaduste alusel ([[PS § 3 lg 1]]). Põhiseadusega vastuolus seadust kohus ei kohalda ([[PS § 152]]).")
m("pohiseaduse-muutmine", "Põhiseaduse muutmine", ["o-t10-01"], ["PS § 161", "PS § 162", "PS § 163"],
  "Põhiseadust saab muuta, aga palju raskemini kui tavalist seadust: algatajad, menetlus ja häälteenamus on eraldi kirjas ([[PS § 161]], [[PS § 162]], [[PS § 163]]).")
m("demokraatia", "Demokraatia", ["o-t10-02", "o-t10-03"], ["PS § 1", "PS § 56"],
  "Kõrgeim võim on rahval ([[PS § 1]]). Rahvas teostab seda Riigikogu valimise ja rahvahääletuse kaudu ([[PS § 56]]).")
m("oigusriik", "Õigusriik", ["o-t10-02"], ["PS § 10"],
  "Riik, kus võim on seotud õigusega: kõik käib seaduse alusel, võimu kontrollitakse ja reeglid on ette teada. Põhiseadus nimetab õigusriiki põhimõttena ([[PS § 10]]).")
m("seaduslikkus", "Seaduslik alus", ["o-t10-02", "o-t11-03", "o-t11-04"], ["PS § 3 lg 1", "HMS § 3 lg 1"],
  "Riik tohib tegutseda ainult seaduse alusel ([[PS § 3 lg 1]]). Põhiõigusi võib piirata ainult seaduse alusel ([[HMS § 3 lg 1]]).")
m("oiguskindlus", "Õiguskindlus", ["o-t10-02", "t01-15"], ["PS § 3 lg 2", "PS § 13 lg 2"], termin="oiguskindlus")
m("proportsionaalsus", "Proportsionaalsus", ["o-t10-02", "o-t11-03", "o-t11-04", "o-t11-05", "t01-15"], ["PS § 11", "HMS § 3 lg 2"], termin="proportsionaalsus")
m("sotsiaalriik", "Sotsiaalriik", ["o-t10-02", "o-t11-06"], ["PS § 28"],
  "Riik ei jäta abivajajat üksi. Igaühel on õigus tervise kaitsele ning Eesti kodanikul õigus riigi abile vanaduse, töövõimetuse, toitjakaotuse ja puuduse korral ([[PS § 28]]).")
m("voimude-lahusus", "Võimude lahusus", ["o-t10-03"], ["PS § 4"],
  "Riigivõim on jagatud ja harud tasakaalustavad üksteist, et keegi ei saaks kogu võimu enda kätte ([[PS § 4]]).")
m("riigikogu", "Riigikogu", ["o-t10-03"], ["PS § 59", "PS § 65"],
  "Seadusandlik võim: Riigikogu võtab vastu seadused ([[PS § 59]], [[PS § 65]]).")
m("valitsus", "Valitsus", ["o-t10-03"], ["PS § 86", "PS § 87"],
  "Täidesaatev võim: valitsus viib seadusi ellu ja annab nende täitmiseks määrusi ([[PS § 86]], [[PS § 87]]). Vangla on ministeeriumi valitsemisalas olev valitsusasutus ([[VangS § 105 lg 1]]).")
m("kohus", "Kohus", ["o-t10-03", "t01-06"], ["PS § 146", "PS § 149"],
  "Kohtuvõim: õigust mõistab ainult kohus, ja kohus on sõltumatu ([[PS § 146]]). Kolm astet: esimese astme kohtud, ringkonnakohtud ja Riigikohus ([[PS § 149]]).")
m("riigikohus", "Riigikohus", ["o-t10-04", "t01-06"], ["PS § 149", "PSJKS § 15 lg 1"],
  "Riigi kõrgeim kohus ja ühtlasi põhiseadusliku järelevalve kohus ([[PS § 149]]). Võib tunnistada seaduse põhiseadusega vastuolus olevaks ja kehtetuks ([[PSJKS § 15 lg 1]]).")
m("oiguskantsler", "Õiguskantsler", ["o-t10-03", "o-t10-04", "t01-06", "t01-14"], ["PS § 139", "OKS § 19"],
  "Sõltumatu järelevalvaja: kontrollib, kas õigustloovad aktid vastavad põhiseadusele ja seadustele ([[PS § 139]]). Igaüks võib pöörduda tema poole oma õiguste kaitseks ([[OKS § 19]]).")
m("normikontroll", "Normikontroll", ["o-t10-04"], ["PS § 152", "PSJKS § 9 lg 1"],
  "Kontroll, kas seadus või määrus ise vastab põhiseadusele. Kohus jätab põhiseadusega vastuolus seaduse kohaldamata ([[PS § 152]]) ja asi liigub Riigikohtusse ([[PSJKS § 9 lg 1]]).")

# ---------- Õiguse alused: põhiõigused (tund 11)
m("pohioigus", "Põhiõigus", ["o-t11-01"], ["PS § 10"],
  "Inimese õigus riigi vastu. Põhiseaduses loetletud õigused ei välista muid õigusi, mis tulenevad põhiseaduse mõttest ([[PS § 10]]).")
m("vabadusoigus", "Vabadusõigus", ["o-t11-01", "o-t11-04"], ["PS § 20 lg 1"],
  "Õigus, et riik jätaks rahule – näiteks vabadus ja isikupuutumatus ([[PS § 20 lg 1]]). Rikkumine on riigi sekkumine.")
m("vordsusoigus", "Võrdsusõigus", ["o-t11-01", "o-t11-05", "t01-15"], ["PS § 12 lg 1"],
  "Sarnaseid tuleb kohelda sarnaselt: kõik on seaduse ees võrdsed ([[PS § 12 lg 1]]). Rikkumine on põhjendamatu erinev kohtlemine.")
m("sooritusoigus", "Sooritusõigus", ["o-t11-01", "o-t11-06"], ["PS § 14"],
  "Õigus, et riik teeks midagi: kaitseks, looks menetluse või aitaks. Õiguste tagamine on kõigi võimude kohustus ([[PS § 14]]). Rikkumine on tegevusetus.")
m("kandja", "Põhiõiguse kandja", ["o-t11-02"], ["PS § 9 lg 1", "VangS § 4^1 lg 1"],
  "Kellel õigus on. Igaühe õigused kehtivad ka Eestis viibivatel välismaalastel ([[PS § 9 lg 1]]) – ja ka kinnipeetaval, kelle inimväärikust tuleb austada ([[VangS § 4^1 lg 1]]).")
m("adressaat", "Põhiõiguse adressaat", ["o-t11-02"], ["PS § 14"],
  "Kes peab õigust tagama: seadusandlik, täidesaatev ja kohtuvõim ning omavalitsused ([[PS § 14]]) – ka vanglaametnik.")
m("kaitsekohustus", "Kaitse teise isiku eest", ["o-t11-02", "o-t11-06"], ["PS § 13 lg 1", "VangS § 12 lg 1 p 4"],
  "Igaühel on õigus riigi ja seaduse kaitsele ([[PS § 13 lg 1]]). Vanglas hoitakse näiteks eraldi neid, keda ähvardab kättemaks ([[VangS § 12 lg 1 p 4]]).")
m("kaitseala", "Kaitseala", ["o-t11-03", "o-t11-04"], [], termin="kaitseala")
m("riive", "Riive", ["o-t11-03", "o-t11-04", "o-t11-05"], [], termin="riive")
m("rikkumine", "Rikkumine", ["o-t11-03", "o-t11-04"], ["PS § 11"],
  "Riive, mis ei vasta põhiseadusele. Iga riive ei ole rikkumine: piirang on lubatud, kui see on vajalik ega moonuta õiguse olemust ([[PS § 11]]).")
m("reservatsioon", "Piiramise astmed", ["o-t11-04"], ["PS § 29 lg 1", "PS § 26", "PS § 18 lg 1"],
  "Osa õigusi saab piirata lihtsalt seadusega ([[PS § 29 lg 1]]), osa ainult kindlatel eesmärkidel ([[PS § 26]]) ja osa puhul piiramist ette ei nähta ([[PS § 18 lg 1]]).")
m("kohtulik-kaitse", "Õigus pöörduda kohtusse", ["o-t11-02", "o-t11-06", "t01-06", "t01-14"], ["PS § 15 lg 1"],
  "Igaüks võib oma õiguste ja vabaduste rikkumise korral pöörduda kohtusse ([[PS § 15 lg 1]]).")

# ---------- Inimõigused (tund 1)
m("uro", "ÜRO", ["t01-01"], ["ÜRO PK art 1"],
  "Globaalne organisatsioon. Üks eesmärke on edendada inimõiguste austamist ([[ÜRO PK art 1]]).")
m("uldeklaratsioon", "Inimõiguste ülddeklaratsioon", ["t01-01", "t01-08"], ["ÜDIÕ art 1"], termin="uldeklaratsioon")
m("kporp", "Kodaniku- ja poliitiliste õiguste pakt", ["t01-01"], ["KPÕRP art 2", "KPÕRP art 28"],
  "ÜRO leping: riik tagab pakti õigused kõigile oma võimu all olevatele isikutele ([[KPÕRP art 2]]); täitmist jälgib inimõiguste komitee ([[KPÕRP art 28]]).")
m("ammendamine", "Kõigepealt kodumaa vahendid", ["t01-01", "t01-03", "t01-06"], ["EIÕK art 35", "KPÕRP FP art 2"], termin="ammendamine", selgitus=
  "Rahvusvahelise kaebuse saab esitada alles siis, kui riigisisesed õiguskaitsevahendid on läbi käidud ([[EIÕK art 35]], [[KPÕRP FP art 2]]).")
m("eiok", "EIÕK", ["t01-02", "t01-03", "t01-12"], ["EIÕK art 1"], termin="eiok")
m("eik", "Euroopa Inimõiguste Kohus", ["t01-03", "t01-06"], ["EIÕK art 19", "EIÕK art 46"],
  "Alaline kohus, mis tagab EIÕK järgimise ([[EIÕK art 19]]). Riik peab kohtuotsust täitma, täitmist kontrollib ministrite komitee ([[EIÕK art 46]]).")
m("cpt", "Piinamise tõkestamise komitee (CPT)", ["t01-02", "t01-08"], ["CPT art 1"],
  "Külastab kinnipidamiskohti ja uurib vabaduse kaotanud inimeste kohtlemist, et neid piinamise ja alandava kohtlemise eest kaitsta ([[CPT art 1]]).")
m("icc", "Rahvusvaheline Kriminaalkohus", ["t01-04", "t01-06"], ["Rooma art 5"],
  "Mõistab kohut üksikisikute üle nelja raskeima kuriteo eest: genotsiid, inimsusevastased kuriteod, sõjakuriteod ja agressioon ([[Rooma art 5]]).")
m("komplementaarsus", "Komplementaarsus", ["t01-04", "t01-06"], ["Rooma art 17"], termin="komplementaarsus")
m("el-kohus", "Euroopa Liidu Kohus", ["t01-05", "t01-06"], ["ELL art 19"],
  "Tagab, et EL-i õigust tõlgendatakse ja kohaldatakse õigesti ([[ELL art 19]]).")
m("eelotsus", "Eelotsusmenetlus", ["t01-05", "t01-06"], ["ELTL art 267"],
  "Liikmesriigi kohus küsib EL-i Kohtult, kuidas EL-i õigust tõlgendada. Kinnipeetavaga seotud asjas otsustatakse võimalikult kiiresti ([[ELTL art 267]]).")
m("harta", "EL-i põhiõiguste harta", ["t01-02", "t01-05", "t01-14"], ["harta art 51"], termin="harta")
m("humanitaaroigus", "Humanitaarõigus", ["t01-07"], ["Genf III art 3"],
  "Relvakonflikti reeglid: sõjategevusest kõrvale jäänuid tuleb alati kohelda inimlikult ([[Genf III art 3]]).")
m("inimvaarikus", "Inimväärikus", ["t01-08", "o-t10-02"], ["PS § 10", "harta art 1", "VangS § 4^1 lg 1"],
  "Kõigi põhiõiguste alus ([[PS § 10]]); inimväärikus on puutumatu ([[harta art 1]]). Vanglas: kinnipeetavat koheldakse viisil, mis austab tema inimväärikust ([[VangS § 4^1 lg 1]]).")
m("piinamine", "Piinamise keeld", ["t01-08", "o-t11-04"], ["PS § 18 lg 1", "EIÕK art 3"], termin="piinamine")
m("absoluutne", "Piiramatu õigus", ["t01-07", "t01-08", "t01-09", "o-t11-04"], ["EIÕK art 15 lg 2"], termin="absoluutne-oigus", selgitus=
  "Mõnest kohustusest ei tohi riik kõrvale kalduda isegi sõja ajal või hädaolukorras – näiteks piinamise keelust ([[EIÕK art 15 lg 2]]).")
m("oigus-elule", "Õigus elule", ["t01-09"], ["PS § 16", "EIÕK art 2"],
  "Igaühel on õigus elule ja kelleltki ei tohi elu meelevaldselt võtta ([[PS § 16]], [[EIÕK art 2]]).")
m("enesemaaramisoigus", "Enesemääramisõigus", ["t01-10", "t01-01"], ["PS § 19"], termin="enesemaaramisoigus")
m("non-refoulement", "Väljasaatmise keeld", ["t01-11"], ["PagK art 33"], termin="non-refoulement")
m("eraelu", "Era- ja perekonnaelu", ["t01-12"], ["PS § 26", "EIÕK art 8"],
  "Riik ei tohi eraellu ega perekonda sekkuda, välja arvatud seaduses sätestatud juhtudel ja eesmärkidel ([[PS § 26]], [[EIÕK art 8]]).")
m("sonumisaladus", "Sõnumisaladus", ["t01-12", "o-t11-03"], ["PS § 43"],
  "Kirjade ja muude sõnumite saladus ([[PS § 43]]). Vanglas puudutab see kirjavahetust ([[VangS § 29]]).")
m("usuvabadus", "Usuvabadus", ["t01-13"], ["PS § 40", "EIÕK art 9"],
  "Igaüks võib uskuda, mida tahab, ja oma usku muuta; usu väljendamist võib piirata ainult kindlatel eesmärkidel ([[PS § 40]], [[EIÕK art 9]]).")
m("hea-haldus", "Hea haldus", ["t01-14"], ["harta art 41"],
  "Asi aetakse erapooletult, õiglaselt ja mõistliku aja jooksul: inimene kuulatakse ära, ta saab andmetega tutvuda ja otsus põhjendatakse ([[harta art 41]]).")
m("oigusparane-ootus", "Õiguspärane ootus", ["t01-15"], ["HMS § 67"], termin="oigusparane-ootus")

# ---------- Vangla (sild mõlema aine vahel)
m("vangla-piirangud", "Kinnipeetava piirangud", ["o-t11-01", "o-t11-03", "o-t11-04", "t01-10", "t01-15"], ["VangS § 4^1 lg 2"],
  "Kinnipeetava vabadust piiratakse seaduses toodud piirangutega; muid piiranguid ainult julgeoleku kaalutlusel ja nii, et need ei moonuta teiste õiguste olemust ([[VangS § 4^1 lg 2]]).")
m("vaie-vanglas", "Vaie ja kaebus vanglas", ["o-t10-03", "o-t10-04", "o-t11-06", "t01-06", "t01-14"], ["VangS § 1^1 lg 5", "VangS § 1^1 lg 7"], termin="vaie", selgitus=
  "Kinnipeetav esitab kõigepealt vaide ja alles siis kaebuse halduskohtule ([[VangS § 1^1 lg 5]]). Vaie lahendatakse 30 päeva jooksul ([[VangS § 1^1 lg 7]]).")

S = []
def s(a, b, silt): S.append({"a": a, "b": b, "silt": silt})
# põhiseadus ja põhimõtted
s("pohiseaduse-muutmine", "pohiseadus", "muudab")
s("pohiseadus", "demokraatia", "põhimõte")
s("pohiseadus", "oigusriik", "põhimõte")
s("pohiseadus", "sotsiaalriik", "põhimõte")
s("pohiseadus", "inimvaarikus", "põhimõte")
s("pohiseadus", "pohioigus", "loetleb")
s("oigusriik", "seaduslikkus", "nõuab")
s("oigusriik", "oiguskindlus", "nõuab")
s("oigusriik", "proportsionaalsus", "nõuab")
s("oigusriik", "voimude-lahusus", "nõuab")
s("demokraatia", "riigikogu", "rahvas valib")
s("voimude-lahusus", "riigikogu", "seadusandlik")
s("voimude-lahusus", "valitsus", "täidesaatev")
s("voimude-lahusus", "kohus", "kohtuvõim")
s("kohus", "riigikohus", "kõrgeim aste")
s("normikontroll", "pohiseadus", "mõõdupuu")
s("riigikohus", "normikontroll", "otsustab")
s("oiguskantsler", "normikontroll", "algatab")
s("riigikogu", "normikontroll", "seadust kontrollitakse")
# põhiõigused
s("pohioigus", "vabadusoigus", "liik")
s("pohioigus", "vordsusoigus", "liik")
s("pohioigus", "sooritusoigus", "liik")
s("pohioigus", "kandja", "kellel")
s("pohioigus", "adressaat", "kes tagab")
s("sooritusoigus", "kaitsekohustus", "hõlmab")
s("sooritusoigus", "kohtulik-kaitse", "hõlmab menetlust")
s("sooritusoigus", "sotsiaalriik", "abi")
s("vabadusoigus", "kaitseala", "1. samm")
s("kaitseala", "riive", "2. samm")
s("riive", "seaduslikkus", "kontrolli: alus")
s("riive", "proportsionaalsus", "kontrolli: mõõdukus")
s("riive", "rikkumine", "kui ei vasta PS-ile")
s("reservatsioon", "seaduslikkus", "täpsustab")
s("vordsusoigus", "riive", "erinev kohtlemine")
s("vordsusoigus", "proportsionaalsus", "mõistlik põhjus")
s("rikkumine", "kohtulik-kaitse", "vaidlusta")
s("adressaat", "valitsus", "ka ametnik")
# inimõigused
s("uro", "uldeklaratsioon", "ÜRO raames")
s("uro", "kporp", "ÜRO raames")
s("kporp", "ammendamine", "kaebus pärast")
s("eiok", "eik", "kaitseb")
s("ammendamine", "eik", "eeldus")
s("ammendamine", "kohtulik-kaitse", "kõigepealt")
s("eik", "kohus", "täiendab")
s("icc", "komplementaarsus", "põhimõte")
s("komplementaarsus", "kohus", "esmalt riigi kohus")
s("humanitaaroigus", "icc", "sõjakuriteod")
s("el-kohus", "eelotsus", "teeb")
s("eelotsus", "kohus", "küsib")
s("el-kohus", "harta", "tõlgendab")
s("inimvaarikus", "piinamine", "alus")
s("piinamine", "absoluutne", "on")
s("absoluutne", "reservatsioon", "ei saa piirata")
s("cpt", "piinamine", "tõkestab")
s("non-refoulement", "piinamine", "kaitseb ohu eest")
s("eiok", "eraelu", "art 8")
s("eraelu", "vabadusoigus", "on")
s("usuvabadus", "vabadusoigus", "on")
s("enesemaaramisoigus", "vabadusoigus", "on")
s("oigus-elule", "absoluutne", "kõrvalekaldumine piiratud")
s("sonumisaladus", "kaitseala", "näide")
s("eraelu", "sonumisaladus", "lähedane")
s("hea-haldus", "kohtulik-kaitse", "menetlusõigused")
s("oigusparane-ootus", "oiguskindlus", "tuleneb")
s("oiguskantsler", "hea-haldus", "kontrollib")
# vangla
s("kandja", "vangla-piirangud", "ka kinnipeetav")
s("vangla-piirangud", "seaduslikkus", "seaduse alusel")
s("vangla-piirangud", "riive", "on")
s("inimvaarikus", "vangla-piirangud", "piir")
s("vaie-vanglas", "kohtulik-kaitse", "tee kohtusse")
s("hea-haldus", "vaie-vanglas", "vanglas")
s("ammendamine", "vaie-vanglas", "algab siit")

ids = {k["id"] for k in K}
assert len(ids) == len(K)
for x in S: assert x["a"] in ids and x["b"] in ids, x
out = {"kirjeldus": "Mõistekaardi sisu: mõisted (sõlmed), nende teemad ja viited ning sildistatud seosed. Genereeritud skriptiga; teemad ja viited kontrollib tools/ehita.py.",
       "moisted": K, "seosed": S}
import os
json.dump(out, open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/moistekaart.json"), "w"), ensure_ascii=False, indent=1)
print(len(K), "mõistet", len(S), "seost")
