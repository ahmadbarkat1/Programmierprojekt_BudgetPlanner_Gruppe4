# User Stories, Datentypen, Eingaben und erwartete Ausgaben

---

## 🧑‍💻 User Stories

- Als Benutzer möchte ich Einnahmen erfassen, damit ich mein verfügbares Geld sehe.
- Als Benutzer möchte ich Ausgaben erfassen, damit ich meine Kosten nachvollziehen kann.
- Als Benutzer möchte ich Kategorien verwalten, damit meine Einträge übersichtlich bleiben.
- Als Benutzer möchte ich eine Finanzübersicht sehen, damit ich meinen aktuellen Stand erkenne.
- Als Benutzer möchte ich ein monatliches Budget festlegen, damit ich meine Ausgaben kontrollieren kann.
- Als Benutzer möchte ich mein verbleibendes Budget sehen, damit ich weiss, wie viel ich noch ausgeben kann.
- Als Benutzer möchte ich gewarnt werden, wenn mein Budget überschritten wird.
- Als Benutzer möchte ich mehrere Konten verwalten, damit ich den Überblick über meine Finanzen behalte.
- Als Benutzer möchte ich meine Daten speichern, damit nichts verloren geht.

---

## 🗂 Datentypen

### Transaction
- id: int
- amount: float
- date: date
- category_id: int
- account_id: int
- description: string
- type: string (income / expense)

### Category
- id: int
- name: string

### Budget
- id: int
- month: string
- limit: float

### Account
- id: int
- name: string
- balance: float

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
- Name

### Budget festlegen
- Monat
- Budgetbetrag

### Konto erstellen
- Kontoname
- Startsaldo

---

## 📤 Erwartete Ausgaben

### Einnahme / Ausgabe
- Speicherung in der Datenbank
- Aktualisierte Finanzübersicht
- Aktualisierter Kontostand

### Kategorie
- Neue Kategorie ist auswählbar

### Budget
- Anzeige des verbleibenden Budgets
- Vergleich zwischen Ausgaben und Budget

### Finanzübersicht
- Gesamteinnahmen
- Gesamtausgaben
- Aktueller Kontostand
- Verbleibendes Budget

### Warnung
- Hinweis bei Budgetüberschreitung

### Konto
- Anzeige des aktuellen Kontostands