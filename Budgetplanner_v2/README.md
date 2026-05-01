# Budgetplanner

Browserbasierte Python-Anwendung zur Verwaltung persoenlicher Finanzen. Das Projekt
orientiert sich an der Struktur des Pizzeria Reference Project aus dem Modul
Objektorientierte Programmierung.

## Ziel

Der Budgetplanner hilft Benutzern dabei, Einnahmen, Ausgaben, Konten, Kategorien
und Monatsbudgets zu erfassen. Die Anwendung zeigt eine Finanzuebersicht und warnt
indirekt ueber den Budgetstatus, wenn Ausgaben ein Budget ueberschreiten.

## Hauptfunktionen

- Konten verwalten
- Kategorien fuer Einnahmen und Ausgaben verwalten
- Einnahmen und Ausgaben erfassen
- Finanzuebersicht mit Einnahmen, Ausgaben und Saldo anzeigen
- Monatsbudgets pro Ausgabenkategorie erfassen
- Budgetverbrauch und Restbudget anzeigen
- Speicherung in SQLite ueber SQLModel ORM

## Projektstruktur

```text
budget_app/
├── __main__.py
├── application.py
├── data_access/
│   ├── dao.py
│   ├── db.py
│   └── seed.py
├── domain/
│   └── models.py
├── services/
│   ├── account_service.py
│   ├── budget_service.py
│   ├── category_service.py
│   ├── finance_service.py
│   └── transaction_service.py
└── ui/
    ├── controllers.py
    └── pages.py

tests/
├── conftest.py
├── test_integration.py
└── test_unit.py
```

## Architektur

Die Anwendung verwendet eine Schichtenarchitektur wie im Pizzeria-Projekt:

```text
NiceGUI Pages -> Controller -> Services -> DAO -> SQLModel/SQLite
```

- Die UI enthaelt keine Businesslogik.
- Controller koordinieren Benutzeraktionen.
- Services enthalten Validierung und Berechnungen.
- DAOs kapseln Datenbankzugriffe.
- SQLModel bildet Python-Klassen auf Datenbanktabellen ab.

## OOP- und Python-Konzepte

| Konzept | Umsetzung |
| --- | --- |
| Klassen und Objekte | `User`, `Account`, `Category`, `Transaction`, `Budget` |
| Kapselung | Zugriff auf Datenbank nur ueber DAOs, Regeln in Services |
| Single Responsibility Principle | Jede Schicht hat eine klare Aufgabe |
| ORM | SQLModel-Modelle mit Foreign Keys und Relationships |
| DAO Pattern | `AccountDAO`, `CategoryDAO`, `TransactionDAO`, `BudgetDAO` |
| Facade Pattern | `Database` kapselt Engine, Schema und Session Scope |
| MVC-aehnliche Struktur | Pages, Controller, Services/Modelle |
| Testing | Unit Tests fuer Berechnungen, Integration Tests fuer Datenbank |

## Datenmodell

```text
User 1 ---- * Account
User 1 ---- * Category
User 1 ---- * Budget
Account 1 ---- * Transaction
Category 1 ---- * Transaction
Category 1 ---- * Budget
```

Einnahmen und Ausgaben werden bewusst nicht als Unterklassen modelliert. Beide
besitzen dieselben Attribute. Der Unterschied wird ueber `transaction_type`
(`income` oder `expense`) abgebildet. Das haelt das Modell einfach und folgt KISS.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Start

```bash
python -m budget_app
```

Danach ist die App standardmaessig unter `http://localhost:8080` erreichbar.

## Tests

```bash
pytest
```

## Team

- Sven Birrer
- Lorik Kele
- Ahmad Barkat

## Hinweise zur Praesentation

Die wichtigsten Codepfade fuer die Erklaerung:

- `budget_app/domain/models.py`: ORM-Modelle und Beziehungen
- `budget_app/data_access/dao.py`: DAO Pattern und Datenbankzugriffe
- `budget_app/services/finance_service.py`: Berechnung von Einnahmen, Ausgaben und Saldo
- `budget_app/services/budget_service.py`: Budgetstatus und Budgetueberschreitung
- `budget_app/ui/pages.py`: NiceGUI-Oberflaeche

## ORM Umsetzung

Das Datenmodell wird mit SQLModel als ORM umgesetzt.

- Jede Klasse entspricht einer Datenbanktabelle
- Beziehungen werden über Foreign Keys definiert
- Navigation erfolgt über Relationship()

Beispiel:
- account_id verbindet Transaction mit Account
- Relationship erlaubt Zugriff auf das ganze Objekt