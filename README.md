# Bluetooth-to-WiFi Bridge — Sven & Son Platinum Adjustable Bed

Control your **Sven & Son Platinum Series Adjustable Bed Base** over Wi-Fi using a **ESP-WROOM-32** dev board and [ESPHome](https://esphome.io/), fully integrated with [Home Assistant](https://www.home-assistant.io/).

---

## Why This Exists

The Sven & Son Platinum remote uses Bluetooth Low Energy (BLE) to communicate with the bed motor controller. This project creates a permanent Wi-Fi bridge so every button — Head Up/Down, Foot Up/Down, Lumbar, Massage, Under-bed Lighting, and Presets — appears as a native Home Assistant entity. Once bridged, you can automate the bed from Siri, Google Home, a dashboard, or any HA automation.

---

## Two Approaches

This repo documents two parallel strategies. **Start with Approach 1** (no soldering). Fall back to Approach 2 if the bed's BLE protocol can't be fully decoded.

| | Approach 1 — BLE Proxy (Software) | Approach 2 — GPIO Relay (Hardware) |
|---|---|---|
| **Hardware needed** | ESP-WROOM-32 only | ESP-WROOM-32 + PC817 optocouplers + resistors |
| **Soldering** | None | Yes — remote PCB |
| **Complexity** | Low–Medium | Medium–High |
| **Protocol risk** | Depends on BLE being decipherable | None — physically presses buttons |
| **Latency** | ~100–300 ms | ~50–100 ms |

---

## Repository Structure

```
Bluetooth-to-WiFi-Bridge/
├── esphome/
│   ├── ble-proxy/
│   │   └── bluetooth_proxy.yaml      # Approach 1 — BLE passive proxy + active control
│   └── gpio-relay/
│       └── gpio_relay.yaml           # Approach 2 — GPIO momentary switch via optocouplers
├── home-assistant/
│   ├── packages/
│   │   └── adjustable_bed.yaml       # All HA entities (covers, switches, numbers)
│   └── automations/
│       └── bed_automations.yaml      # Example automations (morning, bedtime, etc.)
├── hardware/
│   ├── schematic/
│   │   └── SCHEMATIC.md              # Optocoupler wiring diagram (text + ASCII art)
│   └── bom/
│       └── BOM.md                    # Bill of materials with part numbers
├── docs/
│   ├── SETUP.md                      # End-to-end installation guide
│   ├── BLE_SCANNING.md               # How to discover MAC address & UUIDs
│   └── TROUBLESHOOTING.md            # Common issues and fixes
└── scripts/
    └── ble_scanner.py                # Python helper to scan and log BLE advertisements
```

---

## Quick Start

### Prerequisites

- Home Assistant (any recent version, 2023.x+)
- ESPHome add-on installed in HA (or ESPHome CLI)
- ESP-WROOM-32 development board
- USB cable for initial flash

### Step 1 — Pick Your Approach

Read [`docs/BLE_SCANNING.md`](docs/BLE_SCANNING.md) to determine whether the bed's BLE protocol is accessible. If you can identify characteristic UUIDs, proceed with the BLE proxy. Otherwise, proceed to the hardware relay approach.

### Step 2 — Flash the ESP32

```bash
# Install ESPHome CLI (if not using HA add-on)
pip install esphome

# Approach 1 — BLE Proxy
esphome run esphome/ble-proxy/bluetooth_proxy.yaml

# Approach 2 — GPIO Relay
esphome run esphome/gpio-relay/gpio_relay.yaml
```

### Step 3 — Add Home Assistant Entities

Copy `home-assistant/packages/adjustable_bed.yaml` into your HA `packages/` folder and restart HA. See [`docs/SETUP.md`](docs/SETUP.md) for full details.

---

## Hardware Used

- **Bed:** Sven & Son Platinum Series Adjustable Base (Split King — 2× Twin XL bases, each with independent BLE controller)
- **BLE devices discovered:** `QRRM121500` (service FEE9 — Richmat proprietary) and `QRRM40218` (Nordic UART Service)
- **MCU:** HiLetgo ESP-WROOM-32 (38-pin dev board)
- **Approach 2 extras:** PC817 optocouplers (×8), 470Ω resistors (×8), 5V power supply, perfboard

> **Status (May 2026):** BLE device names confirmed via nRF Connect (`QRRM121500` + `QRRM40218`). MAC addresses to be captured via ESP32 BLE scan. GitHub push via Cowork — confirmed working ✓

---

## Contributing

Issues and PRs welcome. If you own a different Sven & Son model and find different UUIDs, please open an issue with your scan output so we can expand the compatibility table.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

*Last updated: May 2026*
