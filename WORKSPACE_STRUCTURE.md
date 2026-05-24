# Workspace Structure - Bluetooth to WiFi Bridge

## Project Overview
A Bluetooth to WiFi bridge project for controlling an adjustable bed through Home Assistant, utilizing ESPHome and BLE scanning.

## Directory Structure

```
Bluetooth to WiFi Bridge/
├── docs/                          # Documentation files
│   ├── BLE_SCANNING.md           # BLE scanning documentation
│   ├── SETUP.md                  # Setup guide
│   └── TROUBLESHOOTING.md        # Troubleshooting guide
│
├── esphome/                       # ESPHome configurations
│   ├── ble-proxy/                # Bluetooth proxy device config
│   │   ├── bluetooth_proxy.yaml  # Main proxy configuration
│   │   └── secrets.yaml.template # Secrets template
│   └── gpio-relay/               # GPIO relay device config
│       └── gpio_relay.yaml       # GPIO relay configuration
│
├── hardware/                      # Hardware documentation
│   ├── bom/                      # Bill of Materials
│   │   └── BOM.md                # Component list and specifications
│   └── schematic/                # Circuit diagrams
│       └── SCHEMATIC.md          # Schematic documentation
│
├── home-assistant/               # Home Assistant configurations
│   ├── automations/              # Automation rules
│   │   └── bed_automations.yaml  # Bed control automations
│   ├── lovelace/                 # UI dashboards
│   │   └── bed_dashboard.yaml    # Adjustable bed dashboard
│   └── packages/                 # Configuration packages
│       └── adjustable_bed.yaml   # Adjustable bed package config
│
├── scripts/                       # Python scripts
│   └── ble_scanner.py            # BLE device scanner script
│
├── .git/                         # Git repository
├── .gitignore                    # Git ignore rules
├── LICENSE                       # Project license
├── push_to_github.bat            # GitHub push script
└── README.md                     # Project README
```

## File Descriptions

### Documentation (`docs/`)
- **BLE_SCANNING.md** - Information about Bluetooth Low Energy scanning procedures
- **SETUP.md** - Installation and initial setup instructions
- **TROUBLESHOOTING.md** - Common issues and solutions

### ESPHome Configurations (`esphome/`)
- **ble-proxy/** - Configuration for a Bluetooth proxy device that bridges BLE to WiFi
- **gpio-relay/** - Configuration for GPIO relay control module

### Hardware (`hardware/`)
- **bom/BOM.md** - Component list with part numbers and specifications
- **schematic/SCHEMATIC.md** - Circuit schematic and connection diagrams

### Home Assistant (`home-assistant/`)
- **automations/** - Automation rules for bed control
- **lovelace/** - User interface dashboard configuration
- **packages/** - Reusable configuration package for the adjustable bed integration

### Scripts (`scripts/`)
- **ble_scanner.py** - Python utility for scanning and discovering BLE devices

### Root Files
- **README.md** - Main project documentation
- **LICENSE** - Project license file
- **push_to_github.bat** - Batch script for GitHub synchronization
- **.gitignore** - Git repository exclusion rules

## Project Architecture Summary

This project implements a Bluetooth to WiFi bridge solution with three main components:

1. **Hardware Layer** - Circuit design and component specifications
2. **ESPHome Layer** - Firmware configurations for BLE proxy and GPIO relay devices
3. **Home Assistant Layer** - Integration, automations, and UI for controlling an adjustable bed via BLE

The system allows wireless control of an adjustable bed through Home Assistant, with ESPHome handling the Bluetooth communication and GPIO relay control.
