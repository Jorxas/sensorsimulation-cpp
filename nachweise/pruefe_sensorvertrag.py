"""Lokaler Vertragsabgleich für P06-T01, kein ausführbarer C++-Sensorkern."""

import csv
import hashlib
import json
import math
import platform
from datetime import datetime
from pathlib import Path


projektordner = Path(__file__).resolve().parents[1]
konfiguration = json.loads((projektordner / "projekt.json").read_text(encoding="utf-8"))
vertrag = konfiguration["sensorvertrag"]
datendatei = projektordner / konfiguration["fixture"]
pruefsumme = hashlib.sha256(datendatei.read_bytes()).hexdigest()
assert pruefsumme == "075559d75a4d7ac5cf3bd333c28306ab8b0af09c6ad0437fa41114584b1cbbc1", "Originaldaten verändert"
with datendatei.open(encoding="utf-8", newline="") as eingabe:
    leser = csv.DictReader(eingabe)
    assert leser.fieldnames == ["schritt", "temperatur"], "CSV-Kopfzeile abweichend"
    zeilen = list(leser)
assert len(zeilen) == konfiguration["expectedRecords"] == 6, "Genau sechs Originaldatensätze erwartet"
assert (vertrag["minimum_celsius"], vertrag["warnschwelle_celsius"], vertrag["maximum_celsius"]) == (-40, 30, 125), "Vertragsgrenzen abweichend"
assert vertrag["einheit"] == "°C", "Einheit abweichend"
assert vertrag["zustaende"] == ["normal", "warnung", "ungueltig"], "Zustandsmenge abweichend"
nachrichten = vertrag["nachrichten"]
assert len(nachrichten) == len(zeilen), "Nachrichtenanzahl abweichend"

# Zusätzliche flüchtige Prüfeingaben; die sechs Beispieldatensätze bleiben unverändert.
grenzfaelle = [
    (None, None, "ungueltig", "fehlend"),
    ("", None, "ungueltig", "fehlend"),
    ("NaN", None, "ungueltig", "nicht_endlich"),
    ("Infinity", None, "ungueltig", "nicht_endlich"),
    ("-41", None, "ungueltig", "ausserhalb_messbereich"),
    ("126", None, "ungueltig", "ausserhalb_messbereich"),
    ("-40", -40, "normal", "messwert"),
    ("125", 125, "warnung", "messwert"),
]
prueffaelle = []
for schritt, (zeile, nachricht) in enumerate(zip(zeilen, nachrichten)):
    assert set(zeile) == {"schritt", "temperatur"}, "Falsche CSV-Spaltenzahl"
    assert zeile["schritt"] == str(schritt), "CSV-Sequenzindex abweichend"
    assert set(nachricht) == {"schritt", "temperatur_celsius", "einheit", "zustand", "grund"}, "Nachrichtenfelder abweichend"
    assert type(nachricht["schritt"]) is int and nachricht["schritt"] == schritt, "Nachrichtenindex abweichend"
    assert nachricht["einheit"] == vertrag["einheit"], "Nachrichteneinheit abweichend"
    zahl = nachricht["temperatur_celsius"]
    assert zahl is None or (type(zahl) in (int, float) and math.isfinite(zahl)), "JSON-Zahl ungültig"
    prueffaelle.append((zeile["temperatur"], zahl, nachricht["zustand"], nachricht["grund"]))

print(f"Prüfzeit: {datetime.now().astimezone().isoformat(timespec='seconds')}")
print(f"Python: {platform.python_version()}")
print(f"Originaldaten: 6 Datensätze; SHA256 {pruefsumme}")
for nummer, (rohwert, sollwert, sollzustand, sollgrund) in enumerate(prueffaelle + grenzfaelle):
    wert, zustand, grund = None, "ungueltig", "fehlend"
    if rohwert is not None and rohwert.strip():
        try:
            zahl = float(rohwert)
        except ValueError:
            grund = "nicht_numerisch"
        else:
            if not math.isfinite(zahl):
                grund = "nicht_endlich"
            elif not vertrag["minimum_celsius"] <= zahl <= vertrag["maximum_celsius"]:
                grund = "ausserhalb_messbereich"
            else:
                wert, grund = zahl, "messwert"
                zustand = "warnung" if zahl >= vertrag["warnschwelle_celsius"] else "normal"
    assert (wert, zustand, grund) == (sollwert, sollzustand, sollgrund), f"Vertragsabweichung in Prüffall {nummer}: {rohwert!r}"
    print(f"OK {nummer}: Eingabe {rohwert!r} -> {zustand}, {wert}, {grund}")
print("BESTANDEN: 6 erwartete Nachrichten und 8 ergänzende Grenzfälle konsistent.")
print("Grenze: Dokumentationsprüfung; kein C++-Kern, keine Zeiterkennung, kein Qt/MQTT/Hardware-Nachweis.")
