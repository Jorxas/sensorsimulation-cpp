# Lastenheft — P06

## Zielgruppe und Problem

Ein Prototyp soll Temperaturen überwachen und eine Schwellenüberschreitung melden.

## Studentischer Umfang

Portabler C++-Kern mit reproduzierbaren Eingaben; Qt und MQTT als kleine Erweiterungen.

Lokale Einzelbenutzung, synthetische Daten und ein vorführbarer kleiner Ablauf. Umfang bewusst begrenzen, damit eine erste Version innerhalb der Zielwoche möglich bleibt.

## Abnahmekriterien

- [ ] A1 — Normalzustand, Warnung und ungültigen Sensorwert unterscheiden.
- [ ] A2 — Kern ohne Hardware kompilieren und fehlerhafte Eingabe behandeln.
- [ ] A3 — Zustandsübergänge in einem kleinen UML-Diagramm darstellen.
- [ ] A4 — Konsole, Qt, MQTT und physische Hardware jeweils getrennt nachweisen.

## Voraussetzungen

- C++-Compiler
- CMake
- Qt SDK für die grafische Variante
- Lokaler MQTT-Broker für die MQTT-Variante

## Fünfminütige Vorführung

Eine Temperaturfolge oberhalb und anschließend unterhalb des Grenzwerts wiedergeben.

Eine gültige Eingabe, einen Fehlerfall, das Ergebnis und die zuständige Quellcodedatei zeigen. Eine technische Entscheidung und eine Grenze erklären.

## Lieferumfang

- Genaue Startbefehle, verwendete Versionen und Beispieldaten.
- Tatsächlich durchgeführte Abnahme mit Ergebnissen und einem geeigneten Nachweis.
- Aktualisierte Tickets und Journal sowie ein lokaler Commit zum realen Fortschritt.
- Verständlicher Quellcode und nachvollziehbare Unterstützung durch den Assistenten.

## Grenzen

Öffentliche Bereitstellung und Produktivbetrieb gehören nicht zur Basis. Jede Werkzeugvariante benötigt einen eigenen Ausführungsnachweis. Zertifizierung, Berufserfahrung, Sprachniveau und Teamarbeit folgen nicht automatisch aus dieser Übung.

## Spätere Verwendung im Lebenslauf

C++-Sensorsimulation; fehlende Hardware und tatsächlich ausgeführte Erweiterungen ausdrücklich nennen.

Derzeit zutreffend: „Eigenes Lernprojekt in Vorbereitung: Sensorsimulation und industrielle Anzeige“. „Umgesetzt“ setzt die tatsächliche Abnahme voraus.
