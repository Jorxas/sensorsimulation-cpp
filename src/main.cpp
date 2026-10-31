#include <iostream>
#include <stdexcept>

enum class Sensorzustand { normal, warnung, ungueltig };
Sensorzustand naechster_zustand(double temperatur) {
    (void)temperatur;
    throw std::logic_error("P06-T02: Zustandsuebergang noch umzusetzen");
}
int main() {
    std::cout << "P06 initialisiert; Sensorkern und Anzeige noch offen.\n";
    return 0;
}
