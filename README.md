# Sensorsimulation und industrielle Anzeige

Stand: 3. November 2026 — **P06-T02 lokal erledigt und geprüft; C++-Kern umgesetzt**. Veröffentlichung durch den übergeordneten Dienst ausstehend. Geplanter Abschluss der Basis: 2026-11-05, spätestens 8. November 2026. Geschätzter Basisaufwand: 4 Stunden ohne Einrichtung und Erweiterungen.

Ein Prototyp soll Temperaturen überwachen und eine Schwellenüberschreitung melden.

Ergebnis: Portabler C++-Kern mit reproduzierbaren Eingaben; Qt und MQTT als kleine Erweiterungen.

Vorgesehene Technologien: C++, CMake, Linux, Embedded, MQTT/IoT, Qt, UML. Eine Nennung ist kein Nachweis einer Umsetzung.

## Einstieg

1. [Lastenheft](LASTENHEFT.md) lesen.
2. [Erstes Ticket](tickets/P06-T01.md) öffnen.
3. [Technischen Einstieg](START.md) prüfen und ein Ticket nach dem anderen bearbeiten.
4. [Arbeitsjournal](ARBEITSJOURNAL.md) und echte Nachweise aktualisieren.

Abhängigkeiten: keine weiteren Projekte.

## Geprüfter Teilstand P06-T01

Der [Sensorvertrag](tickets/P06-T01.md) beschreibt Zustände, die Warnschwelle von einschließlich 30 °C, den synthetischen Messbereich −40 bis 125 °C und fehlende Daten. [projekt.json](projekt.json) enthält sechs erwartete JSON-Nachrichten zu den unveränderten CSV-Eingaben. Der lokale Abgleich prüft Nachrichtenformat, Reihenfolge und Grenzfälle; [Prüfausgabe](nachweise/P06-T01-pruefung.txt).

Dieser Teilstand ist eine geprüfte Spezifikation; die Ergänzung durch P06-T02 folgt unten.

## Geprüfter C++-Kern P06-T02

[src/main.cpp](src/main.cpp) liest die Temperaturfolge ein und bestimmt pro Messung den Zustand ohne Hysterese. Die Konsole gibt je Schritt eine JSON-Nachricht aus. Ungültige Messwerte ergeben `null`; fehlerhafte CSV-Struktur oder eine fehlende Datei führen zu einer deutschen Fehlermeldung und Exitcode 1 ohne Teilfolge.

Tatsächlich mit GCC 13.1.0 als C++17 ohne Warnungen kompiliert und ausgeführt: sechs unveränderte Originalmessungen, zehn flüchtige Messfälle und vier Datei-/Strukturfehler. [Prüfbefehl](START.md), [Prüfausgabe](nachweise/P06-T02-pruefung.txt). Studentische Schätzung für T02: 90 Minuten; tatsächliche Assistentenzeit und beide Versuche stehen im Journal.

Die direkte Kompilierung dient ausschließlich der Abnahme dieses Kerns. CMake und weitere Szenarien aus P06-T03 sowie UML, Qt, MQTT und Hardware bleiben offen. Alle übergreifenden Lastenheftkriterien bleiben zur gesonderten Gesamtabnahme offen. Die Nutzung des vorhandenen GCC belegt keine praktische Nutzung der CLion-Oberfläche. Hier endet P06-T02; keine Folgephase begonnen.

[Erweiterungen](VARIANTEN.md) haben einen eigenen Umsetzungsstand. [Private Unternehmenszuordnung](UNTERNEHMEN.lokal.md) bleibt außerhalb der Git-Verwaltung.

## Projektsprache

Dokumentation, selbst gewählte Bezeichner, Kommentare, Meldungen und Beispieldaten werden auf Deutsch geschrieben. Festgelegte API-Schlüssel, Sprachsyntax und Produktnamen bleiben unverändert.
