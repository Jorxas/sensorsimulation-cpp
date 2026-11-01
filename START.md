# Technischer Einstieg — P06

## P06-T01 lokal prüfen

Im Projektordner ausführen:

~~~powershell
uv run --offline --python 3.12 python -X utf8 nachweise/pruefe_sensorvertrag.py
~~~

Voraussetzung: die vorhandene lokale Python-3.12-Laufzeit über uv; nur die Standardbibliothek, keine Installation. Prüft die sechs unveränderten Datensätze, die Vertragsparameter und sechs erwartete Nachrichten in `projekt.json` sowie acht flüchtige Grenzfälle. Erwartetes Ergebnis: `BESTANDEN`, Exitcode 0. Reproduzierbare Ausgabe der ausgeführten Prüfung: `nachweise/P06-T01-pruefung.txt`. Der Prüfer ist ein Vertragsabgleich und keine Produktimplementierung.

## Einstiegspunkt ausführen

Für spätere Phasen: C++-Compiler und CMake; Qt SDK nur für die grafische Variante; lokaler MQTT-Broker nur für die MQTT-Variante. In P06-T01 wurden diese Werkzeuge nicht ausgeführt.

~~~powershell
cmake -S . -B build
cmake --build build
~~~

Das Startprogramm meldet den Initialisierungsstand. Fachfunktionen sind bewusst noch nicht implementiert und melden dies bei einem Aufruf. Fehlende Bibliotheken und Frameworks erst im passenden Ticket mit ihrer tatsächlichen Version ergänzen.

## Nächste Aufgabe

P06-T01 ist mit dem lokal geprüften [Sensorvertrag](tickets/P06-T01.md) abgeschlossen. Erst in einer später freigegebenen Phase P06-T02 die C++-Übergangsfunktion und das Einlesen entwickeln.

Die Zahlenwerte und Regeln dieses Vertrags sind lokale Projektentscheidungen. Vor dem späteren Einbinden eines Frameworks dessen aktuelle offizielle Anleitung lesen.
