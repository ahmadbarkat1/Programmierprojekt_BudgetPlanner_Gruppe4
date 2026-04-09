**Eingaben**
- Kontoname
- Kontotyp
- Startsaldo
- Währung

**Validierungen**
- Kontoname darf nicht leer sein
- Startsaldo muss numerisch sein
- Währung darf nicht leer sein

**Erwartete Ausgaben**
- Konto wird gespeichert
- Aktueller Kontostand wird angezeigt
- Kontenübersicht mit allen verfügbaren Mitteln
- Buchungen können einem Konto zugeordnet werden

**Betroffene Datentypen**
- Konto
- Einnahme
- Ausgabe

---

## 5. Typische Eingabeformulare

### Formular Einnahme
- Titel
- Betrag
- Datum
- Kategorie
- Konto
- Beschreibung
- Wiederkehrend

### Formular Ausgabe
- Titel
- Betrag
- Datum
- Kategorie
- Konto
- Ausgabenart
- Beschreibung
- Wiederkehrend

### Formular Budget
- Monat
- Jahr
- Budgetbetrag
- Warnschwelle

### Formular Kategorie
- Name
- Typ
- Beschreibung

### Formular Konto
- Name
- Kontotyp
- Startsaldo
- Währung

### Formular Vermögenswert
- Name
- Typ
- Wert
- Bewertungsdatum
- Beschreibung

---

## 6. Erwartete Ausgaben der Anwendung

Die Anwendung soll insbesondere folgende Ausgaben bzw. Sichten bereitstellen:

### Dashboard / Startseite
- aktueller Monat
- gesamte Einnahmen
- gesamte Ausgaben
- Restbudget
- Budgetstatus
- Kontostände
- letzte Buchungen

### Listenansichten
- Liste aller Einnahmen
- Liste aller Ausgaben
- Filter nach Monat, Konto, Kategorie
- Sortierung nach Datum oder Betrag

### Auswertungen
- Ausgaben pro Kategorie
- Fixkosten vs. variable Kosten
- Monatsvergleich
- Budgetverbrauch in Prozent
- optionale grafische Darstellung

### Warnungen / Meldungen
- Eingabe erfolgreich gespeichert
- ungültige Eingabe
- Budget fast aufgebraucht
- Budget überschritten
- Fehler beim Speichern

---

## 7. Nicht-funktionale Anforderungen

- Die Anwendung läuft browserbasiert mit NiceGUI.
- Die Geschäftslogik wird objektorientiert in Python umgesetzt.
- Die Daten werden über SQLAlchemy mit einer Datenbank verbunden.
- Eingaben sollen validiert und verständlich rückgemeldet werden.
- Die Oberfläche soll einfach, übersichtlich und alltagstauglich sein.
- Die Struktur des Projekts soll modular und erweiterbar bleiben.

---

## 8. Abgrenzung MVP vs. spätere Ausbaustufen

### Zuerst umsetzen
- Einnahmen
- Ausgaben
- Kategorien
- Konten
- Monatsbudget
- Finanzübersicht
- Datenbankspeicherung
- Budgetwarnung

### Danach sinnvoll erweiterbar
- Diagramme
- Sparziele
- wiederkehrende Buchungen
- Export
- Benutzerlogin
- Steuerübersicht
- Monatsvergleich

---

## 9. Kurzfazit

Mit diesen User Stories ist der Projektumfang für den aktuellen Meilenstein klar beschrieben.  
Die Anforderungen decken die geplanten Hauptfunktionen ab und bilden eine gute Grundlage für die nächsten Schritte wie Testfälle, UML-Klassendiagramm, ER-Modell und ORM-Entitäten.