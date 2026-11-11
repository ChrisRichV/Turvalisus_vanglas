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

# ---------- Õiguse alused: normiõpetus (tund 5)
m("taielik-oigusnorm", "Täielik õigusnorm", ["o-t05-01", "o-t06-05"], ["VangS § 63 lg 1"],
  "Norm kujul „kui …, siis …”: hüpotees (tingimused) ja õiguslik tagajärg. Näide: süülise rikkumise eest võib kohaldada distsiplinaarkaristust ([[VangS § 63 lg 1]]).")
m("hupotees", "Hüpotees (faktiline koosseis)", ["o-t05-01", "o-t05-04", "o-t06-05"], ["VangS § 63 lg 1"],
  "Normi „kui”-osa: tingimused, mille korral norm kehtib – nt „süülise rikkumise eest” ([[VangS § 63 lg 1]]).")
m("oiguslik-tagajarg", "Õiguslik tagajärg", ["o-t05-01", "o-t05-04"], ["VangS § 63 lg 1", "VangS § 24 lg 1^1"],
  "Normi „siis”-osa: mida peab, võib või ei tohi teha. „Võib” = kaalutlus ([[VangS § 63 lg 1]]); „keeldutakse” = kohustus ([[VangS § 24 lg 1^1]]).")
m("sanktsioon", "Sanktsioon", ["o-t05-01", "o-t05-03"], ["VangS § 63 lg 1"],
  "Riiklik sund normi rikkumise korral – „vastasel juhul …”. Vanglas distsiplinaarkaristused ([[VangS § 63 lg 1]]).")
m("kaitumisnorm", "Käitumisnorm (primaarnorm)", ["o-t05-02", "o-t05-03"], ["VangS § 67"],
  "Kohustab, keelab või lubab isikut. Näide: kinnipeetava kohustused ([[VangS § 67]]).")
m("padevusnorm", "Pädevusnorm", ["o-t05-02", "o-t07-02"], ["VangS § 64 lg 4", "VSE § 1^2 lg 1"],
  "Ütleb, kes otsustab – nt distsiplinaarkaristuse määrab vanglateenistus ([[VangS § 64 lg 4]]). Pädevus üksi ei ole õiguslik alus.")
m("sekkumisnorm", "Sekkumisnorm (õiguslik alus)", ["o-t05-02", "o-t07-02"], ["VangS § 69 lg 1"],
  "Lubab riigil isiku õigustesse sekkuda ja ütleb, millal – nt täiendavad julgeolekuabinõud ([[VangS § 69 lg 1]]).")
m("volitusnorm", "Volitusnorm", ["o-t05-02"], ["HÕNTE § 11 lg 1", "VangS § 15 lg 3"],
  "Seaduse säte, mis annab õiguse anda määrus ([[HÕNTE § 11 lg 1]]). Näide: keelatud asjade loetelu kehtestab minister ([[VangS § 15 lg 3]]).")
m("maarus", "Määrus (üldakt)", ["o-t05-02", "o-t06-03"], ["HMS § 88", "PS § 87 p 6"],
  "Õigusakt piiritlemata arvu juhtude jaoks ([[HMS § 88]]); antakse seaduse alusel ja täitmiseks ([[PS § 87 p 6]]).")
m("legaaldefinitsioon", "Legaaldefinitsioon", ["o-t05-02", "o-t05-05", "o-t06-06"], ["VangS § 77", "HÕNTE § 18 lg 6"],
  "Seadus ütleb ise, mida sõna tähendab („käesoleva seaduse tähenduses”, [[HÕNTE § 18 lg 6]]). Näide: noor kinnipeetav ([[VangS § 77]]).")
m("spetsialiseeritud-norm", "Spetsialiseeritud normid", ["o-t05-03"], ["VangS § 63 lg 2", "VangS § 71 lg 3^1"],
  "Norm ilma kui–siis ehituseta, mis kitsendab ([[VangS § 63 lg 2]]), seletab või viitab ([[VangS § 71 lg 3^1]]).")
m("koosseisu-liigid", "Kumulatiivne ja alternatiivne koosseis", ["o-t05-04", "o-t06-05"], ["VangS § 41 lg 1", "VangS § 24 lg 1^1"],
  "Kõik tunnused korraga („ja”, [[VangS § 41 lg 1]]) või vähemalt üks („või”, [[VangS § 24 lg 1^1]]).")
m("tolgendamine", "Tõlgendamine", ["o-t05-05"], ["HÕNTE § 18 lg 6", "VangS § 6 lg 1"],
  "Normi sisu väljaselgitamine: grammatiline, süstemaatiline, ajalooline, teleoloogiline võte. Alusta legaaldefinitsioonist ([[HÕNTE § 18 lg 6]]); eesmärgi järgi vt nt [[VangS § 6 lg 1]].")
m("lynk", "Lünk ja analoogia", ["o-t05-06"], ["PS § 23", "HMS § 3 lg 1"],
  "Lünk = normi ei ole. Analoogia on haldus- ja karistusõiguses isiku kahjuks keelatud ([[PS § 23]], [[HMS § 3 lg 1]]).")
m("vastuolu", "Vastuolu: kõrgem, hilisem, erinorm", ["o-t05-06", "o-t07-02"], ["PS § 152", "VangS § 1^1 lg 1"],
  "Kaks normi annavad välistavad tagajärjed. Võidab kõrgem ([[PS § 152]]), hilisem või erinorm ([[VangS § 1^1 lg 1]]).")

# ---------- Õiguse alused: õiguse realiseerimine (tund 6)
m("realiseerimine", "Kasutamine, järgimine, rakendamine", ["o-t06-01"], ["VangS § 28 lg 1", "VangS § 67"],
  "Õigus jõuab ellu: isik kasutab õigust ([[VangS § 28 lg 1]]), järgib kohustust ([[VangS § 67]]) või riik rakendab õigust tema suhtes.")
m("oiguse-rakendamine", "Õiguse rakendamine", ["o-t06-01", "o-t06-04"], ["PS § 3 lg 1", "HMS § 6"],
  "Pädeva riigiorgani otsus normi alusel konkreetse elujuhtumi kohta – seaduslik ([[PS § 3 lg 1]]) ja asjaolud välja selgitatud ([[HMS § 6]]).")
m("oigussuhe", "Õigussuhe", ["o-t06-02"], ["VangS § 28 lg 1", "VangS § 28 lg 3"],
  "Isikute seos normi alusel: ühel õigus, teisel kohustus. Kinnipeetaval on õigus kirjavahetusele ([[VangS § 28 lg 1]]), vangla saab seda piirata ainult seaduse alusel ([[VangS § 28 lg 3]]).")
m("juriidiline-fakt", "Juriidiline fakt", ["o-t06-02"], ["VangS § 63 lg 1"],
  "Elus toimuv muutus, millega seadus seob tagajärje – nt süüline rikkumine ([[VangS § 63 lg 1]]).")
m("uksikakt", "Üksikakt (haldusakt)", ["o-t06-03"], ["HMS § 51 lg 1", "VangS § 64 lg 4"],
  "Konkreetne ja individuaalne, rakendab õigust ([[HMS § 51 lg 1]]). Vanglas nt distsiplinaarkaristuse käskkiri ([[VangS § 64 lg 4]]).")
m("toiming", "Toiming", ["o-t06-03"], ["HMS § 106 lg 1"],
  "Haldusorgani tegevus, mis ei ole õigusakti andmine ([[HMS § 106 lg 1]]) – nt läbiotsimine. Ka see vajab seaduslikku alust.")
m("toendamine", "Asjaolud ja tõendid", ["o-t06-04"], ["HMS § 6", "HMS § 38 lg 2"],
  "Haldusorgan selgitab olulised asjaolud välja ise ([[HMS § 6]]); tõendid on loetletud seaduses ([[HMS § 38 lg 2]]).")
m("subsumeerimine", "Subsumeerimine", ["o-t06-05", "o-t07-01"], ["VangS § 25 lg 1"],
  "Eluliste asjaolude võrdlemine normi koosseisuga; kui kõik tunnused on täidetud, saabub tagajärg. Näide: [[VangS § 25 lg 1]].")
m("maaratlemata", "Määratlemata õigusmõiste", ["o-t06-06"], ["VangS § 24 lg 1^1"],
  "Teadlikult avar mõiste koosseisus – „vangla julgeolek või kord” ([[VangS § 24 lg 1^1]]). Sisustatakse iga juhtumi asjaoludega.")
m("kaalutlusoigus", "Kaalutlusõigus", ["o-t06-06", "o-t05-04"], ["HMS § 4 lg 1", "HMS § 4 lg 2"],
  "Volitus kaaluda või valida mitme otsuse vahel ([[HMS § 4 lg 1]]); kooskõlas eesmärgi ja üldpõhimõtetega ([[HMS § 4 lg 2]]). Märksõna normis: „võib”.")

# ---------- Õiguse alused: kaasuste lahendamine (tund 7)
m("syllogism", "Õiguslik süllogism", ["o-t07-01"], ["VangS § 63 lg 1"],
  "Suur eeldus (norm) + väike eeldus (asjaolud) = järeldus. Iga õigusliku otsuse loogika; näide: [[VangS § 63 lg 1]].")
m("kuus-sammu", "Kuus sammu", ["o-t07-01", "o-t07-04"], ["HMS § 6"],
  "Loe kaasus → loe küsimus → norm ja tunnused → seosta asjaoludega → vajadusel tagajärg → järeldus. Asjaolud peavad olema välja selgitatud ([[HMS § 6]]).")
m("normi-leidmine", "Õige norm", ["o-t07-02"], ["VangS § 1^1 lg 1"],
  "Eelista eriseadust (VangS) üldseadusele (HMS) ja konkreetset normi abstraktsele ([[VangS § 1^1 lg 1]]). Norm peab vastama küsimusele.")
m("analuusiv-stiil", "Analüüsiv ja otsustusstiil", ["o-t07-03"], ["VangS § 64 lg 4"],
  "Eksamil analüüsiv (küsimus → eeldused → järeldus); haldusaktis otsustusstiil (otsus → põhjendus). Käskkirja tuleb põhjendada ([[VangS § 64 lg 4]]).")
m("distsiplinaarkaristus", "Distsiplinaarkaristus", ["o-t05-01", "o-t06-04", "o-t07-04"], ["VangS § 63 lg 1", "VangS § 64 lg 2"],
  "Vangla sanktsioon süülise rikkumise eest ([[VangS § 63 lg 1]]); enne määramist teavitatakse kinnipeetavat ja kuulatakse ta ära ([[VangS § 64 lg 2]]).")

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

# tunnid 5–7 omavahel
s("taielik-oigusnorm", "hupotees", "koosneb")
s("taielik-oigusnorm", "oiguslik-tagajarg", "koosneb")
s("oiguslik-tagajarg", "sanktsioon", "võib olla")
s("kaitumisnorm", "sanktsioon", "rikkumisel")
s("koosseisu-liigid", "hupotees", "liigitab")
s("volitusnorm", "maarus", "lubab anda")
s("padevusnorm", "sekkumisnorm", "ei asenda")
s("spetsialiseeritud-norm", "taielik-oigusnorm", "täiendab")
s("legaaldefinitsioon", "tolgendamine", "1. reegel")
s("tolgendamine", "maaratlemata", "sisustab")
s("lynk", "tolgendamine", "ületatakse")
s("juriidiline-fakt", "oigussuhe", "tekitab")
s("juriidiline-fakt", "hupotees", "on kirjas")
s("realiseerimine", "oiguse-rakendamine", "üks viis")
s("oiguse-rakendamine", "uksikakt", "tulemus")
s("oiguse-rakendamine", "toiming", "tulemus")
s("oiguse-rakendamine", "toendamine", "samm")
s("toendamine", "subsumeerimine", "eeldus")
s("subsumeerimine", "hupotees", "võrdleb")
s("maaratlemata", "hupotees", "on koosseisus")
s("kaalutlusoigus", "oiguslik-tagajarg", "on tagajärjes")
s("syllogism", "subsumeerimine", "tuum")
s("kuus-sammu", "syllogism", "põhineb")
s("normi-leidmine", "vastuolu", "erinorm")
s("normi-leidmine", "padevusnorm", "ära sega")
s("analuusiv-stiil", "kuus-sammu", "kirjapanek")
s("distsiplinaarkaristus", "sanktsioon", "on")
s("distsiplinaarkaristus", "uksikakt", "käskkiri")
s("maarus", "uksikakt", "erineb")
# sillad varasemate tundidega
s("sekkumisnorm", "seaduslikkus", "annab aluse")
s("sekkumisnorm", "riive", "lubab")
s("maarus", "seaduslikkus", "seaduse alusel")
s("vastuolu", "normikontroll", "kõrgem norm")
s("vastuolu", "pohiseadus", "kõrgeim")
s("subsumeerimine", "kaitseala", "sama loogika")
s("kaalutlusoigus", "proportsionaalsus", "piirab")
s("oiguse-rakendamine", "seaduslikkus", "nõue")
s("distsiplinaarkaristus", "vaie-vanglas", "vaidlustatav")
s("vangla-piirangud", "sekkumisnorm", "vajab")
s("lynk", "seaduslikkus", "analoogia ei asenda")
s("oigussuhe", "pohioigus", "riik ↔ isik")

# ---------- Vangla psühholoogia (korrektsioonipsühholoogia, tunnid 1–8)
m("korrektsioonipsuhholoogia", "Korrektsioonipsühholoogia", ["ps-t01-01", "ps-t01-02"], ["VangS § 6 lg 1"],
  "Selgitab, kuidas kriminaalne käitumine tekib, ja annab teadmist, kuidas seda muuta. Teenib vangistuse eesmärki: suunata õiguskuulekale käitumisele ([[VangS § 6 lg 1]]).")
m("teaduspohisus", "Teaduspõhine praktika", ["ps-t01-02", "ps-t01-03"], [],
  "Sekkumine valitakse tõendite, mitte ainult kõhutunde ja kogemuse järgi. Kursuse järgi viib teaduseta praktika kallite ja kahjulike tulemusteni.")
m("karistuse-eesmargid", "Karistuse eesmärgid", ["ps-t01-04", "ps-t01-05"], ["VangS § 6 lg 1", "VangS § 4^1 lg 1"],
  "Valgustusajal: ennetada, suunata kergemale, vähendada kahju, väikese kuluga. Täna: õiguskuulekale käitumisele suunamine ([[VangS § 6 lg 1]]), kannatus ei tohi ületada paratamatut ([[VangS § 4^1 lg 1]]).")
m("heidutus", "Karistuse mõju", ["ps-t01-05"], [],
  "Kursuse järgi ei hoia karistus üksi kuritegudest eemale ei kurjategijaid ega ühiskonda; leitud efektid on nõrgad.")
m("rnr", "RNR-mudel", ["ps-t02-01", "ps-t05-05"], ["VangS § 14 lg 1^2"],
  "Riski-vajaduse-vastavuse mudel – teaduslikult kõige mõjukam teooria sekkumiste valimiseks. Vanglas hinnatakse saabumisel riske ([[VangS § 14 lg 1^2]]).")
m("ope-kaitumine", "Õpitud käitumine", ["ps-t02-01", "ps-t02-02", "ps-t02-03", "ps-t02-05"], [],
  "Kriminaalne käitumine on õpitud – selle lõpetamiseks tuleb õppida prosotsiaalseid viise samade eesmärkide saavutamiseks.")
m("klassikaline-tingimine", "Klassikaline tingimine", ["ps-t02-02", "ps-t05-02"], [],
  "Teadvustamata õppimine: neutraalne stiimul seostub reaktsiooniga (nt seltskond tekitab isu, uksekolin hirmu).")
m("operantne-tingimine", "Operantne tingimine", ["ps-t02-03", "ps-t05-02"], [],
  "Käitumine õpitakse tagajärgede kaudu: positiivne/negatiivne tasu ja karistus. Karistus mõjub kõige paremini kohe pärast tegu.")
m("mudeldamine", "Mudeldamine", ["ps-t02-05", "ps-t08-04"], [],
  "Teisi jälgides õppimine. Ametnik on mudel oma tegudega: reeglite järgimine, täpsus, lugupidamine, vigade tunnistamine.")
m("enesekontroll", "Enesekontroll", ["ps-t02-04", "ps-t03-01", "ps-t03-02"], [],
  "Madal enesekontroll (impulsiivsus, riskialdisus) suurendab kuritegevuse tõenäosust; seda saab arendada enesetõhususe kaudu.")
m("moraalne-tagasitombumine", "Moraalne tagasitõmbumine", ["ps-t02-04", "ps-t03-01"], [],
  "Bandura: viisid oma moraalist lahti öelda – õigustamine, eufemismid, võrdlus, vastutuse hajutamine ja jagamine, tagajärgede eiramine, dehumaniseerimine, süü nihutamine.")
m("motivatsioon", "Motivatsioon", ["ps-t02-05", "ps-t05-05"], [],
  "Enesemääratlemise teooria: väline (4 liiki) ja sisemine motivatsioon; autonoomia on keskne.")
m("muutusering", "Muutusering", ["ps-t02-06", "ps-t05-03"], [],
  "Transteoreetiline mudel: eelkaalutlemine → kaalutlemine → ettevalmistus → tegutsemine → säilitamine; tagasilangus on normaalne.")
m("kriminaalne-motlemine", "Kriminaalne mõtlemine", ["ps-t03-01", "ps-t03-03"], [],
  "Hoiakud ja uskumused, mis toetavad kriminaalset elustiili; üks neljast suurest retsidivismi ennustajast. Proaktiivne või reaktiivne.")
m("sekkumine", "Sekkumise faasid", ["ps-t03-03"], [],
  "Ettevalmistus (kriis, Shamani efekt, avalik lubadus) → tegutsemine (kognitiivsed ja käitumuslikud oskused) → järelfaas.")
m("psuuhikahaire", "Psüühikahäire", ["ps-t04-01", "ps-t04-02", "ps-t04-03", "ps-t04-04"], ["VangS § 52 lg 2"],
  "Märgatav nihe psüühikas, mis takistab toimetulekut. Vanglas suurendab enesevigastamise ja uue kuriteo riski; tervishoiutöötaja jälgib terviseseisundit ([[VangS § 52 lg 2]]).")
m("suitsiidirisk", "Suitsiidirisk", ["ps-t04-05"], ["VangS § 14 lg 1"],
  "Suurim vangistuse alguses, noortel ja sõltuvus- või psüühikahäirega kinnipeetavatel. Isolatsioon ei sobi. Saabumisel tervisekontroll ([[VangS § 14 lg 1]]).")
m("stigma", "Stigma ja märgistamine", ["ps-t04-06", "ps-t06-01"], [],
  "Häbimärgistamine ja silt võivad muutuda identiteediks (teisene hälbivus) – ennasttäitev ennustus.")
m("soltuvus", "Sõltuvus", ["ps-t05-01", "ps-t05-02", "ps-t05-03"], [],
  "Krooniline ajuhaigus: sund tarvitada hoolimata kahjust. Kujuneb paljude tegurite koosmõjul.")
m("ained-ja-kuritegevus", "Ained ja kuritegevus", ["ps-t05-04", "ps-t05-05"], [],
  "Alkohol on rohkem seotud vägivallaga; narkootikumide tarvitamine võib kuriteole eelneda või järgneda.")
m("keeruline-kinnipeetav", "Keeruline kinnipeetav", ["ps-t06-01", "ps-t06-02", "ps-t06-03"], ["VangS § 4^1 lg 2"],
  "Käitumisel on alati funktsioon. Rohkem kontrolli annab lihtsalt rohkem reegleid rikkuda; piirangud peavad olema vajalikud ([[VangS § 4^1 lg 2]]).")
m("suhtlusvotted", "Suhtlusvõtted", ["ps-t06-04", "ps-t06-05"], [],
  "Agressiivne: empaatia, kaasamine, ventileerimine, viimasena piirid. Kinnine: vaikus ja avatud küsimused. Jutukas: eesmärk ja kokkuvõtted.")
m("ametniku-heaolu", "Ametniku heaolu", ["ps-t06-06"], [],
  "Keeruline klient kurnab; tagajärjeks võivad olla stress, vältimine, hüperreaktsioonid ja püsiv hirm.")
m("haavatavus", "Haavatavus", ["ps-t07-01", "ps-t07-02", "ps-t07-03", "ps-t07-04", "ps-t07-05"], ["VangS § 14 lg 3"],
  "Tunnused: psühhiaatriline diagnoos, madal haridus, nõrk tugi, ohvrikogemus, noor vanus, toimetulekuoskuste puudus. Vastuvõtul selgitatakse välja eluloolised andmed ([[VangS § 14 lg 3]]).")
m("noor-kinnipeetav", "Noor kinnipeetav", ["ps-t07-05"], ["VangS § 81 lg 1"],
  "Mitu korda rohkem psühhoosi, ATH-d ja käitumishäireid; vanusegruppe hoitakse eraldi ([[VangS § 81 lg 1]]).")
m("koostoosuhe", "Koostöösuhe", ["ps-t08-01", "ps-t08-02"], ["VangS § 16 lg 2"],
  "Kokkulepitud eesmärgid + ülesannetega seotud koostöö + aktsepteeriv suhe. Täitmiskava arutatakse kinnipeetavaga ([[VangS § 16 lg 2]]).")
m("vaartuskonflikt", "Väärtuskonflikt", ["ps-t08-03"], [],
  "Kaks olulist väärtust põrkuvad. Ametnikul isiklik (hoiakud) või professionaalne (pädevuse piirid).")
m("taitmiskava", "Individuaalne täitmiskava", ["ps-t01-05", "ps-t08-01"], ["VangS § 16 lg 1"],
  "Kava paigutuse, hariduse, töö, soodustuste ja vabanemise ettevalmistuse kohta, kui vangistus on üle aasta ([[VangS § 16 lg 1]]).")

# psühholoogia omavahel
s("korrektsioonipsuhholoogia", "teaduspohisus", "toetub")
s("korrektsioonipsuhholoogia", "karistuse-eesmargid", "teenib")
s("heidutus", "karistuse-eesmargid", "piirab")
s("ope-kaitumine", "klassikaline-tingimine", "üks viis")
s("ope-kaitumine", "operantne-tingimine", "üks viis")
s("ope-kaitumine", "mudeldamine", "üks viis")
s("rnr", "ope-kaitumine", "toetub")
s("enesekontroll", "kriminaalne-motlemine", "madal soodustab")
s("moraalne-tagasitombumine", "kriminaalne-motlemine", "sisu")
s("sekkumine", "kriminaalne-motlemine", "muudab")
s("motivatsioon", "muutusering", "liigutab")
s("muutusering", "soltuvus", "kasutatakse")
s("klassikaline-tingimine", "soltuvus", "isu")
s("operantne-tingimine", "soltuvus", "kinnistab")
s("soltuvus", "psuuhikahaire", "F1")
s("soltuvus", "ained-ja-kuritegevus", "seos")
s("psuuhikahaire", "suitsiidirisk", "tõstab")
s("stigma", "psuuhikahaire", "takistab abi")
s("stigma", "keeruline-kinnipeetav", "ootused")
s("keeruline-kinnipeetav", "suhtlusvotted", "vajab")
s("keeruline-kinnipeetav", "ametniku-heaolu", "kurnab")
s("haavatavus", "suitsiidirisk", "tõstab")
s("haavatavus", "noor-kinnipeetav", "näide")
s("koostoosuhe", "motivatsioon", "toetab")
s("koostoosuhe", "suhtlusvotted", "kasutab")
s("mudeldamine", "koostoosuhe", "osa")
s("vaartuskonflikt", "koostoosuhe", "takistab")
s("taitmiskava", "koostoosuhe", "arutatakse")
s("rnr", "taitmiskava", "riskihindamine")
s("operantne-tingimine", "heidutus", "ajastus")
# sillad teiste ainetega
s("karistuse-eesmargid", "inimvaarikus", "piir")
s("keeruline-kinnipeetav", "vangla-piirangud", "ainult vajalikud")
s("operantne-tingimine", "distsiplinaarkaristus", "karistus")
s("stigma", "vordsusoigus", "ebaõiglane kohtlemine")
s("ained-ja-kuritegevus", "eraelu", "õigus ravist keelduda")
s("taitmiskava", "uksikakt", "kinnitab ametnik")
s("suitsiidirisk", "inimvaarikus", "isolatsioon ei sobi")
s("korrektsioonipsuhholoogia", "seaduslikkus", "seaduse raamides")

ids = {k["id"] for k in K}
assert len(ids) == len(K)
for x in S: assert x["a"] in ids and x["b"] in ids, x
out = {"kirjeldus": "Mõistekaardi sisu: mõisted (sõlmed), nende teemad ja viited ning sildistatud seosed. Genereeritud skriptiga; teemad ja viited kontrollib tools/ehita.py.",
       "moisted": K, "seosed": S}
import os
json.dump(out, open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/moistekaart.json"), "w"), ensure_ascii=False, indent=1)
print(len(K), "mõistet", len(S), "seost")
