# End-to-End Setup Guide

## Prerequisites

- Home Assistant OS or Supervised (any recent version)
- ESPHome add-on installed from the HA Add-on Store
- ESP-WROOM-32 38-pin development board
- A computer with a USB port to flash the ESP32 initially

---

## Step 1 — Decide Your Approach

Run the BLE scanner first to determine if the bed's Bluetooth protocol can be decoded:

```bash
pip install bleak
python scripts/ble_scanner.py
```

Power cycle the bed and press a few buttons on the physical remote during the scan. If you see write events on a characteristic UUID, **Approach 1 (BLE Proxy)** is viable. If you only see advertisement packets with no useful GATT data, go to **Approach 2 (GPIO Relay)**.

---

## Step 2 — Install ESPHome Add-on

In Home Assistant:
1. **Settings → Add-ons → Add-on Store**
2. Search for **ESPHome** and install it
3. Enable "Start on boot" and "Watchdog"
4. Open the ESPHome web UI

---

## Step 3A — Approach 1: BLE Proxy

### 3A.1 — Create secrets.yaml

Copy `esphome/ble-proxy/secrets.yaml.template` to `esphome/ble-proxy/secrets.yaml` and fill in:
- Your Wi-Fi SSID and password
- Generate an API key: run `esphome generate-api-key` in terminal
- Set an OTA password

```yaml
# esphome/ble-proxy/secrets.yaml
wifi_ssid: "YourNetwork"
wifi_password: "YourPassword"
ap_fallback_password: "BedBridgeAP123"
api_encryption_key: "paste-generated-key-here"
ota_password: "choose-a-password"
```

### 3A.2 — Update MAC Address and UUIDs

Edit `esphome/ble-proxy/bluetooth_proxy.yaml` substitutions:
```yaml
bed_mac_address: "AA:BB:CC:DD:EE:FF"   # From BLE scan
service_uuid: "0000ffe0-..."            # From BLE scan
char_uuid_cmd: "0000ffe1-..."           # From BLE scan
```

Also update the command byte arrays `cmd_head_up`, etc., once you've sniffed the actual protocol (see `docs/BLE_SCANNING.md`).

### 3A.3 — Flash the ESP32

Connect the ESP32 via USB to the computer running ESPHome:

```bash
cd esphome/ble-proxy
esphome run bluetooth_proxy.yaml
```

Or paste the YAML into the ESPHome add-on UI and use the web-based OTA flash after the first USB flash.

### 3A.4 — Add to Home Assistant

After flashing, the ESP32 will appear in HA's **Settings → Devices & Services → ESPHome** within 60 seconds. Accept the discovered device and enter your API encryption key.

---

## Step 3B — Approach 2: GPIO Relay

### 3B.1 — Wire the Hardware

Follow `hardware/schematic/SCHEMATIC.md` to wire the optocouplers to the remote PCB and the ESP32 GPIO pins.

### 3B.2 — Create secrets.yaml

Same as 3A.1 but copy from `esphome/gpio-relay/` directory (or symlink the same file).

### 3B.3 — Verify GPIO Mapping

Open `esphome/gpio-relay/gpio_relay.yaml` and confirm the `pin_*` substitutions match your physical wiring.

### 3B.4 — Flash the ESP32

```bash
cd esphome/gpio-relay
esphome run gpio_relay.yaml
```

---

## Step 4 — Add Home Assistant Package

1. Enable packages support in your `configuration.yaml`:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
2. Create the `packages/` directory inside your HA config folder if it doesn't exist.
3. Copy `home-assistant/packages/adjustable_bed.yaml` to that folder.
4. Optionally copy `home-assistant/automations/bed_automations.yaml` and merge into your automations.
5. Restart Home Assistant.

---

## Step 5 — Build a Dashboard Card

In HA Lovelace, create a new card with the following button-card style (requires `custom:button-card` from HACS, or use plain Tile cards):

```yaml
type: grid
columns: 3
cards:
  - type: button
    name: Head Up
    tap_action:
      action: call-service
      service: switch.turn_on
      service_data:
        entity_id: switch.sven_son_bed_bridge_head_up
    icon: mdi:arrow-up-bold-box

  - type: button
    name: Head Down
    tap_action:
      action: call-service
      service: switch.turn_on
      service_data:
        entity_id: switch.sven_son_bed_bridge_head_down
    icon: mdi:arrow-down-bold-box

  # ... repeat for all buttons
```

---

## Step 6 — OTA Updates

After the initial USB flash, all future updates can be done over Wi-Fi:

```bash
esphome run bluetooth_proxy.yaml   # Detects ESP32 on network and uses OTA
```

The ESPHome add-on UI in HA also supports one-click OTA from the browser.
