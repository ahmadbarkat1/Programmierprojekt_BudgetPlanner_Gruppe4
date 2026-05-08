# 📊 Budgetplanner

Der Budgetplanner ist eine browserbasierte Python-Anwendung zur Verwaltung persönlicher Finanzen.  
Das Projekt orientiert sich an der Struktur des Pizzeria Reference Project aus dem Modul Objektorientierte Programmierung.

Die Anwendung hilft Benutzern dabei Einnahmen, Ausgaben, Konten, Kategorien und Monatsbudgets übersichtlich zu verwalten. Dadurch entsteht eine klare Übersicht über die finanzielle Situation und mögliche Budgetüberschreitungen werden schneller sichtbar.

---

## 💡 Problemstellung

Viele Personen verlieren im Alltag schnell den Überblick über ihre Finanzen:

- Einnahmen und Ausgaben werden nicht konsequent erfasst.
- Kleine Ausgaben summieren sich über den Monat.
- Budgetüberschreitungen werden oft zu spät erkannt.
- Mehrere Konten und Kategorien machen die Übersicht schwieriger.
- Fehlende Struktur bei der persönlichen Finanzplanung.

---

## ✅ Lösung

Der Budgetplanner bietet eine einfache und strukturierte Lösung:

- Einnahmen und Ausgaben zentral erfassen
- Transaktionen Kategorien und Konten zuordnen
- Finanzübersicht mit Einnahmen, Ausgaben und Saldo anzeigen
- Monatsbudgets pro Ausgabenkategorie festlegen
- Budgetverbrauch und Restbudget anzeigen
- Hinweise bei Budgetüberschreitungen anzeigen
- Daten dauerhaft in einer SQLite-Datenbank speichern

---

## 🛠 Hauptfunktionen

- Konten erfassen, bearbeiten und löschen
- Kategorien für Einnahmen und Ausgaben verwalten
- Einnahmen und Ausgaben erfassen
- Transaktionen bearbeiten und löschen
- Finanzübersicht mit Einnahmen, Ausgaben und Saldo anzeigen
- Kontostände berechnen und anzeigen
- Monatsbudgets pro Ausgabenkategorie erfassen
- Budgetverbrauch, Restbudget und Überschreitungen anzeigen
- Transaktionen nach Typ, Kategorie und Monat filtern
- Diagramme zur Visualisierung der Ausgaben anzeigen
- Monatsvergleich von Einnahmen und Ausgaben anzeigen
- Speicherung in SQLite über SQLModel ORM

---

## 🧱 Architektur

Die Anwendung verwendet eine Schichtenarchitektur wie im Pizzeria-Projekt:

```text
NiceGUI Pages -> Controller -> Services -> DAO -> SQLModel/SQLite
```

Die Verantwortlichkeiten sind klar getrennt:

- `ui/pages.py`: Benutzeroberfläche, Formulare, Navigation und Tabellen
- `ui/controllers.py`: Vermittlung zwischen UI und Services
- `services/`: Businesslogik, Validierung und Berechnungen
- `data_access/dao.py`: Datenbankzugriffe über DAO-Klassen
- `data_access/db.py`: Datenbank-Facade für Engine, Schema und Seed-Daten
- `domain/models.py`: SQLModel-Klassen und Beziehungen

---

## 🧩 OOP- und Python-Konzepte

| Konzept | Umsetzung |
| --- | --- |
| Klassen und Objekte | `User`, `Account`, `Category`, `Transaction`, `Budget` |
| Kapselung | Datenbankzugriff nur über DAOs, Regeln in Services |
| Single Responsibility Principle | Jede Schicht hat eine klare Aufgabe |
| ORM | SQLModel-Modelle mit Foreign Keys und Relationships |
| DAO Pattern | `AccountDAO`, `CategoryDAO`, `TransactionDAO`, `BudgetDAO` |
| Facade Pattern | `Database` kapselt Engine, Schema und Session Scope |
| MVC-ähnliche Struktur | Pages, Controller, Services und Modelle |
| Testing | Unit Tests und Integration Tests |

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

Diese Lösung hält das Modell einfach, vermeidet unnötige Vererbung und ist für die Anwendung ausreichend nachvollziehbar.

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
|   `-- transaction_service.py
`-- ui/
    |-- controllers.py
    `-- pages.py

tests/
|-- conftest.py
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
- Validierung ungültiger Transaktionen
- Integration mit SQLite-In-Memory-Datenbank

---

## 🎤 Hinweise zur Präsentation

Wichtige Code-Stellen für die Erklärung:

- `budget_app/domain/models.py`: ORM-Modelle und Beziehungen
- `budget_app/data_access/dao.py`: DAO Pattern und Datenbankzugriffe
- `budget_app/services/finance_service.py`: Berechnung von Einnahmen, Ausgaben und Saldo
- `budget_app/services/budget_service.py`: Budgetstatus und Budgetüberschreitung
- `budget_app/services/transaction_service.py`: Validierung von Transaktionen
- `budget_app/ui/controllers.py`: Verbindung zwischen UI und Services
- `budget_app/ui/pages.py`: NiceGUI-Oberfläche

Empfohlene Präsentationslogik:

1. Kurz Problem und Ziel erklären
2. Browser-Demo zeigen
3. Architektur mit Schichten erklären
4. ORM-Modell und Beziehungen zeigen
5. Services und DAO Pattern erklären
6. Tests und Validierung erwähnen

---

## 👥 Autoren

- Sven Birrer
- Lorik Kele
- Ahmad Barkat

---

## 📜 Lizenz
Dieses Projekt wird im Rahmen eines Schulprojekts erstellt.

---

## 📌 Hinweis

Dieses Projekt wurde im Rahmen des Moduls Objektorientierte Programmierung erstellt.

---

## 💸 Viel Erfolg beim Planen!