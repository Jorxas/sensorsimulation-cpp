"""P06-T03: frischer CMake-Bau und kleine Abnahme der C++-Konsole."""

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path


def pruefen():
    argumentparser = argparse.ArgumentParser(description=__doc__)
    for name in ("cmake", "ninja", "kompilierer"):
        argumentparser.add_argument("--" + name, required=True, type=Path)
    argumente = argumentparser.parse_args()
    projektordner = Path(__file__).resolve().parents[1]
    ausgabeordner = projektordner / "ausgabe"
    ausgabeordner.mkdir(exist_ok=True)
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
        ergebnis = subprocess.run(
            befehl, cwd=projektordner, env=umgebung, capture_output=True,
            encoding="utf-8", errors="strict", timeout=60,
        )
        melden(f"Exitcode: {ergebnis.returncode}")
        if ergebnis.stdout:
            melden(ergebnis.stdout.rstrip())
        if ergebnis.stderr:
            melden("Fehlerausgabe: " + ergebnis.stderr.rstrip())
        return ergebnis

    def nachricht(schritt, wert, zustand, grund="messwert"):
        return dict(schritt=schritt, temperatur_celsius=wert, einheit="°C",
                    zustand=zustand, grund=grund)

    daten = projektordner / "beispieldaten/temperaturen.csv"
    pruefsumme = "075559d75a4d7ac5cf3bd333c28306ab8b0af09c6ad0437fa41114584b1cbbc1"
    try:
        melden("Prüfbeginn: " + datetime.now().astimezone().isoformat())
        for werkzeug in (argumente.cmake, argumente.ninja, argumente.kompilierer):
            verlangen(ausfuehren([werkzeug, "--version"]).returncode == 0,
                      "Werkzeug nicht ausführbar")
        verlangen(hashlib.sha256(daten.read_bytes()).hexdigest() == pruefsumme,
                  "Originaldaten verändert")
        konfiguration = json.loads((projektordner / "projekt.json").read_text(encoding="utf-8"))

        # Ein frischer Bauordner schließt die Wiederverwendung einer alten EXE aus.
        with tempfile.TemporaryDirectory(prefix="cmake-t03-", dir=ausgabeordner) as ordner:
            bauordner = Path(ordner) / "bau"
            verlangen(ausfuehren([
                argumente.cmake, "-S", projektordner, "-B", bauordner, "-G", "Ninja",
                "-DCMAKE_MAKE_PROGRAM=" + argumente.ninja.as_posix(),
                "-DCMAKE_CXX_COMPILER=" + argumente.kompilierer.as_posix(),
                "-DCMAKE_BUILD_TYPE=Debug",
            ]).returncode == 0, "CMake-Konfiguration fehlgeschlagen")
            verlangen(ausfuehren([argumente.cmake, "--build", bauordner, "--verbose"]).returncode == 0,
                      "CMake-Bau fehlgeschlagen")
            programm = bauordner / "sensorsimulation.exe"
            verlangen(programm.is_file(), "Frisch gebautes Programm fehlt")

            def messungen_pruefen(name, datei, erwartet):
                melden("Szenario: " + name)
                ergebnis = ausfuehren([programm, datei])
                verlangen(ergebnis.returncode == 0 and not ergebnis.stderr,
                          "Messfolge nicht erfolgreich ausgeführt")
                beobachtet = [json.loads(zeile) for zeile in ergebnis.stdout.splitlines()]
                verlangen(beobachtet == erwartet, "Nachrichten weichen vom Soll ab")
                melden("BESTANDEN: " + name)

            verlangen(konfiguration["expectedRecords"] == 6, "Originalanzahl verändert")
            messungen_pruefen("sechs Originalmessungen einschließlich Normalfall", daten,
                               konfiguration["sensorvertrag"]["nachrichten"])
            pruefdatei = Path(ordner) / "grenzwert.csv"
            inhalt = "schritt,temperatur\n0,29.5\n1,30\n2,30.5\n3,29.5\n"
            pruefdatei.write_text(inhalt, encoding="utf-8")
            melden("Flüchtige Grenzwerteingabe:\n" + inhalt.rstrip())
            messungen_pruefen("Warnschwelle einschließlich 30 °C und Rückkehr", pruefdatei, [
                nachricht(0, 29.5, "normal"), nachricht(1, 30, "warnung"),
                nachricht(2, 30.5, "warnung"), nachricht(3, 29.5, "normal"),
            ])
            pruefdatei = Path(ordner) / "ungueltig.csv"
            inhalt = "schritt,temperatur\n0,ungueltig\n1,20\n"
            pruefdatei.write_text(inhalt, encoding="utf-8")
            melden("Flüchtige ungültige Messung mit Erholung:\n" + inhalt.rstrip())
            messungen_pruefen("ungültiger Messwert und Erholung", pruefdatei, [
                nachricht(0, None, "ungueltig", "nicht_numerisch"),
                nachricht(1, 20, "normal"),
            ])
            inhalt = "schritt,temperatur\n0,20\n2,25\n"
            pruefdatei.write_text(inhalt, encoding="utf-8")
            melden("Flüchtige fehlerhafte Schrittfolge:\n" + inhalt.rstrip())
            ergebnis = ausfuehren([programm, pruefdatei])
            verlangen(ergebnis.returncode == 1 and not ergebnis.stdout
                      and ergebnis.stderr.strip() ==
                      "Fehler: Ungueltige CSV-Struktur oder Schrittfolge in Zeile 3.",
                      "Strukturfehler nicht wie erwartet abgewiesen")
            melden("BESTANDEN: ungültige CSV-Struktur, Exitcode 1 ohne Teilfolge")
        verlangen(hashlib.sha256(daten.read_bytes()).hexdigest() == pruefsumme,
                  "Originaldaten während der Prüfung verändert")
        melden("Originaldaten unverändert: 6 Messungen, SHA256 " + pruefsumme)
        melden("Abnahme BESTANDEN. Nur CMake und C++-Konsole; UML, Qt, MQTT und Hardware offen.")
    except Exception as fehler:
        melden("Abnahme FEHLGESCHLAGEN: " + str(fehler))
        raise
    finally:
        melden("Prüfende: " + datetime.now().astimezone().isoformat())
        (projektordner / "nachweise/P06-T03-pruefung.txt").write_text(
            "\n".join(protokoll) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    pruefen()
