# 📊 Budgetplanner

Der Budgetplanner ist eine browserbasierte Python-Anwendung zur Verwaltung persönlicher Finanzen.  
Das Projekt orientiert sich an der Struktur des Pizzeria Reference Project aus dem Modul Objektorientierte Programmierung.

Die Anwendung hilft Benutzern dabei Einnahmen, Ausgaben, Konten, Kategorien und Monatsbudgets übersichtlich zu verwalten. Zusätzlich unterstützt sie Import, Export, wiederkehrende Transaktionen und grafische Auswertungen, damit die finanzielle Situation schnell verständlich wird.

---

## 💡 Problemstellung

Viele Personen verlieren im Alltag schnell den Überblick über ihre Finanzen:

- Einnahmen und Ausgaben werden nicht konsequent erfasst.
- Kleine Ausgaben summieren sich über den Monat.
- Budgetüberschreitungen werden oft zu spät erkannt.
- Mehrere Konten und Kategorien machen die Übersicht schwieriger.
- Wiederkehrende Zahlungen müssen oft mehrfach manuell erfasst werden.
- Daten sollen bei Bedarf importiert, exportiert oder als Bericht abgelegt werden können.

---

## ✅ Lösung

Der Budgetplanner bietet eine einfache und strukturierte Lösung:

- Einnahmen und Ausgaben zentral erfassen
- Transaktionen Kategorien und Konten zuordnen
- Finanzübersicht mit Einnahmen, Ausgaben, Saldo und Kontoständen anzeigen
- Monatsbudgets pro Ausgabenkategorie festlegen
- Budgetverbrauch, Restbudget und Überschreitungen anzeigen
- Wiederkehrende Transaktionen automatisch für mehrere Zeitpunkte erstellen
- Budgets aus dem Vormonat übernehmen
- Daten dauerhaft in einer SQLite-Datenbank speichern
- CSV-Dateien importieren und Daten als CSV oder PDF exportieren

---

## 📚 Projektdokumentation

- [User Stories, Datentypen, Eingaben und erwartete Ausgaben](docs/user_stories.md)
- [Architektur](docs/architecture.md)
- [Klassendiagramm](<docs/budgetplanner klassendiagram.png>)
- [Test Cases](docs/testcases.md)
- Diagramme: Klassendiagramm und ER-Modell im Ordner `docs/`

---

## 🛠 Hauptfunktionen

- Konten erfassen, bearbeiten und löschen
- Kategorien für Einnahmen und Ausgaben verwalten
- Einnahmen und Ausgaben erfassen, bearbeiten und löschen
- Wiederkehrende Transaktionen wöchentlich, monatlich, quartalsweise oder jährlich erstellen
- Finanzübersicht mit Einnahmen, Ausgaben und Saldo anzeigen
- Kontostände aus Startsaldo und Transaktionen berechnen
- Monatsbudgets pro Ausgabenkategorie erfassen, bearbeiten und löschen
- Budgets aus dem Vormonat übernehmen
- Budgetverbrauch, Restbudget und Überschreitungen anzeigen
- Transaktionen nach Typ, Kategorie und Monat filtern
- Diagramme für Ausgaben nach Kategorie, Monatsvergleich und Ausgabenverlauf anzeigen
- CSV-Import für Konten, Kategorien, Budgets und Transaktionen
- CSV-Export einzelner oder mehrerer Bereiche
- PDF-Export als strukturierter Monatsbericht
- Darkmode und Hilfe-Dialog in der Oberfläche
- Speicherung in SQLite über SQLModel ORM

---

## 🧱 Architektur

Die Anwendung verwendet eine Schichtenarchitektur wie im Pizzeria-Projekt:

```text
NiceGUI Pages -> Controller -> Services -> DAO -> SQLModel/SQLite
```

Die Verantwortlichkeiten sind klar getrennt:

- `budget_app/ui/pages/`: Benutzeroberfläche, Formulare, Navigation und Tabellen
- `budget_app/ui/components/`: wiederverwendbare UI-Komponenten, Tabellen, Karten, Layout, Import und Export
- `budget_app/ui/controllers.py`: Vermittlung zwischen UI und Services
- `budget_app/services/`: Businesslogik, Validierung, Berechnungen, Wiederholungen und PDF-Export
- `budget_app/data_access/dao.py`: Datenbankzugriffe über DAO-Klassen
- `budget_app/data_access/db.py`: Datenbank-Facade für Engine, Schema und Seed-Daten
- `budget_app/data_access/seed.py`: Demo-/Startdaten
- `budget_app/domain/models.py`: SQLModel-Klassen und Beziehungen
- `budget_app/utils/`: Datums- und Format-Hilfsfunktionen

---

## 🧩 OOP- und Python-Konzepte

| Konzept | Umsetzung |
| --- | --- |
| Klassen und Objekte | `User`, `Account`, `Category`, `Transaction`, `Budget` |
| Kapselung | Datenbankzugriff nur über DAOs, Regeln in Services |
| Single Responsibility Principle | Jede Schicht hat eine klare Aufgabe |
| ORM | SQLModel-Modelle mit Foreign Keys und Relationships |
| DAO Pattern | `UserDAO`, `AccountDAO`, `CategoryDAO`, `TransactionDAO`, `BudgetDAO` |
| Facade Pattern | `Database` kapselt Engine, Schema und Session Scope |
| Strategy Pattern | Wiederholungslogik über `RecurrenceStrategy` |
| MVC-ähnliche Struktur | Pages, Controller, Services und Modelle |
| Testing | Unit-, Integrations-, Datenbank-, Import-, Export- und Validierungstests |

---

## 🗃 Datenmodell

```text
User 1 ---- * Account
User 1 ---- * Category
User 1 ---- * Budget
Account 1 ---- * Transaction
Category 1 ---- * Transaction
Category 1 ---- * Budget
```

Einnahmen und Ausgaben werden bewusst nicht als separate Unterklassen modelliert.  
Beide besitzen dieselben Attribute. Der Unterschied wird über `transaction_type` (`income` oder `expense`) abgebildet.

Aktuell verwendet die App einen Default User. Das Modell ist aber bereits so aufgebaut, dass mehrere Benutzer später ergänzt werden könnten.

---

## 📁 Projektstruktur

```text
budget_app/
|-- __main__.py
|-- application.py
|-- data_access/
|   |-- dao.py
|   |-- db.py
|   `-- seed.py
|-- domain/
|   `-- models.py
|-- services/
|   |-- account_service.py
|   |-- budget_service.py
|   |-- category_service.py
|   |-- finance_service.py
|   |-- pdf_export_service.py
|   |-- recurrence_service.py
|   `-- transaction_service.py
|-- ui/
|   |-- controllers.py
|   |-- components/
|   |   |-- cards.py
|   |   |-- forms.py
|   |   |-- layout.py
|   |   |-- tables.py
|   |   `-- theme.py
|   `-- pages/
|       |-- accounts_page.py
|       |-- budget_page.py
|       |-- categories_page.py
|       |-- overview_page.py
|       |-- shared.py
|       `-- transactions_page.py
`-- utils/
    |-- date_utils.py
    `-- format_utils.py

tests/
|-- conftest.py
|-- test_db.py
|-- test_export.py
|-- test_import.py
|-- test_integration.py
|-- test_unit.py
`-- test_validation.py
```

---

## ⚙️ Installation

```bash
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

---

## ▶️ Start

Die App kann über den Kompatibilitäts-Startpunkt gestartet werden:

```bash
python app.py
```

Alternativ kann das Paket direkt gestartet werden:

```bash
python -m budget_app
```

Danach ist die App standardmässig unter folgender Adresse erreichbar:

```text
http://localhost:8080
```

Wenn Port `8080` bereits belegt ist, sucht die Anwendung automatisch den nächsten freien Port.

---

## 🧪 Tests

Die Tests können mit folgendem Befehl ausgeführt werden:

```bash
pytest
```

Die Tests prüfen unter anderem:

- Finanzübersicht mit Einnahmen, Ausgaben und Saldo
- Kontostandberechnung
- Budgetstatus und Budgetüberschreitung
- Wiederkehrende Transaktionen
- Erstellen, Bearbeiten und Löschen von Budgets
- SQLite-Persistenz und Monatsabfragen
- Validierung ungültiger Transaktionen
- CSV-Import für Konten, Kategorien, Budgets und Transaktionen
- CSV-Export, ZIP-Export und PDF-Export
- Integration mit SQLite-In-Memory-Datenbank

Die manuell beschriebenen Testfälle befinden sich in [docs/testcases.md](docs/testcases.md).

---

## 🎤 Hinweise zur Präsentation

Wichtige Code-Stellen für die Erklärung:

- `budget_app/domain/models.py`: ORM-Modelle und Beziehungen
- `budget_app/data_access/dao.py`: DAO Pattern und Datenbankzugriffe
- `budget_app/data_access/db.py`: Datenbank-Facade und SQLite-Setup
- `budget_app/services/finance_service.py`: Berechnung von Einnahmen, Ausgaben und Saldo
- `budget_app/services/budget_service.py`: Budgetstatus, Budgetüberschreitung und Vormonatsübernahme
- `budget_app/services/transaction_service.py`: Validierung von Transaktionen
- `budget_app/services/recurrence_service.py`: Wiederkehrende Transaktionen mit Strategy Pattern
- `budget_app/services/pdf_export_service.py`: PDF-Bericht
- `budget_app/ui/controllers.py`: Verbindung zwischen UI und Services
- `budget_app/ui/pages/`: NiceGUI-Seiten
- `budget_app/ui/components/layout.py`: Navigation, Import, Export und gemeinsame Layout-Logik

Empfohlene Präsentationslogik:

1. Kurz Problem und Ziel erklären
2. Browser-Demo zeigen
3. Architektur mit Schichten erklären
4. ORM-Modell und Beziehungen zeigen
5. Services, DAO Pattern und Wiederholungslogik erklären
6. Budget-Workflow und Validierung zeigen
7. Import, Export und PDF-Bericht erwähnen
8. Tests und Test Cases zeigen

---

## 👥 Autoren

- Sven Birrer
- Lorik Kele
- Ahmad Barkat

---

## 📜 Lizenz

Dieses Projekt wird im Rahmen eines Schulprojekts im Modul Objektorientierte Programmierung erstellt.

---

## 💸 Viel Erfolg beim Planen!
