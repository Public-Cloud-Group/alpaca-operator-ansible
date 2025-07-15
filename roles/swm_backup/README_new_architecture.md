# SWM Backup Role - Neue Architektur

## Übersicht

Die `swm_backup` Rolle wurde komplett neu gestaltet, um eine flexible und direkte Command-Generierung basierend auf CSV-Daten zu ermöglichen. Jede CSV-Zeile wird durch-iteriert und für jede SLA werden die entsprechenden Commands direkt erstellt.

## Neue Architektur

### Workflow
1. **CSV-Einlesen**: Die CSV-Datei wird gelesen und verarbeitet
2. **Zeile-für-Zeile-Verarbeitung**: Jede CSV-Zeile wird einzeln verarbeitet
3. **SLA-Template-Anwendung**: Für jede Zeile werden alle Command-Templates der entsprechenden SLA angewendet
4. **Direkte Command-Erstellung**: Jeder Command wird sofort erstellt und im System gespeichert
5. **Nächste Zeile**: Erst nach Abschluss aller Commands einer Zeile wird die nächste Zeile verarbeitet

### Hauptmerkmale

- **Direkte Command-Erstellung**: Commands werden sofort erstellt, nicht nur generiert
- **Flexible Template-Definition**: Vollständige ALPACA Command-Definitionen pro SLA
- **CSV-Variablen-Integration**: Direkte Verwendung von CSV-Werten in Command-Templates
- **Zeile-für-Zeile-Verarbeitung**: Kontrollierte Verarbeitung ohne Overhead
- **Fehlerbehandlung**: Optionale Fortsetzung bei Fehlern

## Konfiguration

### CSV-Spalten-Mapping

```yaml
csv_column_mapping:
  primary_system: 0      # Column index for primary_system
  hdb_nw_sid: 1          # Maps to systemName
  hdb_tenant: 2          # Column index for hdb_tenant
  system_type: 3         # Column index for system_type
  system_staging: 4      # Column index for system_staging
  system_sla: 5          # Determines which SLA templates to use
  system_vm_type: 6      # Column index for system_vm_type
  system_vm_flavor: 7    # Column index for system_vm_flavor
  system_vdns: 8         # Maps to agentName
  system_az: 9           # Column index for system_az
  # ... weitere Spalten
```

### SLA Command Templates

```yaml
sla_command_templates:
  "SLA1":
    - name: "Production Full Backup"
      system:
        systemName: "{{ csv_row.hdb_nw_sid }}"
      command:
        name: "Production Full Backup - {{ csv_row.hdb_nw_sid }}"
        state: present
        agentName: "{{ csv_row.system_vdns }}"
        processId: 801
        parameters: "-p prod -t {{ csv_row.system_type }} -s {{ csv_row.hdb_nw_sid }} -az {{ csv_row.system_az }} -backup full"
        # ... vollständige ALPACA Command-Konfiguration
```

## Verwendung

### Einfache Verwendung

```yaml
- name: SWM Backup mit Standard-Konfiguration
  include_role:
    name: swm_backup
```

### Erweiterte Verwendung mit Custom Templates

```yaml
- name: SWM Backup mit Custom Templates
  include_role:
    name: swm_backup
  vars:
    sla_command_templates:
      "SLA1":
        - name: "Custom Production Backup"
          system:
            systemName: "{{ csv_row.hdb_nw_sid }}"
          command:
            name: "Custom Production Backup - {{ csv_row.hdb_nw_sid }}"
            state: present
            agentName: "{{ csv_row.system_vdns }}"
            processId: 801
            parameters: "-p prod -t {{ csv_row.system_type }} -s {{ csv_row.hdb_nw_sid }} -az {{ csv_row.system_az }} -backup full"
            # ... weitere Konfiguration
```

## CSV-Variablen in Templates

Alle CSV-Spalten können in Command-Templates verwendet werden:

- `{{ csv_row.hdb_nw_sid }}` → System-Name
- `{{ csv_row.system_vdns }}` → Agent-Name
- `{{ csv_row.system_type }}` → System-Typ
- `{{ csv_row.system_az }}` → Availability Zone
- `{{ csv_row.hdb_tenant }}` → Tenant-Information
- `{{ csv_row.primary_system }}` → Primary System
- `{{ csv_row.system_staging }}` → Staging-Information
- `{{ csv_row.system_vm_type }}` → VM-Typ
- `{{ csv_row.system_vm_flavor }}` → VM-Flavor
- `{{ csv_row.hdb_data_min }}` → Data Minimum
- `{{ csv_row.hdb_data_max }}` → Data Maximum
- `{{ csv_row.hdb_log_min }}` → Log Minimum
- `{{ csv_row.hdb_log_max }}` → Log Maximum
- `{{ csv_row.hdb_shared_min }}` → Shared Minimum
- `{{ csv_row.hdb_shared_max }}` → Shared Maximum
- `{{ csv_row.Instance_no }}` → Instance Number

## Verarbeitungsoptionen

```yaml
processing_options:
  validate_data: true          # CSV-Daten validieren
  log_level: "info"            # Log-Level
  continue_on_error: false     # Bei Fehlern fortfahren
  verbose_output: true         # Detaillierte Ausgabe
```

## Beispiel-Workflow

### Für CSV-Zeile 1 (MHP, SLA1):
1. **Production Full Backup** wird erstellt
2. **Production Log Backup** wird erstellt
3. **Production Health Check** wird erstellt
4. **Production Performance Monitor** wird erstellt
5. **Nächste Zeile** wird verarbeitet

### Für CSV-Zeile 2 (MHP, SLA2):
1. **Staging Backup** wird erstellt
2. **Staging Health Check** wird erstellt
3. **Nächste Zeile** wird verarbeitet

## Vorteile der neuen Architektur

1. **Direkte Ausführung**: Commands werden sofort erstellt
2. **Kontrollierte Verarbeitung**: Zeile-für-Zeile ohne Overhead
3. **Flexible Templates**: Vollständige ALPACA Command-Definitionen
4. **CSV-Integration**: Direkte Verwendung aller CSV-Werte
5. **Fehlerbehandlung**: Optionale Fortsetzung bei Fehlern
6. **Skalierbarkeit**: Einfaches Hinzufügen neuer SLA-Templates
7. **Wartbarkeit**: Klare Trennung von Logik und Konfiguration

## Beispiel-Playbook

Siehe `example_playbook_new_architecture.yml` für ein vollständiges Beispiel.

## Migration von der alten Architektur

Die neue Architektur ist nicht rückwärtskompatibel, bietet aber:

1. **Bessere Performance**: Direkte Command-Erstellung
2. **Mehr Flexibilität**: Vollständige Template-Kontrolle
3. **Bessere Fehlerbehandlung**: Zeile-für-Zeile-Verarbeitung
4. **Einfachere Konfiguration**: Klare Template-Struktur

## Troubleshooting

### Problem: Commands werden nicht erstellt
- Überprüfen Sie die `sla_command_templates` Definition
- Stellen Sie sicher, dass die SLA-Werte in der CSV korrekt sind
- Überprüfen Sie die ALPACA API-Konfiguration

### Problem: CSV-Variablen werden nicht ersetzt
- Überprüfen Sie die `csv_column_mapping` Konfiguration
- Stellen Sie sicher, dass die CSV-Spalten korrekt gemappt sind
- Überprüfen Sie die Template-Syntax

### Problem: Fehler bei der Verarbeitung
- Aktivieren Sie `verbose_output: true` für detaillierte Ausgabe
- Überprüfen Sie `continue_on_error: true` für Fortsetzung bei Fehlern
- Überprüfen Sie die ALPACA API-Verbindung 