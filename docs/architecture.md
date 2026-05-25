# Architektur

Die Anwendung orientiert sich am Pizzeria Reference Project aus dem Modul.

## Schichten

```text
NiceGUI Pages -> Controller -> Services -> DAO -> SQLModel/SQLite
```

## Verantwortlichkeiten

- `budget_app/ui/pages/`: Anzeige, Formulare, Navigation und Seitenlogik
- `budget_app/ui/components/`: wiederverwendbare UI-Komponenten, Tabellen, Karten, Layout, Import und Export
- `budget_app/ui/controllers.py`: Vermittlung zwischen UI und Services
- `budget_app/services/`: Businesslogik, Validierung, Berechnungen, Wiederholungen und PDF-Export
- `budget_app/data_access/dao.py`: Datenbankzugriffe über DAO-Klassen
- `budget_app/data_access/db.py`: Datenbank-Facade für Engine, Schema und Seed-Daten
- `budget_app/data_access/seed.py`: Demo-/Startdaten
- `budget_app/domain/models.py`: SQLModel-Klassen und Beziehungen
- `budget_app/utils/`: Datums- und Format-Hilfsfunktionen

## Eingesetzte Konzepte aus dem Unterricht

- OOP mit Klassen und Objekten
- Kapselung durch Services und DAOs
- Single Responsibility Principle
- ORM mit SQLModel
- Beziehungen mit Foreign Keys
- DAO Pattern
- Facade Pattern in `Database`
- Strategy Pattern in `RecurrenceService`
- MVC-aehnliche Schichtung
- Unit-, Integrations-, Datenbank-, Import-, Export- und Validierungstests

## Define Logical Entities (ORM Entities)

Im ersten Schritt wurden die fachlichen Entitäten definiert. Diese Entitäten entsprechen den Tabellen im ER-Modell und den SQLModel-Klassen in `budget_app/domain/models.py`.

| Logische Entität | ORM-Klasse | Zweck |
| --- | --- | --- |
| User | `User` | Besitzer von Konten, Kategorien und Budgets |
| Account | `Account` | Finanzkonto wie Bankkonto oder Bargeld |
| Category | `Category` | Einordnung von Einnahmen und Ausgaben |
| Transaction | `Transaction` | Einzelne Einnahme oder Ausgabe |
| Budget | `Budget` | Monatsbudget pro Ausgabekategorie |

Bewusste Modellentscheidungen:

- Einnahmen und Ausgaben sind keine separaten Unterklassen. Beide werden als `Transaction` gespeichert und über `transaction_type` unterschieden.
- `FinanceOverview` oder ähnliche Auswertungen sind keine Domänenentitäten, sondern berechnete Daten für Anzeige oder Services.
- `current_balance` wird nicht in `Account` gespeichert, sondern aus Startsaldo und Transaktionen berechnet.
- `spent_amount` wird nicht in `Budget` gespeichert, sondern aus Transaktionen pro Kategorie und Monat berechnet.
- `Budget` ist direkt mit `Category` verknüpft, damit jedes Budget eindeutig zu einer Ausgabekategorie gehört.
- `Transaction` ist nicht direkt mit `Budget` verknüpft. Budgets werden anhand von Kategorie, Monat und Jahr ausgewertet.

## ORM Mapping

Die Entitäten werden mit SQLModel direkt auf Tabellen abgebildet.

### Tabellen und Attribute

`User`
- `id`: Primary Key
- `name`
- `email`

`Account`
- `id`: Primary Key
- `name`
- `account_type`
- `starting_balance_chf`
- `user_id`: Foreign Key auf `User`

`Category`
- `id`: Primary Key
- `name`
- `category_type`
- `user_id`: Foreign Key auf `User`

`Transaction`
- `id`: Primary Key
- `amount_chf`
- `transaction_type`
- `transaction_date`
- `description`
- `account_id`: Foreign Key auf `Account`
- `category_id`: Foreign Key auf `Category`

`Budget`
- `id`: Primary Key
- `month`
- `year`
- `limit_chf`
- `user_id`: Foreign Key auf `User`
- `category_id`: Foreign Key auf `Category`

### Beziehungen

- Ein User hat mehrere Accounts (1:n)
- Ein User hat mehrere Categories (1:n)
- Ein User hat mehrere Budgets (1:n)
- Ein Account hat mehrere Transactions (1:n)
- Eine Category hat mehrere Transactions (1:n)
- Eine Category hat mehrere Budgets (1:n)

Technische Umsetzung:

- Foreign Keys, z. B. `account_id -> account.id`
- Relationships mit `Relationship(back_populates=...)`
- DAOs kapseln den Zugriff auf die SQLModel-Sessions

Beispiel:

Account:
- user_id (FK)
- user (Relationship)
- transactions (Relationship)

Transaction:
- account_id (FK)
- account (Relationship)

Budget:
- user_id (FK)
- category_id (FK)
- user (Relationship)
- category (Relationship)

### Erlaubte Typwerte

Die Typen sind im aktuellen Code als Strings umgesetzt und werden in der Service-Schicht validiert:

- `transaction_type`: `income`, `expense`
- `category_type`: `income`, `expense`
- `account_type`: `Bankkonto`, `Bargeld`

## Verbindung ER-Modell und ORM

Das im vorherigen Milestone erstellte ER-Diagramm wurde direkt in SQLModel-Klassen umgesetzt.

Jede Entität im ER-Modell entspricht einer Klasse im Code:

- User → User
- Account → Account
- Category → Category
- Transaction → Transaction
- Budget → Budget

Das aktuelle Klassendiagramm ist hier dokumentiert:

- [Klassendiagramm](klassendiagramm.png)

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

## Validate & Iterate

Die Validierung und Iteration des Modells erfolgte nach dem Aufbau der ORM-Entitäten.

### Validierung im Modell

Einige technische Regeln werden direkt über SQLModel-Felder definiert:

- `Transaction.amount_chf > 0`
- `Budget.limit_chf > 0`
- `Budget.month` zwischen 1 und 12
- `Budget.year` zwischen 2000 und 2100
- Primary Keys und Foreign Keys über `Field(...)`

### Validierung in Services

Fachliche Regeln liegen bewusst in der Service-Schicht:

- Transaktionstyp muss `income` oder `expense` sein.
- Kategorie muss zum Transaktionstyp passen.
- Konto und Kategorie müssen existieren.
- Ausgaben dürfen im vollständigen App-Workflow nur erstellt werden, wenn ein Budget für Kategorie, Monat und Jahr existiert.
- Budgets dürfen nur für Ausgabekategorien erstellt werden.
- Pro User, Kategorie, Monat und Jahr darf nur ein Budget existieren. Diese Eindeutigkeit wird aktuell im `BudgetService` geprüft.
- Kategorien und Konten, die bereits verwendet werden, dürfen nicht gelöscht werden.

### Iterationen gegenüber früheren Modellen

Das Modell wurde anhand der Rückmeldungen und Tests verbessert:

- `budget_id` wurde nicht in `Transaction` aufgenommen, weil Budgets aus Kategorie, Monat und Jahr berechnet werden.
- `category_id` wurde in `Budget` ergänzt, damit jedes Budget eindeutig einer Kategorie zugeordnet ist.
- `spent_amount` wurde aus `Budget` entfernt, weil der Verbrauch berechnet wird.
- `current_balance` wurde aus `Account` entfernt, weil der aktuelle Kontostand berechnet wird.
- `month` und `year` wurden als getrennte Integer-Werte umgesetzt.
- Auswertungen wie Finanzübersicht oder Monatsvergleich wurden nicht als persistente Entitäten modelliert.

### Testbasierte Prüfung

Die Iterationen werden durch Tests abgesichert:

- `tests/test_unit.py`: Finanzberechnungen, Budgetstatus und Wiederholungsdaten
- `tests/test_integration.py`: vollständige Workflows mit SQLite-In-Memory-Datenbank
- `tests/test_db.py`: Persistenz, Seed-Daten und Monatsabfragen
- `tests/test_validation.py`: Validierungsfehler
- `tests/test_import.py`: CSV-Import
- `tests/test_export.py`: CSV-, ZIP- und PDF-Export
