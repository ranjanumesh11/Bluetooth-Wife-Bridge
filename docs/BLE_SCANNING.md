# BLE Scanning Guide — Finding the Bed's MAC Address and UUIDs

The hardest part of Approach 1 is identifying the exact MAC address, service UUID, characteristic UUID, and command payloads the remote sends to the bed controller. This document walks you through three methods.

---

## Method 1 — nRF Connect (Easiest, Mobile)

**What you need:** An Android or iOS phone with Bluetooth.

1. Install **nRF Connect for Mobile** (Nordic Semiconductor — free on App Store / Play Store).
2. Power on the bed and make sure it's not already connected to anything.
3. Open nRF Connect → **Scanner** tab → Start scan.
4. Look for a device with a name like "Sven", "Adjustable", "BLE", or a generic "Unknown" device at strong RSSI (near -40 to -60 dBm when you're in the same room).
5. Tap the device → **Connect**.
6. Once connected, tap **Discover Services** (or it auto-discovers).
7. Note down:
   - The device MAC address shown at the top.
   - All **Service UUIDs** (128-bit custom UUIDs are the important ones — standard BLE services like `0x180A` are just device info).
   - Under the likely command service, find **Characteristics** — look for one with **WRITE** or **WRITE WITHOUT RESPONSE** properties.
8. With nRF Connect still connected, press a button on the physical remote. If the app shows a notification on a characteristic, that's your command channel. Note the UUID.

---

## Method 2 — scripts/ble_scanner.py (Desktop)

**What you need:** Python 3.8+ and Bluetooth on your computer (or a USB Bluetooth dongle).

```bash
pip install bleak
python scripts/ble_scanner.py
```

The script will:
1. Scan for 10 seconds and list all BLE devices with name, MAC, and RSSI.
2. When you type the MAC address, it connects and dumps all services and characteristics.
3. If you press `S` while connected, it subscribes to all notify/indicate characteristics and logs any incoming data — useful for beds that report position feedback.

---

## Method 3 — Wireshark + HCI Snoop Log (Most Detailed)

Use this method if the above don't reveal the write commands (some remotes connect to the bed before you can intercept).

### Android HCI Snoop Log

1. On your Android phone, enable **Developer Options** (tap Build Number 7×).
2. In Developer Options, enable **Enable Bluetooth HCI snoop log**.
3. Use the Sven & Son app or the physical remote to control the bed for 1–2 minutes.
4. Disable the snoop log and pull the log file:
   ```bash
   adb pull /sdcard/Android/data/btsnoop_hci.log
   ```
   (Path varies: `/data/misc/bluetooth/logs/btsnoop_hci.log` on some devices — check your Android version.)
5. Open the file in **Wireshark** (free).
6. Filter: `btatt` to show Bluetooth ATT traffic.
7. Look for **Write Request** or **Write Command** packets. The **Value** field contains the raw command bytes — this is what goes in your ESPHome `ble_client.ble_write` value arrays.

---

## Filling in the ESPHome Config

After scanning, update the substitutions in `bluetooth_proxy.yaml`:

```yaml
substitutions:
  bed_mac_address: "E4:AA:EC:XX:XX:XX"   # Your real MAC
  service_uuid: "0000ffe0-0000-1000-8000-00805f9b34fb"
  char_uuid_cmd: "0000ffe1-0000-1000-8000-00805f9b34fb"
  
  # Command bytes you captured from Wireshark/nRF Connect
  cmd_head_up:    "AA0101FF"
  cmd_head_down:  "AA0102FF"
  # ...
```

Convert the hex byte string to an ESPHome `value` array like this:

| Wireshark hex | ESPHome value array |
|---|---|
| `AA 01 01 FF` | `[0xAA, 0x01, 0x01, 0xFF]` |
| `F1 02 00 00 5A` | `[0xF1, 0x02, 0x00, 0x00, 0x5A]` |

---

## Sharing Your Findings

If you successfully decode the protocol, please open a GitHub issue with:
- Your bed model (check the label on the motor controller box under the bed)
- The service UUID and characteristic UUID
- The command byte sequences for each button

This will help other Sven & Son owners skip the scanning step entirely.
