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

