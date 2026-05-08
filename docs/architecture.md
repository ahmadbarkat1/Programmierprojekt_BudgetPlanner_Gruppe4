# Architektur

Die Anwendung orientiert sich am Pizzeria Reference Project aus dem Modul.

## Schichten

```text
NiceGUI Pages -> Controller -> Services -> DAO -> SQLModel/SQLite
```

## Verantwortlichkeiten

- `ui/pages.py`: Anzeige, Formulare und Navigation
- `ui/controllers.py`: Vermittlung zwischen UI und Services
- `services/`: Businesslogik, Validierung und Berechnungen
- `data_access/dao.py`: Datenbankzugriffe
- `data_access/db.py`: Datenbank-Facade fuer Engine, Schema und Seed-Daten
- `domain/models.py`: SQLModel-Klassen und Beziehungen

## Eingesetzte Konzepte aus dem Unterricht

- OOP mit Klassen und Objekten
- Kapselung durch Services und DAOs
- Single Responsibility Principle
- ORM mit SQLModel
- Beziehungen mit Foreign Keys
- DAO Pattern
- Facade Pattern in `Database`
- MVC-aehnliche Schichtung
- Unit Tests und Integration Tests

## ORM Mapping

Die Entitäten werden mit SQLModel direkt auf Tabellen abgebildet.

Beispiel Beziehung:

- Ein User hat mehrere Accounts (1:n)
- Ein Account hat mehrere Transactions (1:n)
- Eine Category hat mehrere Transactions und Budgets

Technische Umsetzung:

- Foreign Keys: z. B. `account_id -> account.id`
- Relationships mit `Relationship(back_populates=...)`

Beispiel:

Account:
- user_id (FK)
- user (Relationship)

Transaction:
- account_id (FK)
- account (Relationship)

## Verbindung ER-Modell und ORM

Das im vorherigen Milestone erstellte ER-Diagramm wurde direkt in SQLModel-Klassen umgesetzt.

Jede Entität im ER-Modell entspricht einer Klasse im Code:

- User → User
- Account → Account
- Category → Category
- Transaction → Transaction
- Budget → Budget

Die Beziehungen aus dem ER-Modell wurden wie folgt umgesetzt:

- 1:n Beziehungen → Foreign Keys
- Navigation zwischen Objekten → Relationship(back_populates)

Beispiel:
- Ein Account hat viele Transactions
→ umgesetzt durch:
  - transaction.account_id (Foreign Key)
  - transaction.account (Relationship)
  - account.transactions (Relationship)

  ## Beispiel ORM Mapping

Beispiel: Beziehung zwischen Account und Transaction

ER-Modell:
Account 1 --- * Transaction

Umsetzung im Code:

Transaction:
- account_id: Foreign Key auf Account
- account: Relationship zu Account

Account:
- transactions: Liste von Transaction

Dies erlaubt:
- Zugriff von Transaction → Account
- Zugriff von Account → alle Transactions

## Validierung

Die Validierung erfolgt in der Service-Schicht:

Beispiele:
- Betrag muss > 0 sein
- Monat zwischen 1 und 12
- Kategorie muss existieren
- Budget nur für expense-Kategorien

Warum im Service?
→ Trennung von UI und Businesslogik
→ Wiederverwendbarkeit
→ Testbarkeit

## Iteration des Modells

Das Datenmodell wurde schrittweise verbessert:

Version 1:
- Einfache Klassen ohne Beziehungen
- Keine klare Trennung zwischen Einnahmen und Ausgaben

Problem:
- Keine Auswertung nach Kategorien möglich
- Keine Verknüpfung zwischen Daten

Version 2:
- Einführung von Foreign Keys (user_id, account_id, category_id)
- Einführung von Relationships

Verbesserung:
- Verknüpfte Datenstruktur
- Zugriff auf zusammengehörige Objekte möglich

Version 3:
- Einführung der Budget-Entität
- Verknüpfung von Budget mit Category und User

Verbesserung:
- Monatsbudgets pro Kategorie möglich
- Vergleich zwischen Ausgaben und Budget

Version 4:
- Auslagerung der Validierung in Services

Verbesserung:
- Saubere Trennung von UI, Logik und Datenbank
- Bessere Testbarkeit