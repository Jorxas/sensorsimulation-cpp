# Technischer Einstieg — P06

## P06-T01 lokal prüfen

Im Projektordner ausführen:

~~~powershell
uv run --offline --python 3.12 python -X utf8 nachweise/pruefe_sensorvertrag.py
~~~

Voraussetzung: die vorhandene lokale Python-3.12-Laufzeit über uv; nur die Standardbibliothek, keine Installation. Prüft die sechs unveränderten Datensätze, die Vertragsparameter und sechs erwartete Nachrichten in `projekt.json` sowie acht flüchtige Grenzfälle. Erwartetes Ergebnis: `BESTANDEN`, Exitcode 0. Reproduzierbare Ausgabe der ausgeführten Prüfung: `nachweise/P06-T01-pruefung.txt`. Der Prüfer ist ein Vertragsabgleich und keine Produktimplementierung.

## P06-T02 kompilieren und lokal abnehmen

Tatsächlich verwendeter Compiler: GCC 13.1.0 aus der vorhandenen lokalen Werkzeuginstallation. Die folgende kleine Abnahme verwendet Python 3.12 über uv ausschließlich als Prüftreiber; ausgeführt wird der kompilierte C++-Kern.

~~~powershell
uv run --offline --python 3.12 python -X utf8 nachweise/pruefe_cpp_kern.py --kompilierer 'C:/Program Files/JetBrains/CLion 2025.3.4/bin/mingw/bin/g++.exe'
~~~

Der Prüftreiber ergänzt den Compilerordner nur im Suchpfad seiner Unterprozesse, kompiliert mit `-std=c++17 -Wall -Wextra -Wpedantic -finput-charset=UTF-8 -fexec-charset=UTF-8 src/main.cpp -o ausgabe/sensorsimulation.exe` und führt das Programm aus. Erwartet: Exitcode 0 und `Abnahme BESTANDEN`. Das Protokoll wird unter `nachweise/P06-T02-pruefung.txt` gespeichert. Zehn zusätzliche Messfälle und vier Datei-/Strukturfehler werden nur in einem temporären Unterordner von `ausgabe/` erzeugt; die sechs Originaldatensätze bleiben unverändert.

Direkter Aufruf nach dieser Kompilierung, mit den benötigten Compiler-Laufzeitbibliotheken im prozesslokalen Suchpfad:

~~~powershell
$env:PATH = 'C:/Program Files/JetBrains/CLion 2025.3.4/bin/mingw/bin;' + $env:PATH
./ausgabe/sensorsimulation.exe beispieldaten/temperaturen.csv
~~~

Erwartet sind sechs JSON-Zeilen mit `normal, normal, warnung, warnung, normal, ungueltig`. Ungültige Messwerte sind reguläre Ergebnisse (Exitcode 0); eine falsche Kopfzeile, Spaltenzahl oder Schrittfolge sowie eine fehlende Datei ergeben Exitcode 1. Das unterstützte CSV-Format hat genau zwei unquotierte Spalten, UTF-8, Dezimalpunkt und fortlaufende Indizes ab null. Kein allgemeiner CSV-Parser, keine Echtzeitüberwachung.

## Nächste Aufgabe

P06-T02 ist mit Übergangsfunktion, Einlesen und direkter lokaler Abnahme abgeschlossen. P06-T03 bleibt einer gesonderten Freigabe vorbehalten: CMake und weitere Szenarien. Qt SDK und MQTT-Broker sind erst in ihren eigenen Varianten relevant; keine Ausführung dieser Produkte oder von Hardware behauptet.

Die Zahlenwerte und Regeln dieses Vertrags sind lokale Projektentscheidungen. Vor dem späteren Einbinden eines Frameworks dessen aktuelle offizielle Anleitung lesen.
