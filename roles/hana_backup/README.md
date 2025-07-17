# HANA Backup Role

Diese Ansible-Rolle generiert und führt ALPACA Operator Commands basierend auf CSV-Daten und SLA-Levels aus.

## Beschreibung

Die `hana_backup` Rolle liest eine CSV-Datei mit Systemdaten und generiert automatisch ALPACA Operator Commands basierend auf den SLA-Levels:
- SLA1: 4 Commands
- SLA2: 3 Commands  
- SLA3: 2 Commands
- SLA4: 1 Command

## Voraussetzungen

- Python 3
- ALPACA Ansible Collection installiert
- CSV-Datei mit den erforderlichen Spalten

## CSV-Format

Die CSV-Datei muss folgende Spalten enthalten:
- `hdb_nw_sid`: Wird zu `systemName` gemappt
- `system_vdns`: Wird zu `agentName` gemappt  
- `system_sla`: Bestimmt die Anzahl der Commands (SLA1-SLA4)

## Verwendung

### Einfache Ausführung

```bash
ansible-playbook hana_backup.yml
```

### Mit benutzerdefinierten Variablen

```bash
ansible-playbook hana_backup.yml -e "csv_file=/path/to/your/csv output_dir=/path/to/output"
```

## Variablen

| Variable | Standard | Beschreibung |
|----------|----------|--------------|
| `csv_file` | `{{ playbook_dir }}/roles/hana_backup/files/swm_prod.csv` | Pfad zur CSV-Datei |
| `output_dir` | `{{ playbook_dir }}/generated_commands` | Ausgabeverzeichnis für generierte Playbooks |

## Ausgabe

Die Rolle erstellt:
1. Ein Python-Script zum Lesen der CSV-Datei
2. Individuelle Playbooks für jeden Command basierend auf SLA-Level
3. Ein konsolidiertes Playbook für alle Commands

## Struktur

```
roles/hana_backup/
├── defaults/main.yml          # Standardvariablen
├── files/swm_prod.csv         # Beispiel-CSV-Datei
├── tasks/
│   ├── main.yml              # Hauptaufgaben
│   ├── process_csv.yml       # CSV-Verarbeitung
│   ├── validate_csv.yml      # CSV-Validierung
│   └── create_commands.yml   # Command-Generierung
└── README.md                 # Diese Datei
```

## Beispiel-CSV

```csv
hdb_nw_sid,system_vdns,system_sla
HDB,server1.example.com,SLA1
HDB,server2.example.com,SLA2
HDB,server3.example.com,SLA3
HDB,server4.example.com,SLA4
```

## Troubleshooting

- **CSV nicht gefunden**: Überprüfen Sie den Pfad in der `csv_file` Variable
- **Template-Fehler**: Stellen Sie sicher, dass die CSV-Spalten korrekt benannt sind
- **Berechtigungsfehler**: Überprüfen Sie die Schreibrechte im `output_dir` 