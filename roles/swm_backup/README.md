# CSV Processor Role

Eine Ansible Role zur Verarbeitung von CSV-Dateien und Generierung von ALPACA Operator Commands basierend auf definierten SLA-Levels und Variable-Mappings.

## Features

- **CSV-Verarbeitung**: Automatische Verarbeitung von CSV-Dateien mit konfigurierbaren Spalten
- **SLA-Definitionen**: Drei vordefinierte SLA-Levels (SLA1-3) mit unterschiedlichen Retention-, Timeout- und Escalation-Einstellungen
- **Variable-Mapping**: Environment-spezifische Werte für Command-Parameter (z.B. `<BKP_LOG_SRC>`)
- **Schedule-Templates**: Vordefinierte Schedule-Templates (hourly, daily, every_5min, etc.)
- **Playbook-Generierung**: Automatische Generierung verschiedener Playbook-Typen
- **Validierung**: Umfassende Validierung von CSV-Daten und Konfigurationen

## SLA Definitionen

### SLA 1 - Basic SLA
- Retention: 7 Tage lokale Dateien, 30 Tage Blob-Logs
- Timeout: 300 Sekunden (Standard)
- Escalation: Email bei Fehlern, 2 Fehler bis Escalation
- Schedule: Stündlich, Montag-Freitag

### SLA 2 - Enhanced SLA
- Retention: 14 Tage lokale Dateien, 90 Tage Blob-Logs
- Timeout: 600 Sekunden (Custom)
- Escalation: Email + SMS, 1 Fehler bis Escalation
- Schedule: Alle 5 Minuten, 7 Tage/Woche

### SLA 3 - Premium SLA
- Retention: 30 Tage lokale Dateien, 365 Tage Blob-Logs
- Timeout: 1800 Sekunden (Custom)
- Escalation: Email + SMS, 1 Fehler bis Escalation
- Schedule: Jede Minute, 7 Tage/Woche

## Variable Mappings

Die Role unterstützt folgende Variable-Mappings:

- `<BKP_LOG_SRC>` - Backup Log Source
- `<BKP_LOG_DEST1>` - Primary Backup Destination
- `<BKP_LOG_DEST2>` - Secondary Backup Destination
- `<BKP_LOG_CLEANUP_INT>` - Cleanup Interval 1
- `<BKP_LOG_CLEANUP_INT2>` - Cleanup Interval 2
- `<DB_HOST>` - Database Host

Jede Variable kann environment-spezifische Werte haben (prod, test, dev).

## Schedule Templates

- `manual` - Manuelle Ausführung
- `hourly` - Stündlich
- `daily` - Täglich um 02:00
- `business_hours` - Stündlich, Montag-Freitag
- `weekend` - Täglich um 06:00, Wochenende
- `every_5min` - Alle 5 Minuten
- `every_minute` - Jede Minute

## Verwendung

### 1. Role einbinden

```yaml
- name: Process CSV and generate ALPACA Commands
  hosts: local
  gather_facts: false
  
  tasks:
    - name: Include CSV processor role
      include_role:
        name: csv_processor
```

### 2. Konfiguration anpassen

```yaml
vars:
  csv_processor:
    input_file: "swm_prod.csv"
    output_dir: "{{ playbook_dir }}/output"
  
  processing_options:
    create_commands: false  # Playbooks generieren
    environment: "prod"
```

### 3. CSV-Datei erstellen

```csv
SystemName,AgentName,CommandName,SLA,Parameters,Schedule,Enabled,Critical
"Production Server","backup_agent_01","BKP: DB log sync","2","-p GLTarch -s <BKP_LOG_SRC>","hourly","true","false"
```

## Generierte Dateien

Die Role generiert folgende Dateien im Output-Verzeichnis:

- **Individual Command Playbooks**: Ein Playbook pro Command
- **Consolidated Playbook**: Alle Commands in einem Playbook
- **SLA-specific Playbooks**: Separate Playbooks für jeden SLA-Level
- **System-specific Playbooks**: Separate Playbooks für jedes System
- **Inventory Template**: Ansible Inventory mit API-Konfiguration
- **Variables File**: Alle Konfigurationen und Mappings
- **README**: Dokumentation der generierten Dateien

## Beispiel

Siehe `example_playbook.yml` und `files/swm_prod.csv` für ein vollständiges Beispiel.

## Anforderungen

- Ansible 2.12+
- ALPACA Operator Collection (`pcg.alpaca_operator`)
- CSV-Datei mit erforderlichen Spalten

## Lizenz

GPL-3.0-or-later 