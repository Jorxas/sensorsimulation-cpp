#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <optional>
#include <stdexcept>
#include <string>
#include <vector>

enum class Sensorzustand { normal, warnung, ungueltig };

// Ohne Hysterese: Nur die aktuelle Messung bestimmt den Folgezustand.
Sensorzustand naechster_zustand(double temperatur) {
    if (!std::isfinite(temperatur) || temperatur < -40 || temperatur > 125) {
        return Sensorzustand::ungueltig;
    }
    return temperatur >= 30 ? Sensorzustand::warnung : Sensorzustand::normal;
}

const char* zustandsname(Sensorzustand zustand) {
    switch (zustand) {
        case Sensorzustand::normal: return "normal";
        case Sensorzustand::warnung: return "warnung";
        case Sensorzustand::ungueltig: return "ungueltig";
    }
    return "ungueltig";
}

struct Messung {
    std::optional<double> temperatur;
    Sensorzustand zustand = Sensorzustand::ungueltig;
    const char* grund = "fehlend";
};

Messung messung_auswerten(const std::string& rohwert) {
    const auto anfang = rohwert.find_first_not_of(" \t\r\n");
    if (anfang == std::string::npos) {
        return {};
    }
    const auto ende = rohwert.find_last_not_of(" \t\r\n");
    const auto bereinigt = rohwert.substr(anfang, ende - anfang + 1);
    char* rest = nullptr;
    const double temperatur = std::strtod(bereinigt.c_str(), &rest);
    if (rest == bereinigt.c_str() || *rest != '\0') {
        return {std::nullopt, Sensorzustand::ungueltig, "nicht_numerisch"};
    }
    if (!std::isfinite(temperatur)) {
        return {std::nullopt, Sensorzustand::ungueltig, "nicht_endlich"};
    }
    const auto zustand = naechster_zustand(temperatur);
    if (zustand == Sensorzustand::ungueltig) {
        return {std::nullopt, zustand, "ausserhalb_messbereich"};
    }
    return {temperatur, zustand, "messwert"};
}

std::vector<Messung> temperaturfolge_einlesen(const std::string& dateipfad) {
    std::ifstream eingabe(dateipfad);
    if (!eingabe) {
        throw std::runtime_error("Eingabedatei kann nicht geoeffnet werden: " + dateipfad);
    }
    std::string zeile;
    if (!std::getline(eingabe, zeile)) {
        throw std::runtime_error("CSV-Kopfzeile fehlt.");
    }
    if (!zeile.empty() && zeile.back() == '\r') zeile.pop_back();
    if (zeile != "schritt,temperatur") {
        throw std::runtime_error("CSV-Kopfzeile muss schritt,temperatur lauten.");
    }
    std::vector<Messung> messungen;
    while (std::getline(eingabe, zeile)) {
        if (!zeile.empty() && zeile.back() == '\r') zeile.pop_back();
        const auto komma = zeile.find(',');
        if (komma == std::string::npos || zeile.find(',', komma + 1) != std::string::npos
            || zeile.substr(0, komma) != std::to_string(messungen.size())) {
            throw std::runtime_error("Ungueltige CSV-Struktur oder Schrittfolge in Zeile "
                                     + std::to_string(messungen.size() + 2) + ".");
        }
        messungen.push_back(messung_auswerten(zeile.substr(komma + 1)));
    }
    if (eingabe.bad()) throw std::runtime_error("Fehler beim Lesen der Eingabedatei.");
    if (messungen.empty()) throw std::runtime_error("Temperaturfolge ist leer.");
    return messungen;
}

int main(int anzahl, char* argumente[]) {
    if (anzahl != 2) {
        std::cerr << "Aufruf: sensorsimulation <Temperaturdatei.csv>\n";
        return 1;
    }
    try {
        // Erst die ganze Struktur pruefen, damit ein Dateifehler keine Teilfolge ausgibt.
        const auto messungen = temperaturfolge_einlesen(argumente[1]);
        std::cout << std::setprecision(std::numeric_limits<double>::max_digits10);
        for (std::size_t schritt = 0; schritt < messungen.size(); ++schritt) {
            const auto& messung = messungen[schritt];
            std::cout << "{\"schritt\":" << schritt << ",\"temperatur_celsius\":";
            if (messung.temperatur) std::cout << *messung.temperatur;
            else std::cout << "null";
            std::cout << ",\"einheit\":\"°C\",\"zustand\":\""
                      << zustandsname(messung.zustand) << "\",\"grund\":\""
                      << messung.grund << "\"}\n";
        }
        return 0;
    } catch (const std::exception& fehler) {
        std::cerr << "Fehler: " << fehler.what() << '\n';
        return 1;
    }
}
