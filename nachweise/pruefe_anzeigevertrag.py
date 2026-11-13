"""P06-T04: C++-Ausgabe mit Anzeigeentwurf und MQTT-Nutzdaten abgleichen."""

import argparse
import csv
import hashlib
import json
import os
import platform
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path


def pruefen():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kompilierer", required=True, type=Path)
    argumente = parser.parse_args()
    projektordner = Path(__file__).resolve().parents[1]
    protokoll = []
    umgebung = os.environ.copy()
    umgebung["PATH"] = str(argumente.kompilierer.parent) + os.pathsep + umgebung["PATH"]

    def melden(text):
        protokoll.append(text)
        print(text, flush=True)

    def verlangen(bedingung, meldung):
        if not bedingung:
            raise RuntimeError(meldung)

    def ausfuehren(befehl):
        melden("Befehl: " + subprocess.list2cmdline([str(teil) for teil in befehl]))
        ergebnis = subprocess.run(befehl, cwd=projektordner, env=umgebung,
                                  capture_output=True, encoding="utf-8", timeout=60)
        melden(f"Exitcode: {ergebnis.returncode}")
        if ergebnis.stdout:
            melden(ergebnis.stdout.rstrip())
        if ergebnis.stderr:
            melden("Fehlerausgabe: " + ergebnis.stderr.rstrip())
        verlangen(ergebnis.returncode == 0, "Befehl fehlgeschlagen")
        return ergebnis

    daten = projektordner / "beispieldaten/temperaturen.csv"
    pruefsumme = "075559d75a4d7ac5cf3bd333c28306ab8b0af09c6ad0437fa41114584b1cbbc1"
    try:
        melden("Prüfbeginn: " + datetime.now().astimezone().isoformat())
        melden("Python: " + platform.python_version())
        konfiguration = json.loads((projektordner / "projekt.json").read_text(encoding="utf-8"))
        vorbereitung = konfiguration["anzeigevorbereitung"]
        verlangen(not any(vorbereitung[feld] for feld in
                           ("qt_ausgefuehrt", "mqtt_ausgefuehrt", "hardware_ausgefuehrt")),
                  "Produktnachweis darf nicht aus diesem Vertragsabgleich abgeleitet werden")
        verlangen(hashlib.sha256(daten.read_bytes()).hexdigest() == pruefsumme,
                  "Originaldaten verändert")
        with daten.open(encoding="utf-8", newline="") as eingabe:
            verlangen(len(list(csv.DictReader(eingabe))) == konfiguration["expectedRecords"] == 6,
                      "Originalanzahl verändert")
        verlangen(vorbereitung["mqtt_vertrag"] == {
            "version": "3.1.1", "broker": "127.0.0.1", "port": 1883,
            "thema": "p06/sensor/temperatur", "qos": 0, "retain": False,
            "clean_session": True, "kodierung": "UTF-8",
            "nutzdaten": "sensorvertrag.nachrichten",
        }, "Transportkonfiguration weicht vom dokumentierten lokalen Vertrag ab")
        ausfuehren([argumente.kompilierer, "--version"])
        ausgabeordner = projektordner / "ausgabe"
        ausgabeordner.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="anzeige-t04-", dir=ausgabeordner) as ordner:
            programm = Path(ordner) / "sensorsimulation.exe"
            bau = ausfuehren([
                argumente.kompilierer, "-std=c++17", "-Wall", "-Wextra", "-Wpedantic",
                "-finput-charset=UTF-8", "-fexec-charset=UTF-8",
                projektordner / "src/main.cpp", "-o", programm,
            ])
            verlangen(not bau.stderr, "Compilerwarnungen prüfen")
            ergebnis = ausfuehren([programm, daten])
            verlangen(not ergebnis.stderr, "Unerwartete Fehlerausgabe der Konsole")
            nachrichten = [json.loads(zeile) for zeile in ergebnis.stdout.splitlines()]
        verlangen(nachrichten == konfiguration["sensorvertrag"]["nachrichten"],
                  "C++-Nutzdaten weichen vom Sensorvertrag ab")
        verlangen(len(nachrichten) == 6, "Sechs Nachrichten erwartet")

        # Nur Textprojektion der Skizze, kein Qt und keine MQTT-Übertragung.
        erwartet = [
            ("20 °C", "Normal", "messwert"), ("25 °C", "Normal", "messwert"),
            ("31 °C", "Warnung", "messwert"), ("30 °C", "Warnung", "messwert"),
            ("29 °C", "Normal", "messwert"), ("— °C", "Ungültig", "nicht_numerisch"),
        ]
        for schritt, (nachricht, soll) in enumerate(zip(nachrichten, erwartet)):
            verlangen(type(nachricht["schritt"]) is int and nachricht["schritt"] == schritt,
                      "Schrittindex oder Typ abweichend")
            wert = nachricht["temperatur_celsius"]
            temperatur = (vorbereitung["fehlender_wert"] if wert is None
                          else format(wert, "g").replace(".", ","))
            beobachtet = (temperatur + " °C",
                          vorbereitung["anzeigetexte"][nachricht["zustand"]], nachricht["grund"])
            verlangen(beobachtet == soll, "Anzeigeskizze und Konsole widersprechen sich")
            melden(f"BESTANDEN Textprojektion {schritt}: " + " | ".join(beobachtet))
        verlangen(hashlib.sha256(daten.read_bytes()).hexdigest() == pruefsumme,
                  "Originaldaten während der Prüfung verändert")
        melden("Originaldaten unverändert: 6 Messungen, SHA256 " + pruefsumme)
        melden("Abnahme BESTANDEN: Konsole, sechs Nutzdaten und geplante Textprojektionen konsistent.")
        melden("Grenze: Qt, MQTT und Hardware nicht ausgeführt; keine Transport- oder GUI-Abnahme.")
    except Exception as fehler:
        melden("Abnahme FEHLGESCHLAGEN: " + str(fehler))
        raise
    finally:
        melden("Prüfende: " + datetime.now().astimezone().isoformat())
        (projektordner / "nachweise/P06-T04-pruefung.txt").write_text(
            "\n".join(protokoll) + "\n", encoding="utf-8")


if __name__ == "__main__":
    pruefen()
