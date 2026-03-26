from generators import genereer_unieke_mapnaam, random_bsn
from generateBrp import samenstellen_inspoel
from generateKlassenlijst import samenstellen_klassenlijst
from record import generateAllRecords
import argparse
import datetime
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Optionele argumenten voor het genereren van dossiers
    parser.add_argument("--aantal_dossiers", type=int,
                        help="Aantal dossiers per bestand")
    parser.add_argument("--aantal_bestanden", type=int,
                        help="Aantal bestanden per serie")
    parser.add_argument("--leeftijd", type=float,
                        help="Leeftijd van de gegenereerde personen (standaard in jaren, zie --leeftijd_eenheid)")
    parser.add_argument("--minimum_leeftijd", type=float,
                        help="Minimale leeftijd van de gegenereerde personen (standaard in jaren, zie --leeftijd_eenheid)")
    parser.add_argument("--maximum_leeftijd", type=float,
                        help="Maximale leeftijd van de gegenereerde personen (standaard in jaren, zie --leeftijd_eenheid)")
    parser.add_argument("--leeftijd_eenheid", type=str, choices=["jaar", "maand", "dag"], default="jaar",
                        help="Eenheid voor leeftijdsargumenten: 'jaar', 'maand' of 'dag'. Default: 'jaar'")
    parser.add_argument("--klant", type=str,
                        help="Naam van de klant voor specifieke postcode/plaatsnaam datasets (bv. zuid_limburg)")
    parser.add_argument("--brin", type=str,
                        help="BRIN-code van de school")
    parser.add_argument("--klas_of_groep", type=str,
                        help="Klas of groep aanduiding")
    parser.add_argument("--klasnummer", type=str,
                        help="Klas- of groepsnummer")
    parser.add_argument("--naam_klas", type=str,
                        help="Naam van de klas")
    parser.add_argument("--onderwijssoort", type=str,
                        help="Onderwijssoortcode (bijv. 01 voor basisonderwijs)")
    parser.add_argument("--postcode_range", nargs="+", type=int,
                        help="Lijst van numerieke postcodes (bv. 7411 7412 7413)")
    
    # Argumenten voor het genereren van speciale cases
    parser.add_argument("--brusje", action="store_true",
                        help="Zorgt ervoor dat de gegenereerde personen allemaal familieleden zijn van elkaar (brusje)")
    
    # Override argumenten voor het gebruik van specifieke waarden
    parser.add_argument("--geboortedatum", type=datetime.date.fromisoformat,
                        help="Specifieke geboortedatum in YYYYMMDD formaat, laat leeg om te genereren op basis van leeftijd")
    parser.add_argument("--achternaam", type=str,
                        help="Achternaam van de gegenereerde personen")
    parser.add_argument("--naamvader", type=str,
                        help="Voornaam van de vader van de gegenereerde personen")
    parser.add_argument("--fixbsnvader", action="store_true",
                        help="BSN van de vader van de gegenereerde personen wordt gefixeerd voor alle dossiers")
    parser.add_argument("--naammoeder", type=str,
                        help="Voornaam van de moeder van de gegenereerde personen")
    parser.add_argument("--fixbsnmoeder", action="store_true",
                        help="BSN van de moeder van de gegenereerde personen wordt gefixeerd voor alle dossiers")
    parser.add_argument("--adres", type=str,
                        help="Adres van de gegenereerde personen (bv. 'Waldeckstraat 1 7411AA Deventer')")
    args = parser.parse_args()

    outputmap = genereer_unieke_mapnaam()
    aantal_bestanden = args.aantal_bestanden if args.aantal_bestanden is not None else 1
    aantal_dossiers = args.aantal_dossiers or 10

    # Genereer alle records voor alle bestanden
    # Zorg dat leeftijd_eenheid wordt doorgegeven aan record-generatie
    if not hasattr(args, 'leeftijd_eenheid'):
        args.leeftijd_eenheid = "jaar"
    alle_leerlingen_sets = generateAllRecords(args, aantal_bestanden, aantal_dossiers)

    # Schrijf elk set naar bestanden
    for i, leerlingen in enumerate(alle_leerlingen_sets, 1):
        submap = os.path.join(outputmap, f"set_{i}")
        os.makedirs(submap, exist_ok=True)
        inspoel_pad = os.path.join(submap, f"BRP_inspoel_{i}.txt")
        klassenlijst_pad = os.path.join(submap, f"klassenlijst_{i}.csv")
        samenstellen_inspoel(leerlingen, bestandsnaam=inspoel_pad)
        samenstellen_klassenlijst(leerlingen, args, bestandsnaam=klassenlijst_pad)