# User Stories, Datentypen, Eingaben und erwartete Ausgaben

Dieses Dokument beschreibt den aktuellen Projektstand des Budget Planners. Es ist auf die bestehende NiceGUI-Anwendung, das SQLModel-Datenmodell, die Diagramme und die dokumentierten Test Cases abgestimmt.

---

## Projektstand

Der Budget Planner ist eine browserbasierte Python-Anwendung zur Verwaltung persönlicher Finanzen. Die Anwendung nutzt eine Schichtenarchitektur:

```text
NiceGUI Pages -> Controller -> Services -> DAO -> SQLModel/SQLite
```

Aktuell umgesetzt sind:

- Übersicht mit Einnahmen, Ausgaben, Saldo, Kontoständen, Budgetstatus und Diagrammen
- Kontenverwaltung für Bankkonto und Bargeld
- Kategorienverwaltung für Einnahmen und Ausgaben
- Transaktionen mit Konto, Kategorie, Datum, Betrag und Beschreibung
- Bearbeiten und Löschen von Konten, Kategorien, Budgets und Transaktionen
- Monatsbudgets pro Ausgabenkategorie
- Budgetverbrauch, Restbudget und Anzeige von Überschreitungen
- Budgetübernahme aus dem Vormonat
- Wiederkehrende Transaktionen
- Filterung von Transaktionen nach Typ, Kategorie und Monat
- CSV-Import für Konten, Kategorien, Budgets und Transaktionen
- CSV-Export und PDF-Export ausgewählter Bereiche
- Speicherung in SQLite über SQLModel
- Validierung und Businesslogik in Services
- Unit-, Integrations-, Datenbank-, Import-, Export- und Validierungstests

---

## User Stories

### Muss-Funktionen

| ID | User Story | Status | Bezug |
| --- | --- | --- | --- |
| US-01 | Als Benutzer möchte ich Einnahmen erfassen, damit mein verfügbares Geld sichtbar wird. | Umgesetzt | TC_001, `Transaction`, `FinanceService` |
| US-02 | Als Benutzer möchte ich Ausgaben erfassen, damit ich meine Kosten nachvollziehen kann. | Umgesetzt | TC_002, `Transaction`, `BudgetService` |
| US-03 | Als Benutzer möchte ich Kategorien verwalten, damit Einnahmen und Ausgaben geordnet bleiben. | Umgesetzt | TC_003, TC_013, TC_014, `Category` |
| US-04 | Als Benutzer möchte ich mehrere Konten verwalten, damit ich Bankkonto und Bargeld getrennt betrachten kann. | Umgesetzt | TC_006, TC_012, `Account` |
| US-05 | Als Benutzer möchte ich eine Finanzübersicht sehen, damit ich Einnahmen, Ausgaben und Saldo erkenne. | Umgesetzt | TC_009, TC_010, TC_011, Dashboard |
| US-06 | Als Benutzer möchte ich Monatsbudgets pro Ausgabenkategorie erfassen, damit ich meine Ausgaben kontrollieren kann. | Umgesetzt | TC_004, `Budget` |
| US-07 | Als Benutzer möchte ich mein verbleibendes Budget sehen, damit ich weiss, wie viel ich noch ausgeben kann. | Umgesetzt | TC_005, `BudgetStatus` |
| US-08 | Als Benutzer möchte ich sehen, ob ein Budget überschritten wurde, damit ich rechtzeitig reagieren kann. | Umgesetzt | TC_008 |
| US-09 | Als Benutzer möchte ich meine Daten dauerhaft speichern, damit sie nach einem Neustart erhalten bleiben. | Umgesetzt | TC_007, SQLite |

### Erweiterte Funktionen

| ID | User Story | Status | Bezug |
| --- | --- | --- | --- |
| US-10 | Als Benutzer möchte ich Transaktionen bearbeiten und löschen, damit ich fehlerhafte Eingaben korrigieren kann. | Umgesetzt | TC_017, TC_018 |
| US-11 | Als Benutzer möchte ich Konten bearbeiten und löschen, damit meine Kontenübersicht aktuell bleibt. | Umgesetzt | `AccountService`, `AccountDAO` |
| US-12 | Als Benutzer möchte ich Kategorien bearbeiten und löschen, damit meine Struktur angepasst werden kann. | Umgesetzt | TC_013, TC_014 |
| US-13 | Als Benutzer möchte ich Budgets bearbeiten und löschen, damit sich geänderte Monatspläne korrigieren lassen. | Umgesetzt | `BudgetService`, Integrationstest |
| US-14 | Als Benutzer möchte ich Transaktionen nach Typ, Kategorie und Monat filtern, damit ich bestimmte Einträge schneller finde. | Umgesetzt | TC_015, TC_016 |
| US-15 | Als Benutzer möchte ich Diagramme sehen, damit ich meine Ausgaben besser verstehe. | Umgesetzt | Dashboard, PDF-Export |
| US-16 | Als Benutzer möchte ich einen Monatsvergleich sehen, damit ich Einnahmen und Ausgaben über mehrere Monate vergleichen kann. | Umgesetzt | Dashboard-Diagramm |
| US-17 | Als Benutzer möchte ich den Ausgabenverlauf mit vergangenen Monaten vergleichen, damit ich mein aktuelles Verhalten besser einschätzen kann. | Umgesetzt | Dashboard-Liniendiagramm |
| US-18 | Als Benutzer möchte ich wiederkehrende Transaktionen erfassen, damit regelmässige Einnahmen und Ausgaben schneller angelegt werden. | Umgesetzt | `RecurrenceService`, Integrationstest |
| US-19 | Als Benutzer möchte ich Budgets aus dem Vormonat übernehmen, damit ich wiederkehrende Budgetpläne schneller erstellen kann. | Umgesetzt | `BudgetService.copy_previous_month` |
| US-20 | Als Benutzer möchte ich Daten als CSV importieren, damit bestehende Konten, Kategorien, Budgets und Transaktionen übernommen werden können. | Umgesetzt | Importtests |
| US-21 | Als Benutzer möchte ich ausgewählte Daten als CSV oder PDF exportieren, damit ich sie archivieren oder weitergeben kann. | Umgesetzt | Exporttests |
| US-22 | Als Benutzer möchte ich zwischen hellem und dunklem Design wechseln, damit die App angenehmer nutzbar ist. | Umgesetzt | Header-Funktion |
| US-23 | Als Benutzer möchte ich eine kurze Hilfe sehen, damit ich die wichtigsten Bereiche der App verstehe. | Umgesetzt | Hilfe-Dialog |

### Nicht umgesetzte oder mögliche Weiterentwicklung

| ID | User Story | Status | Hinweis |
| --- | --- | --- | --- |
| US-24 | Als Benutzer möchte ich Transaktionen nach Konto filtern, damit ich Bewegungen einzelner Konten gezielt analysieren kann. | Offen | Datenmodell unterstützt es bereits über `account_id`; UI-Filter fehlt noch. |
| US-25 | Als Benutzer möchte ich mich einloggen können, damit mehrere Benutzer ihre eigenen Finanzdaten getrennt verwalten können. | Offen | Das Modell enthält `User`, aktuell wird ein Default User verwendet. |
| US-26 | Als Benutzer möchte ich Sparkonten als eigenen Kontotyp wählen können. | Teilweise offen | Freitext/Modell wäre möglich, Service erlaubt aktuell `Bankkonto` und `Bargeld`. |

---

## Datenmodell und Diagramm-Abgleich

Das ER-Diagramm und das Klassendiagramm bilden die folgenden Entitäten ab. Die Umsetzung befindet sich in `budget_app/domain/models.py`.

### User

- `id`: int, Primary Key
- `name`: string
- `email`: string

Beziehungen:

- Ein User besitzt mehrere Accounts.
- Ein User besitzt mehrere Categories.
- Ein User besitzt mehrere Budgets.
- Im aktuellen MVP arbeitet die App mit einem automatisch erstellten Default User.

### Account

- `id`: int, Primary Key
- `name`: string
- `account_type`: string, aktuell `Bankkonto` oder `Bargeld`
- `starting_balance_chf`: float
- `user_id`: int, Foreign Key auf `User`

Beziehungen:

- Ein Account gehört zu genau einem User.
- Ein Account kann mehrere Transactions haben.

### Category

- `id`: int, Primary Key
- `name`: string
- `category_type`: string, `income` oder `expense`
- `user_id`: int, Foreign Key auf `User`

Beziehungen:

- Eine Category gehört zu genau einem User.
- Eine Category kann mehrere Transactions haben.
- Eine Category kann mehrere Budgets haben.

### Transaction

- `id`: int, Primary Key
- `amount_chf`: float, muss grösser als 0 sein
- `transaction_type`: string, `income` oder `expense`
- `transaction_date`: date
- `description`: string
- `account_id`: int, Foreign Key auf `Account`
- `category_id`: int, Foreign Key auf `Category`

Beziehungen:

- Eine Transaction gehört zu genau einem Account.
- Eine Transaction gehört zu genau einer Category.
- Einnahmen und Ausgaben werden nicht als Unterklassen modelliert, sondern über `transaction_type` unterschieden.

### Budget

- `id`: int, Primary Key
- `month`: int, 1 bis 12
- `year`: int
- `limit_chf`: float, muss grösser als 0 sein
- `user_id`: int, Foreign Key auf `User`
- `category_id`: int, Foreign Key auf `Category`

Beziehungen:

- Ein Budget gehört zu genau einem User.
- Ein Budget gehört zu genau einer Ausgabenkategorie.
- Pro User, Monat, Jahr und Kategorie darf nur ein Budget existieren.

### Beziehungen im ER-Modell

```text
User 1 ---- * Account
User 1 ---- * Category
User 1 ---- * Budget
Account 1 ---- * Transaction
Category 1 ---- * Transaction
Category 1 ---- * Budget
```

---

## Eingaben

### Konto erstellen oder bearbeiten

- Kontoname
- Kontotyp: `Bankkonto` oder `Bargeld`
- Startsaldo in CHF

### Kategorie erstellen oder bearbeiten

- Kategoriename
- Typ: Einnahme oder Ausgabe

### Transaktion erstellen oder bearbeiten

- Typ: Einnahme oder Ausgabe
- Datum
- Kategorie passend zum Typ
- Konto
- Betrag in CHF
- Optionale Beschreibung
- Optional: wiederkehrende Transaktion mit Wiederholung und Anzahl Buchungen

### Wiederkehrende Transaktion

- Startdatum
- Frequenz: wöchentlich, monatlich, quartalsweise oder jährlich
- Anzahl Wiederholungen

### Budget erstellen oder bearbeiten

- Monat
- Jahr
- Ausgabenkategorie
- Budgetlimit in CHF

### Budget vom Vormonat übernehmen

- Zielmonat
- Zieljahr

### Transaktionen filtern

- Typ
- Kategorie
- Monat

### CSV-Import

- CSV- oder ZIP-Datei
- Unterstützte Bereiche: Konten, Kategorien, Budgets, Transaktionen
- Erwartete Transaktionsspalten: `Datum; Typ; Kategorie; Konto; Beschreibung; Betrag CHF`

### Export

- Datenbereiche: Übersicht, Konten, Kategorien, Budgets, Transaktionen
- Monat für monatsabhängige Daten
- Format: CSV oder PDF

---

## Erwartete Ausgaben

### Übersicht

- Gesamteinnahmen des ausgewählten Monats
- Gesamtausgaben des ausgewählten Monats
- Saldo inklusive Startsalden
- Noch verfügbares Monatsbudget
- Kontenübersicht mit aktuellem Saldo
- Budgetstatus pro Kategorie
- Letzte Transaktionen im Monat
- Warnung bei Budgetüberschreitung
- Hinweis auf Ausgaben ohne Budget

### Konten

- Liste aller Konten
- Aktueller Saldo pro Konto
- Gesamtsaldo
- Anzahl der verknüpften Transaktionen
- Schutz vor Löschen verwendeter Konten

### Kategorien

- Liste aller Kategorien
- Typanzeige für Einnahmen und Ausgaben
- Anzahl der Verwendungen
- Schutz vor Löschen verwendeter Kategorien

### Transaktionen

- Speicherung in der Datenbank
- Aktualisierte Finanzübersicht
- Aktualisierte Kontostände
- Gruppierte Transaktionsliste nach Monat
- Bearbeiten und Löschen bestehender Transaktionen
- Filterbare Liste nach Typ, Kategorie und Monat

### Budgets

- Budget wird gespeichert oder aktualisiert
- Verbrauchtes Budget wird angezeigt
- Verbleibendes Budget wird berechnet
- Überschreitungen werden hervorgehoben
- Budgets können gelöscht werden, ohne bestehende Transaktionen zu entfernen
- Budgets aus dem Vormonat können übernommen werden

### Diagramme

- Ausgaben nach Kategorie
- Einnahmen vs. Ausgaben im Monatsvergleich
- Ausgabenverlauf des aktuellen Monats gegenüber dem Durchschnitt der letzten drei Monate

### Import

- Neue Datensätze werden erstellt
- Bestehende Datensätze werden bei Änderungen aktualisiert
- Unveränderte Datensätze werden übersprungen
- Fehlerhafte Zeilen werden gemeldet, ohne den gesamten Import abzubrechen
- ZIP-Dateien werden in sinnvoller Reihenfolge verarbeitet: Konten, Kategorien, Budgets, Transaktionen

### Export

- CSV-Export einzelner oder mehrerer Bereiche
- ZIP-Export bei mehreren CSV-Dateien
- PDF-Bericht mit den ausgewählten Bereichen
- PDF-Paginierung bei vielen Konten oder Tabellenzeilen

---

## Validierungsregeln

- Beträge für Transaktionen und Budgets müssen grösser als 0 sein.
- Transaktionstypen sind nur `income` oder `expense`.
- Kategorie und Transaktionstyp müssen zusammenpassen.
- Ausgaben dürfen nur erfasst werden, wenn für die Kategorie im jeweiligen Monat ein Budget existiert.
- Budgets dürfen nur für Ausgabenkategorien erstellt werden.
- Monat muss zwischen 1 und 12 liegen.
- Kontotyp muss aktuell `Bankkonto` oder `Bargeld` sein.
- Kategorien und Konten mit bestehenden Verknüpfungen werden vor dem Löschen geschützt.
- Für dieselbe Kategorie darf im selben Monat nicht mehrfach ein Budget erstellt werden.

---

## Abgleich mit Test Cases

| Bereich | Abgedeckt durch |
| --- | --- |
| Einnahmen erfassen | TC_001, Integrationstests |
| Ausgaben erfassen | TC_002, Integrationstests |
| Kategorien erstellen, bearbeiten und löschen | TC_003, TC_013, TC_014 |
| Budgets erstellen und anzeigen | TC_004, TC_005 |
| Budgetüberschreitung | TC_008, Unit Tests |
| Konten anzeigen und verwalten | TC_006, TC_012 |
| Persistenz | TC_007, Datenbanktests |
| Finanzberechnungen | TC_009, TC_010, TC_011, Unit Tests |
| Transaktionen filtern | TC_015, TC_016 |
| Transaktionen löschen | TC_017, TC_018 |
| Wiederkehrende Transaktionen | Integrationstest `test_application_workflow_creates_recurring_budgeted_expenses` |
| Budget bearbeiten und löschen | Integrationstest `test_budget_can_be_updated_and_deleted_through_application_workflow` |
| CSV-Import | `tests/test_import.py` |
| CSV- und PDF-Export | `tests/test_export.py` |
| Validierung ungültiger Eingaben | `tests/test_validation.py` |
| DAO und SQLite | `tests/test_db.py` |

---

## Offene Punkte

- Konto-Filter in der Transaktionsliste ergänzen
- Login oder Benutzerwechsel für mehrere echte Benutzer umsetzen
- Kontotypen erweitern, falls Sparkonto separat auswählbar sein soll
- Klassendiagramm und ER-Modell bei Änderungen am Datenmodell aktuell halten
