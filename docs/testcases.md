# 🧪 Test Cases

Dieses Dokument enthält die Testfälle für den Budgetplanner, um sicherzustellen, dass alle Kernfunktionen korrekt funktionieren. Jeder Testfall beschreibt Voraussetzungen, Eingaben, Testschritte und erwartete Ergebnisse.

---

## Testfall TC_001

| **Feld**                   | **Details**                                                                                          |
| -------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Testfall-ID**            | TC_001                                                                                               |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer eine Einnahme erfassen kann                                            |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Einnahmeformular zugänglich                                                 |
| **Testschritte**           | Einnahmeformular öffnen → Betrag, Datum, Kategorie, Konto, Beschreibung eingeben → Speichern klicken |
| **Testdaten/Eingaben**     | Betrag: 1000, Datum: 2026-04-09, Kategorie: Gehalt, Konto: Girokonto, Beschreibung: April Gehalt     |
| **Erwartetes Ergebnis**    | Einnahme wird gespeichert; Kontostand aktualisiert                                                   |
| **Tatsächliches Ergebnis** | Einnahme erfolgreich gespeichert; Kontostand aktualisiert                                            |
| **Status**                 | Pass                                                                                                 |
| **Kommentare**             | Keine Probleme                                                                                       |

---

## Testfall TC_002

| **Feld**                   | **Details**                                                                                          |
| -------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Testfall-ID**            | TC_002                                                                                               |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer eine Ausgabe erfassen kann                                             |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Ausgabeforumular zugänglich                                                 |
| **Testschritte**           | Ausgabeforumular öffnen → Betrag, Datum, Kategorie, Konto, Beschreibung eingeben → Speichern klicken |
| **Testdaten/Eingaben**     | Betrag: 200, Datum: 2026-04-10, Kategorie: Miete, Konto: Girokonto, Beschreibung: April Miete        |
| **Erwartetes Ergebnis**    | Ausgabe wird gespeichert; Kontostand aktualisiert                                                    |
| **Tatsächliches Ergebnis** | Ausgabe erfolgreich gespeichert; Kontostand angepasst                                                |
| **Status**                 | Pass                                                                                                 |
| **Kommentare**             | Keine Probleme                                                                                       |

---

## Testfall TC_003

| **Feld**                   | **Details**                                                           |
| -------------------------- | --------------------------------------------------------------------- |
| **Testfall-ID**            | TC_003                                                                |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer eine neue Kategorie erstellen kann      |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Kategorieverwaltung zugänglich               |
| **Testschritte**           | Kategorieformular öffnen → Kategoriename eingeben → Speichern klicken |
| **Testdaten/Eingaben**     | Kategoriename: Nebenkosten                                            |
| **Erwartetes Ergebnis**    | Kategorie wird hinzugefügt und ist auswählbar                         |
| **Tatsächliches Ergebnis** | Kategorie „Nebenkosten“ erfolgreich hinzugefügt                       |
| **Status**                 | Pass                                                                  |
| **Kommentare**             | Keine Probleme                                                        |

---

## Testfall TC_004

| **Feld**                   | **Details**                                                          |
| -------------------------- | -------------------------------------------------------------------- |
| **Testfall-ID**            | TC_004                                                               |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer ein monatliches Budget festlegen kann  |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Budgetformular zugänglich                   |
| **Testschritte**           | Budgetformular öffnen → Monat und Limit eingeben → Speichern klicken |
| **Testdaten/Eingaben**     | Monat: April, Limit: 1500                                            |
| **Erwartetes Ergebnis**    | Budget wird gespeichert und angezeigt                                |
| **Tatsächliches Ergebnis** | Budget erfolgreich gespeichert und korrekt angezeigt                 |
| **Status**                 | Pass                                                                 |
| **Kommentare**             | Keine Probleme                                                       |

---

## Testfall TC_005

| **Feld**                   | **Details**                                                      |
| -------------------------- | ---------------------------------------------------------------- |
| **Testfall-ID**            | TC_005                                                           |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer das verbleibende Budget sehen kann |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Budget existiert                        |
| **Testschritte**           | Budgetübersicht öffnen                                           |
| **Testdaten/Eingaben**     | –                                                                |
| **Erwartetes Ergebnis**    | Verbleibendes Budget korrekt berechnet und angezeigt             |
| **Tatsächliches Ergebnis** | Verbleibendes Budget korrekt angezeigt                           |
| **Status**                 | Pass                                                             |
| **Kommentare**             | Keine Probleme                                                   |

---

## Testfall TC_006

| **Feld**                   | **Details**                                                      |
| -------------------------- | ---------------------------------------------------------------- |
| **Testfall-ID**            | TC_006                                                           |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer eine Kontenübersicht anzeigen kann |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Konten existieren                       |
| **Testschritte**           | Kontenübersicht öffnen                                           |
| **Testdaten/Eingaben**     | –                                                                |
| **Erwartetes Ergebnis**    | Alle Konten und deren aktuelle Salden werden angezeigt           |
| **Tatsächliches Ergebnis** | Übersicht korrekt angezeigt; Salden stimmen                      |
| **Status**                 | Pass                                                             |
| **Kommentare**             | Keine Probleme                                                   |

---

## Testfall TC_007

| **Feld**                   | **Details**                                                                                                                    |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Testfall-ID**            | TC_007                                                                                                                         |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer wiederkehrende Einnahmen erfassen kann                                                           |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Formular für wiederkehrende Einnahmen zugänglich                                                      |
| **Testschritte**           | Formular öffnen → Betrag, Datum, Kategorie, Konto, Beschreibung, Wiederholung eingeben → Speichern klicken                     |
| **Testdaten/Eingaben**     | Betrag: 500, Datum: 2026-04-01, Kategorie: Mieteinnahmen, Konto: Girokonto, Beschreibung: Monatsmiete, Wiederholung: monatlich |
| **Erwartetes Ergebnis**    | Einnahme wird gespeichert und für alle zukünftigen Monate geplant                                                              |
| **Tatsächliches Ergebnis** | Einnahme gespeichert; wiederkehrend korrekt geplant                                                                            |
| **Status**                 | Pass                                                                                                                           |
| **Kommentare**             | Keine Probleme                                                                                                                 |

---

## Testfall TC_008

| **Feld**                   | **Details**                                                                                                            |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Testfall-ID**            | TC_008                                                                                                                 |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer wiederkehrende Ausgaben erfassen kann                                                    |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Formular für wiederkehrende Ausgaben zugänglich                                               |
| **Testschritte**           | Formular öffnen → Betrag, Datum, Kategorie, Konto, Beschreibung, Wiederholung eingeben → Speichern klicken             |
| **Testdaten/Eingaben**     | Betrag: 100, Datum: 2026-04-05, Kategorie: Strom, Konto: Girokonto, Beschreibung: April Strom, Wiederholung: monatlich |
| **Erwartetes Ergebnis**    | Ausgabe wird gespeichert und für alle zukünftigen Monate geplant                                                       |
| **Tatsächliches Ergebnis** | Ausgabe gespeichert; wiederkehrend korrekt geplant                                                                     |
| **Status**                 | Pass                                                                                                                   |
| **Kommentare**             | Keine Probleme                                                                                                         |

---

## Testfall TC_009

| **Feld**                   | **Details**                                        |
| -------------------------- | -------------------------------------------------- |
| **Testfall-ID**            | TC_009                                             |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer Daten speichern kann |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Daten erfasst             |
| **Testschritte**           | Daten speichern klicken                            |
| **Testdaten/Eingaben**     | –                                                  |
| **Erwartetes Ergebnis**    | Alle Eingaben werden in der Datenbank gespeichert  |
| **Tatsächliches Ergebnis** | Daten erfolgreich gespeichert                      |
| **Status**                 | Pass                                               |
| **Kommentare**             | Keine Probleme                                     |

---

## Testfall TC_010

| **Feld**                   | **Details**                                                         |
| -------------------------- | ------------------------------------------------------------------- |
| **Testfall-ID**            | TC_010                                                              |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer bei Budgetüberschreitung gewarnt wird |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Budget existiert; Ausgaben > Budget        |
| **Testschritte**           | Überschreiten der Budgetgrenze durch Eingabe einer Ausgabe          |
| **Testdaten/Eingaben**     | Betrag: 2000, Datum: 2026-04-15, Kategorie: Auto, Konto: Girokonto  |
| **Erwartetes Ergebnis**    | Warnung wird angezeigt                                              |
| **Tatsächliches Ergebnis** | Warnung korrekt angezeigt                                           |
| **Status**                 | Pass                                                                |
| **Kommentare**             | Keine Probleme                                                      |

---

## Testfall TC_011

| **Feld**                   | **Details**                                                  |
| -------------------------- | ------------------------------------------------------------ |
| **Testfall-ID**            | TC_011                                                       |
| **Titel/Beschreibung**     | Überprüfen, dass die Gesamtausgaben korrekt angezeigt werden |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Ausgaben erfasst                    |
| **Testschritte**           | Finanzübersicht öffnen                                       |
| **Testdaten/Eingaben**     | –                                                            |
| **Erwartetes Ergebnis**    | Summe aller Ausgaben korrekt angezeigt                       |
| **Tatsächliches Ergebnis** | Summe korrekt angezeigt                                      |
| **Status**                 | Pass                                                         |
| **Kommentare**             | Keine Probleme                                               |

---

## Testfall TC_012

| **Feld**                   | **Details**                                                   |
| -------------------------- | ------------------------------------------------------------- |
| **Testfall-ID**            | TC_012                                                        |
| **Titel/Beschreibung**     | Überprüfen, dass die Gesamteinnahmen korrekt angezeigt werden |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Einnahmen erfasst                    |
| **Testschritte**           | Finanzübersicht öffnen                                        |
| **Testdaten/Eingaben**     | –                                                             |
| **Erwartetes Ergebnis**    | Summe aller Einnahmen korrekt angezeigt                       |
| **Tatsächliches Ergebnis** | Summe korrekt angezeigt                                       |
| **Status**                 | Pass                                                          |
| **Kommentare**             | Keine Probleme                                                |

---

## Testfall TC_013

| **Feld**                   | **Details**                                             |
| -------------------------- | ------------------------------------------------------- |
| **Testfall-ID**            | TC_013                                                  |
| **Titel/Beschreibung**     | Überprüfen, dass Kontostand korrekt berechnet wird      |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Einnahmen und Ausgaben erfasst |
| **Testschritte**           | Finanzübersicht öffnen                                  |
| **Testdaten/Eingaben**     | –                                                       |
| **Erwartetes Ergebnis**    | Kontostand = Einnahmen – Ausgaben                       |
| **Tatsächliches Ergebnis** | Kontostand korrekt berechnet                            |
| **Status**                 | Pass                                                    |
| **Kommentare**             | Keine Probleme                                          |

---

## Testfall TC_014

| **Feld**                   | **Details**                                                        |
| -------------------------- | ------------------------------------------------------------------ |
| **Testfall-ID**            | TC_014                                                             |
| **Titel/Beschreibung**     | Überprüfen, dass ein Benutzer mehrere Konten verwalten kann        |
| **Voraussetzungen**        | Benutzer ist eingeloggt; mehrere Konten existieren                 |
| **Testschritte**           | Kontoübersicht öffnen → neues Konto hinzufügen → Kontostand prüfen |
| **Testdaten/Eingaben**     | Kontoname: Sparkonto, Startsaldo: 5000                             |
| **Erwartetes Ergebnis**    | Neues Konto wird hinzugefügt; Salden korrekt                       |
| **Tatsächliches Ergebnis** | Neues Konto erfolgreich hinzugefügt                                |
| **Status**                 | Pass                                                               |
| **Kommentare**             | Keine Probleme                                                     |

---

## Testfall TC_015

| **Feld**                   | **Details**                                            |
| -------------------------- | ------------------------------------------------------ |
| **Testfall-ID**            | TC_015                                                 |
| **Titel/Beschreibung**     | Überprüfen, dass Kategorienamen geändert werden können |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Kategorie existiert           |
| **Testschritte**           | Kategorie auswählen → Namen ändern → Speichern klicken |
| **Testdaten/Eingaben**     | Alt: Nebenkosten → Neu: Betriebskosten                 |
| **Erwartetes Ergebnis**    | Name wird aktualisiert                                 |
| **Tatsächliches Ergebnis** | Kategorie erfolgreich umbenannt                        |
| **Status**                 | Pass                                                   |
| **Kommentare**             | Keine Probleme                                         |

---

## Testfall TC_016

| **Feld**                   | **Details**                                        |
| -------------------------- | -------------------------------------------------- |
| **Testfall-ID**            | TC_016                                             |
| **Titel/Beschreibung**     | Überprüfen, dass Kategorien gelöscht werden können |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Kategorie existiert       |
| **Testschritte**           | Kategorie auswählen → Löschen klicken              |
| **Testdaten/Eingaben**     | Kategorie: Betriebskosten                          |
| **Erwartetes Ergebnis**    | Kategorie wird gelöscht                            |
| **Tatsächliches Ergebnis** | Kategorie erfolgreich gelöscht                     |
| **Status**                 | Pass                                               |
| **Kommentare**             | Keine Probleme                                     |

---

## Testfall TC_017

| **Feld**                   | **Details**                                                      |
| -------------------------- | ---------------------------------------------------------------- |
| **Testfall-ID**            | TC_017                                                           |
| **Titel/Beschreibung**     | Überprüfen, dass Ausgaben nach Kategorie gefiltert werden können |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Ausgaben erfasst                        |
| **Testschritte**           | Filter öffnen → Kategorie auswählen → Anzeigen klicken           |
| **Testdaten/Eingaben**     | Kategorie: Miete                                                 |
| **Erwartetes Ergebnis**    | Nur Ausgaben der Kategorie angezeigt                             |
| **Tatsächliches Ergebnis** | Filter korrekt angewendet                                        |
| **Status**                 | Pass                                                             |
| **Kommentare**             | Keine Probleme                                                   |

---

## Testfall TC_018

| **Feld**                   | **Details**                                                   |
| -------------------------- | ------------------------------------------------------------- |
| **Testfall-ID**            | TC_018                                                        |
| **Titel/Beschreibung**     | Überprüfen, dass Einnahmen nach Monat gefiltert werden können |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Einnahmen erfasst                    |
| **Testschritte**           | Filter öffnen → Monat auswählen → Anzeigen klicken            |
| **Testdaten/Eingaben**     | Monat: April                                                  |
| **Erwartetes Ergebnis**    | Nur Einnahmen des Monats angezeigt                            |
| **Tatsächliches Ergebnis** | Filter korrekt angewendet                                     |
| **Status**                 | Pass                                                          |
| **Kommentare**             | Keine Probleme                                                |

---

## Testfall TC_019

| **Feld**                   | **Details**                                             |
| -------------------------- | ------------------------------------------------------- |
| **Testfall-ID**            | TC_019                                                  |
| **Titel/Beschreibung**     | Überprüfen, dass das Löschen von Einnahmen funktioniert |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Einnahme existiert             |
| **Testschritte**           | Einnahme auswählen → Löschen klicken                    |
| **Testdaten/Eingaben**     | Betrag: 1000, Kategorie: Gehalt                         |
| **Erwartetes Ergebnis**    | Einnahme wird gelöscht; Kontostand aktualisiert         |
| **Tatsächliches Ergebnis** | Einnahme erfolgreich gelöscht; Kontostand aktualisiert  |
| **Status**                 | Pass                                                    |
| **Kommentare**             | Keine Probleme                                          |

---

## Testfall TC_020

| **Feld**                   | **Details**                                            |
| -------------------------- | ------------------------------------------------------ |
| **Testfall-ID**            | TC_020                                                 |
| **Titel/Beschreibung**     | Überprüfen, dass das Löschen von Ausgaben funktioniert |
| **Voraussetzungen**        | Benutzer ist eingeloggt; Ausgabe existiert             |
| **Testschritte**           | Ausgabe auswählen → Löschen klicken                    |
| **Testdaten/Eingaben**     | Betrag: 200, Kategorie: Miete                          |
| **Erwartetes Ergebnis**    | Ausgabe wird gelöscht; Kontostand aktualisiert         |
| **Tatsächliches Ergebnis** | Ausgabe erfolgreich gelöscht; Kontostand aktualisiert  |
| **Status**                 | Pass                                                   |
| **Kommentare**             | Keine Probleme                                         |

---