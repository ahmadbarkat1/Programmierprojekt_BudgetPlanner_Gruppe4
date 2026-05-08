# User Stories, Datentypen, Eingaben und erwartete Ausgaben

---

## 🧑‍💻 User Stories

### Muss-Funktionen

- Als Benutzer möchte ich Einnahmen erfassen, damit mein verfügbares Geld sichtbar wird.
- Als Benutzer möchte ich Ausgaben erfassen, damit ich meine Kosten nachvollziehen kann.
- Als Benutzer möchte ich Kategorien verwalten, damit Einnahmen und Ausgaben geordnet bleiben.
- Als Benutzer möchte ich mehrere Konten verwalten, damit ich Bankkonto, Bargeld und Sparkonto getrennt betrachten kann.
- Als Benutzer möchte ich eine Finanzübersicht sehen, damit ich Einnahmen, Ausgaben und Saldo erkenne.
- Als Benutzer möchte ich Monatsbudgets pro Ausgabenkategorie erfassen, damit ich meine Ausgaben kontrollieren kann.
- Als Benutzer möchte ich mein verbleibendes Budget sehen, damit ich weiss, wie viel ich noch ausgeben kann.
- Als Benutzer möchte ich sehen, ob ein Budget überschritten wurde.
- Als Benutzer möchte ich meine Daten in einer Datenbank speichern, damit sie nach einem Neustart erhalten bleiben.

### Erweiterte Funktionen

- Als Benutzer möchte ich Transaktionen bearbeiten und löschen, damit ich fehlerhafte Eingaben korrigieren kann.
- Als Benutzer möchte ich Kategorien bearbeiten und löschen, damit ich meine Struktur anpassen kann.
- Als Benutzer möchte ich Konten bearbeiten und löschen, damit meine Kontenübersicht aktuell bleibt.
- Als Benutzer möchte ich Transaktionen nach Typ, Kategorie und Monat filtern, damit ich bestimmte Einträge schneller finde.
- Als Benutzer möchte ich Diagramme sehen, damit ich meine Ausgaben besser verstehen kann.
- Als Benutzer möchte ich einen Monatsvergleich sehen, damit ich Einnahmen und Ausgaben über mehrere Monate vergleichen kann.

### Geplante Erweiterungen

- Als Benutzer möchte ich Transaktionen nach Konto filtern, damit ich Bewegungen einzelner Konten gezielt analysieren kann.
- Als Benutzer möchte ich Daten als CSV exportieren, damit ich sie extern weiterverwenden oder archivieren kann.
- Als Benutzer möchte ich mich einloggen können, damit mehrere Benutzer ihre eigenen Finanzdaten getrennt verwalten können.

---

## 🗂 Datentypen

### User
- id: int
- name: string
- email: string

### Account
- id: int
- name: string
- account_type: string
- starting_balance_chf: float
- user_id: int

### Category
- id: int
- name: string
- category_type: string (income / expense)
- user_id: int

### Transaction
- id: int
- amount_chf: float
- transaction_type: string (income / expense)
- transaction_date: date
- description: string
- account_id: int
- category_id: int

### Budget
- id: int
- month: int
- year: int
- limit_chf: float
- user_id: int
- category_id: int

---

## ⌨️ Eingaben

### Einnahme erfassen
- Betrag
- Datum
- Kategorie
- Konto
- Beschreibung

### Ausgabe erfassen
- Betrag
- Datum
- Kategorie
- Konto
- Beschreibung

### Kategorie erstellen
- Kategoriename
- Kategorietyp (Einnahme oder Ausgabe)

### Budget festlegen
- Monat
- Jahr
- Ausgabenkategorie
- Budgetlimit

### Konto erstellen
- Kontoname
- Kontotyp
- Startsaldo

### Transaktionen filtern
- Typ
- Kategorie
- Monat

---

## 📤 Erwartete Ausgaben

### Einnahme / Ausgabe
- Speicherung in der Datenbank
- Aktualisierte Finanzübersicht
- Aktualisierter Kontostand
- Anzeige in der Transaktionsliste

### Kategorie
- Neue Kategorie ist auswählbar
- Kategorie erscheint in der Kategorienübersicht

### Budget
- Budget wird gespeichert
- Verbrauchtes Budget wird angezeigt
- Verbleibendes Budget wird berechnet
- Budgetüberschreitungen werden sichtbar gemacht

### Finanzübersicht
- Gesamteinnahmen
- Gesamtausgaben
- Saldo
- Gesamtkontostand
- Verfügbares Budget
- Letzte Transaktionen

### Filter
- Transaktionsliste zeigt nur passende Einträge
- Filter können zurückgesetzt werden

### Diagramme
- Ausgaben nach Kategorie
- Einnahmen vs. Ausgaben im Monatsvergleich

### Konto
- Anzeige des aktuellen Kontostands
- Anzeige aller verwalteten Konten

### Warnung
- Hinweis bei Budgetüberschreitung

---

## 🚀 Mögliche Weiterentwicklung

- Filter nach Konto
- CSV-Export
- Login für mehrere Benutzer
