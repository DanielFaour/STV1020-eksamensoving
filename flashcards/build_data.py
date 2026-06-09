from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "STV1020_100_multiple_choice.md"
OUTPUT = Path(__file__).resolve().parent / "data.js"


FLASHCARDS = [
    ("Vitenskapelig metode", "Empirisk påstand", "En påstand som kan undersøkes og vurderes ved hjelp av systematiske observasjoner."),
    ("Vitenskapelig metode", "Normativ påstand", "En vurdering av hvordan noe bør være, heller enn en beskrivelse av hvordan noe faktisk er."),
    ("Vitenskapelig metode", "Teori", "En generell og logisk sammenhengende forklaring på et fenomen."),
    ("Vitenskapelig metode", "Hypotese", "En konkret, testbar forventning som er utledet fra en teori."),
    ("Vitenskapelig metode", "Falsifiserbarhet", "At det finnes et mulig empirisk resultat som ville telle mot en påstand."),
    ("Vitenskapelig metode", "Etterprøvbarhet", "At andre kan undersøke framgangsmåten og forsøke å gjenskape resultatet."),
    ("Vitenskapelig metode", "Parsimoni", "Prinsippet om å foretrekke den enkleste forklaringen som fortsatt forklarer fenomenet godt."),
    ("Vitenskapelig metode", "Avhengig variabel (Y)", "Utfallet eller fenomenet forskeren ønsker å forklare."),
    ("Vitenskapelig metode", "Uavhengig variabel (X)", "En variabel som antas å påvirke eller forklare den avhengige variabelen."),
    ("Kausalitet", "Kausalitet", "At en endring i X fører til en endring i Y, alt annet likt."),
    ("Kausalitet", "Samvariasjon", "At verdier på to variabler varierer systematisk sammen. Samvariasjon alene beviser ikke kausalitet."),
    ("Kausalitet", "Kausalmekanisme", "Prosessen eller kjeden av hendelser som forklarer hvordan X påvirker Y."),
    ("Kausalitet", "Kontrafaktisk", "Det utfallet samme enhet ville hatt dersom årsaksvariabelen hadde hatt en annen verdi."),
    ("Kausalitet", "Mediator", "En mellomliggende variabel som formidler hele eller deler av effekten fra X til Y."),
    ("Kausalitet", "Konfunderende variabel", "En bakenforliggende variabel Z som påvirker Y og samvarierer med X."),
    ("Kausalitet", "Reversert kausalitet", "At årsaksretningen går motsatt vei av den forskeren hevder, for eksempel fra Y til X."),
    ("Kausalitet", "Nødvendig årsak", "En faktor som må være til stede for at et utfall skal kunne oppstå."),
    ("Kausalitet", "Tilstrekkelig årsak", "En faktor som alene er nok til å utløse et utfall."),
    ("Forskningsdesign", "Random assignment", "Tilfeldig fordeling til behandlings- og kontrollgruppe. Styrker intern validitet."),
    ("Forskningsdesign", "Random sampling", "Tilfeldig trekking fra en populasjon. Styrker representativitet og generalisering."),
    ("Forskningsdesign", "Intern validitet", "Hvor troverdig den kausale konklusjonen er for enhetene som er undersøkt."),
    ("Forskningsdesign", "Ekstern validitet", "I hvilken grad funnet kan generaliseres til andre enheter, steder eller tidspunkter."),
    ("Forskningsdesign", "Observasjonsstudie", "En studie der forskeren observerer variasjon uten selv å randomisere behandlingen."),
    ("Forskningsdesign", "Seleksjonsskjevhet", "Systematiske forskjeller mellom de observerte eller sammenlignede gruppene som påvirker resultatet."),
    ("Måling", "Operasjonalisering", "Å oversette et abstrakt begrep til en konkret målbar variabel."),
    ("Måling", "Begrepsvaliditet", "Hvor godt en operasjonalisering faktisk måler begrepet den skal representere."),
    ("Måling", "Reliabilitet", "Hvor stabilt og reproduserbart et mål er ved gjentatte målinger."),
    ("Måling", "Nominalnivå", "Kategorier uten naturlig rangering, som partitilhørighet."),
    ("Måling", "Ordinalnivå", "Kategorier med naturlig rangering, men uten kjent lik avstand mellom nivåene."),
    ("Måling", "Intervallnivå", "Numeriske verdier med like avstander, men uten et meningsfullt absolutt nullpunkt."),
    ("Måling", "Forholdstallsnivå", "Numeriske verdier med like avstander og et meningsfullt absolutt nullpunkt."),
    ("Måling", "Dummyvariabel", "En variabel kodet 0 eller 1 som viser fravær eller tilstedeværelse av en kategori."),
    ("Deskriptiv statistikk", "Gjennomsnitt", "Summen av alle verdier delt på antallet observasjoner. Følsomt for uteliggere."),
    ("Deskriptiv statistikk", "Median", "Den midterste verdien når observasjonene rangeres. Robust mot uteliggere."),
    ("Deskriptiv statistikk", "Standardavvik", "Et mål på hvor mye observasjonene typisk avviker fra gjennomsnittet."),
    ("Deskriptiv statistikk", "Varians", "Gjennomsnittlig kvadrert avvik fra gjennomsnittet. Standardavviket er kvadratroten av variansen."),
    ("Deskriptiv statistikk", "Interkvartilbredde", "Avstanden mellom første og tredje kvartil; beskriver spredningen i de midterste 50 prosentene."),
    ("Deskriptiv statistikk", "Uteliggere", "Observasjoner som ligger uvanlig langt fra resten av fordelingen."),
    ("Deskriptiv statistikk", "Skjevfordeling", "En fordeling med en lengre hale på den ene siden enn den andre."),
    ("Statistisk inferens", "Populasjon", "Hele mengden enheter forskeren ønsker å si noe om."),
    ("Statistisk inferens", "Utvalg", "En delmengde av populasjonen som faktisk observeres."),
    ("Statistisk inferens", "Parameter", "En ukjent sann størrelse i populasjonen, som populasjonsgjennomsnittet."),
    ("Statistisk inferens", "Estimat", "En beregnet verdi fra utvalget som brukes til å anslå en populasjonsparameter."),
    ("Statistisk inferens", "Standardfeil", "Et mål på hvor mye et estimat forventes å variere mellom tilfeldige utvalg."),
    ("Statistisk inferens", "Konfidensintervall", "Et intervall konstruert av en metode som ved gjentatte utvalg vil dekke den sanne parameteren en bestemt andel av gangene."),
    ("Statistisk inferens", "Nullhypotese", "Påstanden som testes, ofte at det ikke finnes noen effekt eller sammenheng i populasjonen."),
    ("Statistisk inferens", "P-verdi", "Sannsynligheten for et minst like ekstremt resultat som det observerte, gitt at nullhypotesen er sann."),
    ("Statistisk inferens", "Signifikansnivå", "Terskelen forskeren velger for å forkaste nullhypotesen, ofte 0,05."),
    ("Statistisk inferens", "Type I-feil", "Å forkaste en sann nullhypotese, altså et falskt positivt funn."),
    ("Statistisk inferens", "Type II-feil", "Å unnlate å forkaste en falsk nullhypotese, altså et falskt negativt funn."),
    ("Statistisk inferens", "Statistisk styrke", "Sannsynligheten for å oppdage en reell effekt og forkaste en falsk nullhypotese."),
    ("Bivariat analyse", "Krysstabell", "En tabell som viser frekvenser eller prosentfordelinger for kombinasjoner av to kategoriske variabler."),
    ("Bivariat analyse", "Kjikvadrattest", "En test av om to kategoriske variabler er statistisk uavhengige."),
    ("Bivariat analyse", "T-test", "En test som ofte brukes til å undersøke om to grupper har ulike gjennomsnitt."),
    ("Bivariat analyse", "Korrelasjon", "Et standardisert mål fra -1 til 1 på retning og styrke i en lineær sammenheng."),
    ("Regresjon", "Regresjonskoeffisient", "Forventet endring i Y når X øker med én enhet, med øvrige inkluderte variabler holdt konstant."),
    ("Regresjon", "Konstantledd", "Modellens forventede verdi på Y når alle forklaringsvariabler er null."),
    ("Regresjon", "Residual", "Forskjellen mellom observert og predikert verdi: Y minus Ŷ."),
    ("Regresjon", "OLS", "Ordinary least squares: estimerer regresjonslinjen ved å minimere summen av kvadrerte residualer."),
    ("Regresjon", "R²", "Andelen av variasjonen i Y som regresjonsmodellen forklarer."),
    ("Regresjon", "Utelatt variabelskjevhet", "Skjevhet som oppstår når en utelatt variabel påvirker Y og er korrelert med en inkludert X."),
    ("Regresjon", "Multikollinearitet", "Sterk lineær sammenheng mellom forklaringsvariabler som gjør separate effekter vanskeligere å estimere presist."),
    ("Regresjon", "Samspill", "At effekten av én forklaringsvariabel avhenger av verdien på en annen variabel."),
    ("Regresjon", "Heteroskedastisitet", "At residualenes varians ikke er konstant på tvers av observasjoner eller X-verdier."),
    ("Regresjon", "Autokorrelasjon", "At residualer er korrelert mellom observasjoner, ofte over tid eller innen grupper."),
    ("Regresjon", "Robuste standardfeil", "En korrigert usikkerhetsberegning som kan håndtere blant annet heteroskedastisitet, men ikke reparerer kausal skjevhet."),
    ("Faste effekter", "Enhetsfaste effekter", "Kontrollerer for alle observerte og uobserverte kjennetegn som er konstante innen enheten over tid."),
    ("Faste effekter", "Tidsfaste effekter", "Kontrollerer for felles sjokk og forhold som påvirker alle enheter i samme tidsperiode."),
    ("Faste effekter", "Toveis faste effekter", "En modell som inkluderer både enhetsfaste og tidsfaste effekter."),
    ("Faste effekter", "Within-variasjon", "Endring innen samme enhet over tid; variasjonen som identifiserer koeffisienter i en enhets-fast-effekt-modell."),
]

FLASHCARDS += [
    ("Kausalitet", "Direkte effekt", "Den delen av effekten fra X til Y som ikke går gjennom en mellomliggende mediator."),
    ("Kausalitet", "Indirekte effekt", "Den delen av effekten fra X til Y som går gjennom en mediator."),
    ("Kausalitet", "Total effekt", "Summen av den direkte og den indirekte effekten av X på Y."),
    ("Forskningsdesign", "Eksperimentell behandling", "Påvirkningen eller intervensjonen som forskeren tilfeldig tildeler enkelte enheter."),
    ("Forskningsdesign", "Kontrollgruppe", "Gruppen som ikke mottar behandlingen og brukes som sammenligningsgrunnlag."),
    ("Forskningsdesign", "Kvasi-eksperiment", "Et design som utnytter en behandlingslignende variasjon uten full tilfeldig tilordning."),
    ("Data", "Enhet", "Typen objekter analysen handler om, for eksempel personer, land eller valg."),
    ("Data", "Observasjon", "Én konkret registrert enhet i datasettet, for eksempel én person eller ett land-år."),
    ("Data", "Variabelverdi", "Den registrerte verdien en bestemt observasjon har på en bestemt variabel."),
    ("Data", "Tverrsnittsdata", "Data om mange enheter observert på ett tidspunkt eller i én kort periode."),
    ("Data", "Tidsseriedata", "Data om én enhet observert på flere tidspunkter."),
    ("Data", "Paneldata", "Data om flere enheter observert gjentatte ganger over tid."),
    ("Måling", "Konseptualisering", "Å avklare og definere hva et abstrakt begrep betyr."),
    ("Måling", "Tilfeldig målefeil", "Målefeil uten fast retning som tilfører støy, senker reliabiliteten og ofte svekker presisjonen."),
    ("Måling", "Systematisk målefeil", "Målefeil som trekker målingen i en bestemt retning og kan skape skjevhet."),
    ("Måling", "Objektiv indikator", "Et mål basert på registrerte forhold eller hendelser, som inntekt eller valgdeltakelse."),
    ("Måling", "Subjektiv indikator", "Et mål basert på menneskers vurderinger, oppfatninger eller selvrapportering."),
    ("Deskriptiv statistikk", "Typetall", "Verdien eller kategorien som forekommer oftest i datasettet."),
    ("Deskriptiv statistikk", "Variasjonsbredde", "Forskjellen mellom den høyeste og laveste observerte verdien."),
    ("Visualisering", "Histogram", "En graf som viser fordelingen til en kontinuerlig variabel ved hjelp av intervaller."),
    ("Visualisering", "Søylediagram", "En graf som sammenligner størrelsen på atskilte kategorier."),
    ("Visualisering", "Spredningsdiagram", "En graf som viser sammenhengen mellom to kontinuerlige variabler som punkter."),
    ("Visualisering", "Linjediagram", "En graf som særlig egner seg til å vise utvikling over tid."),
    ("Visualisering", "Data-to-ink-ratio", "Andelen av grafens visuelle elementer som faktisk formidler relevant informasjon."),
    ("Visualisering", "Logaritmisk skala", "En skala der like avstander representerer like relative eller proporsjonale endringer."),
    ("Statistisk inferens", "Sentralgrenseteoremet", "Ved tilstrekkelig store tilfeldige utvalg blir utvalgsfordelingen til mange estimater omtrent normal."),
    ("Statistisk inferens", "Testverdi", "Et standardisert mål på hvor langt estimatet ligger fra verdien nullhypotesen spesifiserer."),
    ("Statistisk inferens", "Kritisk verdi", "Terskelen testverdien må passere for at nullhypotesen skal forkastes ved valgt signifikansnivå."),
    ("Statistisk inferens", "Frihetsgrader", "Antallet uavhengige informasjonsbiter som er tilgjengelige når en størrelse estimeres."),
    ("Statistisk inferens", "Substansiell signifikans", "Om størrelsen på en effekt er viktig eller meningsfull i praksis."),
    ("Bivariat analyse", "Prosentdifferanse", "Forskjellen mellom prosentandeler i grupper, ofte brukt i krysstabeller."),
    ("Bivariat analyse", "Kovarians", "Et ustandardisert mål på hvordan to variabler varierer sammen."),
    ("Regresjon", "Justert R²", "Et mål på forklart variasjon som justerer for antall forklaringsvariabler og kan synke når en ny variabel bidrar lite."),
    ("Regresjon", "Standardisert koeffisient", "En koeffisient tolket i standardavvik, nyttig for å sammenligne effekter målt på ulike skalaer."),
    ("Regresjon", "Referansekategori", "Den utelatte kategorien som de inkluderte dummykoeffisientene sammenlignes med."),
    ("Regresjon", "Dummyvariabelfellen", "Perfekt multikollinearitet som oppstår når alle kategoridummyer og et konstantledd inkluderes."),
    ("Regresjon", "Lineær sannsynlighetsmodell", "En OLS-modell med en binær 0/1-avhengig variabel, der koeffisienter tolkes som endring i sannsynlighet."),
    ("Regresjon", "VIF", "Et mål på hvor mye multikollinearitet blåser opp variansen til en regresjonskoeffisient."),
    ("Regresjon", "Leverage", "Et mål på hvor uvanlig en observasjons kombinasjon av X-verdier er."),
    ("Regresjon", "Cook's distance", "Et samlet mål på hvor mye én observasjon påvirker regresjonsresultatet."),
    ("Regresjon", "Klyngerobuste standardfeil", "Standardfeil beregnet slik at residualer kan være korrelert innen definerte grupper."),
    ("Regresjon", "BLUE", "Under Gauss-Markov-forutsetningene er OLS den beste lineære forventningsrette estimatoren; dette alene beviser ikke kausalitet."),
    ("Faste effekter", "Between-variasjon", "Forskjeller mellom enheter, i motsetning til endring innen samme enhet over tid."),
]

FLASHCARDS += [
    ("Formler og regning", "T-verdi", "Testverdi i mange regresjons-/gjennomsnittstester: estimat delt på standardfeil."),
    ("Formler og regning", "Omtrent 95 % konfidensintervall", "En nyttig tommelfingerregel er estimat ± 2 × standardfeil."),
    ("Formler og regning", "Kjikvadrat-frihetsgrader", "For en krysstabell er frihetsgradene (antall rader - 1) × (antall kolonner - 1)."),
    ("Formler og regning", "Residualformelen", "Residual = observert Y - predikert Y, altså Y - Ŷ."),
    ("Formler og regning", "Predikert verdi i enkel regresjon", "I modellen Y = α + βX er predikert Y lik konstantleddet pluss koeffisienten ganger X."),
    ("Formler og regning", "Prosentpoeng", "Den absolutte forskjellen mellom to prosentandeler, for eksempel 36 % - 30 % = 6 prosentpoeng."),
    ("Formler og regning", "Relativ prosentvis endring", "Endring delt på startverdien, for eksempel 6 / 30 = 20 prosent."),
    ("Formler og regning", "Forventet treff ved gjetting", "Med fem svaralternativer er forventet treffrate 1 av 5, altså 20 prosent."),
]

TERM_DEFINITIONS = {term: definition for _, term, definition in FLASHCARDS}
DEFINITION_TERMS = {definition: term for _, term, definition in FLASHCARDS}


EXTRA_QUESTIONS = [
    {
        "topic": "Kausalitet og forskningsdesign",
        "question": "Hva er den totale effekten av X på Y?",
        "choices": ["Bare den direkte effekten.", "Bare den indirekte effekten.", "Summen av direkte og indirekte effekt.", "Korrelasjonen mellom X og Y."],
        "correctIndex": 2,
        "explanation": "Total effekt omfatter både direkte og indirekte kausale veier fra X til Y.",
    },
    {
        "topic": "Kausalitet og forskningsdesign",
        "question": "Hva skiller først og fremst et kvasi-eksperiment fra et ekte eksperiment?",
        "choices": ["Kvasi-eksperimenter har aldri en sammenligningsgruppe.", "Kvasi-eksperimenter mangler vanligvis full tilfeldig tilordning.", "Kvasi-eksperimenter kan ikke brukes på politikk.", "Kvasi-eksperimenter bruker bare kvalitative data."],
        "correctIndex": 1,
        "explanation": "Kvasi-eksperimenter utnytter behandlingslignende variasjon uten full random assignment.",
    },
    {
        "topic": "Kausalitet og forskningsdesign",
        "question": "Hva er kontrollgruppens viktigste funksjon i et eksperiment?",
        "choices": ["Å garantere ekstern validitet.", "Å vise det kontrafaktiske utfallet så godt som mulig.", "Å øke reliabiliteten til måleinstrumentet.", "Å sikre at alle mottar behandling."],
        "correctIndex": 1,
        "explanation": "Kontrollgruppen gir et sammenligningsgrunnlag for hva som ville skjedd uten behandlingen.",
    },
    {
        "topic": "Kausalitet og forskningsdesign",
        "question": "Hva er en indirekte effekt?",
        "choices": ["Effekten av X på Y som går gjennom en mediator.", "Effekten av Y på X.", "En effekt som ikke kan måles.", "Forskjellen mellom to standardfeil."],
        "correctIndex": 0,
        "explanation": "En indirekte effekt går fra X via en mellomliggende variabel til Y.",
    },
    {
        "topic": "Kausalitet og forskningsdesign",
        "question": "Hvorfor kan en stor korrelasjon fortsatt være spuriøs?",
        "choices": ["Fordi korrelasjoner alltid er tilfeldige.", "Fordi en tredje variabel kan påvirke både X og Y.", "Fordi store korrelasjoner mangler retning.", "Fordi korrelasjon bare kan brukes på kategorier."],
        "correctIndex": 1,
        "explanation": "En sterk sammenheng kan skyldes en felles bakenforliggende årsak.",
    },
    {
        "topic": "Data og måling",
        "question": "Hva kjennetegner paneldata?",
        "choices": ["Én enhet observert én gang.", "Mange enheter observert bare på ett tidspunkt.", "Flere enheter observert gjentatte ganger over tid.", "Bare data fra eksperimenter."],
        "correctIndex": 2,
        "explanation": "Paneldata kombinerer enhets- og tidsdimensjonen.",
    },
    {
        "topic": "Data og måling",
        "question": "Hva er tidsseriedata?",
        "choices": ["Én enhet observert på flere tidspunkter.", "Mange enheter observert én gang.", "Tilfeldig tildeling over tid.", "En krysstabell med tidsvariabler."],
        "correctIndex": 0,
        "explanation": "En tidsserie følger én enhet eller aggregert størrelse over tid.",
    },
    {
        "topic": "Data og måling",
        "question": "Hva er tverrsnittsdata?",
        "choices": ["Gjentatte observasjoner av én enhet.", "Observasjoner av flere enheter på ett tidspunkt eller i en kort periode.", "Data uten variabler.", "Bare kvalitative intervjuer."],
        "correctIndex": 1,
        "explanation": "Tverrsnittsdata sammenligner enheter på omtrent samme tidspunkt.",
    },
    {
        "topic": "Data og måling",
        "question": "Hva er forskjellen mellom en enhet og en observasjon?",
        "choices": ["Det er alltid det samme.", "Enheten er typen objekt, mens observasjonen er ett konkret registrert tilfelle.", "Observasjonen er en variabel, enheten er en verdi.", "Enheten er alltid et land."],
        "correctIndex": 1,
        "explanation": "Enheten beskriver hva slags objekter analysen gjelder; observasjonen er ett registrert tilfelle.",
    },
    {
        "topic": "Data og måling",
        "question": "Hva gjør forskeren under konseptualisering?",
        "choices": ["Å beregne en p-verdi.", "Å definere og avklare et abstrakt begrep.", "Å velge antall observasjoner.", "Å lage en regresjonstabell."],
        "correctIndex": 1,
        "explanation": "Konseptualisering avklarer hva et begrep betyr før det operasjonaliseres.",
    },
    {
        "topic": "Data og måling",
        "question": "Hva er en vanlig konsekvens av tilfeldig målefeil?",
        "choices": ["Målingen trekkes alltid oppover.", "Målingen blir mer støyete og reliabiliteten lavere.", "Kausalitet blir garantert.", "Utvalget blir representativt."],
        "correctIndex": 1,
        "explanation": "Tilfeldig målefeil har ingen fast retning, men gjør målingen mindre stabil og ofte mindre presis.",
    },
    {
        "topic": "Data og måling",
        "question": "Hva kjennetegner systematisk målefeil?",
        "choices": ["Feilen varierer tilfeldig rundt null.", "Feilen trekker målingen i en bestemt retning.", "Feilen forsvinner alltid i store utvalg.", "Feilen påvirker bare grafens farger."],
        "correctIndex": 1,
        "explanation": "Systematisk målefeil kan skape varig skjevhet i målingen.",
    },
    {
        "topic": "Data og måling",
        "question": "Hvilket er best eksempel på en subjektiv indikator?",
        "choices": ["Registrert valgdeltakelse.", "Offisiell arbeidsledighetsrate.", "Selvrapportert tilfredshet med demokratiet.", "Antall stortingsrepresentanter."],
        "correctIndex": 2,
        "explanation": "Subjektive indikatorer bygger på menneskers vurderinger eller oppfatninger.",
    },
    {
        "topic": "Deskriptiv statistikk og visualisering",
        "question": "Hva er typetallet?",
        "choices": ["Den midterste verdien.", "Verdien som forekommer oftest.", "Forskjellen mellom maksimum og minimum.", "Gjennomsnittlig avvik."],
        "correctIndex": 1,
        "explanation": "Typetallet er den hyppigst observerte verdien eller kategorien.",
    },
    {
        "topic": "Deskriptiv statistikk og visualisering",
        "question": "Hva er variasjonsbredden?",
        "choices": ["Maksimum minus minimum.", "Tredje kvartil minus første kvartil.", "Gjennomsnitt minus median.", "Variansen delt på N."],
        "correctIndex": 0,
        "explanation": "Variasjonsbredden er avstanden mellom største og minste verdi.",
    },
    {
        "topic": "Deskriptiv statistikk og visualisering",
        "question": "Hvilken graf passer best for å vise fordelingen til en kontinuerlig variabel?",
        "choices": ["Histogram.", "Kakediagram.", "Krysstabell.", "Kart uten tegnforklaring."],
        "correctIndex": 0,
        "explanation": "Histogrammer viser hvor mange kontinuerlige observasjoner som faller i ulike intervaller.",
    },
    {
        "topic": "Deskriptiv statistikk og visualisering",
        "question": "Hvilken graf passer best for å undersøke en lineær sammenheng mellom to kontinuerlige variabler?",
        "choices": ["Søylediagram.", "Spredningsdiagram.", "Histogram.", "Kakediagram."],
        "correctIndex": 1,
        "explanation": "Et spredningsdiagram viser parvise X- og Y-verdier som punkter.",
    },
    {
        "topic": "Deskriptiv statistikk og visualisering",
        "question": "Hvilken graf passer vanligvis best for utvikling over tid?",
        "choices": ["Linjediagram.", "Kakediagram.", "Boksplott uten tidsakse.", "Frekvenstabell uten årstall."],
        "correctIndex": 0,
        "explanation": "Linjediagrammer gjør tidsutvikling og endringer mellom perioder tydelige.",
    },
    {
        "topic": "Deskriptiv statistikk og visualisering",
        "question": "Når er et søylediagram særlig egnet?",
        "choices": ["Når atskilte kategorier skal sammenlignes.", "Når to kontinuerlige variabler skal korreleres.", "Når en regresjon skal estimeres.", "Når residualer skal klynges."],
        "correctIndex": 0,
        "explanation": "Søylediagrammer sammenligner størrelser mellom diskrete kategorier.",
    },
    {
        "topic": "Deskriptiv statistikk og visualisering",
        "question": "Hva betyr høy data-to-ink-ratio?",
        "choices": ["Grafen har mange dekorasjoner.", "Mye av det visuelle uttrykket formidler relevant data.", "Alle datapunktene har samme farge.", "Grafen bruker bare prosent."],
        "correctIndex": 1,
        "explanation": "En høy data-to-ink-ratio innebærer lite unødvendig visuelt støy.",
    },
    {
        "topic": "Statistisk inferens",
        "question": "Hva gjelder sentralgrenseteoremet først og fremst?",
        "choices": ["At alle rådata blir normalfordelte.", "At utvalgsfordelingen til mange estimater blir omtrent normal ved store tilfeldige utvalg.", "At alle store utvalg er representative.", "At standardfeilen blir null."],
        "correctIndex": 1,
        "explanation": "Teoremet handler om estimatorens utvalgsfordeling, ikke nødvendigvis rådataene.",
    },
    {
        "topic": "Statistisk inferens",
        "question": "Hva er en testverdi?",
        "choices": ["Et mål på avstanden mellom estimatet og nullhypotesens verdi, relativt til usikkerheten.", "Sannsynligheten for at H0 er sann.", "Antall observasjoner.", "Den største verdien i datasettet."],
        "correctIndex": 0,
        "explanation": "Testverdien standardiserer avstanden fra nullhypotesen ved hjelp av standardfeilen.",
    },
    {
        "topic": "Statistisk inferens",
        "question": "Hva er en kritisk verdi?",
        "choices": ["Terskelen en testverdi må passere for å forkaste H0.", "Den sanne populasjonsparameteren.", "Gjennomsnittet i kontrollgruppen.", "En tilfeldig uteligger."],
        "correctIndex": 0,
        "explanation": "Den kritiske verdien avgrenser forkastningsområdet ved valgt signifikansnivå.",
    },
    {
        "topic": "Statistisk inferens",
        "question": "Hva uttrykker frihetsgrader?",
        "choices": ["Antallet uavhengige informasjonsbiter tilgjengelig for estimering.", "Sannsynligheten for type I-feil.", "Antallet riktige hypoteser.", "Størrelsen på en kausal effekt."],
        "correctIndex": 0,
        "explanation": "Frihetsgrader beskriver hvor mye uavhengig informasjon som gjenstår etter estimerte begrensninger.",
    },
    {
        "topic": "Statistisk inferens",
        "question": "Hva er substansiell signifikans?",
        "choices": ["Om effekten er stor eller viktig i praksis.", "Om p-verdien er under 0,05.", "Om utvalget er tilfeldig.", "Om målingen er reliabel."],
        "correctIndex": 0,
        "explanation": "Substansiell signifikans handler om praktisk eller teoretisk betydning, ikke bare statistisk usikkerhet.",
    },
    {
        "topic": "Statistisk inferens",
        "question": "En svært liten effekt er statistisk signifikant i et enormt utvalg. Hva er den beste vurderingen?",
        "choices": ["Effekten er nødvendigvis viktig.", "Effekten kan være presist estimert, men substantielt ubetydelig.", "Effekten er nødvendigvis kausal.", "Nullhypotesen er sann."],
        "correctIndex": 1,
        "explanation": "Store utvalg kan gjøre svært små, praktisk uviktige effekter statistisk signifikante.",
    },
    {
        "topic": "Statistisk inferens",
        "question": "Hva øker vanligvis statistisk styrke?",
        "choices": ["Større utvalg og sterkere reell effekt.", "Mer systematisk målefeil.", "Lavere reliabilitet.", "Flere irrelevante kontrollvariabler."],
        "correctIndex": 0,
        "explanation": "Større utvalg og større effekter gjør det lettere å oppdage en reell sammenheng.",
    },
    {
        "topic": "Bivariat analyse",
        "question": "Hva er en prosentdifferanse?",
        "choices": ["Forskjellen mellom prosentandeler i to grupper.", "En relativ prosentvis endring fra én verdi til en annen.", "Forskjellen mellom to standardavvik.", "En korrelasjonskoeffisient."],
        "correctIndex": 0,
        "explanation": "I tabellanalyse sammenlignes grupper ofte ved å trekke én prosentandel fra en annen.",
    },
    {
        "topic": "Bivariat analyse",
        "question": "Hvorfor er korrelasjon lettere å sammenligne enn kovarians?",
        "choices": ["Korrelasjon er standardisert til intervallet -1 til 1.", "Korrelasjon beviser kausalitet.", "Kovarians kan ikke være negativ.", "Korrelasjon krever ikke variasjon."],
        "correctIndex": 0,
        "explanation": "Korrelasjon standardiserer kovariansen og er derfor uavhengig av variablenes måleenheter.",
    },
    {
        "topic": "Bivariat analyse",
        "question": "Hva kan en positiv kovarians fortelle?",
        "choices": ["Variablene tenderer til å øke sammen.", "X forårsaker Y.", "Sammenhengen er statistisk signifikant.", "Variablene har identiske gjennomsnitt."],
        "correctIndex": 0,
        "explanation": "Positiv kovarians viser at høye verdier på én variabel tenderer til å opptre med høye verdier på den andre.",
    },
    {
        "topic": "Regresjon og modellspesifikasjon",
        "question": "Hvorfor brukes justert R²?",
        "choices": ["Det justerer R² for modellens kompleksitet og kan synke når nye variabler bidrar lite.", "Det beviser kausalitet.", "Det blir alltid større enn R².", "Det fjerner heteroskedastisitet."],
        "correctIndex": 0,
        "explanation": "Justert R² tar hensyn til antallet forklaringsvariabler og belønner ikke enhver ny variabel automatisk.",
    },
    {
        "topic": "Regresjon og modellspesifikasjon",
        "question": "Hva er en fordel med standardiserte koeffisienter?",
        "choices": ["De kan gjøre effekter målt på ulike skalaer lettere å sammenligne.", "De garanterer korrekt modellspesifikasjon.", "De fjerner målefeil.", "De kan bare være positive."],
        "correctIndex": 0,
        "explanation": "Standardiserte koeffisienter uttrykkes i standardavvik og kan sammenlignes på tvers av skalaer.",
    },
    {
        "topic": "Regresjon og modellspesifikasjon",
        "question": "Hva viser en dummykoeffisient i en regresjon?",
        "choices": ["Forskjellen i forventet Y fra referansekategorien, alt annet likt.", "Gjennomsnittet til alle kategorier.", "Korrelasjonen mellom alle X-er.", "Antallet kategorier."],
        "correctIndex": 0,
        "explanation": "Dummykoeffisienten sammenligner kategorien med den utelatte referansekategorien.",
    },
    {
        "topic": "Regresjon og modellspesifikasjon",
        "question": "Hva er dummyvariabelfellen?",
        "choices": ["Perfekt multikollinearitet når alle kategoridummyer og konstantleddet inkluderes.", "At en dummy bare kan ha verdien 1.", "At referansekategorien alltid har flest observasjoner.", "At Y må være kontinuerlig."],
        "correctIndex": 0,
        "explanation": "Alle k dummyer summerer til konstantleddet og skaper en eksakt lineær sammenheng.",
    },
    {
        "topic": "Regresjon og modellspesifikasjon",
        "question": "Hva er et problem med en lineær sannsynlighetsmodell?",
        "choices": ["Den kan gi predikerte sannsynligheter under 0 eller over 1.", "Koeffisientene kan ikke tolkes.", "Den kan ikke ha dummyvariabler som X.", "Den krever at Y er kontinuerlig."],
        "correctIndex": 0,
        "explanation": "OLS-linjen er ikke begrenset til sannsynlighetsintervallet fra 0 til 1.",
    },
    {
        "topic": "Regresjon og modellspesifikasjon",
        "question": "Hvordan tolkes en koeffisient på 0,08 i en lineær sannsynlighetsmodell?",
        "choices": ["Åtte prosentpoeng høyere forventet sannsynlighet ved én enhets økning i X.", "Åtte prosent høyere R².", "Sannsynligheten er alltid 8 prosent.", "Standardfeilen er 0,08."],
        "correctIndex": 0,
        "explanation": "Når Y er 0/1, tolkes OLS-koeffisienten som en endring i sannsynlighet uttrykt som andel eller prosentpoeng.",
    },
    {
        "topic": "Regresjon og modellspesifikasjon",
        "question": "Hva måler VIF?",
        "choices": ["Hvor mye multikollinearitet øker variansen til en koeffisient.", "Hvor mye Y varierer.", "Hvor kausal modellen er.", "Hvor mange uteliggere modellen har."],
        "correctIndex": 0,
        "explanation": "VIF viser hvor mye lite unik X-variasjon blåser opp koeffisientens varians.",
    },
    {
        "topic": "Regresjon og modellspesifikasjon",
        "question": "Hva kjennetegner en observasjon med høy leverage?",
        "choices": ["Den har en uvanlig kombinasjon av X-verdier.", "Den har nødvendigvis den største residualen.", "Den har alltid Y = 0.", "Den er statistisk signifikant."],
        "correctIndex": 0,
        "explanation": "Leverage handler om hvor langt observasjonen ligger fra de andre i X-rommet.",
    },
    {
        "topic": "Regresjon og modellspesifikasjon",
        "question": "Hva brukes Cook's distance til?",
        "choices": ["Å vurdere hvor mye én observasjon påvirker regresjonsmodellen.", "Å beregne gjennomsnittet.", "Å velge referansekategori.", "Å teste reliabilitet."],
        "correctIndex": 0,
        "explanation": "Cook's distance kombinerer informasjon om residual og leverage for å vurdere innflytelse.",
    },
    {
        "topic": "Regresjon og modellspesifikasjon",
        "question": "Hva kan klyngerobuste standardfeil håndtere?",
        "choices": ["At residualer er korrelert innen grupper.", "At X og Y er reversert.", "At en konfunder er utelatt.", "At begrepsvaliditeten er svak."],
        "correctIndex": 0,
        "explanation": "Klyngerobuste standardfeil tillater avhengighet mellom observasjoner innen samme klynge.",
    },
    {
        "topic": "Regresjon og modellspesifikasjon",
        "question": "Hva betyr at OLS er BLUE under Gauss-Markov-forutsetningene?",
        "choices": ["OLS er den beste lineære forventningsrette estimatoren i den aktuelle klassen.", "OLS er alltid kausal.", "OLS har alltid høyest R².", "OLS krever blå grafer."],
        "correctIndex": 0,
        "explanation": "BLUE betyr best linear unbiased estimator, der best viser til lavest varians blant lineære forventningsrette estimatorer.",
    },
    {
        "topic": "Regresjon og modellspesifikasjon",
        "question": "Hva reparerer robuste standardfeil ikke?",
        "choices": ["Utelatt variabelskjevhet.", "Feil usikkerhetsberegning ved heteroskedastisitet.", "Noen former for varierende residualvarians.", "Standardfeilenes robusthet."],
        "correctIndex": 0,
        "explanation": "Robuste standardfeil endrer usikkerhetsberegningen, ikke en skjev koeffisient fra feil kausalmodell.",
    },
    {
        "topic": "Regresjon og modellspesifikasjon",
        "question": "Hva er en mulig konsekvens av høy multikollinearitet?",
        "choices": ["Store standardfeil og ustabile koeffisienter.", "Automatisk kausal identifikasjon.", "Alle residualer blir null.", "R² blir nødvendigvis null."],
        "correctIndex": 0,
        "explanation": "Når X-er inneholder lite unik informasjon, blir separate koeffisienter vanskeligere å estimere presist.",
    },
    {
        "topic": "Faste effekter",
        "question": "Hva er between-variasjon?",
        "choices": ["Forskjeller mellom enheter.", "Endring innen samme enhet over tid.", "Bare tilfeldig målefeil.", "Forskjellen mellom residual og predikert verdi."],
        "correctIndex": 0,
        "explanation": "Between-variasjon viser hvordan enheter skiller seg fra hverandre.",
    },
    {
        "topic": "Faste effekter",
        "question": "Hvorfor kan en tidsinvariant variabel normalt ikke estimeres separat med enhetsfaste effekter?",
        "choices": ["Den har ingen within-variasjon.", "Den har for høy standardfeil.", "Den er alltid en mediator.", "Den har nødvendigvis målefeil."],
        "correctIndex": 0,
        "explanation": "Enhetsfaste effekter identifiserer koeffisienter fra endring innen enheten, og en konstant variabel endrer seg ikke.",
    },
    {
        "topic": "Faste effekter",
        "question": "Hvorfor brukes ofte klyngerobuste standardfeil med paneldata?",
        "choices": ["Residualer kan være korrelert innen samme enhet over tid.", "Alle paneldata er randomiserte.", "Faste effekter skaper alltid målefeil.", "For å estimere tidsinvariante variabler."],
        "correctIndex": 0,
        "explanation": "Gjentatte observasjoner fra samme enhet kan ha avhengige residualer.",
    },
    {
        "topic": "Faste effekter",
        "question": "Hva er en viktig begrensning ved enhetsfaste effekter?",
        "choices": ["De kontrollerer ikke automatisk for tidsvarierende konfundere.", "De kan ikke brukes på paneldata.", "De kontrollerer ikke for stabile enhetsforskjeller.", "De krever alltid random assignment."],
        "correctIndex": 0,
        "explanation": "Faste effekter fjerner stabile forhold, men tidsvarierende alternative forklaringer kan fortsatt skape skjevhet.",
    },
    {
        "topic": "Faste effekter",
        "question": "Hva er formålet med tidsfaste effekter?",
        "choices": ["Å kontrollere for felles sjokk i hver tidsperiode.", "Å kontrollere for alle stabile forskjeller mellom enheter.", "Å fjerne alle residualer.", "Å estimere bare mellom-enhetsforskjeller."],
        "correctIndex": 0,
        "explanation": "Tidsfaste effekter absorberer forhold som påvirker alle enheter i samme periode.",
    },
    {
        "topic": "Faste effekter",
        "question": "Hvilken sammenligning dominerer i en modell med enhetsfaste effekter?",
        "choices": ["Samme enhet sammenlignes med seg selv over tid.", "Ulike enheter sammenlignes bare én gang.", "Behandlingsgruppen sammenlignes alltid med en randomisert kontrollgruppe.", "Bare gjennomsnitt sammenlignes."],
        "correctIndex": 0,
        "explanation": "Enhetsfaste effekter bruker within-variasjon og sammenligner enheten med seg selv.",
    },
    {
        "topic": "Regresjon og modellspesifikasjon",
        "question": "Hvorfor kan en forsker logaritmetransformere en sterkt høyreskjev variabel?",
        "choices": ["For å komprimere store verdier og gjøre relative forskjeller lettere å modellere.", "For å gjøre alle verdier negative.", "For å garantere statistisk signifikans.", "For å fjerne behovet for et konstantledd."],
        "correctIndex": 0,
        "explanation": "Logaritmen komprimerer store verdier og kan gjøre proporsjonale sammenhenger mer lineære og lettere å tolke.",
    },
]

FORMULA_QUESTIONS = [
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "En koeffisient er 6 og standardfeilen er 3. Hva er t-verdien?",
        "choices": ["0,5.", "2.", "3.", "6.", "18."],
        "correctIndex": 1,
        "explanation": "T-verdien er estimat delt på standardfeil: 6 / 3 = 2.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "En koeffisient er -4 og standardfeilen er 2. Hva er t-verdien?",
        "choices": ["-8.", "-2.", "0.", "2.", "8."],
        "correctIndex": 1,
        "explanation": "T-verdien er -4 / 2 = -2.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "Et estimat er 12 og standardfeilen er 2. Hva er et omtrent 95-prosent konfidensintervall?",
        "choices": ["[10; 14].", "[8; 16].", "[6; 18].", "[0; 24].", "[11; 13]."],
        "correctIndex": 1,
        "explanation": "Bruk omtrent estimat ± 2 × SE: 12 ± 4 gir [8; 16].",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "Et estimat er 5 og standardfeilen er 1. Hvilket intervall er nærmest et 95-prosent konfidensintervall?",
        "choices": ["[4; 6].", "[3; 7].", "[1; 9].", "[0; 10].", "[5; 6]."],
        "correctIndex": 1,
        "explanation": "Omtrent 95-prosent KI er 5 ± 2 × 1, altså rundt [3; 7].",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "Et parti går fra 30 prosent til 36 prosent. Hva er økningen i prosentpoeng?",
        "choices": ["3 prosentpoeng.", "6 prosentpoeng.", "12 prosentpoeng.", "20 prosentpoeng.", "36 prosentpoeng."],
        "correctIndex": 1,
        "explanation": "Prosentpoeng er absolutt forskjell mellom prosentandeler: 36 - 30 = 6.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "Et parti går fra 30 prosent til 36 prosent. Hva er den relative prosentvise økningen?",
        "choices": ["6 prosent.", "12 prosent.", "20 prosent.", "30 prosent.", "36 prosent."],
        "correctIndex": 2,
        "explanation": "Relativ økning er 6 / 30 = 0,20, altså 20 prosent.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "En krysstabell har 2 rader og 5 kolonner. Hvor mange frihetsgrader har kjikvadrattesten?",
        "choices": ["2.", "4.", "5.", "7.", "10."],
        "correctIndex": 1,
        "explanation": "Frihetsgrader er (rader - 1) × (kolonner - 1): 1 × 4 = 4.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "En krysstabell har 4 rader og 3 kolonner. Hvor mange frihetsgrader har kjikvadrattesten?",
        "choices": ["3.", "4.", "6.", "7.", "12."],
        "correctIndex": 2,
        "explanation": "Frihetsgrader er (4 - 1) × (3 - 1) = 3 × 2 = 6.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "I modellen Y = 10 + 3X, hva er predikert Y når X = 4?",
        "choices": ["12.", "13.", "14.", "22.", "40."],
        "correctIndex": 3,
        "explanation": "Predikert Y er 10 + 3 × 4 = 22.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "I modellen Y = 2 + 5X, hva er predikert Y når X = 3?",
        "choices": ["8.", "10.", "15.", "17.", "25."],
        "correctIndex": 3,
        "explanation": "Predikert Y er 2 + 5 × 3 = 17.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "En observasjon har Y = 20 og predikert Y = 17. Hva er residualen?",
        "choices": ["-3.", "3.", "17.", "20.", "37."],
        "correctIndex": 1,
        "explanation": "Residualen er observert Y minus predikert Y: 20 - 17 = 3.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "En observasjon har Y = 9 og predikert Y = 12. Hva er residualen?",
        "choices": ["-3.", "3.", "9.", "12.", "21."],
        "correctIndex": 0,
        "explanation": "Residualen er Y - Ŷ: 9 - 12 = -3.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "Hvis R² = 0,25, hva betyr det i en vanlig regresjonsmodell?",
        "choices": ["Modellen forklarer 25 prosent av variasjonen i Y.", "Effekten er 25 prosent kausal.", "P-verdien er 0,25.", "25 prosent av observasjonene er feil.", "Standardfeilen er 0,25."],
        "correctIndex": 0,
        "explanation": "R² er andelen variasjon i Y som modellen forklarer.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "En lineær sannsynlighetsmodell gir koeffisienten 0,12. Hvordan tolkes dette enklest?",
        "choices": ["12 prosentpoeng høyere sannsynlighet.", "12 prosent høyere R².", "12 flere observasjoner.", "0,12 i standardfeil.", "12 prosent lavere standardavvik."],
        "correctIndex": 0,
        "explanation": "Med binær Y tolkes 0,12 som 12 prosentpoeng endring i sannsynlighet.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "Hvis en kategorisk variabel har 6 kategorier, hvor mange dummyvariabler inkluderes vanligvis med konstantledd?",
        "choices": ["4.", "5.", "6.", "7.", "12."],
        "correctIndex": 1,
        "explanation": "Med konstantledd inkluderes vanligvis k - 1 dummyer, altså 5.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "Hvis en kategorisk variabel har 3 kategorier, hvor mange dummyvariabler inkluderes vanligvis med konstantledd?",
        "choices": ["1.", "2.", "3.", "4.", "6."],
        "correctIndex": 1,
        "explanation": "Med konstantledd brukes k - 1 dummyer, altså 2.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "Du svarer riktig på 28 av 70 spørsmål. Hvor stor andel riktig er dette omtrent?",
        "choices": ["20 prosent.", "30 prosent.", "40 prosent.", "50 prosent.", "70 prosent."],
        "correctIndex": 2,
        "explanation": "28 av 70 er 0,40, altså 40 prosent.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "Ved tilfeldig gjetting på 70 spørsmål med fem alternativer, hvor mange riktige forventes omtrent?",
        "choices": ["5.", "10.", "14.", "25.", "35."],
        "correctIndex": 2,
        "explanation": "Med fem alternativer er forventet treffrate 1/5. 70 / 5 = 14.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "En koeffisient er 2 og standardfeilen er 4. Hva antyder t-verdien?",
        "choices": ["T-verdien er 0,5, altså langt fra omtrent 2.", "T-verdien er 2, altså klart signifikant.", "T-verdien er 4, altså perfekt kausalitet.", "T-verdien er 8, altså høy R².", "T-verdien kan ikke beregnes."],
        "correctIndex": 0,
        "explanation": "T-verdien er 2 / 4 = 0,5, som normalt ikke er nær en vanlig 5-prosentgrense.",
    },
    {
        "topic": "Formler og regning uten kalkulator",
        "question": "En koeffisient er 9 og standardfeilen er 3. Hva antyder t-verdien?",
        "choices": ["T-verdien er 0,33.", "T-verdien er 3, altså relativt langt fra null.", "T-verdien er 6.", "T-verdien er 12.", "T-verdien er lik R²."],
        "correctIndex": 1,
        "explanation": "T-verdien er 9 / 3 = 3, som er relativt stor i absoluttverdi.",
    },
]

SPECIFIC_FIFTH_CHOICES = {
    1: "Den må bygge på en moralsk vurdering.",
    2: "En hypotese er alltid bredere enn en teori.",
    3: "Den må være formulert slik at alle mulige funn støtter den.",
    4: "Utvalget består av 500 respondenter.",
    5: "Bare den opprinnelige forskeren skal forstå framgangsmåten.",
    6: "At teorien må inkludere alle tenkelige variabler.",
    7: "Variabelen som antas å påvirke utfallet.",
    8: "Analyse av samme variabel på to ulike tidspunkt.",
    9: "En grafisk presentasjon uten observasjoner.",
    10: "Fordi data alltid er feil og derfor bør ignoreres.",
    11: "X kommer før Y i tid.",
    12: "En sammenligning der årsaksvariabelen måles etter utfallet.",
    13: "Et mål på hvor presist en koeffisient er estimert.",
    14: "En avhengig variabel som aldri påvirkes av X.",
    15: "X og Y varierer ikke i datasettet.",
    16: "At årsaken kommer før virkningen, slik teorien forventer.",
    17: "En årsak som øker sannsynligheten, men ikke må være til stede.",
    18: "En årsak som må være til stede, men ikke alene er nok.",
    19: "X endrer måleenheten til Y uten å påvirke sannsynligheten.",
    20: "Muligheten til å generalisere til hele populasjonen.",
    21: "Intern validitet gjennom balanse mellom behandlingsgrupper.",
    22: "Fordi forskeren kan plassere de mest like personene i samme gruppe.",
    23: "En studie der forskeren manipulerer X med full tilfeldig tilordning.",
    24: "At forskeren alltid har for få observasjoner.",
    25: "At bare én variabel kan variere i hele datasettet.",
    26: "Å oversette et mål til en teoretisk forklaring.",
    27: "Å formulere en normativ vurdering av begrepet.",
    28: "At målet gir identiske tall ved hver måling.",
    29: "At målet nødvendigvis fanger det riktige begrepet.",
    30: "En vekt viser tilfeldige tall fra gang til gang.",
    31: "Om målet gir samme verdi ved gjentatte målinger.",
    32: "At avvikene går tilfeldig i begge retninger rundt sann verdi.",
    33: "Standardavvik.",
    34: "9.",
    35: "7.",
    36: "Gjennomsnittets plassering på skalaen.",
    37: "Varians delt på standardavvik.",
    38: "Minimum og maksimum alene.",
    39: "Verdiene har like store avstander og absolutt nullpunkt.",
    40: "Verdiene består av uordnede kategorier.",
    41: "Forholdstallsnivå kan rangeres, intervallnivå kan ikke.",
    42: "En variabel som bare kan brukes som avhengig variabel.",
    43: "Alle år for ett land samlet i én verdi.",
    44: "Linjediagram.",
    45: "Histogram.",
    46: "Søylediagram.",
    47: "Like avstander viser like p-verdier.",
    48: "At grafen har høy oppløsning og mange farger.",
    49: "Grafen blir automatisk mer representativ.",
    50: "Gjennomsnitt, standardfeil og t-verdi alene.",
    51: "En enkelt observasjon med ekstrem verdi.",
    52: "Hele universet av relevante enheter.",
    53: "Å beskrive en normativ teori uten data.",
    54: "En verdi beregnet fra utvalget.",
    55: "En konstant som alltid er kjent før datainnsamling.",
    56: "At kontrollvariabler fjerner all skjevhet i store utvalg.",
    57: "Hvor mye enkeltobservasjonene varierer rundt gjennomsnittet.",
    58: "Den påvirkes ikke av utvalgsstørrelsen.",
    59: "At forskningshypotesen alltid er sann.",
    60: "At 3 prosent av observasjonene er feilklassifisert.",
    61: "Når standardfeilen er større enn koeffisienten.",
    62: "Å forkaste en falsk nullhypotese.",
    63: "Å godta en sann nullhypotese.",
    64: "At 95 prosent av utvalgsverdiene ligger innenfor intervallet.",
    65: "4.",
    66: "[4; 16].",
    67: "Intervallet viser at effekten må være større enn 1,4.",
    68: "Prosentpoeng brukes bare når tallet er over 100.",
    69: "5 prosent og 25 prosent.",
    70: "Den viser alltid om målingen har høy begrepsvaliditet.",
    71: "Histogram og standardavvik.",
    72: "Kjikvadrattest mellom gjennomsnitt.",
    73: "Krysstabell alene.",
    74: "Observerte gjennomsnitt med medianer i hver gruppe.",
    75: "3.",
    76: "R² må være lik 1.",
    77: "At alle punkter ligger på en perfekt stigende rett linje.",
    78: "En p-verdi for om to variabler er uavhengige.",
    79: "At Y forklares helt uten feilledd.",
    80: "13.",
    81: "Verdien av X når Y er null.",
    82: "Standardfeilen til residualene.",
    83: "Gjennomsnittet av X og Y.",
    84: "14.",
    85: "Minimerer summen av absolutte residualer.",
    86: "Hvor stor andel av X som skyldes målefeil.",
    87: "Endringen i Y når X øker og Z får endre seg fritt.",
    88: "Når Z påvirker X, men ikke Y.",
    89: "Forskeren kan automatisk fjerne alle konfunderende variabler.",
    90: "At to observasjoner har samme residual.",
    91: "At X og Z aldri kan inkluderes i samme modell.",
    92: "β₁ + β₂.",
    93: "At residualenes gjennomsnitt er høyere enn Y.",
    94: "At residualer garantert er uavhengige over tid.",
    95: "Feil koeffisient som skyldes utelatt variabel.",
    96: "At X må være uavhengig av alle kontrollvariabler.",
    97: "Kontrollerer for forskjeller som endrer seg ulikt over tid.",
    98: "Variasjon mellom enheter etter at tidstrender fjernes.",
    99: "Både robuste og klyngerobuste standardfeil.",
    100: "Landets faste geografiske størrelse.",
    101: "Gjennomsnittet av X og Y i samme modell.",
    102: "Kvasi-eksperimenter har alltid lavere reliabilitet i målingen.",
    103: "Å gjøre behandlingsgruppen større enn utvalget.",
    104: "Effekten som ikke går gjennom noen mellomliggende variabel.",
    105: "Fordi korrelasjonen alltid forsvinner i større utvalg.",
    106: "Målinger av én variabel uten informasjon om enheter.",
    107: "Mange land observert på ett tilfeldig valgt tidspunkt.",
    108: "Samme enhet observert gjennom mange år.",
    109: "Enheten er en målefeil, mens observasjonen er en parameter.",
    110: "Å bestemme regresjonskoeffisientens standardfeil.",
    111: "Målingen blir systematisk trukket i én bestemt retning.",
    112: "Feilen går tilfeldig opp og ned rundt sann verdi.",
    113: "Antall registrerte stemmer i en valgkrets.",
    114: "Summen av alle verdier delt på antall observasjoner.",
    115: "Gjennomsnittlig avstand til regresjonslinjen.",
    116: "Linjediagram over tid.",
    117: "Boksplott av én variabel.",
    118: "Spredningsdiagram uten tidsrekkefølge.",
    119: "Når en kontinuerlig variabel skal deles i intervaller.",
    120: "At grafen bør bruke mest mulig tredimensjonal pynt.",
    121: "At p-verdier blir identiske i alle utvalg.",
    122: "Den sanne verdien til parameteren i populasjonen.",
    123: "Den observerte verdien som alltid er lik p-verdien.",
    124: "Antallet observasjoner som er fjernet fordi de er uteliggere.",
    125: "Om resultatet er metodisk etterprøvbart.",
    126: "Effekten må være stor fordi p-verdien er liten.",
    127: "Mindre utvalg og mer tilfeldig målefeil.",
    128: "Forskjellen mellom to korrelasjonskoeffisienter.",
    129: "Korrelasjon bruker alltid flere observasjoner enn kovarians.",
    130: "At variablene nødvendigvis har samme måleenhet.",
    131: "Det gjør alle modeller sammenlignbare uansett avhengig variabel.",
    132: "De gjør standardfeilen uavhengig av utvalgsstørrelse.",
    133: "Forskjellen mellom to kontinuerlige X-verdier.",
    134: "At Y må kodes som én dummy for hver kategori.",
    135: "Den tvinger alle prediksjoner til å ligge mellom 0 og 1.",
    136: "Åtte prosent lavere sannsynlighet når X øker.",
    137: "Hvor mye en observasjon påvirker regresjonslinjen.",
    138: "Den har en uvanlig Y-verdi, uansett X-verdier.",
    139: "Å avgjøre om Y er ordinal eller nominal.",
    140: "At gruppene er tilfeldig trukket fra populasjonen.",
    141: "OLS har lavest skjevhet blant alle mulige estimatorer uansett modell.",
    142: "For lavt rapporterte standardfeil ved varierende residualvarians.",
    143: "At koeffisientene blir mer presise og stabile.",
    144: "Endring i en enhet fra år til år.",
    145: "Fordi den har perfekt korrelasjon med tidsfaste effekter.",
    146: "Fordi faste effekter alltid gjør koeffisientene kausale.",
    147: "De fjerner alle tidsvarierende forskjeller automatisk.",
    148: "Å kontrollere for stabile forskjeller mellom land.",
    149: "Ulike enheter sammenlignes på tvers av hele perioden.",
    150: "For å gjøre tolkningen mer avhengig av ekstreme verdier.",
}

FALLBACK_FIFTH_CHOICES = [
    "Alternativet blander deskriptiv statistikk og kausal identifikasjon.",
    "Alternativet forveksler målevaliditet med statistisk usikkerhet.",
    "Alternativet tolker en assosiasjon som en sikker årsak.",
    "Alternativet gjør en populasjonsparameter til en utvalgsobservasjon.",
    "Alternativet bytter om på forklaringsvariabel og utfallsvariabel.",
]


def ensure_five_choices(question: dict) -> dict:
    question = {**question, "choices": list(question["choices"])}
    if len(question["choices"]) > 5:
        raise ValueError(f"Question has too many choices: {question['question']}")
    if len(question["choices"]) == 5:
        return question
    candidates = []
    if question["id"] in SPECIFIC_FIFTH_CHOICES:
        candidates.append(SPECIFIC_FIFTH_CHOICES[question["id"]])
    candidates.extend(FALLBACK_FIFTH_CHOICES)
    for candidate in candidates:
        if candidate not in question["choices"]:
            question["choices"].append(candidate)
            return question
    raise ValueError(f"Could not add fifth choice to question {question['id']}")


def rebuilt_question(
    topic: str,
    prompt: str,
    correct: str,
    distractors: list[str],
    explanation: str,
) -> dict:
    if len(distractors) != 4:
        raise ValueError(f"Question needs exactly four distractors: {prompt}")
    choices = [correct, *distractors]
    if len(set(choices)) != 5:
        raise ValueError(f"Duplicate choices in question: {prompt}")
    return {
        "topic": topic,
        "question": prompt,
        "choices": choices,
        "correctIndex": 0,
        "explanation": explanation,
    }


def explain_choice(question: dict, choice: str, index: int) -> str:
    if choice in TERM_DEFINITIONS:
        return f"«{choice}» betyr: {TERM_DEFINITIONS[choice]}"
    if index == question["correctIndex"]:
        return question["explanation"]
    if question["topic"].startswith("Flashcards reversert:") and choice in DEFINITION_TERMS:
        return f"Denne definisjonen hører til «{DEFINITION_TERMS[choice]}». {question['explanation']}"
    if question["topic"] == "Formler og regning uten kalkulator" or question["topic"].startswith("Eksamensstil: regresjon"):
        return f"«{choice}» følger ikke modellen eller regningen i denne oppgaven. {question['explanation']}"
    if choice.endswith("."):
        return f"«{choice}» passer ikke her. {question['explanation']}"
    return f"«{choice}» er ikke riktig her. {question['explanation']}"


EXAMPLE_QUESTIONS = [
    rebuilt_question(
        "Eksempelspørsmål og regresjon",
        "Vi har en regresjonsmodell med samspillsledd der Y = a + b1X1 + b2X2 + b3(X1 × X2) + u. X1 varierer mellom 0 og 1. Hva blir den forkortede regresjonslinjen når X1 er 0?",
        "Y = a + b2X2 + u",
        ["Y = b2X2 + u", "Y = a + b1X1 + b3(X1 × X2) + u", "Y = a + u", "Y = a + b1X1 + b2X2 + u"],
        "Når X1 = 0 faller både b1X1 og b3(X1 × X2) bort, slik at modellen reduseres til Y = a + b2X2 + u.",
    ),
    rebuilt_question(
        "Eksempelspørsmål og inferens",
        "Hva innebærer det at et stigningstall er signifikant forskjellig fra null med et signifikansnivå på 5 prosent?",
        "Dersom vi trekker 100 utvalg fra populasjonen, vil stigningstallet være forskjellig fra null i ca. 95 av dem.",
        ["Vi er 5 prosent sikre på at stigningstallet er valid.", "Dersom vi trekker 100 utvalg fra populasjonen, vil stigningstallet være forskjellig fra null i ca. 5 av dem.", "At sammenhengen mellom X og Y med 95 prosent sikkerhet er stor.", "Vi er 95 prosent sikre på at stigningstallet er valid."],
        "Dette følger fasiten i eksempelspørsmålet: 5-prosentnivået knyttes til at resultatet regnes som statistisk tydelig i omtrent 95 av 100 gjentatte utvalg, ikke til validitet eller effektstørrelse.",
    ),
    rebuilt_question(
        "Eksempelspørsmål og regresjonsdiagnostikk",
        "Hva er en uteligger i en regresjonsanalyse?",
        "En observasjon som modellen predikerer svært dårlig.",
        ["En observasjon med spesielt lav validitet.", "En observasjon med mange missingverdier.", "En observasjon med spesielt høy validitet.", "En observasjon som overensstemmer med teorien."],
        "I regresjon handler en uteligger ofte om en observasjon med stor residual: observert Y ligger langt fra predikert Y.",
    ),
    rebuilt_question(
        "Eksempelspørsmål og visualisering",
        "Når er et kakediagram en nyttig måte å beskrive en variabel på?",
        "Når vi er interessert i relative størrelser.",
        ["Når vi er interessert i hvilken verdi som er vanligst.", "Når vi har mange mulige verdier.", "Når vi har mange observasjoner.", "Når vi skal vise usikkerheten i et estimat."],
        "Kakediagram kan brukes når få kategorier skal sammenlignes som andeler av en helhet.",
    ),
    rebuilt_question(
        "Eksempelspørsmål og regresjon",
        "Vi bruker notasjon a for konstantleddet. Hvordan tolkes konstantleddet a i en regresjonsmodell?",
        "Forventet verdi på Y når alle de uavhengige variablene har verdien 0.",
        ["Forventet verdi på Y når alle stigningstallene er 0.", "Forventet verdi på Y når R² er 0.", "Forventet verdi på X når alle de uavhengige variablene har verdien 0.", "Forventet verdi på R² når alle de uavhengige variablene har verdien 0."],
        "Konstantleddet er modellens predikerte Y-verdi når alle inkluderte X-er settes til null.",
    ),
    rebuilt_question(
        "Eksempelspørsmål og forskningsdesign",
        "Hva er det viktigste formålet med et forskningsdesign som baserer seg på observasjonsstudier og ønsker å avdekke en årsakssammenheng mellom X og Y?",
        "Å kontrollere for så mange bakenforliggende variabler som mulig og dermed redusere faren for forurensning utenfra.",
        ["Å være sikker på at utvalget representerer populasjonen.", "Å bevise med matematisk logikk at X fører til Y.", "Å gjennomgå eksisterende litteratur så grundig at man vet at ingen har gjort det samme tidligere.", "Å lage overbevisende deskriptiv statistikk av X og Y."],
        "I observasjonsstudier er hovedproblemet alternative forklaringer, særlig konfunderende variabler som påvirker både X og Y.",
    ),
    rebuilt_question(
        "Eksempelspørsmål og kausalitet",
        "Hvilket av de følgende punktene er ikke å regne som et kausalt hinder i empirisk forskning?",
        "Måler variablene det de forsøker å måle?",
        ["Har vi kontrollert for alle bakenforliggende variabler?", "Er det en troverdig kausalmekanisme som kobler X til Y?", "Er det samvariasjon mellom X og Y?", "Kan Y forårsake X?"],
        "Målespørsmålet handler om validitet. Det er viktig, men de klassiske kausale hindrene handler om samvariasjon, mekanisme, tidsrekkefølge/reversert kausalitet og konfunderende variabler.",
    ),
    rebuilt_question(
        "Eksempelspørsmål og måling",
        "At to uavhengige forskere bruker samme metode for å hente inn data og kommer fram til samme svar betyr at vi har høy ...",
        "Reliabilitet",
        ["Måloppnåelse", "R²", "Forklaringskraft", "Validitet"],
        "Reliabilitet handler om stabilitet og reproduserbarhet i målingen.",
    ),
    rebuilt_question(
        "Eksempelspørsmål og bivariat regresjon",
        "Hvilke av disse påstandene om bivariat regresjon er riktige?",
        "Alle alternativene er riktige.",
        ["En bivariat regresjonsmodell vil ofte ha mer heteroskedastisitet ettersom den har færre variabler.", "Når vi spesifiserer en bivariat regresjonsmodell, antar vi at effekten av en enhets økning i X alltid vil være like stor som regresjonskoeffisienten.", "Når vi spesifiserer en bivariat regresjonsmodell, måler vi sammenhengen mellom X og Y uten å kontrollere for noen variabler.", "Ingen av dem er riktige."],
        "Bivariat regresjon beskriver en ukontrollert lineær sammenheng mellom X og Y, og koeffisienten tolkes som konstant endring per enhet i X innen modellen.",
    ),
    rebuilt_question(
        "Eksempelspørsmål og inferens",
        "Hvilket av disse punktene gjør vi antakelser om når vi ønsker å bruke funn fra regresjonen til å si noe om populasjonen?",
        "Den stokastiske komponenten i populasjonen.",
        ["Sammenhengens styrke.", "Fordelingen på de uavhengige variablene.", "Regneprogrammets prosesseringskraft.", "Antall observasjoner i studien."],
        "Inferens krever antakelser om den stokastiske prosessen som har generert dataene, slik at utvalgsresultater kan knyttes til populasjonen.",
    ),
]


CURATED_EXAM_QUESTIONS = [
    rebuilt_question("Vitenskapelig metode", "Hva skiller best en teori fra en hypotese?", "En teori er en generell forklaring, mens en hypotese er en konkret testbar forventning.", ["En hypotese er alltid bredere enn en teori.", "En teori er alltid normativ, mens en hypotese er empirisk.", "En teori kan ikke testes indirekte.", "En hypotese trenger ikke å være falsifiserbar."], "Hypoteser utledes fra teorier og gjør dem empirisk testbare."),
    rebuilt_question("Vitenskapelig metode", "Hvilken påstand er empirisk snarere enn normativ?", "Valgdeltakelsen var høyere blant eldre enn blant yngre velgere.", ["Regjeringen bør senke skattene.", "Det er urettferdig at valgdeltakelsen varierer mellom grupper.", "Demokratiet bør alltid prioriteres over effektivitet.", "Partiene burde samarbeide mer."], "Empiriske påstander kan undersøkes med observasjoner; normative påstander uttrykker vurderinger."),
    rebuilt_question("Kausalitet", "Hva er den kontrafaktiske utfordringen i kausal analyse?", "Vi kan ikke observere samme enhet både med og uten behandling på samme tidspunkt.", ["Vi kan aldri observere noen enheter over tid.", "Vi kan ikke beregne gjennomsnitt i en kontrollgruppe.", "Vi kan ikke formulere hypoteser om årsaker.", "Vi kan bare undersøke normative påstander."], "Kausal effekt defineres relativt til et kontrafaktisk utfall som ikke kan observeres direkte."),
    rebuilt_question("Kausalitet", "Når er Z en konfunderende variabel i forholdet mellom X og Y?", "Når Z påvirker Y og samtidig er korrelert med X.", ["Når Z bare påvirker X, men ikke Y.", "Når Z er en konsekvens av Y.", "Når Z er en ren mediator mellom X og Y.", "Når Z bare er en annen måleenhet for Y."], "Utelatt variabelskjevhet krever at Z både er relevant for Y og samvarierer med X."),
    rebuilt_question("Kausalitet", "Hva er en mediator?", "En mellomliggende variabel som ligger på kausalveien fra X til Y.", ["En variabel som påvirker både X og Y før X oppstår.", "En variabel som bare måler tilfeldig støy.", "En kontrollgruppe i et eksperiment.", "En observasjon med høy leverage."], "Mediatorer formidler en del av effekten fra årsak til utfall."),
    rebuilt_question("Forskningsdesign", "Hva styrker random assignment først og fremst?", "Intern validitet.", ["Ekstern validitet gjennom representativitet.", "Begrepsvaliditet i målingen.", "At alle utvalg blir store.", "At standardfeilen alltid blir null."], "Tilfeldig tilordning gjør behandlings- og kontrollgruppe sammenlignbare i forventning."),
    rebuilt_question("Forskningsdesign", "Hva styrker random sampling først og fremst?", "Muligheten til å generalisere fra utvalget til populasjonen.", ["Sikkerheten for at X kommer før Y.", "At behandlingsgruppen og kontrollgruppen blir like.", "At alle målefeil forsvinner.", "At forskeren kan droppe teori."], "Tilfeldig trekking handler om representativitet, ikke behandlingstilordning."),
    rebuilt_question("Forskningsdesign", "Hva er hovedproblemet i observasjonelle studier av kausalitet?", "Forskeren kontrollerer vanligvis ikke hvem som får hvilken verdi på X.", ["Det finnes aldri variasjon i X.", "De kan ikke inneholde kontrollvariabler.", "De kan bare brukes til kakediagrammer.", "Alle observasjoner må være land-år."], "Uten randomisering blir alternative forklaringer vanskeligere å utelukke."),
    rebuilt_question("Forskningsdesign", "Hva kjennetegner et kvasi-eksperiment?", "En hendelse eller regel skaper behandlingslignende variasjon uten full random assignment.", ["Forskeren velger utfall etter at data er samlet inn.", "Alle variabler må være kvalitative.", "Studien mangler alltid sammenligningsgruppe.", "Det er bare et annet ord for tverrsnittsdata."], "Kvasi-eksperimenter forsøker å etterligne eksperimentell variasjon med institusjonelle eller naturlige kilder."),
    rebuilt_question("Forskningsdesign", "Hva er kontrollgruppens viktigste funksjon?", "Å gi et anslag på hva som ville skjedd uten behandling.", ["Å sikre at alle mottar behandling.", "Å gjøre utvalget representativt.", "Å fjerne behovet for hypotese.", "Å øke antall variabler i datasettet."], "Kontrollgruppen brukes som praktisk kontrafaktisk sammenligning."),
    rebuilt_question("Måling", "Hva er operasjonalisering?", "Å oversette et teoretisk begrep til en observerbar indikator.", ["Å forklare hvorfor X fører til Y.", "Å beregne p-verdien i en test.", "Å velge om grafen skal være grønn.", "Å forkaste nullhypotesen."], "Operasjonalisering handler om hvordan begreper måles i data."),
    rebuilt_question("Måling", "Hva er forskjellen på validitet og reliabilitet?", "Validitet handler om å måle riktig begrep; reliabilitet handler om stabil måling.", ["Validitet handler om utvalgsstørrelse; reliabilitet handler om R².", "Validitet er bare relevant i eksperimenter.", "Reliabilitet betyr at en effekt er kausal.", "Begrepene betyr det samme."], "Et mål kan være stabilt uten å måle riktig fenomen."),
    rebuilt_question("Måling", "Hva kjennetegner systematisk målefeil?", "Målingen trekkes i en bestemt retning.", ["Feilen varierer tilfeldig rundt null.", "Feilen forsvinner alltid i små utvalg.", "Feilen gjør målet mer reliabelt.", "Feilen er det samme som høy R²."], "Systematisk målefeil kan gi skjeve mål fordi avviket har retning."),
    rebuilt_question("Måling", "Hvilket målenivå har en variabel med kategorier som kan rangeres, men der avstanden mellom kategoriene ikke er kjent?", "Ordinalnivå.", ["Nominalnivå.", "Intervallnivå.", "Forholdstallsnivå.", "Residualnivå."], "Ordinalvariabler har rekkefølge, men ikke nødvendigvis like avstander."),
    rebuilt_question("Data", "Hva er en observasjon i et land-år-datasett?", "Ett bestemt land i ett bestemt år.", ["Alle land samlet for hele perioden.", "Én variabel som BNP.", "Bare navnet på landet.", "Gjennomsnittet av alle år."], "I land-år-data er hver rad typisk en kombinasjon av enhet og tidspunkt."),
    rebuilt_question("Data", "Hva kjennetegner paneldata?", "Flere enheter observeres gjentatte ganger over tid.", ["Én enhet observeres én gang.", "Mange enheter observeres bare på ett tidspunkt.", "Data uten variabler.", "Bare eksperimentelle data."], "Paneldata kombinerer tverrsnittsdimensjon og tidsdimensjon."),
    rebuilt_question("Deskriptiv statistikk", "Hvilke mål egner seg ofte for en sterkt høyreskjev fordeling?", "Median og interkvartilbredde.", ["Gjennomsnitt og standardavvik alene.", "P-verdi og t-verdi.", "Korrelasjon og kovarians.", "Konstantledd og R²."], "Median og IQR påvirkes mindre av ekstreme verdier enn gjennomsnitt og standardavvik."),
    rebuilt_question("Deskriptiv statistikk", "Hva viser et boksplott vanligvis?", "Median, kvartiler, spredning og mulige uteliggere.", ["Bare p-verdi og R².", "Bare sammenhengen mellom to kontinuerlige variabler.", "Bare antall kategorier.", "Bare kausalmekanismen."], "Boksplott oppsummerer fordelingen til én variabel."),
    rebuilt_question("Visualisering", "Hva er en risiko ved å kutte y-aksen i et søylediagram?", "Små forskjeller kan se større ut enn de er.", ["Alle forskjeller forsvinner.", "Variabelen blir automatisk ordinal.", "Utvalget blir mer representativt.", "Standardfeilen blir mindre."], "Avkortede akser kan overdrive visuelle forskjeller."),
    rebuilt_question("Visualisering", "Hva er en egenskap ved en logaritmisk skala?", "Like avstander viser like relative eller proporsjonale forskjeller.", ["Like avstander viser alltid like absolutte forskjeller.", "Null kan alltid plottes uten problemer.", "Den brukes bare for nominalvariabler.", "Den gjør alle effekter kausale."], "Log-skala komprimerer store verdier og fremhever relative endringer."),
    rebuilt_question("Statistisk inferens", "Hva sier sentralgrenseteoremet først og fremst?", "Utvalgsfordelingen til mange estimater blir omtrent normal ved store tilfeldige utvalg.", ["Alle rådata blir normalfordelte.", "Alle store utvalg er representative.", "Standardfeilen blir alltid null.", "Alle p-verdier blir signifikante."], "Teoremet handler om estimatorens utvalgsfordeling, ikke nødvendigvis rådataene."),
    rebuilt_question("Statistisk inferens", "Hva er korrekt tolkning av en p-verdi på 0,03?", "Gitt at nullhypotesen er sann, er sannsynligheten for et like ekstremt eller mer ekstremt resultat 3 prosent.", ["Det er 3 prosent sannsynlighet for at nullhypotesen er sann.", "Det er 97 prosent sannsynlighet for at forskningshypotesen er sann.", "Effekten forklarer 3 prosent av variasjonen.", "3 prosent av observasjonene er feil."], "P-verdien er betinget på nullhypotesen."),
    rebuilt_question("Statistisk inferens", "Hvordan tolkes et 95-prosent konfidensintervall i frekventistisk statistikk?", "Metoden vil dekke den sanne parameteren i omtrent 95 prosent av gjentatte utvalg.", ["Det er alltid 95 prosent sannsynlighet for at den konkrete parameteren flytter seg inn i intervallet.", "95 prosent av observasjonene ligger i intervallet.", "Nullhypotesen er 95 prosent sann.", "Effekten er 95 prosent kausal."], "Dekningsgraden gjelder metoden over hypotetiske gjentatte utvalg."),
    rebuilt_question("Statistisk inferens", "Hva er substansiell signifikans?", "Om effekten er stor eller viktig i praksis.", ["Om p-verdien er under 0,05.", "Om utvalget er tilfeldig trukket.", "Om målet er reliabelt.", "Om residualene summerer til null."], "Statistisk signifikans er ikke det samme som praktisk betydning."),
    rebuilt_question("Statistisk inferens", "Hva øker vanligvis statistisk styrke?", "Større utvalg og sterkere reell effekt.", ["Mer tilfeldig målefeil.", "Lavere reliabilitet.", "Færre observasjoner.", "Flere irrelevante kontrollvariabler."], "Styrke er sannsynligheten for å oppdage en reell effekt."),
    rebuilt_question("Bivariat analyse", "Hvilken analyse passer best når både X og Y er kategoriske?", "Krysstabell og kjikvadrattest.", ["Korrelasjon alene.", "T-test av to gjennomsnitt.", "Lineært samspill uten kategorier.", "Cook's distance."], "Krysstabeller viser kombinasjoner av kategorier, og kjikvadrat tester uavhengighet."),
    rebuilt_question("Bivariat analyse", "Hva betyr korrelasjonen r = 0?", "Det er ingen lineær samvariasjon.", ["Det finnes ingen mulig sammenheng.", "X forårsaker ikke Y med sikkerhet.", "Variablene har samme gjennomsnitt.", "R² må være 1."], "Pearsons r = 0 utelukker ikke alle ikke-lineære mønstre."),
    rebuilt_question("Bivariat analyse", "Hvorfor er korrelasjon lettere å sammenligne enn kovarians?", "Korrelasjon er standardisert til intervallet -1 til 1.", ["Korrelasjon beviser kausalitet.", "Kovarians kan aldri være negativ.", "Korrelasjon krever ikke variasjon.", "Kovarians er alltid en p-verdi."], "Korrelasjon skalerer kovariansen med variablenes standardavvik."),
    rebuilt_question("Regresjon", "Hva gjør OLS?", "Minimerer summen av kvadrerte residualer.", ["Minimerer summen av absolutte residualer.", "Maksimerer alle koeffisienter.", "Fjerner alle konfunderende variabler.", "Gjør Y normalfordelt."], "OLS velger linjen som gir lavest sum av kvadrerte feil."),
    rebuilt_question("Regresjon", "Hva viser R² i en vanlig regresjonsmodell?", "Andelen variasjon i Y som modellen forklarer.", ["Sannsynligheten for at modellen er kausal.", "Målingens reliabilitet.", "P-verdien til konstantleddet.", "Antall kontrollvariabler."], "R² handler om forklart variasjon, ikke kausalitet."),
    rebuilt_question("Regresjon", "Hva er en residual?", "Observert Y minus predikert Y.", ["Predikert Y minus X.", "Koeffisienten delt på standardfeilen.", "Variansen til X.", "R² minus p-verdien."], "Residualen er modellens prediksjonsfeil for en observasjon."),
    rebuilt_question("Regresjon", "Når oppstår utelatt variabelskjevhet?", "Når en utelatt variabel påvirker Y og er korrelert med X.", ["Når en irrelevant variabel ikke inkluderes.", "Når utvalget er stort.", "Når residualene summerer til null.", "Når X er en dummyvariabel."], "Den utelatte variabelen må både være relevant for utfallet og samvariere med forklaringsvariabelen."),
    rebuilt_question("Regresjon", "Hva kan skje hvis forskeren kontrollerer for en mediator mellom X og Y?", "En del av den totale effekten av X kan kontrolleres bort.", ["Alle konfunderende variabler fjernes automatisk.", "X og Y blir nødvendigvis kategoriske.", "R² må bli null.", "Standardfeilen blir alltid mindre."], "Kontroll for en mediator kan gjøre estimatet mer likt en direkte effekt enn en total effekt."),
    rebuilt_question("Regresjon", "Hva er perfekt multikollinearitet?", "En eksakt lineær sammenheng mellom forklaringsvariabler.", ["En svak korrelasjon mellom X og Y.", "At residualene har varierende varians.", "Et perfekt representativt utvalg.", "At R² er lav."], "Perfekt multikollinearitet gjør separate koeffisienter umulige å estimere."),
    rebuilt_question("Regresjon", "Hva er heteroskedastisitet?", "Residualenes varians er ikke konstant.", ["Residualenes gjennomsnitt er alltid positivt.", "Alle X-er er perfekt korrelert.", "Alle observasjoner har samme Y.", "Y må være binær."], "Heteroskedastisitet påvirker særlig usikkerhetsberegningen."),
    rebuilt_question("Regresjon", "Hva reparerer robuste standardfeil ikke?", "Utelatt variabelskjevhet.", ["Feil standardfeil ved heteroskedastisitet.", "Noen former for varierende residualvarians.", "Usikkerhetsberegning som er for optimistisk.", "At residualvariansen ikke er konstant."], "Robuste standardfeil endrer standardfeilene, ikke selve koeffisientens kausale tolkning."),
    rebuilt_question("Regresjon", "Hva kan klyngerobuste standardfeil håndtere?", "At residualer er korrelert innen grupper.", ["At Y forårsaker X.", "At en konfunder er utelatt.", "At begrepsvaliditeten er svak.", "At alle kategorier mangler referanseverdi."], "Klyngerobuste standardfeil tillater avhengighet innen klynger."),
    rebuilt_question("Regresjon", "Hva er et problem med en lineær sannsynlighetsmodell?", "Den kan gi predikerte sannsynligheter under 0 eller over 1.", ["Koeffisientene kan aldri tolkes.", "Den kan ikke bruke dummyvariabler som X.", "Den krever at Y er kontinuerlig.", "Den kan bare estimeres uten konstantledd."], "OLS-linjen er ikke begrenset til sannsynlighetsintervallet [0, 1]."),
    rebuilt_question("Regresjon", "Hva er dummyvariabelfellen?", "Perfekt multikollinearitet når alle kategoridummyer og konstantledd inkluderes samtidig.", ["At en dummy bare kan ha verdien 1.", "At referansekategorien alltid er størst.", "At Y må være kontinuerlig.", "At dummyvariabler ikke kan brukes i regresjon."], "Med konstantledd må én kategori utelates som referansekategori."),
    rebuilt_question("Regresjon", "Hva er en standardisert koeffisient nyttig for?", "Å sammenligne effekter målt på ulike skalaer.", ["Å garantere kausal identifikasjon.", "Å fjerne målefeil.", "Å gjøre p-verdien uavhengig av N.", "Å tvinge R² til å bli 1."], "Standardiserte koeffisienter uttrykker endringer i standardavvik."),
    rebuilt_question("Regresjon", "Hva kjennetegner en observasjon med høy leverage?", "Den har en uvanlig kombinasjon av X-verdier.", ["Den har nødvendigvis størst residual.", "Den har alltid Y = 0.", "Den er alltid statistisk signifikant.", "Den er alltid en målefeil."], "Leverage handler om plassering i X-rommet."),
    rebuilt_question("Regresjon", "Hva brukes Cook's distance til?", "Å vurdere hvor mye én observasjon påvirker regresjonsresultatet.", ["Å avgjøre om en variabel er nominal.", "Å beregne medianen.", "Å velge signifikansnivå.", "Å teste random sampling."], "Cook's distance kombinerer informasjon om residual og leverage."),
    rebuilt_question("Regresjon", "I modellen Y = a + b1X1 + b2X2 + b3(X1 × X2) + u, hva er effekten av X2 når X1 = 1?", "b2 + b3.", ["b1.", "b2.", "b3.", "a + b1."], "Med samspill avhenger effekten av X2 av X1; når X1 = 1 blir helningen b2 + b3."),
    rebuilt_question("Faste effekter", "Hva gjør enhetsfaste effekter?", "Kontrollerer for stabile kjennetegn ved hver enhet.", ["Kontrollerer automatisk for alle tidsvarierende konfundere.", "Sammenligner bare ulike enheter på ett tidspunkt.", "Gjør randomisering unødvendig.", "Fjerner alle residualer."], "Enhetsfaste effekter absorberer forhold som ikke endrer seg innen enheten."),
    rebuilt_question("Faste effekter", "Hva er within-variasjon?", "Endring innen samme enhet over tid.", ["Forskjeller mellom enheter.", "Bare tilfeldig målefeil.", "Forskjellen mellom Y og gjennomsnittet av X.", "Antall kategorier i en dummyvariabel."], "Faste effekter identifiserer effekter fra endringer innen enheten."),
    rebuilt_question("Faste effekter", "Hva er formålet med tidsfaste effekter?", "Å kontrollere for felles sjokk i hver tidsperiode.", ["Å kontrollere for stabile forskjeller mellom enheter.", "Å fjerne alle målefeil.", "Å estimere bare mellom-variasjon.", "Å gjøre alle X-er tidsinvariante."], "Tidsfaste effekter absorberer perioderelaterte forhold som rammer alle enheter."),
    rebuilt_question("Faste effekter", "Hvorfor kan en tidsinvariant variabel normalt ikke estimeres separat med enhetsfaste effekter?", "Den har ingen within-variasjon.", ["Den har alltid for lav reliabilitet.", "Den er alltid en mediator.", "Den har nødvendigvis høy p-verdi.", "Den er det samme som residualen."], "Enhetsfaste effekter bruker endring innen enheten; en konstant variabel endrer seg ikke."),
    rebuilt_question("Regresjon", "Hvorfor kan en forsker logaritmetransformere en sterkt høyreskjev variabel?", "For å komprimere store verdier og gjøre relative forskjeller lettere å modellere.", ["For å gjøre alle verdier negative.", "For å garantere statistisk signifikans.", "For å fjerne behovet for konstantledd.", "For å gjøre variabelen nominal."], "Log-transformasjon kan gjøre proporsjonale sammenhenger mer lineære og mindre dominert av ekstreme verdier."),
]


ADDITIONAL_EXAM_STYLE_QUESTIONS = [
    rebuilt_question("Eksamensstil: samspill og regresjon", "I modellen Y = a + b1X1 + b2X2 + b3(X1 × X2) + u, hva er effekten av X2 når X1 = 0?", "b2.", ["b1.", "b2 + b3.", "a + b2.", "b3."], "Når X1 = 0 blir samspillsleddet b3(X1 × X2) lik null, så helningen for X2 er b2."),
    rebuilt_question("Eksamensstil: samspill og regresjon", "I modellen Y = a + b1X1 + b2X2 + b3(X1 × X2) + u, hva er effekten av X1 når X2 = 1?", "b1 + b3.", ["b1.", "b2 + b3.", "a + b1.", "b3 alene."], "Når X2 = 1 består effekten av X1 av hovedleddet b1 og samspillsleddet b3."),
    rebuilt_question("Eksamensstil: regresjon og prediksjon", "I modellen Y = 10 + 4Kvinne + 2Alder, der Kvinne = 1 og Alder = 30. Hva er predikert Y?", "74.", ["60.", "70.", "44.", "16."], "Predikert verdi er 10 + 4 × 1 + 2 × 30 = 74."),
    rebuilt_question("Eksamensstil: regresjon og prediksjon", "I modellen Y = 5 + 3X - 2Z. Hva er predikert Y når X = 4 og Z = 1?", "15.", ["10.", "12.", "17.", "19."], "Sett inn verdiene: 5 + 3 × 4 - 2 × 1 = 15."),
    rebuilt_question("Eksamensstil: regresjon og residualer", "En observasjon har Y = 30 og modellen predikerer Ŷ = 24. Hva er residualen?", "6.", ["-6.", "24.", "30.", "54."], "Residualen er observert Y minus predikert Y: 30 - 24 = 6."),
    rebuilt_question("Eksamensstil: regresjon og residualer", "Hva betyr en positiv residual?", "Observert Y er høyere enn modellen predikerer.", ["Observert Y er lavere enn modellen predikerer.", "X har nødvendigvis positiv kausal effekt.", "Modellen har R² lik 1.", "P-verdien er under 0,05."], "Residual = Y - Ŷ. Positiv residual betyr at observasjonen ligger over regresjonslinjen."),
    rebuilt_question("Eksamensstil: signifikans", "En koeffisient er 3 og standardfeilen er 2. Hva er omtrent t-verdien, og hva antyder det ved vanlig 5-prosentnivå?", "t ≈ 1,5, som vanligvis ikke er nok til å forkaste nullhypotesen.", ["t ≈ 0,67, som alltid er signifikant.", "t ≈ 5, som viser perfekt kausalitet.", "t ≈ 6, som betyr at R² er høy.", "t kan ikke beregnes uten R-kode."], "t-verdien er 3 / 2 = 1,5, som er under den vanlige tommelfingergrensen rundt 2."),
    rebuilt_question("Eksamensstil: signifikans", "En p-verdi er 0,08. Hva er riktig konklusjon på 5-prosentnivå?", "Vi forkaster vanligvis ikke nullhypotesen.", ["Vi forkaster alltid nullhypotesen.", "Nullhypotesen er bevist sann.", "Effekten er nødvendigvis stor.", "Målingen er nødvendigvis invalid."], "0,08 er større enn 0,05, så resultatet regnes vanligvis ikke som statistisk signifikant på 5-prosentnivå."),
    rebuilt_question("Eksamensstil: signifikans", "Et 95-prosent konfidensintervall for en koeffisient er [0,2; 1,1]. Hva antyder dette ved en tosidig 5-prosenttest?", "Koeffisienten er statistisk signifikant forskjellig fra null.", ["Koeffisienten er ikke signifikant fordi intervallet er positivt.", "Nullhypotesen er bevist sann.", "Effekten er nødvendigvis kausal.", "Standardfeilen er null."], "Intervallet inneholder ikke null, derfor vil en tosidig 5-prosenttest normalt forkaste H0: β = 0."),
    rebuilt_question("Eksamensstil: signifikans", "Et 95-prosent konfidensintervall for en koeffisient er [-0,5; 0,9]. Hva er beste tolkning?", "Vi kan ikke forkaste at koeffisienten er null på 5-prosentnivå.", ["Koeffisienten er sikkert negativ.", "Koeffisienten er sikkert positiv.", "Effekten er bevist kausal.", "R² må være lavere enn null."], "Siden intervallet inneholder null, er koeffisienten ikke tydelig forskjellig fra null ved 5-prosentnivå."),
    rebuilt_question("Eksamensstil: hypotesetesting", "Hva er nullhypotesen vanligvis når vi tester en regresjonskoeffisient?", "At koeffisienten i populasjonen er lik null.", ["At koeffisienten i utvalget er størst mulig.", "At R² er lik én.", "At alle variabler er normalfordelte.", "At målingen er valid."], "Nullhypotesen er typisk ingen sammenheng eller effekt i populasjonen."),
    rebuilt_question("Eksamensstil: feilslutninger", "Hva er en type I-feil i hypotesetesting?", "Å forkaste en sann nullhypotese.", ["Å ikke forkaste en falsk nullhypotese.", "Å måle en variabel reliabelt.", "Å velge for få svaralternativer.", "Å få en høy R²."], "Type I-feil er falsk positiv: man finner effekt selv om nullhypotesen er sann."),
    rebuilt_question("Eksamensstil: feilslutninger", "Hva er en type II-feil i hypotesetesting?", "Å ikke forkaste en falsk nullhypotese.", ["Å forkaste en sann nullhypotese.", "Å bruke en kontrollgruppe.", "Å tolke en koeffisient som prosentpoeng.", "Å måle samme fenomen to ganger."], "Type II-feil er falsk negativ: man overser en reell effekt."),
    rebuilt_question("Eksamensstil: kausalitet", "Hvilken situasjon illustrerer reversert kausalitet?", "Forskeren hevder at politisk interesse øker nyhetsbruk, men nyhetsbruk kan også øke politisk interesse.", ["En tredje variabel påvirker både X og Y.", "X påvirker Y gjennom en mediator.", "Utvalget er tilfeldig trukket.", "Y er målt på ordinalnivå."], "Reversert kausalitet handler om at årsaksretningen kan gå motsatt vei av den forskeren legger til grunn."),
    rebuilt_question("Eksamensstil: kausalitet", "Hvilket eksempel passer best på en konfunderende variabel?", "Utdanning kan påvirke både politisk kunnskap og valgdeltakelse.", ["En mediator ligger alltid etter Y.", "Et kakediagram viser relative størrelser.", "En residual er positiv.", "En dummyvariabel har verdiene 0 og 1."], "En konfunder påvirker utfallet og samvarierer med forklaringsvariabelen."),
    rebuilt_question("Eksamensstil: kausalitet", "Hvorfor er kontroll for bakenforliggende variabler viktig i observasjonsstudier?", "Fordi slike variabler kan skape en spuriøs sammenheng mellom X og Y.", ["Fordi kontrollvariabler alltid øker kausal effekt.", "Fordi alle kontrollvariabler er mediatorer.", "Fordi random sampling ellers blir umulig.", "Fordi R² ellers ikke kan beregnes."], "Kontrollvariabler brukes for å redusere risikoen for konfunderende forklaringer."),
    rebuilt_question("Eksamensstil: kausalitet", "Hva kan være problemet med å kontrollere for en variabel som ligger mellom X og Y?", "Man kan kontrollere bort deler av effekten man egentlig vil estimere.", ["Man får alltid mer ekstern validitet.", "Man fjerner automatisk reversert kausalitet.", "Man gjør alle variabler nominale.", "Man gjør standardfeilen lik null."], "En mediator er del av kausalveien. Kontroll for den kan endre estimatet fra total effekt til direkte effekt."),
    rebuilt_question("Eksamensstil: kausalitet", "Hva er en spuriøs sammenheng?", "En tilsynelatende sammenheng mellom X og Y som skyldes en tredje variabel.", ["En sammenheng der X garantert forårsaker Y.", "En sammenheng med perfekt reliabilitet.", "En sammenheng som bare finnes i eksperimenter.", "En sammenheng der Y ikke varierer."], "Spuriøsitet oppstår når en bakenforliggende faktor skaper samvariasjonen."),
    rebuilt_question("Eksamensstil: forskningsdesign", "Hva er forskjellen mellom random sampling og random assignment?", "Random sampling handler om trekking fra populasjonen; random assignment handler om fordeling til behandling.", ["Begge betyr nøyaktig det samme.", "Random sampling gir intern validitet, random assignment gir bare større N.", "Random assignment brukes bare i observasjonsstudier.", "Random sampling fjerner alltid alle konfunderende variabler."], "Sampling handler om hvem som er med; assignment handler om hvem som får hvilken behandling."),
    rebuilt_question("Eksamensstil: forskningsdesign", "Hva er sterkest grunn til at et eksperiment ofte har høy intern validitet?", "Behandling tildeles tilfeldig, slik at gruppene blir sammenlignbare i forventning.", ["Utvalget er alltid representativt for populasjonen.", "Alle variabler måles uten feil.", "Forskerne trenger ikke teori.", "R² blir alltid høy."], "Random assignment reduserer systematiske forskjeller mellom behandlings- og kontrollgruppe."),
    rebuilt_question("Eksamensstil: forskningsdesign", "Hvorfor kan et eksperiment likevel ha begrenset ekstern validitet?", "Fordi deltakerne eller situasjonen ikke nødvendigvis representerer andre populasjoner eller kontekster.", ["Fordi random assignment alltid skaper målefeil.", "Fordi eksperimenter ikke kan ha kontrollgruppe.", "Fordi p-verdier ikke kan beregnes.", "Fordi alle eksperimenter mangler intern validitet."], "Intern validitet og generaliserbarhet er ulike vurderinger."),
    rebuilt_question("Eksamensstil: forskningsdesign", "Hva er poenget med en kontrollgruppe?", "Å gi et sammenligningsgrunnlag for hva som ville skjedd uten behandling.", ["Å sikre at alle får behandling.", "Å gjøre behandlingen sterkere.", "Å fjerne behovet for data.", "Å gjøre utvalget mindre."], "Kontrollgruppen fungerer som et praktisk anslag på det kontrafaktiske utfallet."),
    rebuilt_question("Eksamensstil: måling", "Et mål gir nesten samme verdi hver gang, men måler feil fenomen. Hvordan beskrives dette best?", "Høy reliabilitet, lav validitet.", ["Lav reliabilitet, høy validitet.", "Høy validitet og høy reliabilitet.", "Lav reliabilitet og lav kausalitet.", "Høy R², lav standardfeil."], "Stabil måling er reliabilitet; riktig begrepsmåling er validitet."),
    rebuilt_question("Eksamensstil: måling", "Hvis en survey om politisk kunnskap systematisk undervurderer kunnskapen til én gruppe, hva er dette et eksempel på?", "Systematisk målefeil.", ["Tilfeldig målefeil.", "Random assignment.", "Høy ekstern validitet.", "Klyngerobuste standardfeil."], "Systematisk målefeil trekker målingen i en bestemt retning for noen eller alle observasjoner."),
    rebuilt_question("Eksamensstil: måling", "Hva er en vanlig konsekvens av tilfeldig målefeil i en forklaringsvariabel?", "Mer støy og ofte svakere/presisjonsmessig dårligere estimater.", ["Sikrere kausal identifikasjon.", "Perfekt multikollinearitet.", "At alle p-verdier blir null.", "At utvalget blir representativt."], "Tilfeldig målefeil gjør målingen mindre presis og kan svekke observerte sammenhenger."),
    rebuilt_question("Eksamensstil: data", "Hva er forskjellen mellom en enhet og en variabel?", "Enheten er objektet vi observerer; variabelen er egenskapen vi måler ved objektet.", ["Enheten er alltid tallet 1, variabelen er alltid tallet 0.", "En variabel er en type utvalg.", "Enheten er alltid en p-verdi.", "Det finnes ingen forskjell."], "Eksempel: person er enhet, alder er variabel."),
    rebuilt_question("Eksamensstil: data", "Hva kjennetegner tverrsnittsdata?", "Flere enheter observert på ett tidspunkt eller i en kort periode.", ["Én enhet observert over lang tid.", "Flere enheter observert gjentatte ganger over tid.", "Data uten observasjoner.", "Bare eksperimentelle behandlingsdata."], "Tverrsnitt sammenligner enheter omtrent samtidig."),
    rebuilt_question("Eksamensstil: data", "Hva kjennetegner tidsseriedata?", "Én enhet eller aggregert størrelse observert over flere tidspunkter.", ["Mange enheter observert bare én gang.", "Flere land-år uten tidsrekkefølge.", "Bare kategoriske variabler.", "Bare data fra surveyeksperimenter."], "Tidsserier følger utvikling over tid for én enhet eller én aggregert serie."),
    rebuilt_question("Eksamensstil: visualisering", "Hvilken graf passer best for én kontinuerlig variabels fordeling?", "Histogram.", ["Spredningsdiagram.", "Linjediagram.", "Krysstabell.", "Samspillsplot uten X-akse."], "Histogrammer viser frekvensfordelingen til en kontinuerlig variabel."),
    rebuilt_question("Eksamensstil: visualisering", "Hvilken graf passer best for sammenhengen mellom to kontinuerlige variabler?", "Spredningsdiagram.", ["Kakediagram.", "Histogram av én variabel.", "Frekvenstabell uten grupper.", "Søylediagram uten kategorier."], "Spredningsdiagrammer viser parvise X- og Y-verdier."),
    rebuilt_question("Eksamensstil: visualisering", "Hvilken graf passer best for utvikling i arbeidsledighet fra år til år?", "Linjediagram.", ["Kakediagram.", "Boksplott uten tid.", "Krysstabell uten år.", "Histogram av partivalg."], "Linjediagrammer egner seg godt til ordnede tidspunkter."),
    rebuilt_question("Eksamensstil: visualisering", "Når er et søylediagram særlig egnet?", "Når atskilte kategorier skal sammenlignes.", ["Når to kontinuerlige variabler skal korreleres.", "Når residualer skal klynges.", "Når en p-verdi skal regnes ut.", "Når alle data er tidsserier."], "Søylediagrammer sammenligner størrelser mellom diskrete kategorier."),
    rebuilt_question("Eksamensstil: deskriptiv statistikk", "Hvorfor er medianen ofte nyttig ved høyreskjeve fordelinger?", "Den påvirkes mindre av ekstreme høye verdier enn gjennomsnittet.", ["Den bruker alltid flere observasjoner enn gjennomsnittet.", "Den er det samme som standardavviket.", "Den viser kausal effekt.", "Den krever at variabelen er nominal."], "Medianen er robust mot uteliggere og skjeve haler."),
    rebuilt_question("Eksamensstil: deskriptiv statistikk", "Hva beskriver standardavviket?", "Typisk spredning rundt gjennomsnittet.", ["Usikkerheten rundt nullhypotesen alene.", "Andelen forklart variasjon.", "Forskjellen mellom to prosentandeler.", "Antallet kontrollvariabler."], "Standardavvik er et mål på variasjon i observasjonene."),
    rebuilt_question("Eksamensstil: bivariat analyse", "Hva tester en kjikvadrattest i en krysstabell?", "Om de observerte cellefrekvensene avviker fra det vi ville forventet ved uavhengighet.", ["Om to gjennomsnitt er like.", "Om en regresjonskoeffisient er standardisert.", "Om residualer er normalfordelte.", "Om X kommer før Y i tid."], "Kjikvadrattesten sammenligner observerte og forventede frekvenser."),
    rebuilt_question("Eksamensstil: bivariat analyse", "Hva betyr en positiv korrelasjon?", "Høye verdier på én variabel tenderer til å opptre sammen med høye verdier på den andre.", ["X forårsaker alltid Y.", "Sammenhengen er alltid statistisk signifikant.", "Variablene har identiske gjennomsnitt.", "Målingen er alltid valid."], "Korrelasjon beskriver lineær samvariasjon, ikke alene kausalitet."),
    rebuilt_question("Eksamensstil: regresjon", "Hva betyr en regresjonskoeffisient i multippel regresjon?", "Forventet endring i Y ved én enhets økning i X, når andre inkluderte variabler holdes konstant.", ["Forskjellen mellom maksimum og minimum i Y.", "Sannsynligheten for at H0 er sann.", "Andelen av X som modellen forklarer.", "Antall observasjoner i datasettet."], "Multippel regresjon gir en ceteris-paribus-tolkning innen modellen."),
    rebuilt_question("Eksamensstil: regresjon", "Hva betyr det at en koeffisient er kontrollert for Z?", "Sammenhengen mellom X og Y estimeres for en gitt verdi av Z i modellen.", ["Z er fjernet fra datasettet.", "Z kan ikke være korrelert med X.", "X blir automatisk randomisert.", "Y blir gjort om til en dummy."], "Kontroll betyr at modellen holder den inkluderte variabelen konstant når X-koeffisienten tolkes."),
    rebuilt_question("Eksamensstil: regresjon", "Hva er en mulig konsekvens av høy multikollinearitet?", "Store standardfeil og ustabile enkeltkoeffisienter.", ["Perfekt kausal identifikasjon.", "Alle residualer blir null.", "R² blir nødvendigvis negativ.", "Målingen blir mer valid."], "Når forklaringsvariabler overlapper mye, blir det vanskeligere å skille deres separate bidrag."),
    rebuilt_question("Eksamensstil: regresjon", "Hva måler VIF?", "Hvor mye multikollinearitet øker variansen til en koeffisient.", ["Hvor mye én observasjon påvirker regresjonslinjen.", "Hvor stor andel av Y som er forklart.", "Hvor mange kategorier en dummy har.", "Hvor ofte nullhypotesen er sann."], "VIF står for variance inflation factor."),
    rebuilt_question("Eksamensstil: regresjon", "Hva betyr en dummykoeffisient når modellen har et konstantledd og en referansekategori?", "Forskjellen i forventet Y mellom dummyens kategori og referansekategorien, alt annet likt.", ["Gjennomsnittet til alle kategorier samlet.", "At kategorien alltid har verdien 1.", "At Y må være binær.", "At variabelen ikke kan tolkes."], "Dummykoeffisienter sammenligner med den utelatte referansekategorien."),
    rebuilt_question("Eksamensstil: regresjon", "Hva betyr en koeffisient på 0,12 i en lineær sannsynlighetsmodell?", "12 prosentpoeng høyere forventet sannsynlighet.", ["12 prosent høyere R².", "12 flere observasjoner.", "0,12 i standardfeil.", "12 prosent lavere standardavvik."], "Når Y er 0/1, tolkes OLS-koeffisienten som endring i sannsynlighet målt i andeler/prosentpoeng."),
    rebuilt_question("Eksamensstil: regresjon", "Hva er problemet hvis en lineær sannsynlighetsmodell predikerer 1,08?", "Prediksjonen ligger utenfor mulig sannsynlighetsområde.", ["Prediksjonen er automatisk mer reliabel.", "Koeffisienten må være null.", "Utvalget er nødvendigvis representativt.", "R² er negativ."], "Sannsynligheter skal ligge mellom 0 og 1, men OLS kan predikere utenfor dette intervallet."),
    rebuilt_question("Eksamensstil: faste effekter", "Hva kontrollerer enhetsfaste effekter for?", "Alle stabile kjennetegn ved enhetene, observerte og uobserverte.", ["Alle tidsvarierende konfundere automatisk.", "Bare tilfeldige målefeil.", "Alle p-verdier over 0,05.", "Kun forskjeller mellom år."], "Enhetsfaste effekter fjerner tidsinvariante forskjeller mellom enhetene."),
    rebuilt_question("Eksamensstil: faste effekter", "Hva kontrollerer tidsfaste effekter for?", "Felles sjokk eller forhold som påvirker alle enheter i samme periode.", ["Stabile forskjeller mellom enheter.", "Alle individuelle trender automatisk.", "Bare målefeil i Y.", "Alle uteliggere."], "Tidsfaste effekter absorberer periodeeffekter som er felles for alle enheter."),
    rebuilt_question("Eksamensstil: faste effekter", "Hva er en begrensning ved enhetsfaste effekter?", "De kontrollerer ikke automatisk for tidsvarierende konfunderende variabler.", ["De kan ikke brukes med paneldata.", "De kontrollerer ikke for stabile enhetsforskjeller.", "De gjør alltid standardfeilen null.", "De krever at Y er nominal."], "Faste effekter fjerner stabile forskjeller, men ikke nødvendigvis alt som endrer seg over tid."),
    rebuilt_question("Eksamensstil: faste effekter", "Hvorfor brukes ofte klyngerobuste standardfeil i paneldata?", "Fordi residualer kan være korrelert innen samme enhet over tid.", ["Fordi faste effekter alltid gjør data uavhengige.", "Fordi alle paneldata er randomiserte.", "Fordi tidsinvariante variabler ellers får koeffisient.", "Fordi R² ellers ikke kan beregnes."], "Gjentatte observasjoner av samme enhet kan gi avhengige feil innen klynger."),
    rebuilt_question("Eksamensstil: inferens", "Hva skjer vanligvis med standardfeilen når antall observasjoner øker, alt annet likt?", "Den blir mindre.", ["Den blir større.", "Den blir negativ.", "Den blir lik koeffisienten.", "Den påvirkes aldri av N."], "Større utvalg gir vanligvis mer presise estimater."),
    rebuilt_question("Eksamensstil: inferens", "Hva er forskjellen mellom statistisk og substansiell signifikans?", "Statistisk signifikans handler om usikkerhet; substansiell signifikans handler om praktisk betydning.", ["Begrepene betyr det samme.", "Substansiell signifikans betyr alltid p < 0,05.", "Statistisk signifikans beviser alltid kausalitet.", "Statistisk signifikans handler bare om målevaliditet."], "Et funn kan være statistisk tydelig, men lite viktig i praksis."),
    rebuilt_question("Eksamensstil: inferens", "Hva er den beste grunnen til å være forsiktig med en svært liten effekt som er signifikant i et enormt utvalg?", "Effekten kan være presist estimert, men praktisk ubetydelig.", ["Effekten må være kausal.", "Nullhypotesen er bevist sann.", "Målingen er alltid invalid.", "R² må være 1."], "Store utvalg kan gjøre små effekter statistisk signifikante."),
    rebuilt_question("Eksamensstil: populasjon og generalisering", "Hva må vi særlig vurdere før vi generaliserer fra et utvalg til en populasjon?", "Hvordan utvalget er trukket og hvilken populasjon det skal representere.", ["Om konstantleddet er positivt.", "Om alle variabler har navn på engelsk.", "Om R² er over 0,5.", "Om det finnes et kakediagram."], "Generalisering avhenger av utvalgsdesign og målpopulasjon."),
    rebuilt_question("Eksamensstil: populasjon og generalisering", "Hva betyr den stokastiske komponenten i en regresjonsmodell?", "Den delen av Y som modellen ikke forklarer systematisk med X-variablene.", ["At X alltid er tilfeldig tilordnet.", "At alle koeffisienter er null.", "At data ikke kan analyseres.", "At utvalget alltid er representativt."], "Feilleddet representerer usystematiske eller utelatte forhold i modellen."),
]


PRIORITY_EXAM_DRILL_QUESTIONS = [
    rebuilt_question("Eksamensdrill: regresjon og regning", "I modellen Y = 8 + 3X. Hva er predikert Y når X = 6?", "26.", ["18.", "21.", "24.", "32."], "Predikert verdi finnes ved å sette inn X: 8 + 3 × 6 = 26."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "I modellen Y = 12 - 2X + 5Z. Hva er predikert Y når X = 3 og Z = 2?", "16.", ["6.", "10.", "20.", "28."], "Predikert verdi er 12 - 2 × 3 + 5 × 2 = 16."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "En modell predikerer Ŷ = 41, men observert Y er 35. Hva er residualen?", "-6.", ["6.", "35.", "41.", "76."], "Residualen er Y - Ŷ, altså 35 - 41 = -6."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "En koeffisient er -6 og standardfeilen er 3. Hva er t-verdien?", "-2.", ["2.", "-0,5.", "0,5.", "-18."], "t-verdien er koeffisient delt på standardfeil: -6 / 3 = -2."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "En koeffisient er 1,2 og standardfeilen er 0,3. Hva er t-verdien?", "4.", ["0,25.", "1,5.", "2,4.", "3."], "t-verdien er 1,2 / 0,3 = 4."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "Et estimat er 10 og standardfeilen er 2. Hva er et omtrent 95-prosent konfidensintervall?", "[6; 14].", ["[8; 12].", "[4; 16].", "[10; 12].", "[2; 20]."], "Tommelfingerregelen er estimat ± 2 × standardfeil: 10 ± 4."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "Et estimat er -3 og standardfeilen er 1. Hva er et omtrent 95-prosent konfidensintervall?", "[-5; -1].", ["[-4; -2].", "[-3; 1].", "[-1; 5].", "[1; 5]."], "Bruk estimat ± 2 × standardfeil: -3 ± 2 gir [-5; -1]."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "Hva betyr en koeffisient på -0,08 i en lineær sannsynlighetsmodell?", "8 prosentpoeng lavere forventet sannsynlighet.", ["8 prosent lavere R².", "0,08 færre observasjoner.", "80 prosentpoeng høyere sannsynlighet.", "At Y ikke kan være binær."], "I en lineær sannsynlighetsmodell er koeffisienter endringer i sannsynlighet målt i andeler/prosentpoeng."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "Hvis andelen øker fra 30 prosent til 45 prosent, hvor stor er økningen i prosentpoeng?", "15 prosentpoeng.", ["15 prosent.", "30 prosentpoeng.", "45 prosentpoeng.", "50 prosentpoeng."], "Prosentpoeng er den absolutte forskjellen mellom prosentandeler: 45 - 30 = 15."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "Hvis andelen øker fra 30 prosent til 45 prosent, hva er relativ prosentvis økning?", "50 prosent.", ["15 prosent.", "15 prosentpoeng.", "30 prosent.", "45 prosent."], "Relativ økning er endring delt på startverdi: 15 / 30 = 0,5 = 50 prosent."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "Ved 70 spørsmål med fem svaralternativer, hva er forventet antall riktige ved ren gjetting?", "14.", ["10.", "20.", "25.", "35."], "Forventet treffrate er 1 av 5. 70 / 5 = 14."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "Hvis du får 35 riktige av 70 spørsmål, hva er prosent riktig?", "50 prosent.", ["35 prosent.", "40 prosent.", "55 prosent.", "70 prosent."], "35 / 70 = 0,5, altså 50 prosent."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "Hvor mange riktige av 70 tilsvarer 40 prosent?", "28.", ["14.", "25.", "35.", "40."], "0,40 × 70 = 28."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "I en 3 × 4 krysstabell, hvor mange frihetsgrader har kjikvadrattesten?", "6.", ["3.", "4.", "7.", "12."], "Frihetsgrader er (rader - 1) × (kolonner - 1), altså 2 × 3 = 6."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "I en 2 × 5 krysstabell, hvor mange frihetsgrader har kjikvadrattesten?", "4.", ["2.", "5.", "6.", "10."], "Frihetsgrader er (2 - 1) × (5 - 1) = 4."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "Hvis R² = 0,36, hva betyr det?", "Modellen forklarer 36 prosent av variasjonen i Y.", ["Modellen er 36 prosent kausal.", "36 prosent av X er målefeil.", "P-verdien er 0,36.", "Standardfeilen er 36."], "R² er andelen av variasjonen i Y som forklares av modellen."),
    rebuilt_question("Eksamensdrill: regresjon og regning", "I modellen Y = 4 + 2X + 6D, der D er en dummy. Hva betyr koeffisienten til D?", "Når D går fra 0 til 1, øker forventet Y med 6, gitt X.", ["Når X øker med 6, blir D lik 1.", "D forklarer alltid 6 prosent av Y.", "Konstantleddet blir 6.", "Y må være en sannsynlighet."], "Dummykoeffisienten sammenligner D = 1 med D = 0, alt annet likt."),
    rebuilt_question("Eksamensdrill: samspill", "I modellen Y = 2 + 3X + 4Z + 5(X × Z), hva er effekten av X når Z = 0?", "3.", ["4.", "5.", "8.", "12."], "Når Z = 0 faller samspillsleddet bort, så effekten av X er hovedleddet 3."),
    rebuilt_question("Eksamensdrill: samspill", "I modellen Y = 2 + 3X + 4Z + 5(X × Z), hva er effekten av X når Z = 1?", "8.", ["3.", "4.", "5.", "12."], "Effekten av X er 3 + 5Z. Når Z = 1 blir den 8."),
    rebuilt_question("Eksamensdrill: samspill", "I modellen Y = a + b1X + b2Z + b3(X × Z), hva betyr et positivt b3?", "Effekten av X på Y blir større når Z øker.", ["Effekten av X forsvinner alltid.", "Konstantleddet øker med X.", "Z kan ikke tolkes.", "Modellen mangler feilledd."], "Et samspillsledd viser hvordan effekten av én variabel avhenger av en annen."),
    rebuilt_question("Eksamensdrill: samspill", "Hva må man huske når man tolker hovedleddet b1 i en modell med X × Z?", "b1 er effekten av X når Z = 0.", ["b1 er alltid totaleffekten av X for alle Z.", "b1 kan ikke tolkes i det hele tatt.", "b1 er effekten av Z når X = 1.", "b1 er alltid lik b3."], "I en interaksjonsmodell er hovedleddet effekten når den andre samspillsvariabelen er null."),
    rebuilt_question("Eksamensdrill: ikke riktig", "Hvilket utsagn om p-verdier er ikke riktig?", "P-verdien er sannsynligheten for at nullhypotesen er sann.", ["P-verdien beregnes gitt nullhypotesen.", "Lav p-verdi kan gi grunnlag for å forkaste H0.", "P-verdien sier ikke alene om effekten er stor.", "P-verdien påvirkes av utvalgsstørrelse."], "P-verdien er ikke sannsynligheten for at H0 er sann; den er sannsynligheten for data minst så ekstreme gitt H0."),
    rebuilt_question("Eksamensdrill: ikke riktig", "Hvilket utsagn om konfidensintervall er ikke riktig?", "Et 95-prosent konfidensintervall betyr at 95 prosent av observasjonene ligger i intervallet.", ["Et intervall som ikke inneholder null kan tyde på signifikans.", "Bredere intervall tyder ofte på mer usikkerhet.", "Konfidensintervall bygger på en metode med dekningsgrad.", "Standardfeil påvirker intervallets bredde."], "Konfidensintervall handler om usikkerhet rundt en parameter, ikke om hvor observasjonene ligger."),
    rebuilt_question("Eksamensdrill: ikke riktig", "Hvilket utsagn om R² er ikke riktig?", "Høy R² beviser at X forårsaker Y.", ["R² måler forklart variasjon i Y.", "R² kan øke når flere variabler legges til.", "Lav R² betyr ikke nødvendigvis at en kausal effekt er uinteressant.", "R² er ikke det samme som p-verdi."], "Forklart variasjon er ikke det samme som kausal identifikasjon."),
    rebuilt_question("Eksamensdrill: ikke riktig", "Hvilket utsagn om kontrollvariabler er ikke riktig?", "Kontrollvariabler garanterer at estimatet blir kausalt.", ["Kontrollvariabler kan redusere noen alternative forklaringer.", "Kontroll for mediatorer kan endre estimatet.", "Kontrollvariabler bør begrunnes teoretisk.", "En utelatt konfunder kan gi skjevhet."], "Kontroller hjelper bare hvis relevante antakelser holder og riktige variabler er målt."),
    rebuilt_question("Eksamensdrill: ikke riktig", "Hvilket utsagn om random assignment er ikke riktig?", "Random assignment sikrer at utvalget er representativt for populasjonen.", ["Random assignment styrker intern validitet.", "Random assignment fordeler behandling tilfeldig.", "Random assignment kan balansere grupper i forventning.", "Random assignment er noe annet enn random sampling."], "Representativitet handler primært om random sampling, ikke random assignment."),
    rebuilt_question("Eksamensdrill: ikke riktig", "Hvilket utsagn om reliabilitet er ikke riktig?", "Høy reliabilitet garanterer høy validitet.", ["Reliabilitet handler om stabilitet.", "Et mål kan være reliabelt, men invalid.", "Tilfeldig målefeil kan svekke reliabilitet.", "To forskere som måler likt kan tyde på reliabilitet."], "Stabile målinger kan fortsatt måle feil begrep."),
    rebuilt_question("Eksamensdrill: ikke riktig", "Hvilket utsagn om uteliggere i regresjon er ikke riktig?", "En uteligger er alltid en observasjon med lav begrepsvaliditet.", ["En uteligger kan ha stor residual.", "Uteligger kan påvirke estimater.", "Cook's distance kan brukes til å vurdere påvirkning.", "Høy leverage handler om uvanlige X-verdier."], "Uteliggerbegrepet i regresjon handler primært om plassering/prediksjonsfeil, ikke begrepsvaliditet."),
    rebuilt_question("Eksamensdrill: ikke riktig", "Hvilket utsagn om robuste standardfeil er ikke riktig?", "Robuste standardfeil fjerner utelatt variabelskjevhet.", ["Robuste standardfeil kan håndtere heteroskedastisitet bedre.", "Robuste standardfeil endrer usikkerhetsberegningen.", "Koeffisienten får ikke automatisk kausal tolkning.", "Standardfeil brukes i t-tester."], "Robuste standardfeil reparerer ikke skjevhet i selve koeffisienten."),
    rebuilt_question("Eksamensdrill: kausalitet", "En forsker finner at kommuner med høy inntekt har høyere valgdeltakelse. Hva må til for å hevde kausalitet mer troverdig?", "Blant annet kontrollere alternative forklaringer og begrunne mekanisme og tidsrekkefølge.", ["Bare vise at korrelasjonen er positiv.", "Bare lage et kakediagram.", "Bare ha en høy R².", "Bare måle inntekt på forholdstallsnivå."], "Kausalitet krever mer enn samvariasjon: plausibel mekanisme, tidsrekkefølge og håndtering av konfunderende variabler."),
    rebuilt_question("Eksamensdrill: kausalitet", "En studie viser at politisk interesse og nyhetsbruk henger sammen. Hva er en mulig kausal utfordring?", "Nyhetsbruk kan påvirke interesse, men interesse kan også påvirke nyhetsbruk.", ["Variablene kan ikke måles.", "Begge variabler må være konstante.", "Korrelasjon kan aldri beregnes.", "Alle surveydata er eksperimenter."], "Dette er et eksempel på mulig reversert kausalitet."),
    rebuilt_question("Eksamensdrill: kausalitet", "En forsker kontrollerer for utdanning når hun undersøker inntekt og valgdeltakelse. Hva forsøker hun mest sannsynlig å redusere?", "Konfunderende påvirkning fra en bakenforliggende variabel.", ["Type II-feil alene.", "At Y er binær.", "At grafen er misvisende.", "At utvalget får flere respondenter."], "Utdanning kan påvirke både inntekt og valgdeltakelse og dermed fungere som konfunder."),
    rebuilt_question("Eksamensdrill: kausalitet", "Hvis X påvirker Y gjennom M, hva kaller vi M?", "Mediator.", ["Konfunder.", "Residual.", "Leverage.", "Referansekategori."], "En mediator ligger på kausalveien fra årsak til utfall."),
    rebuilt_question("Eksamensdrill: kausalitet", "Hva er en nødvendig årsak?", "En faktor som må være til stede for at utfallet kan oppstå.", ["En faktor som alene alltid skaper utfallet.", "En faktor som aldri kan måles.", "En tilfeldig feil i Y.", "En variabel med lav standardfeil."], "Nødvendig årsak betyr at utfallet ikke oppstår uten faktoren."),
    rebuilt_question("Eksamensdrill: kausalitet", "Hva er en tilstrekkelig årsak?", "En faktor som alene er nok til å frambringe utfallet.", ["En faktor som alltid må være til stede, men aldri er nok alene.", "En variabel som bare brukes som kontroll.", "En målefeil uten retning.", "En observasjon med høy residual."], "Tilstrekkelig årsak betyr at faktoren er nok til å produsere utfallet."),
    rebuilt_question("Eksamensdrill: forskningsdesign", "Hva er hovedfordelen med et ekte eksperiment?", "Forskeren kan tilfeldig tildele behandling.", ["Forskeren får alltid et representativt utvalg.", "Alle målinger blir perfekte.", "R² blir alltid høy.", "Det krever ingen hypotese."], "Tilfeldig tilordning styrker intern validitet ved å gjøre grupper sammenlignbare i forventning."),
    rebuilt_question("Eksamensdrill: forskningsdesign", "Hva er et vanlig problem med observasjonsstudier?", "Det kan være systematiske forskjeller mellom dem som har ulike verdier på X.", ["Det er umulig å måle Y.", "Det finnes aldri variasjon.", "De kan ikke bruke regresjon.", "De kan ikke ha teori."], "Forskeren kontrollerer ikke tilordningen til X, så seleksjon og konfunderende faktorer kan være problematiske."),
    rebuilt_question("Eksamensdrill: forskningsdesign", "Hva er forskjellen på intern og ekstern validitet?", "Intern validitet handler om troverdig kausal konklusjon; ekstern validitet om generalisering.", ["Intern validitet er R²; ekstern validitet er p-verdi.", "Intern validitet handler bare om figurer.", "Ekstern validitet betyr at målingen er stabil.", "Begrepene er synonymer."], "Intern validitet gjelder kausal troverdighet i studien; ekstern validitet gjelder overførbarhet."),
    rebuilt_question("Eksamensdrill: forskningsdesign", "Hva er seleksjonsskjevhet?", "Systematiske forskjeller i hvem som inngår eller sammenlignes, som påvirker resultatet.", ["En tilfeldig p-verdi under 0,05.", "At alle observasjoner har samme X.", "At residualene er positive.", "At standardavviket er null."], "Seleksjonsskjevhet oppstår når utvalg eller grupper ikke er sammenlignbare på relevante måter."),
    rebuilt_question("Eksamensdrill: forskningsdesign", "Hva er et kvasi-eksperiment?", "Et design som utnytter behandlingslignende variasjon uten full random assignment.", ["En studie uten data.", "Et design der alle velger behandling selv uten sammenligning.", "Et rent normativt argument.", "En vanlig frekvenstabell."], "Kvasi-eksperimenter forsøker å etterligne eksperimentell logikk med naturlige eller institusjonelle kilder til variasjon."),
    rebuilt_question("Eksamensdrill: forskningsdesign", "Hva er viktigst når vi vurderer om et utvalg kan generaliseres til en populasjon?", "Hvordan utvalget er trukket fra populasjonen.", ["Om konstantleddet er stort.", "Om samspillsleddet er positivt.", "Om residualene summerer til null.", "Om alle figurer er pene."], "Ekstern validitet og generalisering avhenger særlig av utvalgsdesign og målpopulasjon."),
    rebuilt_question("Eksamensdrill: inferens", "Hva er standardfeil?", "Et mål på hvor mye et estimat forventes å variere mellom utvalg.", ["Spredningen til rådata rundt medianen.", "Forskjellen mellom X og Y.", "Andelen forklart variasjon.", "En type kontrollvariabel."], "Standardfeil beskriver usikkerhet i estimatet, ikke spredningen til enkeltobservasjonene direkte."),
    rebuilt_question("Eksamensdrill: inferens", "Hva skjer hvis et 95-prosent konfidensintervall for en koeffisient inkluderer null?", "Koeffisienten er vanligvis ikke signifikant forskjellig fra null på 5-prosentnivå.", ["Koeffisienten er nødvendigvis null i utvalget.", "Effekten er bevist negativ.", "R² er null.", "Modellen er invalid."], "Et intervall som inkluderer null er forenlig med null effekt ved en vanlig tosidig 5-prosenttest."),
    rebuilt_question("Eksamensdrill: inferens", "Hva betyr statistisk styrke?", "Sannsynligheten for å oppdage en reell effekt.", ["Sannsynligheten for at H0 er sann.", "Hvor pen en graf er.", "Hvor mange variabler som er nominale.", "Andelen av Y som forklares."], "Statistisk styrke er sannsynligheten for å forkaste en falsk nullhypotese."),
    rebuilt_question("Eksamensdrill: inferens", "Hva er beste tolkning av en liten p-verdi?", "Dataene ville vært uvanlige dersom nullhypotesen var sann.", ["Nullhypotesen er usann med sikkerhet.", "Effekten er stor.", "Målingen er valid.", "Utvalget er representativt."], "En liten p-verdi er evidens mot H0, men sier ikke alene effektstørrelse, validitet eller generaliserbarhet."),
    rebuilt_question("Eksamensdrill: inferens", "Hva er forholdet mellom større utvalg og statistisk signifikans?", "Større utvalg kan gjøre det lettere å finne små effekter signifikante.", ["Større utvalg gjør alle effekter kausale.", "Større utvalg øker alltid p-verdien.", "Større utvalg fjerner alle målefeil.", "Større utvalg gjør R² lik 1."], "Når standardfeilen ofte blir mindre med større N, kan små estimater bli statistisk tydelige."),
    rebuilt_question("Eksamensdrill: inferens", "Hva er en type I-feil hvis H0 sier at koeffisienten er null?", "Å konkludere med effekt selv om den sanne koeffisienten er null.", ["Å overse en reell effekt.", "Å ha for lav R².", "Å bruke en dummyvariabel.", "Å måle Y på ordinalnivå."], "Type I-feil er å forkaste en sann nullhypotese."),
    rebuilt_question("Eksamensdrill: inferens", "Hva er en type II-feil hvis H0 sier at koeffisienten er null?", "Å ikke konkludere med effekt selv om den sanne koeffisienten ikke er null.", ["Å forkaste en sann nullhypotese.", "Å ha for høy reliabilitet.", "Å bruke paneldata.", "Å inkludere en referansekategori."], "Type II-feil er å ikke forkaste en falsk nullhypotese."),
    rebuilt_question("Eksamensdrill: visualisering", "Når passer et histogram best?", "Når vi vil vise fordelingen til én kontinuerlig variabel.", ["Når vi vil vise andeler av en helhet med få kategorier.", "Når vi vil sammenligne to kontinuerlige variabler.", "Når vi vil vise en regresjonskoeffisient alene.", "Når vi vil teste en nullhypotese direkte."], "Histogrammer deler en kontinuerlig variabel i intervaller og viser fordelingen."),
    rebuilt_question("Eksamensdrill: visualisering", "Når passer et spredningsdiagram best?", "Når vi vil vise forholdet mellom to kontinuerlige variabler.", ["Når vi vil vise én kategorisk variabels andeler.", "Når vi vil vise medianen alene.", "Når vi vil vise en krysstabell med tekst.", "Når vi vil beregne frihetsgrader."], "Spredningsdiagram viser hvert observasjonspar som et punkt."),
    rebuilt_question("Eksamensdrill: visualisering", "Når passer et kakediagram best?", "Når få kategorier skal vises som relative deler av en helhet.", ["Når en kontinuerlig variabel har mange verdier.", "Når vi vil vise utvikling over tid.", "Når vi vil vise residualer mot predikerte verdier.", "Når vi vil vise usikkerheten rundt et estimat."], "Kakediagram fungerer best for få kategorier og relative andeler."),
    rebuilt_question("Eksamensdrill: visualisering", "Hva er data-to-ink-ratio?", "Andelen visuelle elementer som faktisk formidler relevant informasjon.", ["Forholdet mellom p-verdi og standardfeil.", "Antall farger delt på antall observasjoner.", "Hvor mye tekst som står i boka.", "En metode for random assignment."], "Begrepet handler om å redusere unødvendig visuell pynt."),
    rebuilt_question("Eksamensdrill: visualisering", "Hva kan være problemet med for mange 3D-effekter og pynt i en figur?", "Det kan gjøre dataene vanskeligere å lese og sammenligne.", ["Det øker alltid reliabiliteten.", "Det gjør effekter kausale.", "Det reduserer standardfeilen.", "Det gir flere observasjoner."], "God visualisering bør støtte sammenligning og tolkning, ikke skjule mønstre."),
    rebuilt_question("Eksamensdrill: visualisering", "Når er logaritmisk skala særlig nyttig?", "Når relative forskjeller er viktigere enn absolutte forskjeller og verdiene varierer mye.", ["Når variabelen er nominal.", "Når alle verdier er null.", "Når man vil unngå akser.", "Når man vil bevise kausalitet."], "Log-skala gjør proporsjonale endringer lettere å sammenligne."),
    rebuilt_question("Eksamensdrill: deskriptiv statistikk", "Hva er mest robust mot ekstreme uteliggere?", "Median.", ["Gjennomsnitt.", "Varians.", "Standardavvik.", "Maksimum."], "Medianen påvirkes mindre av ekstreme verdier enn gjennomsnittet."),
    rebuilt_question("Eksamensdrill: deskriptiv statistikk", "Hva måler interkvartilbredde?", "Spredningen i de midterste 50 prosentene av observasjonene.", ["Avstanden mellom gjennomsnitt og null.", "Andelen forklart variasjon.", "Forskjellen mellom X og Y.", "Antall frihetsgrader."], "IQR er Q3 - Q1 og beskriver midtre del av fordelingen."),
    rebuilt_question("Eksamensdrill: deskriptiv statistikk", "Hvis gjennomsnittet er mye høyere enn medianen, hva kan det tyde på?", "En høyreskjev fordeling med høye ekstreme verdier.", ["Perfekt symmetri.", "At alle verdier er like.", "At variabelen er nominal.", "At p-verdien er lav."], "Høye ekstremverdier trekker gjennomsnittet opp mer enn medianen."),
    rebuilt_question("Eksamensdrill: bivariat analyse", "Når passer en t-test godt?", "Når vi vil sammenligne gjennomsnitt mellom to grupper.", ["Når begge variabler er nominale med mange kategorier.", "Når vi vil beregne R².", "Når vi vil teste et samspillsledd uten modell.", "Når vi vil finne Cook's distance."], "T-test brukes ofte for forskjeller i gjennomsnitt mellom grupper."),
    rebuilt_question("Eksamensdrill: bivariat analyse", "Når passer en krysstabell godt?", "Når vi vil undersøke sammenhengen mellom to kategoriske variabler.", ["Når både X og Y er kontinuerlige.", "Når vi vil beregne residualer fra OLS.", "Når vi vil predikere med samspillsledd.", "Når vi vil måle standardavviket alene."], "Krysstabeller viser fordelingen på kombinasjoner av kategorier."),
    rebuilt_question("Eksamensdrill: bivariat analyse", "Hva betyr negativ korrelasjon?", "Høye verdier på én variabel henger lineært sammen med lave verdier på den andre.", ["Begge variabler er ugyldige.", "X kan ikke påvirke Y.", "R² er negativ.", "P-verdien er alltid over 0,05."], "Negativ korrelasjon beskriver en fallende lineær samvariasjon."),
    rebuilt_question("Eksamensdrill: faste effekter", "Hva identifiserer en koeffisient i en modell med enhetsfaste effekter primært fra?", "Endring innen samme enhet over tid.", ["Forskjeller mellom enheter som aldri endrer seg.", "Bare variasjon i referansekategorien.", "Bare tilfeldig målefeil.", "Bare første observasjon i datasettet."], "Enhetsfaste effekter bruker within-variasjon."),
    rebuilt_question("Eksamensdrill: faste effekter", "Hva kontrollerer toveis faste effekter for?", "Både stabile enhetsforskjeller og felles tidsperioder.", ["Bare observerte tidsvarierende konfunderende variabler.", "Bare forskjeller mellom menn og kvinner.", "Bare residualenes varians.", "Bare random sampling."], "Toveis faste effekter inkluderer både enhets- og tidsfaste effekter."),
    rebuilt_question("Eksamensdrill: faste effekter", "Hva skjer med en variabel som aldri endrer seg innen enhet i en enhets-fast-effekt-modell?", "Den kan normalt ikke estimeres separat fra enhetsfaste effekter.", ["Den får alltid perfekt signifikans.", "Den blir automatisk en mediator.", "Den gir alltid høyere R².", "Den må være avhengig variabel."], "Uten within-variasjon kan effekten ikke skilles fra den faste enhetseffekten."),
    rebuilt_question("Eksamensdrill: faste effekter", "Hvorfor er faste effekter ikke en magisk løsning på kausalitet?", "De fjerner ikke nødvendigvis tidsvarierende konfunderende variabler.", ["De kan ikke kontrollere for stabile forskjeller.", "De kan aldri brukes med paneldata.", "De gjør alle standardfeil negative.", "De fjerner alle observasjoner."], "Faste effekter håndterer stabile forskjeller, men ikke alt som endrer seg samtidig med X og påvirker Y."),
]


def normalize_question(question: dict) -> dict:
    normalized = ensure_five_choices(question)
    if len(normalized["choices"]) != 5:
        raise ValueError(f"Question does not have five choices: {normalized['question']}")
    if len(set(normalized["choices"])) != 5:
        raise ValueError(f"Question has duplicate choices: {normalized['question']}")
    if not 0 <= normalized["correctIndex"] < 5:
        raise ValueError(f"Question has bad correctIndex: {normalized['question']}")
    normalized["choiceExplanations"] = [
        explain_choice(normalized, choice, index)
        for index, choice in enumerate(normalized["choices"])
    ]
    return normalized


def flashcard_questions() -> list[dict]:
    by_topic: dict[str, list[tuple[str, str]]] = {}
    for topic, term, definition in FLASHCARDS:
        by_topic.setdefault(topic, []).append((term, definition))

    all_cards = [(topic, term, definition) for topic, term, definition in FLASHCARDS]
    questions: list[dict] = []
    for card_index, (topic, term, definition) in enumerate(all_cards):
        same_topic = [
            other_term
            for other_term, other_definition in by_topic[topic]
            if other_term != term
        ]
        broader = [
            other_term
            for other_topic, other_term, other_definition in all_cards
            if other_topic != topic and other_term != term
        ]
        distractors: list[str] = []
        rotated = same_topic[card_index % max(len(same_topic), 1):] + same_topic[:card_index % max(len(same_topic), 1)]
        for candidate in [*rotated, *broader]:
            if candidate != term and candidate not in distractors:
                distractors.append(candidate)
            if len(distractors) == 4:
                break
        questions.append(
            rebuilt_question(
                f"Flashcards: {topic}",
                f"«{definition}»",
                term,
                distractors,
                f"Riktig begrep er «{term}»: {definition}",
            )
        )
    return questions


def reverse_flashcard_questions() -> list[dict]:
    by_topic: dict[str, list[tuple[str, str]]] = {}
    for topic, term, definition in FLASHCARDS:
        by_topic.setdefault(topic, []).append((term, definition))

    all_cards = [(topic, term, definition) for topic, term, definition in FLASHCARDS]
    questions: list[dict] = []
    for card_index, (topic, term, definition) in enumerate(all_cards):
        same_topic = [
            other_definition
            for other_term, other_definition in by_topic[topic]
            if other_definition != definition
        ]
        broader = [
            other_definition
            for other_topic, other_term, other_definition in all_cards
            if other_topic != topic and other_definition != definition
        ]
        distractors: list[str] = []
        rotated = same_topic[card_index % max(len(same_topic), 1):] + same_topic[:card_index % max(len(same_topic), 1)]
        for candidate in [*rotated, *broader]:
            if candidate != definition and candidate not in distractors:
                distractors.append(candidate)
            if len(distractors) == 4:
                break
        questions.append(
            rebuilt_question(
                f"Flashcards reversert: {topic}",
                f"Hvilken definisjon passer til begrepet «{term}»?",
                definition,
                distractors,
                f"Riktig definisjon for «{term}» er: {definition}",
            )
        )
    return questions


def parse_questions() -> list[dict]:
    raw_questions = [
        *EXAMPLE_QUESTIONS,
        *CURATED_EXAM_QUESTIONS,
        *ADDITIONAL_EXAM_STYLE_QUESTIONS,
        *PRIORITY_EXAM_DRILL_QUESTIONS,
        *FORMULA_QUESTIONS,
        *flashcard_questions(),
        *reverse_flashcard_questions(),
    ]
    questions = []
    seen_prompts: set[str] = set()
    for index, question in enumerate(raw_questions, start=1):
        normalized = normalize_question({"id": index, **question})
        prompt_key = normalized["question"].strip().lower()
        if prompt_key in seen_prompts:
            raise ValueError(f"Duplicate question prompt: {normalized['question']}")
        seen_prompts.add(prompt_key)
        questions.append(normalized)
    return questions


def main() -> None:
    flashcards = [
        {"id": index, "topic": topic, "term": term, "definition": definition}
        for index, (topic, term, definition) in enumerate(FLASHCARDS, start=1)
    ]
    payload = {"flashcards": flashcards, "questions": parse_questions()}
    OUTPUT.write_text(
        "window.STV1020_DATA = "
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(flashcards)} flashcards and {len(payload['questions'])} questions to {OUTPUT}")


if __name__ == "__main__":
    main()
