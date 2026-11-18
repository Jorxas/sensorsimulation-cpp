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

## P06-T03 mit CMake kompilieren und Szenarien prüfen

Im Projektordner mit den vorhandenen lokalen Werkzeugen ausführen:

~~~powershell
uv run --offline --python 3.12 python -X utf8 nachweise/pruefe_cmake_szenarien.py --cmake 'C:/Program Files/JetBrains/CLion 2025.3.4/bin/cmake/win/x64/bin/cmake.exe' --ninja 'C:/Program Files/JetBrains/CLion 2025.3.4/bin/ninja/win/x64/ninja.exe' --kompilierer 'C:/Program Files/JetBrains/CLion 2025.3.4/bin/mingw/bin/g++.exe'
~~~

Tatsächlich verwendet: CMake 4.1.2, Ninja 1.12.1, GCC 13.1.0 unter Windows. Python ist nur Prüftreiber (Standardbibliothek); die Ausgaben stammen aus der frisch kompilierten C++-Konsole. Die Werkzeugpfade können bei einer anderen lokalen Installation über die drei Argumente angepasst werden. Kein Download nötig.

Der Prüfer führt `cmake -S <Projektordner> -B <frischer Bauordner> -G Ninja -DCMAKE_MAKE_PROGRAM=<Ninja-Pfad> -DCMAKE_CXX_COMPILER=<GCC-Pfad> -DCMAKE_BUILD_TYPE=Debug` und danach `cmake --build <Bauordner> --verbose` aus. Die vollständigen konkreten Befehle und Werkzeugversionen stehen im Protokoll. `CMakeLists.txt` fordert mindestens C++17 für das Ziel `sensorsimulation`; der verwendete GCC erfüllt dies bereits mit seinem Standardmodus. Quellcode und CMake-Konfiguration mussten für diesen Endpunkt nicht geändert werden.

Anschließend: sechs Originalmessungen, Grenzwertfolge 29,5 / 30 / 30,5 / 29,5 °C, ungültiger Messwert mit Erholung sowie eine falsche CSV-Schrittfolge. Vollständige JSON-Nachrichten werden verglichen. Die Messfolgen müssen Exitcode 0 ergeben, die falsche Struktur Exitcode 1 ohne Standardausgabe. Erwarteter Gesamtausgang: `Abnahme BESTANDEN`, Exitcode 0; Protokoll `nachweise/P06-T03-pruefung.txt`.

Alle zusätzlichen CSV-Eingaben stehen im Prüfskript und werden samt frischem Bau ausschließlich vorübergehend unter `ausgabe/` angelegt und anschließend entfernt. Die Originaldatei bleibt mit sechs Einträgen und unveränderter SHA256-Prüfsumme erhalten. Zur Wiederholung benötigt: `nachweise/pruefe_cmake_szenarien.py`, `CMakeLists.txt`, `src/main.cpp`, `projekt.json`, `beispieldaten/temperaturen.csv` und die oben genannten lokalen Laufzeiten. Keine weiteren Testquellen oder Bibliotheken erforderlich.

## Abgrenzung nach P06-T03

P06-T03 endete nach CMake-Bau und Szenarien. UML sowie Lastenheft-Gesamtabnahme bleiben offen; der später freigegebene Vorbereitungsschritt T04 steht unten. Qt SDK, MQTT-Broker und Hardware sind nur in gesonderten Varianten relevant. Die Werkzeugausführung unter Windows belegt keine Nutzung von Linux oder der CLion-Oberfläche.

Die Zahlenwerte und Regeln dieses Vertrags sind lokale Projektentscheidungen. Vor dem späteren Einbinden eines Frameworks dessen aktuelle offizielle Anleitung lesen.

## P06-T04: Anzeigeentwurf und MQTT-Nutzdaten lokal prüfen

Im Projektordner ausführen:

~~~powershell
uv run --offline --python 3.12 python -X utf8 nachweise/pruefe_anzeigevertrag.py --kompilierer 'C:/Program Files/JetBrains/CLion 2025.3.4/bin/mingw/bin/g++.exe'
~~~

Voraussetzungen: vorhandenes Python 3.12 über uv und GCC 13.1.0. Keine Installation, keine Python-Zusatzpakete. GCC-Pfad bei anderer lokaler Installation über das Argument anpassen. Der Prüftreiber kompiliert `src/main.cpp` mit C++17 und Warnungen in einen frischen temporären Ordner unter `ausgabe/`, führt die Konsole mit `beispieldaten/temperaturen.csv` aus und entfernt den temporären Bau. Die konkreten Compiler- und Programmbefehle stehen im Protokoll.

Erwartet: Exitcode 0 und `Abnahme BESTANDEN`. Sechs C++-JSON-Nachrichten entsprechen vollständig `sensorvertrag.nachrichten`; die abgeleiteten Textprojektionen passen zur Tabelle in `tickets/P06-T04.md`. Insbesondere 30 °C ergibt Warnung und `null` ergibt „— °C“/„Ungültig“. Die MQTT-Konfiguration wird auf die dokumentierten lokalen Parameter abgeglichen. Originaldaten bleiben mit sechs Einträgen und derselben SHA256-Prüfsumme erhalten. Keine neuen Beispieldaten.

Nachweise: `nachweise/P06-T04-pruefung.txt`, `nachweise/P06-T04-diffpruefung.txt`, `nachweise/P06-T04-abschluss.json`. Zur Wiederholung nötig: `nachweise/pruefe_anzeigevertrag.py` (enthält sämtliche Sollprojektionen), `src/main.cpp`, `projekt.json`, `beispieldaten/temperaturen.csv`, `tickets/P06-T04.md` und diese Anleitung. Keine weiteren Testquellen; CMake ist für diese kleine Wiederholungsprüfung nicht erforderlich, sein Nachweis bleibt separat bei T03.

Die Qt-Ansicht ist eine Textskizze, MQTT ein dokumentierter Vertrag. Der Prüfer startet weder Qt noch MQTT und simuliert keinen Broker. Qt, MQTT, physische Hardware, UML und die Lastenheft-Gesamtabnahme bleiben ohne neuen Ausführungsnachweis offen. Vor einer Kompetenzangabe muss die jeweilige Variante tatsächlich ausgeführt werden. Hier endet der Vorbereitungsschritt T04; keine Erweiterung begonnen.
