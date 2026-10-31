# Technischer Einstieg — P06


## Einstiegspunkt ausführen

Voraussetzungen: C++-Compiler; CMake; Qt SDK für die grafische Variante; Lokaler MQTT-Broker für die MQTT-Variante.

~~~powershell
cmake -S . -B build
cmake --build build
~~~

Das Startprogramm meldet den Initialisierungsstand. Fachfunktionen sind bewusst noch nicht implementiert und melden dies bei einem Aufruf. Fehlende Bibliotheken und Frameworks erst im passenden Ticket mit ihrer tatsächlichen Version ergänzen.

## Nächste Aufgabe

Übergänge, Einheiten und Verhalten bei fehlenden Daten beschreiben.

## Technische Quellen

- [Python-CSV-Modul](https://docs.python.org/3/library/csv.html)
- [Offizielle Angular-CLI-Anleitung](https://angular.dev/tools/cli/setup-local)
- [WPF mit .NET](https://learn.microsoft.com/de-de/dotnet/desktop/wpf/get-started/create-app-visual-studio)

Vor dem Einbinden eines Frameworks dessen aktuelle offizielle Anleitung lesen.
