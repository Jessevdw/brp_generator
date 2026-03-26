from generators import genereer_a_nummer

def samenstellen_inspoel(records, bestandsnaam="BRP_inspoel.txt"):
    with open(bestandsnaam, "w", encoding="utf-8") as f:
        for r in records:
            a_nummer = genereer_a_nummer()

            a_regel = (
                f"A100000000020200000000126300000000126D4000001261209280330ZAg113000250"
                f"{' ' * 11}{a_nummer}BATCH{' ' * 45}N00000  00000000A00000000{' ' * 13}"
                f"0000{' ' * 10}{r.bsn}{' ' * 17}00000{' ' * 41}X\n"
            )

            b_regels = [
                maak_brp_regel("B010110", a_nummer),                              # A-nummer
                maak_brp_regel("B010120", r.bsn),                                 # Burgerservicenummer
                maak_brp_regel("B010210", r.voornaamKind),                        # Voornamen
                # maak_brp_regel("B01230", )                                      # Voorvoegsel geslachtsnaam
                maak_brp_regel("B010240", r.achternaam),                          # Geslachtsnaam
                maak_brp_regel("B010310", r.geboortedatum.strftime("%Y%m%d")),    # Geboortedatum
                maak_brp_regel("B010320", r.geboorteplaats),                      # Geboorteplaats
                maak_brp_regel("B010330", "Nederland"),                           # Geboorteland
                maak_brp_regel("B010410", r.geslacht),                            # Geslachtsaanduiding
                maak_brp_regel("B080910", r.woonplaats),                          # Gemeente van inschrijving
                maak_brp_regel("B081110", r.straatnaam),                          # Straatnaam
                maak_brp_regel("B081120", str(r.huisnummer)),                     # Huisnummer
                maak_brp_regel("B081160", r.postcode),                            # Postcode
                maak_brp_regel("B020120", r.bsnMoeder),                           # BSN Moeder
                maak_brp_regel("B020210", r.voornaamMoeder),                      # Voornaam moeder
                maak_brp_regel("B020240", r.achternaam),                          # Achternaam moeder zelfde als kind
                maak_brp_regel("B030120", r.bsnVader),                            # BSN Vader
                maak_brp_regel("B030210", r.voornaamVader),                       # Voornaam vader
                maak_brp_regel("B030240", r.achternaam),                          # Achternaam vader zelfde als kind
            ]

            f.write(a_regel)
            f.writelines(regel + "\n" for regel in b_regels)

def maak_brp_regel(code, inhoud):
    inhoud_schoon = str(inhoud).strip()
    prefix = f"{code}  I"
    inhoud_max_len = 264 - len(prefix)
    if len(inhoud_schoon) > inhoud_max_len:
        raise ValueError(f"Inhoud te lang: {inhoud_schoon}")
    regel = prefix + inhoud_schoon.ljust(inhoud_max_len) + "X"
    return regel