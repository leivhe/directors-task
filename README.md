# Director Task

Nettleserbasert implementasjon av [Keysar Director Task](https://sites.google.com/site/idcnlab/director-task) for måling av perspektivtaking. Bygget med [jsPsych 7.3.4](https://www.jspsych.org/).

## Bakgrunn

Director Task er et psykologisk eksperiment der deltakeren ser en hylle med objekter og en «direktør» som ber deltakeren flytte et bestemt objekt. Noen hylleceller er blokkert (grå bakgrunn) og usynlige for direktøren. I de kritiske forsøkene finnes det to objekter med samme beskrivelse – ett synlig og ett usynlig for direktøren. Deltakeren må ta direktørens perspektiv og velge riktig objekt.

Eksperimentet er en forenklet versjon basert på Tamnes et al., der deltakeren klikker på ønsket objekt fremfor å dra det.

## Struktur

```
experiment/
├── index.html          # Hele eksperimentet (én selvinneholdt fil)
├── setup.sh            # Engangsoppsett: konverterer BMP→PNG og kopierer WAV
├── js/
│   └── trials_data.js  # Forsøksdata for alle 6 testvariantar
├── img/                # PNG-bilder av hyllescener (68 filer)
├── snd/                # WAV-lydinstruksjoner (108 filer)
└── jspsych/            # jsPsych 7.3.4 (lokale filer, fungerer uten internett)
```

## Oppsett

Kjør `setup.sh` én gang for å konvertere originalbildene (BMP) og lydfilene (WAV) til riktig mappe. Krever [ImageMagick](https://imagemagick.org/).

```bash
cd experiment
bash setup.sh
```

Hvis originalfilene allerede er konvertert (mappen `img/` og `snd/` er fylt), kan dette steget hoppes over.

## Kjøre eksperimentet

Start en lokal webserver fra `experiment/`-mappen:

```bash
cd experiment
python3 -m http.server 8080
```

Åpne deretter `http://localhost:8080` i nettleseren.

## Gjennomføring

1. Forskningsassistenten fyller inn deltakar-ID og velger testversjon (1–6).
2. Deltakeren gjennomfører øvingsforsøk, så de to betingelsene (Director og No-Director) i rekkefølge bestemt av testversjonen.
3. Etter siste forsøk klikker assistenten «Last ned data» – en CSV-fil lastes ned automatisk.

### Testversjoner

| Versjon | Rekkefølge         |
|---------|--------------------|
| 1–3     | Director først     |
| 4–6     | No-Director først  |

### Kortversjon (kun for testing)

Kryss av «Kortversjon» på startsiden for å kjøre 3 øvingsforsøk + 3 ekte forsøk. Brukes til å teste nye versjoner raskt.

## Dataformat

CSV-filen lagres som `director_[ID]_[dato].csv` med én rad per forsøk:

| Kolonne           | Innhold                                              |
|-------------------|------------------------------------------------------|
| `timeline_index`  | Løpenummer i jsPsych-tidslinjen                      |
| `participant_id`  | Deltakar-ID                                          |
| `test_version`    | Testversjon (1–6)                                    |
| `condition`       | `director` eller `no_director`                       |
| `order_set`       | Blokknummer (1–16)                                   |
| `item_number`     | Forsøksnummer innen blokk (1–3)                      |
| `trial_type_num`  | 0 = filler, 1 = kontroll, 2 = eksperimentell         |
| `trial_type_label`| `filler`, `control` eller `experimental`             |
| `picture`         | Bildefil                                             |
| `instruction`     | Tekstlig instruksjon                                 |
| `soundfile`       | Lydfil                                               |
| `correct_answer`  | Riktig celle (bokstav A–P)                           |
| `competitor_cell` | Konkurrerende celle (kun eksperimentelle forsøk)     |
| `cell_clicked`    | Cellen deltakeren klikket (f.eks. `r2c1`)            |
| `rt_from_audio`   | Reaksjonstid fra lydstart i millisekunder            |
| `correct`         | 1 = riktig, 0 = feil, tom = ingen respons            |
| `chose_competitor`| 1/0 hvis feil eksperimentelt svar; ellers tom        |

### Cellekoding

Cellene i 4×4-hyllen er kodet som `rXcY` (rad × kolonne, 0-indeksert fra øverst til venstre) og som bokstaver A–P i `correct_answer`/`competitor_cell`:

```
A(r0c0)  B(r0c1)  C(r0c2)  D(r0c3)
E(r1c0)  F(r1c1)  G(r1c2)  H(r1c3)
I(r2c0)  J(r2c1)  K(r2c2)  L(r2c3)
M(r3c0)  N(r3c1)  O(r3c2)  P(r3c3)
```

## Tekniske merknader

- Eksperimentet kjører helt lokalt – ingen data sendes til eksterne tjenere.
- jsPsych er inkludert som lokale filer og krever ikke internett.
- Reaksjonstid måles fra `audio.play()`-eventet, ikke fra trial-start.
- Lydfilen spiller alltid ferdig før neste forsøk starter, selv om deltakeren klikker tidlig.
- Makstid per forsøk er 6 sekunder; tom `cell_clicked` betyr at deltakeren ikke svarte.
