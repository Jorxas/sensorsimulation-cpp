"""Kleine lokale Abnahme des echten C++-Kerns für P06-T02, ohne CMake."""

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
    argumentparser.add_argument("--kompilierer", required=True, type=Path)
    argumente = argumentparser.parse_args()
    projektordner = Path(__file__).resolve().parents[1]
    ausgabeordner = projektordner / "ausgabe"
    ausgabeordner.mkdir(exist_ok=True)
    protokoll = []

    def melden(text):
        protokoll.append(text)
        print(text, flush=True)

    umgebung = os.environ.copy()
    umgebung["PATH"] = str(argumente.kompilierer.parent) + os.pathsep + umgebung["PATH"]

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

    try:
        melden("Prüfbeginn: " + datetime.now().astimezone().isoformat())
        version = ausfuehren([argumente.kompilierer, "--version"])
        assert version.returncode == 0, "Compiler nicht ausführbar"
        programm = ausgabeordner / "sensorsimulation.exe"
        kompilierung = ausfuehren([
            argumente.kompilierer, "-std=c++17", "-Wall", "-Wextra", "-Wpedantic",
            "-finput-charset=UTF-8", "-fexec-charset=UTF-8",
            "src/main.cpp", "-o", programm,
        ])
        assert kompilierung.returncode == 0, "Kompilierung fehlgeschlagen"
        assert not kompilierung.stderr, "Compiler meldet Warnungen"
        konfiguration = json.loads((projektordner / "projekt.json").read_text(encoding="utf-8"))
        daten = projektordner / konfiguration["fixture"]
        pruefsumme = hashlib.sha256(daten.read_bytes()).hexdigest()
        assert pruefsumme == "075559d75a4d7ac5cf3bd333c28306ab8b0af09c6ad0437fa41114584b1cbbc1", "Originaldaten verändert"
        ergebnis = ausfuehren([programm, daten])
        assert ergebnis.returncode == 0 and not ergebnis.stderr
        nachrichten = [json.loads(zeile) for zeile in ergebnis.stdout.splitlines()]
        assert nachrichten == konfiguration["sensorvertrag"]["nachrichten"]
        assert len(nachrichten) == konfiguration["expectedRecords"] == 6
        melden("BESTANDEN: sechs Originalmessungen entsprechen dem Sensorvertrag; SHA256 " + pruefsumme)

        # Flüchtige Eingaben ergänzen die Originaldaten nicht.
        with tempfile.TemporaryDirectory(prefix="kernpruefung-", dir=ausgabeordner) as ordner:
            pruefdatei = Path(ordner) / "temperaturen.csv"
            faelle = [
                ("", None, "ungueltig", "fehlend"),
                ("NaN", None, "ungueltig", "nicht_endlich"),
                ("Infinity", None, "ungueltig", "nicht_endlich"),
                ("-41", None, "ungueltig", "ausserhalb_messbereich"),
                ("126", None, "ungueltig", "ausserhalb_messbereich"),
                ("-40", -40, "normal", "messwert"),
                ("125", 125, "warnung", "messwert"),
                ("29.5", 29.5, "normal", "messwert"),
                ("20rest", None, "ungueltig", "nicht_numerisch"),
                ("20", 20, "normal", "messwert"),
            ]
            pruefdatei.write_text("schritt,temperatur\n" + "".join(
                f"{schritt},{fall[0]}\n" for schritt, fall in enumerate(faelle)
            ), encoding="utf-8")
            ergebnis = ausfuehren([programm, pruefdatei])
            assert ergebnis.returncode == 0 and not ergebnis.stderr
            nachrichten = [json.loads(zeile) for zeile in ergebnis.stdout.splitlines()]
            assert nachrichten == [
                dict(schritt=schritt, temperatur_celsius=wert, einheit="°C", zustand=zustand, grund=grund)
                for schritt, (_, wert, zustand, grund) in enumerate(faelle)
            ]
            melden("BESTANDEN: zehn flüchtige Messfälle einschließlich Erholung nach ungültigem Wert.")
            for inhalt in ["falscher,kopf\n0,20\n", "schritt,temperatur\n0,20\n2,25\n",
                           "schritt,temperatur\n0,20,30\n"]:
                pruefdatei.write_text(inhalt, encoding="utf-8")
                ergebnis = ausfuehren([programm, pruefdatei])
                assert ergebnis.returncode == 1 and not ergebnis.stdout
                assert ergebnis.stderr.startswith("Fehler: ")
            ergebnis = ausfuehren([programm, Path(ordner) / "fehlt.csv"])
            assert ergebnis.returncode == 1 and not ergebnis.stdout
            assert ergebnis.stderr.startswith("Fehler: ")
            melden("BESTANDEN: drei Strukturfehler und fehlende Datei werden ohne Teilfolge abgewiesen.")
        melden("Abnahme BESTANDEN. Grenze: C++-Konsole; kein CMake-, Qt-, MQTT- oder Hardware-Nachweis.")
    finally:
        melden("Prüfende: " + datetime.now().astimezone().isoformat())
        (projektordner / "nachweise/P06-T02-pruefung.txt").write_text(
            "\n".join(protokoll) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    pruefen()
