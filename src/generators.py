import data.adressen as adressen
from datetime import datetime, timedelta
import random
import string
import os

def genereer_unieke_mapnaam(prefix="BRP_serie_", basispad="../output"):
    teller = 1
    while True:
        mapnaam = os.path.join(basispad, f"{prefix}{teller}")
        if not os.path.exists(mapnaam):
            os.makedirs(mapnaam)
            return mapnaam
        teller += 1


def genereer_a_nummer():
    while True:
        cijfers = [random.randint(0, 9) for _ in range(10)]
        if cijfers[0] == 0:
            continue
        if any(cijfers[i] == cijfers[i + 1] for i in range(9)):
            continue
        som = sum(cijfers)
        if som % 11 not in (0, 5):
            continue
        gewogen_som = sum(c * (2 ** i) for i, c in enumerate(cijfers))
        if gewogen_som % 11 != 0:
            continue
        return ''.join(str(c) for c in cijfers)

def get_adressen_dataset(klant=None):
    if klant:
        # Dynamisch zoeken naar dataset, bv. postcode_range_zuid_limburg
        try:
            postcode_range = getattr(adressen, f"postcode_range_{klant}")
            postcode_letters = getattr(adressen, f"postcode_letters_{klant}")
            plaatsnamen = getattr(adressen, f"plaatsnamen_{klant}")
        except AttributeError:
            raise ValueError(f"Geen adresdataset gevonden voor klant '{klant}'. Voeg deze toe aan adressen.py.")
    else:
        postcode_range = adressen.postcode_range
        postcode_letters = adressen.postcode_letters
        plaatsnamen = adressen.plaatsnamen
    return postcode_range, postcode_letters, plaatsnamen

def generate_random_postcode(klant=None):
    postcode_range, postcode_letters, _ = get_adressen_dataset(klant)
    nummer = str(random.choice(postcode_range))
    letters = random.choice(postcode_letters)
    return f"{nummer}{letters}"

def random_bsn():
    def is_geldig_bsn(bsn_str):
        if len(bsn_str) != 9 or not bsn_str.isdigit():
            return False
        totaal = sum(int(cijfer) * (9 - i) for i, cijfer in enumerate(bsn_str[:8]))
        totaal -= int(bsn_str[8])
        return totaal % 11 == 0

    while True:
        bsn = random.randint(100000000, 999999999)
        if is_geldig_bsn(str(bsn)):
            return str(bsn)


def random_datum(minimum_leeftijd, maximum_leeftijd=None, eenheid="jaar"):
    """
    Genereert een willekeurige geboortedatum tussen minimum en maximum leeftijd.

    Args:
        minimum_leeftijd (int/float): Minimale leeftijd
        maximum_leeftijd (int/float, optional): Maximale leeftijd. 
            Als niet opgegeven, wordt minimum_leeftijd als maximum gebruikt.
        eenheid (str): Eenheid van leeftijd: "jaar", "maand", "dag" (default: "jaar")

    Returns:
        datetime.date: Geboortedatum die resulteert in een leeftijd tussen min en max
    """
    if maximum_leeftijd is None:
        maximum_leeftijd = minimum_leeftijd

    if minimum_leeftijd > maximum_leeftijd:
        raise ValueError("Minimum leeftijd kan niet groter zijn dan maximum leeftijd")

    huidige_datum = datetime.today()

    # Bereken het aantal dagen voor min/max leeftijd afhankelijk van eenheid
    if eenheid == "jaar":
        min_leeftijd_dagen = int(minimum_leeftijd * 365.25)
        max_leeftijd_dagen = int(maximum_leeftijd * 365.25)
    elif eenheid == "maand":
        min_leeftijd_dagen = int(minimum_leeftijd * 30.44)
        max_leeftijd_dagen = int(maximum_leeftijd * 30.44)
    elif eenheid == "dag":
        min_leeftijd_dagen = int(minimum_leeftijd)
        max_leeftijd_dagen = int(maximum_leeftijd)
    else:
        raise ValueError(f"Ongeldige eenheid: {eenheid}. Kies uit 'jaar', 'maand', 'dag'.")

    # min_geboortedatum = jongste toegestane geboortedatum (dus recentste, bijv. 1 dag geleden)
    min_geboortedatum = huidige_datum - timedelta(days=min_leeftijd_dagen)
    # max_geboortedatum = oudste toegestane geboortedatum (bijv. 31 dagen geleden)
    max_geboortedatum = huidige_datum - timedelta(days=max_leeftijd_dagen)

    delta = (min_geboortedatum - max_geboortedatum).days
    if delta <= 0:
        random_date = min_geboortedatum
    else:
        random_date = max_geboortedatum + timedelta(days=random.randint(0, delta))

    # Valideer dat de gegenereerde datum resulteert in de juiste leeftijd
    leeftijd_dagen = (huidige_datum - random_date).days
    if eenheid == "jaar":
        leeftijd = leeftijd_dagen / 365.25
    elif eenheid == "maand":
        leeftijd = leeftijd_dagen / 30.44
    elif eenheid == "dag":
        leeftijd = leeftijd_dagen
    else:
        leeftijd = None

    # Sta kleine afrondingsfouten toe bij floats
    if leeftijd < minimum_leeftijd - 0.01 or leeftijd > maximum_leeftijd + 0.01:
        # Als validatie faalt, probeer het opnieuw (max 10x, daarna forceer min_geboortedatum)
        for _ in range(10):
            if delta <= 0:
                random_date = min_geboortedatum
            else:
                random_date = max_geboortedatum + timedelta(days=random.randint(0, delta))
            leeftijd_dagen = (huidige_datum - random_date).days
            if eenheid == "jaar":
                leeftijd = leeftijd_dagen / 365.25
            elif eenheid == "maand":
                leeftijd = leeftijd_dagen / 30.44
            elif eenheid == "dag":
                leeftijd = leeftijd_dagen
            if minimum_leeftijd - 0.01 <= leeftijd <= maximum_leeftijd + 0.01:
                break
        else:
            random_date = min_geboortedatum
    return random_date.date()