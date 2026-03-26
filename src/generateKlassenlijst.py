from dataclasses import dataclass

@dataclass
class schoolRecord:
    def __init__(
        self,
        brinCode=None,
        klasOfGroep=None,
        klasnummer=None,
        naamKlas=None,
        onderwijssoort=None
    ):
        self.brinCode = brinCode or "BRIN"
        self.klasOfGroep = klasOfGroep or "groep"
        self.klasnummer = klasnummer or "6"
        self.naamKlas = naamKlas or ""
        self.onderwijssoort = onderwijssoort or "01"

# ONDERWIJSSOORTEN                      ID
#------------------------------------------
# Basisonderwijs                        01
# Basisvorming VMBO/HAVO                02
# Basisvorming HAVO/VWO/Gymnasium       04
# VMBO theoretische leerweg             05
# VMBO overig                           06
# IVBO of VBO                           07
# MAVO                                  08
# Leerlingwezen of KMBO                 09
# HAVO                                  10
# VWO                                   11
# MBO                                   12
# HBO                                   13
# Universiteit                          14
# Speciaal basisonderwijs               15
# Speciaal Boortgezet Onderwijs         16
# REC                                   17
# Praktijkonderwijs                     18
# Geen                                  19
# Anders                                98
# Onbekend                              99

def samenstellen_klassenlijst(records, args, bestandsnaam="klassenlijst.csv"):
    # Maak schoolRecord aan op basis van args
    school_record = schoolRecord(
        brinCode=args.brin,
        klasOfGroep=args.klas_of_groep,
        klasnummer=args.klasnummer,
        naamKlas=args.naam_klas,
        onderwijssoort=args.onderwijssoort
    )
    
    header = [
        "BRIN-vestigingsnummer", "Klas of groep", "Klas- of groepnummer", "Naam klas", "Onderwijssoort",
        "Zorgpad", "BSN", "Team", "Geboortedatum", "Geslacht", "Achternaam", "Tussenvoegsel",
        "Roepnaam", "Telefoonnummer", "Telefoonnummer 2", "Postcode", "Huisnummer",
        "Voornaam contactpersoon", "Achternaam contactpersoon", "Telefoonnummer contactpersoon",
        "Functie contactpersoon", "Email contactpersoon"
    ]
    with open(bestandsnaam, "w", encoding="utf-8") as f:
        f.write(";".join(header) + "\n")
        for r in records:
            velden = [
                school_record.brinCode,                # BRIN-vestigingsnummer
                school_record.klasOfGroep,             # Klas of groep
                school_record.klasnummer,              # Klas- of groepnummer
                school_record.naamKlas,                # Naam klas
                school_record.onderwijssoort,          # Onderwijssoort
                "",                                   # Zorgpad
                r.bsn,                                # BSN
                "",                                   # Team
                r.geboortedatum.strftime("%d-%m-%Y"), # Geboortedatum
                r.geslacht,                           # Geslacht
                r.achternaam,                         # Achternaam
                "",                                   # Tussenvoegsel
                r.voornaamKind,                       # Roepnaam
                "",                                   # Telefoonnummer
                "",                                   # Telefoonnummer 2
                r.postcode,                           # Postcode
                "",                                   # Huisnummer
                "",                                   # Voornaam contactpersoon
                "",                                   # Achternaam contactpersoon
                "",                                   # Telefoonnummer contactpersoon
                "",                                   # Functie contactpersoon
                ""                                    # Email contactpersoon
            ]
            f.write(";".join(velden) + "\n")