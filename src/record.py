from data.namen import voornamen_man, voornamen_vrouw, achternamen
from generators import random_bsn, random_datum, generate_random_postcode
from data.adressen import straatnamen, plaatsnamen
from dataclasses import dataclass
import datetime
import random

@dataclass
class Record:
    bsn: str
    voornaamKind: str
    achternaam: str
    geboortedatum: datetime.date
    straatnaam: str
    huisnummer: int
    postcode: str
    woonplaats: str
    geslacht: str
    geboorteplaats: str
    voornaamVader: str
    bsnVader: str
    voornaamMoeder: str
    bsnMoeder: str

def generateSingleRecord(args, geslacht, fixed_bsn_vader=None, fixed_bsn_moeder=None):
    voornaam = random.choice(voornamen_man if geslacht == "M" else voornamen_vrouw)
    achternaam = getattr(args, "achternaam", None) or random.choice(achternamen)
    
    # Bepaal geboortedatum
    if getattr(args, "geboortedatum", None):
        geboortedatum = args.geboortedatum
    else:
        # Gebruik nieuwe minimum/maximum leeftijd argumenten
        minimum_leeftijd = getattr(args, "minimum_leeftijd", None)
        maximum_leeftijd = getattr(args, "maximum_leeftijd", None)
        
        # Backward compatibility met oude --leeftijd argument
        if minimum_leeftijd is None and maximum_leeftijd is None:
            leeftijd_arg = getattr(args, "leeftijd", None)
            minimum_leeftijd = leeftijd_arg if leeftijd_arg is not None else 10
            maximum_leeftijd = minimum_leeftijd
        elif minimum_leeftijd is None:
            minimum_leeftijd = maximum_leeftijd
        elif maximum_leeftijd is None:
            maximum_leeftijd = minimum_leeftijd
        
    eenheid = getattr(args, "leeftijd_eenheid", "jaar")
    geboortedatum = random_datum(minimum_leeftijd, maximum_leeftijd, eenheid)

    # Genereer voornamen voor ouders
    voornaam_vader = getattr(args, "naamvader", None) or random.choice(voornamen_man)
    voornaam_moeder = getattr(args, "naammoeder", None) or random.choice(voornamen_vrouw)

    # Gebruik fixed BSN's als opgegeven, anders genereer nieuwe
    bsn_vader = fixed_bsn_vader if fixed_bsn_vader else random_bsn()
    bsn_moeder = fixed_bsn_moeder if fixed_bsn_moeder else random_bsn()

    klant = getattr(args, "klant", None)
    if getattr(args, "adres", None):
        straatnaam, huisnummer, postcode, woonplaats = args.adres.split(" ")
    else:
        straatnaam = random.choice(straatnamen)
        huisnummer = random.randint(1, 100)
        postcode = generate_random_postcode(klant)
        # Dynamisch ophalen van plaatsnamen per klant
        try:
            from generators import get_adressen_dataset
            _, _, plaatsnamen_set = get_adressen_dataset(klant)
        except Exception as e:
            raise ValueError(str(e))
        woonplaats = random.choice(plaatsnamen_set)

    # Ook geboorteplaats op basis van klant
    try:
        from generators import get_adressen_dataset
        _, _, plaatsnamen_set = get_adressen_dataset(klant)
    except Exception as e:
        raise ValueError(str(e))
    return Record(
        bsn=random_bsn(),
        voornaamKind=voornaam,
        achternaam=achternaam,
        geboortedatum=geboortedatum,
        straatnaam=straatnaam,
        huisnummer=huisnummer,
        postcode=postcode,
        woonplaats=woonplaats,
        geslacht=geslacht,
        geboorteplaats=random.choice(plaatsnamen_set),
        voornaamVader=voornaam_vader,
        bsnVader=bsn_vader,
        voornaamMoeder=voornaam_moeder,
        bsnMoeder=bsn_moeder
    )

def generateMultipleRecords(args, aantal, gebruikte_bsns=None, gebruikte_namen=None, fixed_bsn_vader=None, fixed_bsn_moeder=None):
    if gebruikte_bsns is None:
        gebruikte_bsns = set()
    if gebruikte_namen is None:
        gebruikte_namen = set()
    
    # Voeg fixed BSN's toe aan gebruikte BSN's (als ze bestaan)
    if fixed_bsn_vader:
        gebruikte_bsns.add(fixed_bsn_vader)
    if fixed_bsn_moeder:
        gebruikte_bsns.add(fixed_bsn_moeder)
    
    records = []
    max_attempts = aantal * 50  # Voorkom oneindige loops
    attempts = 0
    
    # Logging variabelen
    bsn_conflicts = 0
    naam_conflicts = 0
    
    while len(records) < aantal and attempts < max_attempts:
        attempts += 1
        geslacht = random.choice(["M", "V"])
        record = generateSingleRecord(args, geslacht, fixed_bsn_vader, fixed_bsn_moeder)
        naam = (record.voornaamKind, record.achternaam)
        
        # Alleen BSN van het kind moet uniek zijn (ouder-BSN's mogen herhaald worden)
        if record.bsn in gebruikte_bsns:
            bsn_conflicts += 1
            continue
            
        # Namen mogen herhaald worden (realistische scenario)
        # Alleen controleren op exacte duplicaten binnen dezelfde set
        if naam in gebruikte_namen:
            naam_conflicts += 1
            continue
        
        # Voeg alleen kind-BSN toe aan gebruikte set
        gebruikte_bsns.add(record.bsn)
        gebruikte_namen.add(naam)
        
        # Voeg ouder-BSN's alleen toe als ze niet gefixed zijn
        if not fixed_bsn_vader:
            gebruikte_bsns.add(record.bsnVader)
        if not fixed_bsn_moeder:
            gebruikte_bsns.add(record.bsnMoeder)
            
        records.append(record)
    
    if len(records) < aantal:
        print(f"Waarschuwing: Kon slechts {len(records)} van {aantal} records genereren na {max_attempts} pogingen")
        print(f"  - BSN conflicten: {bsn_conflicts}")
        print(f"  - Naam conflicten: {naam_conflicts}")
        print(f"  - Totaal gebruikte BSN's: {len(gebruikte_bsns)}")
        print(f"  - Totaal gebruikte namen: {len(gebruikte_namen)}")
        print(f"  - Beschikbare mannelijke namen: {len(voornamen_man)}")
        print(f"  - Beschikbare vrouwelijke namen: {len(voornamen_vrouw)}")
        print(f"  - Beschikbare achternamen: {len(achternamen)}")
        print(f"  - Theoretisch max namen (man): {len(voornamen_man) * len(achternamen)}")
        print(f"  - Theoretisch max namen (vrouw): {len(voornamen_vrouw) * len(achternamen)}")
        
        # Toon een sample van de gebruikte namen
        if len(gebruikte_namen) > 0:
            sample_names = list(gebruikte_namen)[:10]
            print(f"  - Sample gebruikte namen: {sample_names}")
            
        # Brusje modus specifieke info
        if getattr(args, 'brusje', False):
            print(f"  - Brusje modus: Alle kinderen hebben achternaam '{getattr(args, 'achternaam', 'ONBEKEND')}'")
            print(f"  - Brusje modus: Alleen voornamen kunnen variëren")
    
    return records

def generateBrusjeRecords(args, aantal, gebruikte_bsns=None, gebruikte_namen=None):
    """
    Genereert records voor broers en zussen met dezelfde ouders en hetzelfde adres.
    """
    # Genereer fixed BSN's voor brusje modus
    fixed_bsn_vader = random_bsn()
    fixed_bsn_moeder = random_bsn()
    
    print(f"Brusje modus: Fixed BSN voor vader gegenereerd: {fixed_bsn_vader}")
    print(f"Brusje modus: Fixed BSN voor moeder gegenereerd: {fixed_bsn_moeder}")
    
    # Zet alle andere overrides die nodig zijn voor brusje
    if not getattr(args, 'naamvader', None):
        args.naamvader = random.choice(voornamen_man)
        print(f"Brusje modus: Naam vader gezet op: {args.naamvader}")
    
    if not getattr(args, 'naammoeder', None):
        args.naammoeder = random.choice(voornamen_vrouw)
        print(f"Brusje modus: Naam moeder gezet op: {args.naammoeder}")
    
    if not getattr(args, 'achternaam', None):
        args.achternaam = random.choice(achternamen)
        print(f"Brusje modus: Achternaam gezet op: {args.achternaam}")
    
    if not getattr(args, 'adres', None):
        straat = random.choice(straatnamen)
        huisnr = random.randint(1, 100)
        postcode = generate_random_postcode()
        plaats = random.choice(plaatsnamen)
        args.adres = f"{straat} {huisnr} {postcode} {plaats}"
        print(f"Brusje modus: Adres gezet op: {args.adres}")
    
    print("Brusje modus actief: Alle kinderen krijgen dezelfde ouders en hetzelfde adres")
    
    # Roep generateMultipleRecords aan met de gefixeerde BSN's
    return generateMultipleRecords(
        args, 
        aantal, 
        gebruikte_bsns, 
        gebruikte_namen, 
        fixed_bsn_vader, 
        fixed_bsn_moeder
    )

def generateRecords(args, aantal, gebruikte_bsns=None, gebruikte_namen=None):
    """
    Centrale functie voor het genereren van records. Bepaalt automatisch de juiste modus
    op basis van de opgegeven argumenten.
    """
    # Check of brusje modus actief is
    if getattr(args, 'brusje', False):
        return generateBrusjeRecords(args, aantal, gebruikte_bsns, gebruikte_namen)
    
    # Bepaal of er fixed BSN's nodig zijn
    fixed_bsn_vader = None
    fixed_bsn_moeder = None
    
    if getattr(args, 'fixbsnvader', False):
        fixed_bsn_vader = random_bsn()
        print(f"Fixed BSN voor vader gegenereerd: {fixed_bsn_vader}")
    
    if getattr(args, 'fixbsnmoeder', False):
        fixed_bsn_moeder = random_bsn()
        print(f"Fixed BSN voor moeder gegenereerd: {fixed_bsn_moeder}")
    
    # Gebruik de standaard generatie met eventuele fixed BSN's
    return generateMultipleRecords(
        args, 
        aantal, 
        gebruikte_bsns, 
        gebruikte_namen, 
        fixed_bsn_vader, 
        fixed_bsn_moeder
    )

def generateAllRecords(args, aantal_bestanden, aantal_dossiers_per_bestand):
    """
    Genereert alle records voor alle bestanden, met state tracking voor unieke BSN's en namen.
    """
    gebruikte_bsns = set()
    gebruikte_namen = set()
    
    alle_sets = []
    
    print(f"Genereren van {aantal_bestanden} bestanden met {aantal_dossiers_per_bestand} dossiers per bestand")
    print(f"Brusje modus: {getattr(args, 'brusje', False)}")
    print()
    
    for i in range(1, aantal_bestanden + 1):
        print(f"Genereren van bestand {i}/{aantal_bestanden}...")
        
        # In brusje modus: reset namen per bestand omdat elk bestand een andere familie is
        # BSN's blijven globaal uniek
        if getattr(args, 'brusje', False):
            namen_voor_dit_bestand = set()
            print(f"  - Huidige staat: {len(gebruikte_bsns)} gebruikte BSN's (globaal)")
            print(f"  - Brusje modus: Namen worden gereset per bestand (nieuwe familie)")
        else:
            namen_voor_dit_bestand = gebruikte_namen
            print(f"  - Huidige staat: {len(gebruikte_bsns)} gebruikte BSN's, {len(gebruikte_namen)} gebruikte namen")
        
        leerlingen = generateRecords(
            args,
            aantal_dossiers_per_bestand,
            gebruikte_bsns,
            namen_voor_dit_bestand
        )
        
        print(f"  - Resultaat: {len(leerlingen)} records gegenereerd")
        if len(leerlingen) < aantal_dossiers_per_bestand:
            print(f"  - PROBLEEM: Verwachtte {aantal_dossiers_per_bestand} maar kreeg {len(leerlingen)} records")
        
        alle_sets.append(leerlingen)
        
        # Update globale staat alleen als we niet in brusje modus zijn
        if not getattr(args, 'brusje', False):
            gebruikte_namen.update(namen_voor_dit_bestand)
        
        # Logging: toon relevante informatie per modus
        if getattr(args, 'brusje', False):
            print(f"  - Nieuwe staat: {len(gebruikte_bsns)} gebruikte BSN's, {len(namen_voor_dit_bestand)} namen in dit bestand")
        else:
            print(f"  - Nieuwe staat: {len(gebruikte_bsns)} gebruikte BSN's, {len(gebruikte_namen)} gebruikte namen")
        print()
    
    return alle_sets

