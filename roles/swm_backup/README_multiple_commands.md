# SWM Backup Role - Multiple Commands Feature

## Übersicht

Die erweiterte `swm_backup` Rolle ermöglicht es nun, mehrere ALPACA Commands pro CSV-Eintrag zu erstellen, basierend auf SLA-spezifischen Command-Templates. Dies eliminiert den Overhead an überschüssigem Code und ermöglicht eine flexible Konfiguration ohne Anpassung der Rolle selbst.

## Neue Funktionalität

### Command-Templates pro SLA

Jede SLA-Definition kann nun `command_templates` enthalten, die definieren, welche Commands für Systeme dieser SLA erstellt werden sollen.

### Beispiel: SLA1 mit 4 Commands

```yaml
sla_definitions:
  "SLA1":
    name: "Production"
    # ... andere SLA-Einstellungen ...
    command_templates:
      - name: "Production Full Backup"
        processId: 801
        parameters: "-p prod -t __SYSTEM_TYPE__ -s __HDB_NW_SID__ -az __SYSTEM_AZ__ -backup full"
        schedule:
          period: "hourly"
          time: "00:00:00"
        critical: true
        autoDeploy: true
      - name: "Production Log Backup"
        processId: 802
        parameters: "-p prod -t __SYSTEM_TYPE__ -s __HDB_NW_SID__ -az __SYSTEM_AZ__ -backup log"
        schedule:
          period: "every_5min"
          time: "00:00:00"
        critical: true
        autoDeploy: true
      - name: "Production Health Check"
        processId: 803
        parameters: "-p prod -t __SYSTEM_TYPE__ -s __HDB_NW_SID__ -az __SYSTEM_AZ__ -health"
        schedule:
          period: "every_5min"
          time: "00:00:00"
        critical: true
        autoDeploy: true
      - name: "Production Performance Monitor"
        processId: 804
        parameters: "-p prod -t __SYSTEM_TYPE__ -s __HDB_NW_SID__ -az __SYSTEM_AZ__ -perf"
        schedule:
          period: "every_5min"
          time: "00:00:00"
        critical: false
        autoDeploy: true
```

## Verwendung

### 1. Standard-Verwendung (rückwärtskompatibel)

Die Rolle funktioniert weiterhin wie bisher, wenn keine `command_templates` definiert sind:

```yaml
- name: Standard SWM Backup
  include_role:
    name: swm_backup
```

### 2. Erweiterte Verwendung mit Command-Templates

```yaml
- name: SWM Backup with Multiple Commands
  include_role:
    name: swm_backup
  vars:
    sla_definitions:
      "SLA1":
        # ... SLA-Konfiguration ...
        command_templates:
          - name: "Production Full Backup"
            processId: 801
            parameters: "-p prod -t __SYSTEM_TYPE__ -s __HDB_NW_SID__ -az __SYSTEM_AZ__ -backup full"
            schedule:
              period: "hourly"
              time: "00:00:00"
            critical: true
            autoDeploy: true
          # ... weitere Templates ...
```

## Command-Template Struktur

Jedes Command-Template kann folgende Felder enthalten:

### Erforderliche Felder
- `name`: Name des Commands (wird mit System-Name kombiniert)

### Optionale Felder (verwenden Defaults aus SLA wenn nicht angegeben)
- `processId`: Process ID für den Command
- `parameters`: Command-Parameter mit Platzhaltern
- `schedule`: Scheduling-Konfiguration
- `critical`: Ob der Command kritisch ist
- `autoDeploy`: Ob Auto-Deploy aktiviert ist
- `disabled`: Ob der Command deaktiviert ist
- `parametersNeeded`: Ob Parameter benötigt werden
- `history`: History-Konfiguration
- `timeout`: Timeout-Konfiguration
- `escalation`: Escalation-Konfiguration

## Platzhalter in Parametern

Die folgenden Platzhalter werden in Command-Parametern ersetzt:
- `__SYSTEM_TYPE__`: System-Typ aus CSV
- `__HDB_NW_SID__`: HDB NW SID aus CSV
- `__SYSTEM_AZ__`: System Availability Zone aus CSV

## Beispiel-Playbook

Siehe `example_playbook_multiple_commands.yml` für ein vollständiges Beispiel.

## Vorteile

1. **Flexibilität**: Verschiedene Command-Sets pro SLA ohne Code-Änderungen
2. **Wartbarkeit**: Zentrale Konfiguration in YAML
3. **Skalierbarkeit**: Einfaches Hinzufügen neuer Command-Templates
4. **Rückwärtskompatibilität**: Bestehende Konfigurationen funktionieren weiterhin
5. **Übersichtlichkeit**: Klare Trennung zwischen SLA-Definitionen und Command-Templates

## Migration von bestehenden Konfigurationen

Bestehende Konfigurationen funktionieren ohne Änderungen. Um Command-Templates zu nutzen:

1. Fügen Sie `command_templates` zu den gewünschten SLA-Definitionen hinzu
2. Definieren Sie die gewünschten Commands als Templates
3. Die Rolle erstellt automatisch alle definierten Commands pro System

## Troubleshooting

### Problem: Commands werden nicht erstellt
- Überprüfen Sie, ob `command_templates` korrekt definiert sind
- Stellen Sie sicher, dass die SLA-Werte in der CSV mit den SLA-Definitionen übereinstimmen

### Problem: Falsche Parameter
- Überprüfen Sie die Platzhalter in den Command-Parametern
- Stellen Sie sicher, dass die CSV-Spalten korrekt gemappt sind

### Problem: Scheduling-Probleme
- Überprüfen Sie die Schedule-Konfiguration in den Command-Templates
- Stellen Sie sicher, dass gültige Perioden verwendet werden

### Gültige Perioden-Werte
Die folgenden Werte sind für das `period` Feld gültig:
- `every_5min`: Alle 5 Minuten
- `every_minute`: Jede Minute
- `hourly`: Stündlich
- `hourly_with_mn`: Stündlich mit Minuten
- `one_per_day`: Einmal pro Tag
- `manually`: Manuell
- `fixed_time`: Feste Zeit
- `fixed_time_once`: Feste Zeit einmalig
- `fixed_time_immediate`: Feste Zeit sofort
- `cron_expression`: Cron-Ausdruck
- `disabled`: Deaktiviert
- `even_hours`: Gerade Stunden
- `odd_hours`: Ungerade Stunden
- `even_hours_with_mn`: Gerade Stunden mit Minuten
- `odd_hours_with_mn`: Ungerade Stunden mit Minuten
- `start_fixed_time_and_hourly_mn`: Start fester Zeit und stündlich mit Minuten 