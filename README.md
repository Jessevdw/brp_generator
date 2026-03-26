# brp_generator

## Optionele arguments;

--aantal_dossiers
Bepaald het aantal dossiers wat gegenereerd wordt
Default: 10

--aantal_bestanden
Bepaald het aantal bestanden waarin de dossiers worden opgenomen
Default: 1

--leeftijd
Leeftijd van de te genereren personen. Standaard in jaren, maar kan ook in maanden of dagen worden opgegeven met --leeftijd_eenheid.
Default: 10

--minimum_leeftijd
Minimale leeftijd van de te genereren personen. Standaard in jaren, zie --leeftijd_eenheid.
Er wordt een willekeurige geboortedatum gekozen die resulteert in een leeftijd tussen minimum en maximum.
Default: Gebruikt --leeftijd waarde of 10

--maximum_leeftijd
Maximale leeftijd van de te genereren personen. Standaard in jaren, zie --leeftijd_eenheid.
Als niet opgegeven wordt de minimum_leeftijd als maximum gebruikt.
Default: Gebruikt minimum_leeftijd waarde

--leeftijd_eenheid
Eenheid voor leeftijdsargumenten: 'jaar', 'maand' of 'dag'.
Default: jaar
Voorbeeld: --minimum_leeftijd 1 --maximum_leeftijd 3 --leeftijd_eenheid maand (kinderen van 1 tot 3 maanden oud)

--brin
Brin van de school waar de kinderen in worden geplaatst
Default: BRIN

--klas_of_groep
Of het een klas of groep is waarin de kinderen worden geplaatst
Default: Groep

--klasnummer
Nummer van de klas of groep waarin de kinderen worden geplaatst
Default: 6

--naam_klas
Naam van de klas of groep waarin de kinderen worden geplaatst
Default: Leeg

--onderwijssoort
Onderwijssoort voor de klas of groep waarin de kinderen worden geplaatst
Op basis van de BDS onderwijssoorten.
Default: 01

--postcode_range
Postcode range die gebruikt dient te worden
Default: [7411]

## Speciale cases

--brusje
Voeg deze optie toe om te zorgen dat alle dossiers dezelfde achternaam, ouders en adressen bevatten.
Deze worden dan éénmaal gegenereerd en vervolgens voor alle dossiers hergebruikt.

--klant
Met deze optie kun je klant-specifieke datasets gebruiken voor postcode en plaatsnaam.
Voorbeeld: --klant zuid_limburg
Hiermee worden alleen postcodes en plaatsnamen uit de zuid_limburg-datasets gebruikt (zie src/data/adressen.py).
Als er geen dataset voor de opgegeven klant bestaat, krijg je een nette foutmelding.
Je kunt eenvoudig nieuwe klant-datasets toevoegen door in adressen.py een lijst aan te maken zoals:
	plaatsnamen_<klantnaam>, postcode_range_<klantnaam>, postcode_letters_<klantnaam>

## Override arguments

--geboortedatum
Override om een specifieke geboortedatum te hanteren voor alle dossiers
Format: YYYYMMDD

--achternaam
Override om een specifieke achternaam te hanteren voor alle dossiers

--naamvader
Override om een specifieke voornaam voor de vader te hanteren voor alle dossiers

--fixbsnvader
Override om een specifiek BSN voor de vader te hanteren voor alle dossiers

--naammoeder
Override om een specifieke voornaam voor de moeder te hanteren voor alle dossiers

--fixbsnmoeder
Override om een specifiek BSN voor de moeder te hanteren voor alle dossiers

--adres
Override om een specifiek adres te hanteren voor alle dossiers
Format: "Straatnaam 1 1234AA Plaats"
