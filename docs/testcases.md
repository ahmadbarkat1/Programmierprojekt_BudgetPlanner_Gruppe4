# Test Cases

Dieses Dokument beschreibt die Test Cases des Budget Planners im Format der vorgegebenen Vorlage. Die Testfälle sind auf den aktuellen Code-Stand abgestimmt und ergänzen die automatisierten Tests im Ordner `tests/`.

Wichtige Grundregel im aktuellen Projektstand: Ausgaben können über den vollständigen App-Workflow nur erfasst werden, wenn für die Ausgabenkategorie im jeweiligen Monat bereits ein Budget existiert.

---

## Testfallübersicht

| Testfall-ID | Bereich | Titel/Beschreibung | Abdeckung |
| --- | --- | --- | --- |
| TC_001 | Transaktionen | Überprüfen, dass eine Einnahme erstellt werden kann | Automatisiert / Service-Workflow |
| TC_002 | Transaktionen | Überprüfen, dass eine Ausgabe mit vorhandenem Budget erstellt werden kann | Automatisiert / Integrationstest |
| TC_003 | Kategorien | Überprüfen, dass eine Kategorie erstellt werden kann | Service-/UI-Workflow |
| TC_004 | Budgets | Überprüfen, dass ein Monatsbudget erstellt werden kann | Automatisiert / Integrationstest |
| TC_005 | Budgets | Überprüfen, dass das Restbudget korrekt berechnet wird | Automatisiert / Unit Test |
| TC_006 | Konten | Überprüfen, dass die Kontenübersicht angezeigt wird | Manuell / Service-Workflow |
| TC_007 | Datenbank | Überprüfen, dass Daten in SQLite gespeichert bleiben | Automatisiert / Datenbanktest |
| TC_008 | Budgets | Überprüfen, dass eine Budgetüberschreitung angezeigt wird | Automatisiert / Unit Test |
| TC_009 | Übersicht | Überprüfen, dass die Gesamtausgaben korrekt berechnet werden | Automatisiert / Unit Test |
| TC_010 | Übersicht | Überprüfen, dass die Gesamteinnahmen korrekt berechnet werden | Automatisiert / Unit Test |
| TC_011 | Konten | Überprüfen, dass der Kontostand korrekt berechnet wird | Automatisiert / Unit Test |
| TC_012 | Konten | Überprüfen, dass mehrere Konten verwaltet werden können | Manuell / Service-Workflow |
| TC_013 | Kategorien | Überprüfen, dass eine Kategorie bearbeitet werden kann | Manuell / Service-Workflow |
| TC_014 | Kategorien | Überprüfen, dass eine verwendete Kategorie nicht gelöscht werden kann | Service-Regel |
| TC_015 | Transaktionen | Überprüfen, dass Transaktionen nach Kategorie gefiltert werden können | Manueller UI-Test |
| TC_016 | Transaktionen | Überprüfen, dass Transaktionen nach Monat gefiltert werden können | Automatisiert / Datenbanktest |
| TC_017 | Transaktionen | Überprüfen, dass eine Einnahme gelöscht werden kann | Manuell / DAO-Workflow |
| TC_018 | Transaktionen | Überprüfen, dass eine Ausgabe gelöscht werden kann | Manuell / DAO-Workflow |
| TC_019 | Transaktionen | Überprüfen, dass eine Transaktion bearbeitet werden kann | Manuell / DAO-Workflow |
| TC_020 | Konten | Überprüfen, dass ein Konto bearbeitet werden kann | Manuell / Service-Workflow |
| TC_021 | Konten | Überprüfen, dass ein verwendetes Konto nicht gelöscht werden kann | Service-Regel |
| TC_022 | Budgets | Überprüfen, dass ein Budget bearbeitet werden kann | Automatisiert / Integrationstest |
| TC_023 | Budgets | Überprüfen, dass ein Budget gelöscht werden kann | Automatisiert / Integrationstest |
| TC_024 | Budgets | Überprüfen, dass Budgets aus dem Vormonat übernommen werden können | Service-/UI-Workflow |
| TC_025 | Transaktionen | Überprüfen, dass wiederkehrende Transaktionen erstellt werden können | Automatisiert / Integrationstest |
| TC_026 | Validierung | Überprüfen, dass ein ungültiger Betrag abgelehnt wird | Automatisiert / Validierungstest |
| TC_027 | Validierung | Überprüfen, dass ein ungültiger Transaktionstyp abgelehnt wird | Automatisiert / Validierungstest |
| TC_028 | Validierung | Überprüfen, dass Kategorie und Transaktionstyp zusammenpassen müssen | Service-Regel |
| TC_029 | Import | Überprüfen, dass ein Konto aus CSV importiert werden kann | Automatisiert / Importtest |
| TC_030 | Import | Überprüfen, dass eine Kategorie aus CSV importiert werden kann | Automatisiert / Importtest |
| TC_031 | Import | Überprüfen, dass ein Budget aus CSV importiert oder aktualisiert werden kann | Automatisiert / Importtest |
| TC_032 | Import | Überprüfen, dass Transaktionen aus CSV importiert werden können | Automatisiert / Importtest |
| TC_033 | Import | Überprüfen, dass fehlerhafte CSV-Zeilen gemeldet werden | Automatisiert / Importtest |
| TC_034 | Export | Überprüfen, dass CSV-Exportdateien erstellt werden | Automatisiert / Exporttest |
| TC_035 | Export | Überprüfen, dass mehrere CSV-Bereiche als ZIP exportiert werden | Automatisiert / Exporttest |
| TC_036 | Export | Überprüfen, dass ein PDF-Bericht erstellt wird | Automatisiert / Exporttest |
| TC_037 | Export | Überprüfen, dass der PDF-Export viele Konten paginiert | Automatisiert / Exporttest |
| TC_038 | UI | Überprüfen, dass der Darkmode umgeschaltet werden kann | Manueller UI-Test |
| TC_039 | UI | Überprüfen, dass der Hilfe-Dialog geöffnet werden kann | Manueller UI-Test |
| TC_040 | Navigation | Überprüfen, dass `/settings` zu `/accounts` weiterleitet | Manueller UI-Test |

---

## TC_001

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_001 |
| Testfall Titel/Beschreibung | Überprüfen, dass ein Benutzer eine Einnahme erfassen kann |
| Vorbedingungen | - Benutzer existiert<br>- Konto existiert<br>- Einnahmekategorie existiert<br>- Transaktionsseite ist zugänglich |
| Testschritte | 1. Transaktionsseite öffnen<br>2. Transaktionstyp `Einnahme` auswählen<br>3. Datum, Kategorie, Konto, Betrag und Beschreibung eingeben<br>4. Auf `Speichern` klicken |
| Testdaten/Eingabe | Betrag: `1000.00`<br>Datum: `2026-04-09`<br>Kategorie: `Nebenjob`<br>Konto: `Studentenkonto`<br>Beschreibung: `April Lohn` |
| Erwartetes Ergebnis | Einnahme wird erfolgreich gespeichert; Übersicht, Saldo und Kontostand werden aktualisiert |
| Tatsächliches Ergebnis | Einnahme wird erfolgreich gespeichert; Übersicht, Saldo und Kontostand werden aktualisiert |
| Status | Pass |
| Kommentare | Durch Transaktionsservice und Integrationsworkflow abgedeckt |

---

## TC_002

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_002 |
| Testfall Titel/Beschreibung | Überprüfen, dass ein Benutzer eine Ausgabe mit vorhandenem Budget erfassen kann |
| Vorbedingungen | - Benutzer existiert<br>- Konto existiert<br>- Ausgabekategorie existiert<br>- Monatsbudget für die ausgewählte Ausgabekategorie existiert |
| Testschritte | 1. Transaktionsseite öffnen<br>2. Transaktionstyp `Ausgabe` auswählen<br>3. Datum, Kategorie, Konto, Betrag und Beschreibung eingeben<br>4. Auf `Speichern` klicken |
| Testdaten/Eingabe | Budgetmonat: `Mai 2026`<br>Kategorie: `Reisen`<br>Budgetlimit: `300.00`<br>Ausgabe: `180.00`<br>Datum: `2026-05-18`<br>Beschreibung: `Zugticket` |
| Erwartetes Ergebnis | Ausgabe wird erfolgreich gespeichert; Monatsausgaben und Budgetstatus werden aktualisiert; Restbudget beträgt `120.00 CHF` |
| Tatsächliches Ergebnis | Ausgabe wird erfolgreich gespeichert; Monatsausgaben und Budgetstatus werden aktualisiert; Restbudget beträgt `120.00 CHF` |
| Status | Pass |
| Kommentare | Durch `test_application_workflow_creates_budgeted_expense_and_dashboard_status` abgedeckt |

---

## TC_003

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_003 |
| Testfall Titel/Beschreibung | Überprüfen, dass ein Benutzer eine Kategorie erstellen kann |
| Vorbedingungen | - Benutzer existiert<br>- Kategorienseite ist zugänglich |
| Testschritte | 1. Kategorienseite öffnen<br>2. Kategoriename eingeben<br>3. Kategorietyp auswählen<br>4. Auf `Erstellen` klicken |
| Testdaten/Eingabe | Kategoriename: `Betriebskosten`<br>Typ: `Ausgabe` |
| Erwartetes Ergebnis | Kategorie wird gespeichert, in der Kategorienliste angezeigt und ist für passende Transaktionen auswählbar |
| Tatsächliches Ergebnis | Kategorie wird gespeichert, in der Kategorienliste angezeigt und ist für passende Transaktionen auswählbar |
| Status | Pass |
| Kommentare | Kategorieerstellung ist in `CategoryService` umgesetzt |

---

## TC_004

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_004 |
| Testfall Titel/Beschreibung | Überprüfen, dass ein Benutzer ein monatliches Budget erstellen kann |
| Vorbedingungen | - Benutzer existiert<br>- Ausgabekategorie existiert<br>- Budgetseite ist zugänglich |
| Testschritte | 1. Budgetseite öffnen<br>2. Monat und Jahr eingeben<br>3. Ausgabekategorie auswählen<br>4. Budgetlimit eingeben<br>5. Auf `Speichern` klicken |
| Testdaten/Eingabe | Monat: `5`<br>Jahr: `2026`<br>Kategorie: `Lebensmittel`<br>Limit: `500.00` |
| Erwartetes Ergebnis | Budget wird gespeichert und im ausgewählten Monat angezeigt |
| Tatsächliches Ergebnis | Budget wird gespeichert und im ausgewählten Monat angezeigt |
| Status | Pass |
| Kommentare | Durch `test_budget_can_be_created_for_expense_category` abgedeckt |

---

## TC_005

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_005 |
| Testfall Titel/Beschreibung | Überprüfen, dass das verbleibende Budget korrekt berechnet wird |
| Vorbedingungen | - Budget existiert<br>- Passende Ausgabetransaktion existiert |
| Testschritte | 1. Übersicht oder Budgetseite öffnen<br>2. Budgetverbrauch prüfen<br>3. Restbudget prüfen |
| Testdaten/Eingabe | Budget: `500.00`<br>Ausgaben: `120.00` |
| Erwartetes Ergebnis | Verbrauchter Betrag ist `120.00 CHF`; Restbudget ist `380.00 CHF`; Budget ist nicht überschritten |
| Tatsächliches Ergebnis | Verbrauchter Betrag ist `120.00 CHF`; Restbudget ist `380.00 CHF`; Budget ist nicht überschritten |
| Status | Pass |
| Kommentare | Durch `test_budget_status_not_exceeded` abgedeckt |

---

## TC_006

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_006 |
| Testfall Titel/Beschreibung | Überprüfen, dass die Kontenübersicht angezeigt wird |
| Vorbedingungen | - Benutzer existiert<br>- Mindestens ein Konto existiert<br>- Kontenseite ist zugänglich |
| Testschritte | 1. Kontenseite öffnen<br>2. Kontoliste prüfen<br>3. Salden und Zusammenfassung prüfen |
| Testdaten/Eingabe | Konto: `Studentenkonto`<br>Startsaldo: `1000.00` |
| Erwartetes Ergebnis | Alle Konten, Startsalden, aktuelle Salden und Zusammenfassungswerte werden angezeigt |
| Tatsächliches Ergebnis | Alle Konten, Startsalden, aktuelle Salden und Zusammenfassungswerte werden angezeigt |
| Status | Pass |
| Kommentare | Kontostände werden mit `FinanceService.account_balance` berechnet |

---

## TC_007

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_007 |
| Testfall Titel/Beschreibung | Überprüfen, dass Daten in SQLite gespeichert bleiben |
| Vorbedingungen | - SQLite-Datenbank ist aktiv<br>- App-Schema ist initialisiert |
| Testschritte | 1. Datensatz erstellen<br>2. Aktuelle Daten abfragen<br>3. App neu starten oder Daten erneut laden<br>4. Prüfen, ob die Daten weiterhin existieren |
| Testdaten/Eingabe | Beispielkonto oder Beispieltransaktion |
| Erwartetes Ergebnis | Erstellte Daten bleiben in SQLite gespeichert und werden wieder angezeigt |
| Tatsächliches Ergebnis | Erstellte Daten bleiben in SQLite gespeichert und werden wieder angezeigt |
| Status | Pass |
| Kommentare | Durch `tests/test_db.py` abgedeckt |

---

## TC_008

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_008 |
| Testfall Titel/Beschreibung | Überprüfen, dass eine Budgetüberschreitung angezeigt wird |
| Vorbedingungen | - Budget existiert<br>- Passende Ausgabe ist höher als das Budgetlimit |
| Testschritte | 1. Budget erstellen oder auswählen<br>2. Ausgabe über dem Limit erfassen<br>3. Übersicht oder Budgetseite öffnen<br>4. Budgetstatus prüfen |
| Testdaten/Eingabe | Budget: `100.00`<br>Ausgabe: `120.00` |
| Erwartetes Ergebnis | Restbudget ist `-20.00 CHF`; Budgetstatus wird als überschritten markiert |
| Tatsächliches Ergebnis | Restbudget ist `-20.00 CHF`; Budgetstatus wird als überschritten markiert |
| Status | Pass |
| Kommentare | Durch `test_budget_status_exceeded` abgedeckt |

---

## TC_009

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_009 |
| Testfall Titel/Beschreibung | Überprüfen, dass die Gesamtausgaben korrekt berechnet werden |
| Vorbedingungen | - Ausgabetransaktionen existieren |
| Testschritte | 1. Übersicht öffnen<br>2. Gesamtwert der Ausgaben prüfen |
| Testdaten/Eingabe | Ausgaben: `800.00` und `120.00` |
| Erwartetes Ergebnis | Gesamtausgaben betragen `920.00 CHF` |
| Tatsächliches Ergebnis | Gesamtausgaben betragen `920.00 CHF` |
| Status | Pass |
| Kommentare | Durch `test_finance_overview` abgedeckt |

---

## TC_010

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_010 |
| Testfall Titel/Beschreibung | Überprüfen, dass die Gesamteinnahmen korrekt berechnet werden |
| Vorbedingungen | - Einnahmetransaktionen existieren |
| Testschritte | 1. Übersicht öffnen<br>2. Gesamtwert der Einnahmen prüfen |
| Testdaten/Eingabe | Einnahme: `3000.00` |
| Erwartetes Ergebnis | Gesamteinnahmen betragen `3000.00 CHF` |
| Tatsächliches Ergebnis | Gesamteinnahmen betragen `3000.00 CHF` |
| Status | Pass |
| Kommentare | Durch `test_finance_overview` abgedeckt |

---

## TC_011

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_011 |
| Testfall Titel/Beschreibung | Überprüfen, dass der Kontostand korrekt berechnet wird |
| Vorbedingungen | - Konto existiert<br>- Einnahmen und Ausgaben existieren |
| Testschritte | 1. Kontenseite oder Übersicht öffnen<br>2. Berechneten Kontostand prüfen |
| Testdaten/Eingabe | Startsaldo: `1000.00`<br>Einnahme: `3000.00`<br>Ausgaben: `920.00` |
| Erwartetes Ergebnis | Kontostand beträgt `3080.00 CHF` |
| Tatsächliches Ergebnis | Kontostand beträgt `3080.00 CHF` |
| Status | Pass |
| Kommentare | Durch `test_account_balance` abgedeckt |

---

## TC_012

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_012 |
| Testfall Titel/Beschreibung | Überprüfen, dass mehrere Konten verwaltet werden können |
| Vorbedingungen | - Benutzer existiert<br>- Kontenseite ist zugänglich |
| Testschritte | 1. Kontenseite öffnen<br>2. Neues Konto erstellen<br>3. Kontenübersicht prüfen<br>4. Transaktionsformular öffnen und Kontoauswahl prüfen |
| Testdaten/Eingabe | Kontoname: `Bargeld Ferien`<br>Kontotyp: `Bargeld`<br>Startsaldo: `250.00` |
| Erwartetes Ergebnis | Neues Konto wird gespeichert, angezeigt und ist in Transaktionsformularen auswählbar |
| Tatsächliches Ergebnis | Neues Konto wird gespeichert, angezeigt und ist in Transaktionsformularen auswählbar |
| Status | Pass |
| Kommentare | Kontoerstellung ist in `AccountService` umgesetzt |

---

## TC_013

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_013 |
| Testfall Titel/Beschreibung | Überprüfen, dass eine Kategorie bearbeitet werden kann |
| Vorbedingungen | - Kategorie existiert<br>- Kategorienseite ist zugänglich |
| Testschritte | 1. Kategorienseite öffnen<br>2. Bearbeiten-Aktion für eine Kategorie klicken<br>3. Name oder Typ ändern<br>4. Auf `Speichern` klicken |
| Testdaten/Eingabe | Alter Name: `Nebenkosten`<br>Neuer Name: `Betriebskosten` |
| Erwartetes Ergebnis | Kategorie wird aktualisiert und mit den neuen Daten angezeigt |
| Tatsächliches Ergebnis | Kategorie wird aktualisiert und mit den neuen Daten angezeigt |
| Status | Pass |
| Kommentare | Kategorieaktualisierung ist in `CategoryService.update_category` umgesetzt |

---

## TC_014

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_014 |
| Testfall Titel/Beschreibung | Überprüfen, dass eine verwendete Kategorie nicht gelöscht werden kann |
| Vorbedingungen | - Kategorie existiert<br>- Kategorie ist mit einer Transaktion oder einem Budget verknüpft |
| Testschritte | 1. Kategorienseite öffnen<br>2. Löschen-Aktion für eine verwendete Kategorie klicken<br>3. Löschung bestätigen |
| Testdaten/Eingabe | Kategorie: `Lebensmittel` mit bestehendem Budget |
| Erwartetes Ergebnis | Kategorie wird nicht gelöscht; Warnmeldung wird angezeigt |
| Tatsächliches Ergebnis | Kategorie wird nicht gelöscht; Warnmeldung wird angezeigt |
| Status | Pass |
| Kommentare | Löschschutz ist mit `CategoryDAO.is_used` umgesetzt |

---

## TC_015

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_015 |
| Testfall Titel/Beschreibung | Überprüfen, dass Transaktionen nach Kategorie gefiltert werden können |
| Vorbedingungen | - Transaktionen mit unterschiedlichen Kategorien existieren<br>- Transaktionsseite ist zugänglich |
| Testschritte | 1. Transaktionsseite öffnen<br>2. Kategorie im Filter auswählen<br>3. Transaktionsliste prüfen |
| Testdaten/Eingabe | Kategoriefilter: `Miete` |
| Erwartetes Ergebnis | Nur Transaktionen der ausgewählten Kategorie werden angezeigt |
| Tatsächliches Ergebnis | Nur Transaktionen der ausgewählten Kategorie werden angezeigt |
| Status | Pass |
| Kommentare | Manueller UI-Test; Filter ist in `transactions_page.py` umgesetzt |

---

## TC_016

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_016 |
| Testfall Titel/Beschreibung | Überprüfen, dass Transaktionen nach Monat gefiltert werden können |
| Vorbedingungen | - Transaktionen aus unterschiedlichen Monaten existieren |
| Testschritte | 1. Transaktionsseite öffnen<br>2. Monat im Filter auswählen<br>3. Transaktionsliste prüfen |
| Testdaten/Eingabe | Monatsfilter: `Mai 2026` |
| Erwartetes Ergebnis | Nur Transaktionen aus Mai 2026 werden angezeigt |
| Tatsächliches Ergebnis | Nur Transaktionen aus Mai 2026 werden angezeigt |
| Status | Pass |
| Kommentare | Monatsabfrage ist durch `test_monthly_transaction_query_returns_only_matching_month` abgedeckt |

---

## TC_017

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_017 |
| Testfall Titel/Beschreibung | Überprüfen, dass eine Einnahme gelöscht werden kann |
| Vorbedingungen | - Einnahmetransaktion existiert |
| Testschritte | 1. Transaktionsseite öffnen<br>2. Löschen-Aktion bei Einnahmetransaktion klicken<br>3. Löschung bestätigen |
| Testdaten/Eingabe | Einnahme: `1000.00`<br>Kategorie: `Nebenjob` |
| Erwartetes Ergebnis | Einnahmetransaktion wird gelöscht; Übersicht und Kontostand werden aktualisiert |
| Tatsächliches Ergebnis | Einnahmetransaktion wird gelöscht; Übersicht und Kontostand werden aktualisiert |
| Status | Pass |
| Kommentare | Löschung ist in `TransactionService.delete_transaction` umgesetzt |

---

## TC_018

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_018 |
| Testfall Titel/Beschreibung | Überprüfen, dass eine Ausgabe gelöscht werden kann |
| Vorbedingungen | - Ausgabetransaktion existiert |
| Testschritte | 1. Transaktionsseite öffnen<br>2. Löschen-Aktion bei Ausgabetransaktion klicken<br>3. Löschung bestätigen |
| Testdaten/Eingabe | Ausgabe: `200.00`<br>Kategorie: `Miete` |
| Erwartetes Ergebnis | Ausgabetransaktion wird gelöscht; Übersicht, Kontostand und Budgetstatus werden aktualisiert |
| Tatsächliches Ergebnis | Ausgabetransaktion wird gelöscht; Übersicht, Kontostand und Budgetstatus werden aktualisiert |
| Status | Pass |
| Kommentare | Löschung ist in `TransactionDAO.delete` umgesetzt |

---

## TC_019

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_019 |
| Testfall Titel/Beschreibung | Überprüfen, dass eine Transaktion bearbeitet werden kann |
| Vorbedingungen | - Transaktion existiert<br>- Passendes Konto und passende Kategorie existieren |
| Testschritte | 1. Transaktionsseite öffnen<br>2. Bearbeiten-Aktion bei Transaktion klicken<br>3. Betrag, Datum, Konto, Kategorie oder Beschreibung ändern<br>4. Auf `Speichern` klicken |
| Testdaten/Eingabe | Alter Betrag: `45.00`<br>Neuer Betrag: `50.00` |
| Erwartetes Ergebnis | Transaktion wird aktualisiert; Berechnungen verwenden den geänderten Betrag |
| Tatsächliches Ergebnis | Transaktion wird aktualisiert; Berechnungen verwenden den geänderten Betrag |
| Status | Pass |
| Kommentare | Aktualisierung ist in `TransactionService.update_transaction` umgesetzt |

---

## TC_020

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_020 |
| Testfall Titel/Beschreibung | Überprüfen, dass ein Konto bearbeitet werden kann |
| Vorbedingungen | - Konto existiert<br>- Kontenseite ist zugänglich |
| Testschritte | 1. Kontenseite öffnen<br>2. Bearbeiten-Aktion bei Konto klicken<br>3. Name, Typ oder Startsaldo ändern<br>4. Auf `Speichern` klicken |
| Testdaten/Eingabe | Alter Name: `Testkonto`<br>Neuer Name: `Haushaltskonto` |
| Erwartetes Ergebnis | Konto wird aktualisiert und mit den neuen Daten angezeigt |
| Tatsächliches Ergebnis | Konto wird aktualisiert und mit den neuen Daten angezeigt |
| Status | Pass |
| Kommentare | Aktualisierung ist in `AccountService.update_account` umgesetzt |

---

## TC_021

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_021 |
| Testfall Titel/Beschreibung | Überprüfen, dass ein verwendetes Konto nicht gelöscht werden kann |
| Vorbedingungen | - Konto existiert<br>- Konto ist mit mindestens einer Transaktion verknüpft |
| Testschritte | 1. Kontenseite öffnen<br>2. Löschen-Aktion bei verwendetem Konto klicken<br>3. Löschung bestätigen |
| Testdaten/Eingabe | Konto: `Studentenkonto` mit bestehender Transaktion |
| Erwartetes Ergebnis | Konto wird nicht gelöscht; Warnmeldung wird angezeigt |
| Tatsächliches Ergebnis | Konto wird nicht gelöscht; Warnmeldung wird angezeigt |
| Status | Pass |
| Kommentare | Löschschutz ist in `AccountService.delete_account` umgesetzt |

---

## TC_022

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_022 |
| Testfall Titel/Beschreibung | Überprüfen, dass ein Budget bearbeitet werden kann |
| Vorbedingungen | - Budget existiert<br>- Ausgabekategorie existiert |
| Testschritte | 1. Budgetseite öffnen<br>2. Bearbeiten-Aktion bei Budget klicken<br>3. Budgetlimit ändern<br>4. Auf `Speichern` klicken |
| Testdaten/Eingabe | Altes Limit: `200.00`<br>Neues Limit: `250.00` |
| Erwartetes Ergebnis | Budget wird aktualisiert; Restbudget und Auslastung werden neu berechnet |
| Tatsächliches Ergebnis | Budget wird aktualisiert; Restbudget und Auslastung werden neu berechnet |
| Status | Pass |
| Kommentare | Durch `test_budget_can_be_updated_and_deleted_through_application_workflow` abgedeckt |

---

## TC_023

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_023 |
| Testfall Titel/Beschreibung | Überprüfen, dass ein Budget gelöscht werden kann |
| Vorbedingungen | - Budget existiert |
| Testschritte | 1. Budgetseite öffnen<br>2. Löschen-Aktion bei Budget klicken<br>3. Löschung bestätigen |
| Testdaten/Eingabe | Budget: `Studium`<br>Monat: `Mai 2026` |
| Erwartetes Ergebnis | Budget wird gelöscht; bestehende Transaktionen bleiben unverändert |
| Tatsächliches Ergebnis | Budget wird gelöscht; bestehende Transaktionen bleiben unverändert |
| Status | Pass |
| Kommentare | Durch `test_budget_can_be_updated_and_deleted_through_application_workflow` abgedeckt |

---

## TC_024

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_024 |
| Testfall Titel/Beschreibung | Überprüfen, dass Budgets aus dem Vormonat übernommen werden können |
| Vorbedingungen | - Mindestens ein Budget existiert im Vormonat<br>- Passendes Budget fehlt im Zielmonat |
| Testschritte | 1. Budgetseite öffnen<br>2. Zielmonat und Zieljahr eingeben<br>3. Auf `Budget vom Vormonat übernehmen` klicken |
| Testdaten/Eingabe | Quellmonat: `April 2026`<br>Zielmonat: `Mai 2026`<br>Kategorie: `Lebensmittel`<br>Limit: `500.00` |
| Erwartetes Ergebnis | Fehlende Budgets werden in den Zielmonat kopiert; bestehende Budgets werden nicht doppelt erstellt |
| Tatsächliches Ergebnis | Fehlende Budgets werden in den Zielmonat kopiert; bestehende Budgets werden nicht doppelt erstellt |
| Status | Pass |
| Kommentare | In `BudgetService.copy_previous_month` umgesetzt |

---

## TC_025

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_025 |
| Testfall Titel/Beschreibung | Überprüfen, dass wiederkehrende Transaktionen erstellt werden können |
| Vorbedingungen | - Konto existiert<br>- Kategorie existiert<br>- Benötigte Monatsbudgets existieren |
| Testschritte | 1. Transaktionsseite öffnen<br>2. Wiederkehrende Transaktion aktivieren<br>3. Frequenz auswählen<br>4. Anzahl Wiederholungen eingeben<br>5. Auf `Speichern` klicken |
| Testdaten/Eingabe | Betrag: `45.00`<br>Startdatum: `2026-05-18`<br>Frequenz: `monthly`<br>Wiederholungen: `2` |
| Erwartetes Ergebnis | Zwei Transaktionen werden erstellt: `2026-05-18` und `2026-06-18`; zweite Beschreibung erhält Zusatz `(2/2)` |
| Tatsächliches Ergebnis | Zwei Transaktionen werden erstellt: `2026-05-18` und `2026-06-18`; zweite Beschreibung erhält Zusatz `(2/2)` |
| Status | Pass |
| Kommentare | Durch `test_application_workflow_creates_recurring_budgeted_expenses` abgedeckt |

---

## TC_026

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_026 |
| Testfall Titel/Beschreibung | Überprüfen, dass ein ungültiger Betrag abgelehnt wird |
| Vorbedingungen | - Transaktionsformular oder Transaktionsservice ist verfügbar |
| Testschritte | 1. Transaktionsformular öffnen<br>2. Betrag `0.00` eingeben<br>3. Restliche Pflichtfelder ausfüllen<br>4. Auf `Speichern` klicken |
| Testdaten/Eingabe | Betrag: `0.00` |
| Erwartetes Ergebnis | Transaktion wird nicht gespeichert; Validierungsfehler wird angezeigt |
| Tatsächliches Ergebnis | Transaktion wird nicht gespeichert; Validierungsfehler wird angezeigt |
| Status | Pass |
| Kommentare | Durch `test_transaction_invalid_amount` abgedeckt |

---

## TC_027

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_027 |
| Testfall Titel/Beschreibung | Überprüfen, dass ein ungültiger Transaktionstyp abgelehnt wird |
| Vorbedingungen | - Validierung des Transaktionsservices wird ausgeführt |
| Testschritte | 1. Transaktion über Service erstellen<br>2. Ungültigen Transaktionstyp verwenden<br>3. Validierung ausführen |
| Testdaten/Eingabe | Transaktionstyp: `invalid` |
| Erwartetes Ergebnis | Transaktion wird nicht gespeichert; `ValueError` wird ausgelöst |
| Tatsächliches Ergebnis | Transaktion wird nicht gespeichert; `ValueError` wird ausgelöst |
| Status | Pass |
| Kommentare | Durch `test_transaction_invalid_type` abgedeckt |

---

## TC_028

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_028 |
| Testfall Titel/Beschreibung | Überprüfen, dass Kategorie und Transaktionstyp zusammenpassen müssen |
| Vorbedingungen | - Einnahmekategorie existiert<br>- Ausgabe soll erstellt werden |
| Testschritte | 1. Transaktionsseite öffnen<br>2. Transaktionstyp `Ausgabe` auswählen<br>3. Einnahmekategorie auswählen oder über Service mitgeben<br>4. Speichern versuchen |
| Testdaten/Eingabe | Transaktionstyp: `expense`<br>Kategorie: `Nebenjob` |
| Erwartetes Ergebnis | Transaktion wird abgelehnt; Fehlermeldung zeigt, dass die Kategorie nicht zum Transaktionstyp passt |
| Tatsächliches Ergebnis | Transaktion wird abgelehnt; Fehlermeldung zeigt, dass die Kategorie nicht zum Transaktionstyp passt |
| Status | Pass |
| Kommentare | Regel ist in `TransactionService._validate_transaction` umgesetzt |

---

## TC_029

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_029 |
| Testfall Titel/Beschreibung | Überprüfen, dass ein Konto aus CSV importiert werden kann |
| Vorbedingungen | - Importdialog ist zugänglich |
| Testschritte | 1. Importdialog öffnen<br>2. Konto-CSV hochladen<br>3. Kontenliste prüfen |
| Testdaten/Eingabe | Kopfzeile: `Kontoname;Kontotyp;Startsaldo CHF`<br>Zeile: `Juni Konto;Bankkonto;250.00` |
| Erwartetes Ergebnis | Konto wird erstellt und in der Kontenliste angezeigt |
| Tatsächliches Ergebnis | Konto wird erstellt und in der Kontenliste angezeigt |
| Status | Pass |
| Kommentare | Durch `test_import_creates_new_account_from_csv` abgedeckt |

---

## TC_030

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_030 |
| Testfall Titel/Beschreibung | Überprüfen, dass eine Kategorie aus CSV importiert werden kann |
| Vorbedingungen | - Importdialog ist zugänglich |
| Testschritte | 1. Importdialog öffnen<br>2. Kategorie-CSV hochladen<br>3. Kategorienliste prüfen |
| Testdaten/Eingabe | Kopfzeile: `Kategoriename;Typ`<br>Zeile: `Juni Kategorie;Ausgabe` |
| Erwartetes Ergebnis | Kategorie wird erstellt und als Ausgabekategorie gespeichert |
| Tatsächliches Ergebnis | Kategorie wird erstellt und als Ausgabekategorie gespeichert |
| Status | Pass |
| Kommentare | Durch `test_import_creates_new_category_from_csv` abgedeckt |

---

## TC_031

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_031 |
| Testfall Titel/Beschreibung | Überprüfen, dass ein Budget aus CSV importiert oder aktualisiert werden kann |
| Vorbedingungen | - Passende Ausgabekategorie existiert<br>- Importdialog ist zugänglich |
| Testschritte | 1. Budget-CSV mit erstem Limit importieren<br>2. Budget-CSV mit gleichem Monat/gleicher Kategorie und geändertem Limit importieren<br>3. Budgetseite prüfen |
| Testdaten/Eingabe | Kopfzeile: `Monat;Jahr;Kategorie;Limit CHF`<br>Erstes Limit: `400.00`<br>Zweites Limit: `800.00` |
| Erwartetes Ergebnis | Erster Import erstellt das Budget; zweiter Import aktualisiert das vorhandene Budget |
| Tatsächliches Ergebnis | Erster Import erstellt das Budget; zweiter Import aktualisiert das vorhandene Budget |
| Status | Pass |
| Kommentare | Durch `test_import_updates_existing_june_budget` abgedeckt |

---

## TC_032

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_032 |
| Testfall Titel/Beschreibung | Überprüfen, dass Transaktionen aus CSV importiert werden können |
| Vorbedingungen | - Konto existiert<br>- Kategorien existieren<br>- Benötigte Budgets für Ausgaben existieren |
| Testschritte | 1. Importdialog öffnen<br>2. Transaktions-CSV hochladen<br>3. Transaktionsliste prüfen |
| Testdaten/Eingabe | Zeilen mit `income`, `Einnahme`, `expense`, `Ausgabe` sowie positiven oder negativen Ausgabebeträgen |
| Erwartetes Ergebnis | Alle gültigen Transaktionen werden importiert; Ausgabebeträge werden intern positiv gespeichert und über den Transaktionstyp getrennt |
| Tatsächliches Ergebnis | Alle gültigen Transaktionen werden importiert; Ausgabebeträge werden intern positiv gespeichert und über den Transaktionstyp getrennt |
| Status | Pass |
| Kommentare | Durch `test_import_transactions_accepts_income_expense_and_positive_or_negative_expenses` abgedeckt |

---

## TC_033

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_033 |
| Testfall Titel/Beschreibung | Überprüfen, dass fehlerhafte CSV-Zeilen gemeldet werden |
| Vorbedingungen | - Importdialog ist zugänglich |
| Testschritte | 1. CSV mit fehlender Abhängigkeit hochladen<br>2. Importmeldung prüfen |
| Testdaten/Eingabe | Budgetzeile mit Kategorie `Fehlende Kategorie` |
| Erwartetes Ergebnis | Datensatz wird nicht erstellt; Fehlerliste enthält die fehlende Kategorie |
| Tatsächliches Ergebnis | Datensatz wird nicht erstellt; Fehlerliste enthält die fehlende Kategorie |
| Status | Pass |
| Kommentare | Durch `test_import_reports_missing_dependencies_instead_of_silent_skip` abgedeckt |

---

## TC_034

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_034 |
| Testfall Titel/Beschreibung | Überprüfen, dass CSV-Exportdateien erstellt werden |
| Vorbedingungen | - Exportdialog ist zugänglich |
| Testschritte | 1. Exportdialog öffnen<br>2. Einen Exportbereich auswählen<br>3. Format `CSV` auswählen<br>4. Auf `Exportieren` klicken |
| Testdaten/Eingabe | Exportbereiche: Übersicht, Konten, Kategorien, Budgets oder Transaktionen |
| Erwartetes Ergebnis | CSV-Datei wird mit passender Kopfzeile und Daten erzeugt |
| Tatsächliches Ergebnis | CSV-Datei wird mit passender Kopfzeile und Daten erzeugt |
| Status | Pass |
| Kommentare | Durch `test_export_csv_templates_include_headers` abgedeckt |

---

## TC_035

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_035 |
| Testfall Titel/Beschreibung | Überprüfen, dass mehrere CSV-Exportbereiche als ZIP exportiert werden |
| Vorbedingungen | - Exportdialog ist zugänglich<br>- Mehr als ein Exportbereich ist ausgewählt |
| Testschritte | 1. Exportdialog öffnen<br>2. Mehrere Bereiche auswählen<br>3. Format `CSV` auswählen<br>4. Auf `Exportieren` klicken |
| Testdaten/Eingabe | Exportbereiche: Konten, Kategorien, Budgets |
| Erwartetes Ergebnis | ZIP-Datei wird erzeugt und enthält die ausgewählten CSV-Dateien |
| Tatsächliches Ergebnis | ZIP-Datei wird erzeugt und enthält die ausgewählten CSV-Dateien |
| Status | Pass |
| Kommentare | Durch `test_create_export_zip_contains_selected_csv_files` abgedeckt |

---

## TC_036

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_036 |
| Testfall Titel/Beschreibung | Überprüfen, dass ein PDF-Bericht erstellt wird |
| Vorbedingungen | - Exportdialog ist zugänglich |
| Testschritte | 1. Exportdialog öffnen<br>2. Exportbereiche auswählen<br>3. Format `PDF` auswählen<br>4. Auf `Exportieren` klicken |
| Testdaten/Eingabe | Exportbereiche: Übersicht, Konten, Kategorien, Budgets, Transaktionen |
| Erwartetes Ergebnis | PDF-Bericht beginnt mit `%PDF-`; ausgewählte Bereiche sind als PDF-Seiten enthalten |
| Tatsächliches Ergebnis | PDF-Bericht beginnt mit `%PDF-`; ausgewählte Bereiche sind als PDF-Seiten enthalten |
| Status | Pass |
| Kommentare | Durch `test_pdf_export_returns_pdf_bytes_for_all_areas` abgedeckt |

---

## TC_037

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_037 |
| Testfall Titel/Beschreibung | Überprüfen, dass der PDF-Export viele Konten paginiert |
| Vorbedingungen | - Viele Konten existieren<br>- Exportdialog ist zugänglich |
| Testschritte | 1. Viele Konten erstellen<br>2. Kontenbereich als PDF exportieren<br>3. Seitenanzahl prüfen |
| Testdaten/Eingabe | `12` zusätzliche Konten |
| Erwartetes Ergebnis | PDF enthält mehr als eine Seite für Konten |
| Tatsächliches Ergebnis | PDF enthält mehr als eine Seite für Konten |
| Status | Pass |
| Kommentare | Durch `test_pdf_export_paginates_accounts_when_many_exist` abgedeckt |

---

## TC_038

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_038 |
| Testfall Titel/Beschreibung | Überprüfen, dass der Darkmode umgeschaltet werden kann |
| Vorbedingungen | - App läuft im Browser |
| Testschritte | 1. App öffnen<br>2. Button `Darkmode` im Header klicken<br>3. Button erneut klicken |
| Testdaten/Eingabe | Keine Eingabedaten |
| Erwartetes Ergebnis | UI wechselt zwischen hellem und dunklem Design; gewählter Modus wird im Browser gespeichert |
| Tatsächliches Ergebnis | UI wechselt zwischen hellem und dunklem Design; gewählter Modus wird im Browser gespeichert |
| Status | Pass |
| Kommentare | Manueller UI-Test; umgesetzt in `toggle_dark_mode` |

---

## TC_039

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_039 |
| Testfall Titel/Beschreibung | Überprüfen, dass der Hilfe-Dialog geöffnet werden kann |
| Vorbedingungen | - App läuft im Browser |
| Testschritte | 1. App öffnen<br>2. Hilfe-Icon im Header klicken<br>3. Hilfe-Dialog lesen<br>4. Dialog schließen |
| Testdaten/Eingabe | Keine Eingabedaten |
| Erwartetes Ergebnis | Hilfe-Dialog mit Kurzinfos zu Übersicht, Konten, Kategorien, Budget, Transaktionen, Import und Export wird angezeigt |
| Tatsächliches Ergebnis | Hilfe-Dialog mit Kurzinfos zu Übersicht, Konten, Kategorien, Budget, Transaktionen, Import und Export wird angezeigt |
| Status | Pass |
| Kommentare | Manueller UI-Test; umgesetzt in `open_help_dialog` |

---

## TC_040

| Feld | Details |
| --- | --- |
| Testfall-ID | TC_040 |
| Testfall Titel/Beschreibung | Überprüfen, dass `/settings` zu `/accounts` weiterleitet |
| Vorbedingungen | - App läuft im Browser |
| Testschritte | 1. URL `/settings` öffnen<br>2. Navigationsziel beobachten |
| Testdaten/Eingabe | URL: `/settings` |
| Erwartetes Ergebnis | Benutzer wird automatisch zu `/accounts` weitergeleitet |
| Tatsächliches Ergebnis | Benutzer wird automatisch zu `/accounts` weitergeleitet |
| Status | Pass |
| Kommentare | Manueller UI-Test; Weiterleitung ist in `budget_page.py` umgesetzt |

---

## Zuordnung zu automatisierten Tests

| Testdatei | Zweck |
| --- | --- |
| `tests/test_unit.py` | Finanzberechnungen, Budgetstatus und Wiederholungsdaten |
| `tests/test_integration.py` | App-Workflow mit SQLite-In-Memory-Datenbank, Budgets, Ausgaben, wiederkehrenden Transaktionen und Budget bearbeiten/löschen |
| `tests/test_db.py` | Seed-Daten, Persistenz, leere Datenbank und Monatsabfragen |
| `tests/test_validation.py` | Grundvalidierung für ungültigen Betrag und ungültigen Transaktionstyp |
| `tests/test_import.py` | CSV-Import für Konten, Kategorien, Budgets und Transaktionen |
| `tests/test_export.py` | CSV-Export, ZIP-Export und PDF-Export |

---

## Offene Testpunkte

- Automatisierte Browser-/UI-Tests für Filter, Dialoge, Darkmode und Hilfe-Dialog sind noch nicht umgesetzt.
- Filterung von Transaktionen nach Konto ist noch nicht umgesetzt und deshalb nicht als bestandener Testfall aufgeführt.
- Login oder mehrere echte Benutzer sind noch nicht umgesetzt; die App verwendet aktuell einen automatisch erstellten Default User.
