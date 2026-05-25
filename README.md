# 📊 Budgetplanner

Der Budgetplanner ist eine browserbasierte Python-Anwendung zur Verwaltung persönlicher Finanzen.  
Das Projekt orientiert sich an der Struktur des Pizzeria Reference Project aus dem Modul Objektorientierte Programmierung.

Die Anwendung hilft Benutzern dabei Einnahmen, Ausgaben, Konten, Kategorien und Monatsbudgets übersichtlich zu verwalten. Zusätzlich unterstützt sie Import, Export, wiederkehrende Transaktionen und grafische Auswertungen, damit die finanzielle Situation schnell verständlich wird.

---

## Inhaltsverzeichnis

| Abschnitt | Inhalt |
| --- | --- |
| [Problemstellung](#problemstellung) | Ausgangslage und Motivation |
| [Lösung](#loesung) | Kurzbeschreibung der Projektlösung |
| [Projektdokumentation](#projektdokumentation) | Links zu User Stories, Diagrammen, Tests und Screens |
| [Projektmanagement](#projektmanagement) | Übersicht zur Planung und Organisation |
| [Hauptfunktionen](#hauptfunktionen) | Überblick über die umgesetzten Funktionen |
| [Screens und Navigation](#screens-und-navigation) | Wireframe und Figma-Screens |
| [Architektur](#architektur) | Schichtenmodell und Verweis auf die technische Dokumentation |
| [OOP- und Python-Konzepte](#oop-und-python-konzepte) | Eingesetzte OOP-/Python-Konzepte |
| [Ausgewählte Design Patterns](#ausgewaehlte-design-patterns) | Passende Design Patterns des Projekts |
| [Datenmodell](#datenmodell) | Entitäten, Klassendiagramm und ER-Modell |
| [Projektstruktur](#projektstruktur) | Ordner- und Dateiaufbau |
| [Installation](#installation) | Lokales Setup |
| [Start](#start) | Anwendung starten |
| [Tests](#tests) | Testausführung und Testdokumentation |
| [Hinweise zur Präsentation](#hinweise-zur-praesentation) | Vorschlag für die Projektvorstellung |
| [Autoren](#autoren) | Projektteam |
| [Lizenz](#lizenz) | Projektkontext |

---

<a id="problemstellung"></a>

## 💡 Problemstellung

Viele Personen verlieren im Alltag schnell den Überblick über ihre Finanzen:

- Einnahmen und Ausgaben werden nicht konsequent erfasst.
- Kleine Ausgaben summieren sich über den Monat.
- Budgetüberschreitungen werden oft zu spät erkannt.
- Mehrere Konten und Kategorien machen die Übersicht schwieriger.
- Wiederkehrende Zahlungen müssen oft mehrfach manuell erfasst werden.
- Daten sollen bei Bedarf importiert, exportiert oder als Bericht abgelegt werden können.

---

<a id="loesung"></a>

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

<a id="projektdokumentation"></a>

## 📚 Projektdokumentation

- [User Stories, Datentypen, Eingaben und erwartete Ausgaben](docs/user_stories.md)
- [Architektur](docs/architecture.md)
- [Klassendiagramm](docs/klassendiagramm.png)
- [ER-Modell](docs/er_modell.png)
- [Test Cases](docs/testcases.md)
- [Wireframe](docs/wireframe.png)
- [Projektmanagement](docs/projektmanagement.png)
- Figma-Screens: [Home](docs/figma_1_home.png), [Transaktionen](docs/figma_2_transaktion.png), [Kategorien](docs/figma_3_kategorien.png), [Konten](docs/figma_4_konten.png), [Budget](docs/figma_5_budget.png)

---

<a id="projektmanagement"></a>

## Projektmanagement

Das Projektmanagement zeigt die organisatorische Planung und Aufgabenübersicht des Projekts. Damit ist nachvollziehbar, wie die Projektarbeit strukturiert und vorbereitet wurde.

![Projektmanagement](docs/projektmanagement.png)

---

<a id="hauptfunktionen"></a>

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

<a id="screens-und-navigation"></a>

## 🖼 Screens und Navigation

Für die Umsetzung wurden die fokussierten Screens [Home](docs/figma_1_home.png), [Transaktionen](docs/figma_2_transaktion.png), [Kategorien](docs/figma_3_kategorien.png), [Konten](docs/figma_4_konten.png) und [Budget](docs/figma_5_budget.png) ausgewählt. Das [Wireframe](docs/wireframe.png) zeigt die grobe Navigation und Struktur der Anwendung. Die finalen Screens wurden in Figma erstellt und bilden die wichtigsten Benutzerabläufe des Budgetplanners ab.

### Wireframe

![Wireframe](docs/wireframe.png)

### Figma-Screens

![Home Screen](docs/figma_1_home.png)

![Transaktionen Screen](docs/figma_2_transaktion.png)

![Kategorien Screen](docs/figma_3_kategorien.png)

![Konten Screen](docs/figma_4_konten.png)

![Budget Screen](docs/figma_5_budget.png)

---

<a id="architektur"></a>

## 🧱 Architektur

Die Anwendung verwendet eine Schichtenarchitektur wie im Pizzeria-Projekt. Die UI ruft Controller auf, Controller arbeiten mit Services, Services greifen über DAOs auf SQLModel/SQLite zu.

```text
NiceGUI Pages -> Controller -> Services -> DAO -> SQLModel/SQLite
```

Die detaillierten Verantwortlichkeiten, ORM-Mappings und Modellentscheidungen sind in der [Architekturdokumentation](docs/architecture.md) beschrieben.

---

<a id="oop-und-python-konzepte"></a>

## 🧩 OOP- und Python-Konzepte

| Konzept | Umsetzung |
| --- | --- |
| Klassen und Objekte | `User`, `Account`, `Category`, `Transaction`, `Budget` |
| Kapselung | Datenbankzugriff nur über DAOs, Regeln in Services |
| Single Responsibility Principle | Jede Schicht hat eine klare Aufgabe |
| ORM | SQLModel-Modelle mit Foreign Keys und Relationships |
| Testing | Automatisierte Tests und dokumentierte manuelle Test Cases |

---

<a id="ausgewaehlte-design-patterns"></a>

## 🧠 Ausgewählte Design Patterns

Für unser Projekt passen vor allem `Strategy`, `Facade`, `DAO` und eine MVC-ähnliche Schichtenarchitektur. `Strategy` verwenden wir für wiederkehrende Transaktionen, `Facade` für die Datenbank-Kapselung, `DAO` für Datenbankzugriffe und MVC, um UI, Controller, Services und Datenmodell sauber zu trennen. Diese Patterns wurden gewählt, weil sie die Wartbarkeit verbessern, ohne das Projekt unnötig komplex zu machen.

---

<a id="datenmodell"></a>

## 🗃 Datenmodell

Das Datenmodell besteht aus `User`, `Account`, `Category`, `Transaction` und `Budget`. Einnahmen und Ausgaben werden nicht als separate Unterklassen modelliert, sondern über `transaction_type` (`income` oder `expense`) unterschieden. Die vollständigen Datentypen, Beziehungen und ORM-Mappings stehen in [User Stories](docs/user_stories.md) und [Architektur](docs/architecture.md).

### Klassendiagramm

![Klassendiagramm](docs/klassendiagramm.png)

### ER-Modell

![ER-Modell](docs/er_modell.png)

---

<a id="projektstruktur"></a>

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

<a id="installation"></a>

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

<a id="start"></a>

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

<a id="tests"></a>

## 🧪 Tests

Die Tests können mit folgendem Befehl ausgeführt werden:

```bash
pytest
```

Die Tests prüfen unter anderem:

- Finanz-, Konto- und Budgetberechnungen
- vollständige App-Workflows mit SQLite
- Validierung, Import und Export
- wiederkehrende Transaktionen

Die vollständige Testfallübersicht mit anklickbarem Inhaltsverzeichnis befindet sich in [docs/testcases.md](docs/testcases.md).

---

<a id="hinweise-zur-praesentation"></a>

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

<a id="autoren"></a>

## 👥 Autoren

- Sven Birrer
- Lorik Kele
- Ahmad Barkat

---

<a id="lizenz"></a>

## 📜 Lizenz

Dieses Projekt wird im Rahmen eines Schulprojekts im Modul Objektorientierte Programmierung erstellt.

---

## 💸 Viel Erfolg beim Planen!
