# 🧪 Test Cases

Dieses Dokument enthält die Testfälle für den Budgetplanner, um sicherzustellen, dass alle Kernfunktionen korrekt funktionieren. Jeder Testfall beschreibt Voraussetzungen, Eingaben, Testschritte und erwartete Ergebnisse.

---

## Testfall TC_001

| **Feld**                   | **Details**                                                                                              |
| :------------------------- | :------------------------------------------------------------------------------------------------------ |
| **Testfall-ID**            | TC_001                                                                                                  |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer eine Einnahme erfassen kann                                                |
| **Voraussetzungen**        | Benutzer ist angelegt; Einnahmeformular ist zugänglich                                                   |
| **Testschritte**           | Einnahmeformular öffnen -> Betrag, Datum, Kategorie, Konto, Beschreibung eingeben -> Speichern klicken  |
| **Testdaten/Eingaben**     | Betrag: 1000, Datum: 2026-04-09, Kategorie: Lohn, Konto: Bankkonto, Beschreibung: April Lohn            |
| **Erwartetes Ergebnis**    | Einnahme wird gespeichert; Finanzübersicht und Kontostand werden aktualisiert                            |
| **Tatsächliches Ergebnis** | Einnahme erfolgreich gespeichert; Finanzübersicht und Kontostand aktualisiert                            |
| **Status**                 | Pass                                                                                                    |
| **Kommentare**             | Keine Probleme                                                                                          |

---

## Testfall TC_002

| **Feld**                   | **Details**                                                                                              |
| :------------------------- | :------------------------------------------------------------------------------------------------------ |
| **Testfall-ID**            | TC_002                                                                                                  |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer eine Ausgabe erfassen kann                                                 |
| **Voraussetzungen**        | Benutzer ist angelegt; Ausgabeformular ist zugänglich                                                    |
| **Testschritte**           | Ausgabeformular öffnen -> Betrag, Datum, Kategorie, Konto, Beschreibung eingeben -> Speichern klicken   |
| **Testdaten/Eingaben**     | Betrag: 200, Datum: 2026-04-10, Kategorie: Miete, Konto: Bankkonto, Beschreibung: April Miete           |
| **Erwartetes Ergebnis**    | Ausgabe wird gespeichert; Finanzübersicht und Kontostand werden aktualisiert                             |
| **Tatsächliches Ergebnis** | Ausgabe erfolgreich gespeichert; Finanzübersicht und Kontostand aktualisiert                             |
| **Status**                 | Pass                                                                                                    |
| **Kommentare**             | Keine Probleme                                                                                          |

---

## Testfall TC_003

| **Feld**                   | **Details**                                                                       |
| :------------------------- | :------------------------------------------------------------------------------- |
| **Testfall-ID**            | TC_003                                                                           |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer eine neue Kategorie erstellen kann                  |
| **Voraussetzungen**        | Benutzer ist angelegt; Kategorieverwaltung ist zugänglich                         |
| **Testschritte**           | Kategorieformular öffnen -> Kategoriename und Typ eingeben -> Speichern klicken  |
| **Testdaten/Eingaben**     | Kategoriename: Nebenkosten, Typ: Ausgabe                                         |
| **Erwartetes Ergebnis**    | Kategorie wird hinzugefügt und ist bei Transaktionen auswählbar                  |
| **Tatsächliches Ergebnis** | Kategorie erfolgreich hinzugefügt                                                |
| **Status**                 | Pass                                                                             |
| **Kommentare**             | Keine Probleme                                                                   |

---

## Testfall TC_004

| **Feld**                   | **Details**                                                                                 |
| :------------------------- | :------------------------------------------------------------------------------------------ |
| **Testfall-ID**            | TC_004                                                                                      |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer ein monatliches Budget festlegen kann                         |
| **Voraussetzungen**        | Benutzer ist angelegt; Ausgabekategorie existiert; Budgetformular ist zugänglich            |
| **Testschritte**           | Budgetformular öffnen -> Monat, Jahr, Kategorie und Limit eingeben -> Speichern klicken     |
| **Testdaten/Eingaben**     | Monat: April, Jahr: 2026, Kategorie: Lebensmittel, Limit: 500                               |
| **Erwartetes Ergebnis**    | Budget wird gespeichert und korrekt angezeigt                                               |
| **Tatsächliches Ergebnis** | Budget erfolgreich gespeichert und korrekt angezeigt                                        |
| **Status**                 | Pass                                                                                        |
| **Kommentare**             | Keine Probleme                                                                              |

---

## Testfall TC_005

| **Feld**                   | **Details**                                                                       |
| :------------------------- | :------------------------------------------------------------------------------- |
| **Testfall-ID**            | TC_005                                                                           |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer das verbleibende Budget sehen kann                  |
| **Voraussetzungen**        | Benutzer ist angelegt; Budget und Ausgaben existieren                             |
| **Testschritte**           | Budgetübersicht oder Dashboard öffnen                                             |
| **Testdaten/Eingaben**     | Budget: 500, Ausgaben: 120                                                       |
| **Erwartetes Ergebnis**    | Budgetverbrauch und Restbudget werden korrekt berechnet und angezeigt             |
| **Tatsächliches Ergebnis** | Budgetverbrauch und Restbudget korrekt angezeigt                                  |
| **Status**                 | Pass                                                                             |
| **Kommentare**             | Keine Probleme                                                                   |

---

## Testfall TC_006

| **Feld**                   | **Details**                                             |
| :------------------------- | :------------------------------------------------------ |
| **Testfall-ID**            | TC_006                                                  |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer eine Kontenübersicht anzeigen kann |
| **Voraussetzungen**        | Benutzer ist angelegt; Konten existieren                |
| **Testschritte**           | Kontenübersicht öffnen                                  |
| **Testdaten/Eingaben**     | Konto: Bankkonto, Startsaldo: 1000                      |
| **Erwartetes Ergebnis**    | Alle Konten und deren aktuelle Salden werden angezeigt  |
| **Tatsächliches Ergebnis** | Übersicht korrekt angezeigt; Salden stimmen             |
| **Status**                 | Pass                                                    |
| **Kommentare**             | Keine Probleme                                          |

---

## Testfall TC_007

| **Feld**                   | **Details**                                                                           |
| :------------------------- | :------------------------------------------------------------------------------------ |
| **Testfall-ID**            | TC_007                                                                                |
| **Titel/Beschreibung**     | Überprüfen, dass Daten dauerhaft gespeichert werden                                   |
| **Voraussetzungen**        | Benutzer ist angelegt; Daten wurden erfasst                                           |
| **Testschritte**           | Einnahme, Ausgabe, Konto oder Kategorie erfassen -> App neu starten -> Daten anzeigen |
| **Testdaten/Eingaben**     | Beispieltransaktion oder Beispielkonto                                                |
| **Erwartetes Ergebnis**    | Erfasste Daten bleiben in der SQLite-Datenbank gespeichert                            |
| **Tatsächliches Ergebnis** | Daten erfolgreich gespeichert und wieder angezeigt                                    |
| **Status**                 | Pass                                                                                  |
| **Kommentare**             | Keine Probleme                                                                        |

---

## Testfall TC_008

| **Feld**                   | **Details**                                                                                 |
| :------------------------- | :------------------------------------------------------------------------------------------ |
| **Testfall-ID**            | TC_008                                                                                      |
| **Titel/Beschreibung**     | Überprüfen, dass eine Budgetüberschreitung angezeigt wird                                   |
| **Voraussetzungen**        | Benutzer ist angelegt; Budget existiert; Ausgaben liegen über dem Budget                    |
| **Testschritte**           | Ausgabe erfassen, die das Budget überschreitet -> Dashboard oder Budgetübersicht öffnen     |
| **Testdaten/Eingaben**     | Budget: 500, Ausgabe: 700, Kategorie: Lebensmittel                                          |
| **Erwartetes Ergebnis**    | Budgetüberschreitung wird sichtbar angezeigt                                                |
| **Tatsächliches Ergebnis** | Budgetüberschreitung korrekt angezeigt                                                      |
| **Status**                 | Pass                                                                                        |
| **Kommentare**             | Keine Probleme                                                                              |

---

## Testfall TC_009

| **Feld**                   | **Details**                                                       |
| :------------------------- | :---------------------------------------------------------------- |
| **Testfall-ID**            | TC_009                                                           |
| **Titel/Beschreibung**     | Überprüfen, dass die Gesamtausgaben korrekt angezeigt werden      |
| **Voraussetzungen**        | Benutzer ist angelegt; Ausgaben sind erfasst                      |
| **Testschritte**           | Finanzübersicht öffnen                                            |
| **Testdaten/Eingaben**     | Ausgaben: 800 und 120                                             |
| **Erwartetes Ergebnis**    | Summe aller Ausgaben wird korrekt angezeigt                       |
| **Tatsächliches Ergebnis** | Summe korrekt angezeigt                                           |
| **Status**                 | Pass                                                              |
| **Kommentare**             | Durch Unit Test abgedeckt                                         |

---

## Testfall TC_010

| **Feld**                   | **Details**                                                       |
| :------------------------- | :---------------------------------------------------------------- |
| **Testfall-ID**            | TC_010                                                           |
| **Titel/Beschreibung**     | Überprüfen, dass die Gesamteinnahmen korrekt angezeigt werden     |
| **Voraussetzungen**        | Benutzer ist angelegt; Einnahmen sind erfasst                     |
| **Testschritte**           | Finanzübersicht öffnen                                            |
| **Testdaten/Eingaben**     | Einnahme: 3000                                                    |
| **Erwartetes Ergebnis**    | Summe aller Einnahmen wird korrekt angezeigt                      |
| **Tatsächliches Ergebnis** | Summe korrekt angezeigt                                           |
| **Status**                 | Pass                                                              |
| **Kommentare**             | Durch Unit Test abgedeckt                                         |

---

## Testfall TC_011

| **Feld**                   | **Details**                                                                         |
| :------------------------- | :---------------------------------------------------------------------------------- |
| **Testfall-ID**            | TC_011                                                                              |
| **Titel/Beschreibung**     | Überprüfen, dass der Kontostand korrekt berechnet wird                              |
| **Voraussetzungen**        | Benutzer ist angelegt; Startsaldo, Einnahmen und Ausgaben existieren                |
| **Testschritte**           | Finanzübersicht oder Kontenübersicht öffnen                                         |
| **Testdaten/Eingaben**     | Startsaldo: 1000, Einnahmen: 3000, Ausgaben: 920                                    |
| **Erwartetes Ergebnis**    | Kontostand wird aus Startsaldo, Einnahmen und Ausgaben korrekt berechnet            |
| **Tatsächliches Ergebnis** | Kontostand korrekt berechnet                                                        |
| **Status**                 | Pass                                                                                |
| **Kommentare**             | Durch Unit Test abgedeckt                                                           |

---

## Testfall TC_012

| **Feld**                   | **Details**                                                                    |
| :------------------------- | :----------------------------------------------------------------------------- |
| **Testfall-ID**            | TC_012                                                                         |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer mehrere Konten verwalten kann                     |
| **Voraussetzungen**        | Benutzer ist angelegt; Kontenverwaltung ist zugänglich                          |
| **Testschritte**           | Kontenübersicht öffnen -> neues Konto hinzufügen -> Kontostand prüfen           |
| **Testdaten/Eingaben**     | Kontoname: Sparkonto, Kontotyp: Bankkonto, Startsaldo: 5000                    |
| **Erwartetes Ergebnis**    | Neues Konto wird hinzugefügt und angezeigt                                      |
| **Tatsächliches Ergebnis** | Neues Konto erfolgreich hinzugefügt                                             |
| **Status**                 | Pass                                                                           |
| **Kommentare**             | Keine Probleme                                                                 |

---

## Testfall TC_013

| **Feld**                   | **Details**                                                                 |
| :------------------------- | :-------------------------------------------------------------------------- |
| **Testfall-ID**            | TC_013                                                                      |
| **Titel/Beschreibung**     | Überprüfen, dass Kategorien bearbeitet werden können                         |
| **Voraussetzungen**        | Benutzer ist angelegt; Kategorie existiert                                   |
| **Testschritte**           | Kategorie auswählen -> Namen oder Typ ändern -> Speichern klicken            |
| **Testdaten/Eingaben**     | Alt: Nebenkosten -> Neu: Betriebskosten                                      |
| **Erwartetes Ergebnis**    | Kategorie wird aktualisiert                                                  |
| **Tatsächliches Ergebnis** | Kategorie erfolgreich aktualisiert                                           |
| **Status**                 | Pass                                                                         |
| **Kommentare**             | Keine Probleme                                                               |

---

## Testfall TC_014

| **Feld**                   | **Details**                                                                    |
| :------------------------- | :----------------------------------------------------------------------------- |
| **Testfall-ID**            | TC_014                                                                         |
| **Titel/Beschreibung**     | Überprüfen, dass Kategorien gelöscht werden können                              |
| **Voraussetzungen**        | Benutzer ist angelegt; Kategorie existiert und wird nicht verwendet             |
| **Testschritte**           | Kategorie auswählen -> Löschen klicken                                         |
| **Testdaten/Eingaben**     | Kategorie: Betriebskosten                                                      |
| **Erwartetes Ergebnis**    | Kategorie wird gelöscht                                                        |
| **Tatsächliches Ergebnis** | Kategorie erfolgreich gelöscht                                                 |
| **Status**                 | Pass                                                                           |
| **Kommentare**             | Verwendete Kategorien werden geschützt                                          |

---

## Testfall TC_015

| **Feld**                   | **Details**                                                                         |
| :------------------------- | :---------------------------------------------------------------------------------- |
| **Testfall-ID**            | TC_015                                                                              |
| **Titel/Beschreibung**     | Überprüfen, dass Transaktionen nach Kategorie gefiltert werden können               |
| **Voraussetzungen**        | Benutzer ist angelegt; Transaktionen sind erfasst                                   |
| **Testschritte**           | Transaktionsliste öffnen -> Kategorie auswählen                                     |
| **Testdaten/Eingaben**     | Kategorie: Miete                                                                    |
| **Erwartetes Ergebnis**    | Nur Transaktionen der ausgewählten Kategorie werden angezeigt                       |
| **Tatsächliches Ergebnis** | Filter korrekt angewendet                                                           |
| **Status**                 | Pass                                                                                |
| **Kommentare**             | Keine Probleme                                                                      |

---

## Testfall TC_016

| **Feld**                   | **Details**                                                                         |
| :------------------------- | :---------------------------------------------------------------------------------- |
| **Testfall-ID**            | TC_016                                                                              |
| **Titel/Beschreibung**     | Überprüfen, dass Transaktionen nach Monat gefiltert werden können                   |
| **Voraussetzungen**        | Benutzer ist angelegt; Transaktionen sind erfasst                                   |
| **Testschritte**           | Transaktionsliste öffnen -> Monat auswählen                                         |
| **Testdaten/Eingaben**     | Monat: April 2026                                                                   |
| **Erwartetes Ergebnis**    | Nur Transaktionen des ausgewählten Monats werden angezeigt                          |
| **Tatsächliches Ergebnis** | Filter korrekt angewendet                                                           |
| **Status**                 | Pass                                                                                |
| **Kommentare**             | Keine Probleme                                                                      |

---

## Testfall TC_017

| **Feld**                   | **Details**                                                                         |
| :------------------------- | :---------------------------------------------------------------------------------- |
| **Testfall-ID**            | TC_017                                                                              |
| **Titel/Beschreibung**     | Überprüfen, dass das Löschen von Einnahmen funktioniert                             |
| **Voraussetzungen**        | Benutzer ist angelegt; Einnahme existiert                                           |
| **Testschritte**           | Einnahme auswählen -> Löschen klicken                                               |
| **Testdaten/Eingaben**     | Betrag: 1000, Kategorie: Lohn                                                       |
| **Erwartetes Ergebnis**    | Einnahme wird gelöscht; Finanzübersicht und Kontostand werden aktualisiert          |
| **Tatsächliches Ergebnis** | Einnahme erfolgreich gelöscht; Übersicht aktualisiert                               |
| **Status**                 | Pass                                                                                |
| **Kommentare**             | Keine Probleme                                                                      |

---

## Testfall TC_018

| **Feld**                   | **Details**                                                                         |
| :------------------------- | :---------------------------------------------------------------------------------- |
| **Testfall-ID**            | TC_018                                                                              |
| **Titel/Beschreibung**     | Überprüfen, dass das Löschen von Ausgaben funktioniert                              |
| **Voraussetzungen**        | Benutzer ist angelegt; Ausgabe existiert                                            |
| **Testschritte**           | Ausgabe auswählen -> Löschen klicken                                                |
| **Testdaten/Eingaben**     | Betrag: 200, Kategorie: Miete                                                       |
| **Erwartetes Ergebnis**    | Ausgabe wird gelöscht; Finanzübersicht und Kontostand werden aktualisiert           |
| **Tatsächliches Ergebnis** | Ausgabe erfolgreich gelöscht; Übersicht aktualisiert                                |
| **Status**                 | Pass                                                                                |
| **Kommentare**             | Keine Probleme                                                                      |
