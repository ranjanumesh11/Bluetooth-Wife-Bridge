# End-to-End Setup Guide

## Overview

This guide has three phases:

| Phase | What Happens | Tool Used |
|-------|-------------|-----------|
| **Phase 1** | First-ever firmware flash to ESP32 via USB cable | Laptop + Edge browser + USB |
| **Phase 2** | Home Assistant adopts the ESP32 over WiFi | HA Green web UI |
| **Phase 3** | Upload the full bed-control config wirelessly | HA Green ESPHome add-on (OTA) |

After Phase 1, you never need a USB cable again. All future updates are wireless.

---

## Prerequisites Checklist

Before you start, make sure you have:

- [ ] HA Green powered on and Home Assistant accessible at `http://homeassistant.local:8123`
- [ ] ESP-WROOM-32D dev board (HiLetgo 38-pin)
- [ ] Micro-USB cable (data cable — not a charge-only cable)
- [ ] Microsoft Edge or Google Chrome on your laptop (Firefox/Safari will NOT work)
- [ ] Your home WiFi name (SSID) and password written down

---

## Phase 1 — First Flash (USB, one-time only)

### Step 1.1 — Install the USB driver (if needed)

The HiLetgo ESP-WROOM-32D uses the **CH340** USB-to-serial chip. Windows 10/11 usually installs this automatically, but if it doesn't:

1. Plug the ESP32 into your laptop via micro-USB
2. Open **Device Manager** (right-click Start → Device Manager)
3. Look under "Ports (COM & LPT)" — you should see something like **"USB-SERIAL CH340 (COM3)"**
4. If it shows up with a yellow warning ⚠️ or doesn't appear at all:
   - Download the driver: https://www.wch-ic.com/downloads/CH341SER_EXE.html
   - Install it, then unplug and replug the ESP32
5. Once you see the COM port listed normally (no warning icon), you're ready

### Step 1.2 — Create your secrets file

1. Go to the folder: `esphome/first-flash/` in this project
2. Copy `secrets.yaml.template` → rename the copy to `secrets.yaml`
3. Open `secrets.yaml` in Notepad and fill in:
   - Your home WiFi name and password
   - An API encryption key (instructions are in the file)
   - An OTA password (any string you choose)
4. Save the file. **Do not rename or move it** — it stays in `esphome/first-flash/`

> **Note:** `secrets.yaml` is in `.gitignore` — it will never be uploaded to GitHub.

### Step 1.3 — Flash via ESPHome Web

1. Open **Microsoft Edge** on your laptop
2. Go to: **https://web.esphome.io**
3. Make sure the ESP32 is plugged in via USB
4. Click the blue **"Connect"** button
5. A popup appears listing serial ports — select the one labeled **CH340** or **Silicon Labs CP210x**
   - If nothing appears: check Device Manager (Step 1.1)
6. Once connected, click **"Install"**
7. Choose **"Prepare for first use"** — this is the fastest option:
   - ESPHome Web installs a minimal firmware
   - After flashing, the ESP32 broadcasts a WiFi hotspot for you to enter your credentials (Step 1.4)

8. Wait for "Flashing complete" ✅ — takes about 2 minutes

### Step 1.4 — Configure WiFi via captive portal

After flashing, the ESP32 broadcasts its own temporary WiFi network:

1. On your phone or laptop, open WiFi settings
2. Connect to the network named **"sven-son-bed-bridge"** (or similar)
3. A browser page opens automatically — if it doesn't, open `http://192.168.4.1`
4. Enter your home WiFi name and password → **Save**
5. The ESP32 reboots and joins your home network

### Step 1.5 — Verify the ESP32 is online

1. In HA Green, go to **Settings → Devices & Services**
2. Within ~60 seconds you should see: **"New ESPHome device discovered"**
3. Click **"Configure"** → **Finish** (no encryption key needed at this stage)
4. The ESP32 now appears in HA as a device

> If it doesn't appear after 2 minutes: check your router's device list for "sven-son-bed-bridge". If it's there but not in HA, go to Settings → Devices & Services → ESPHome → three-dot menu → Reload.

---

## Phase 2 — Install ESPHome Add-on on HA Green

You need the ESPHome add-on to manage and update the ESP32 from HA Green.

1. In HA, go to **Settings → Add-ons → Add-on Store** (button bottom-right)
2. Search for **"ESPHome Device Builder"**
3. Click it → **Install** (takes a few minutes)
4. After install, enable:
   - ☑ **Start on boot**
   - ☑ **Watchdog**
5. Click **Start** → then **Open Web UI**
6. The ESP32 you flashed should appear in the ESPHome dashboard automatically

---

## Phase 3 — OTA Update with Full Bed Control Config

Now we replace the minimal firmware with the full bed-control firmware. No USB needed.

### Step 3.1 — Scan for your bed's MAC address

You need this before deploying the full config:

1. Download **nRF Connect** on your phone (free, by Nordic Semiconductor)
2. Open nRF Connect → **Scanner** tab → press **Scan**
3. Power-cycle the bed base (unplug and replug the power cable)
4. Look for a BLE device named **"HJC0"**, **"Richmat"**, or similar within 30 seconds
5. Tap on it — note the **MAC address** (format: `AA:BB:CC:DD:EE:FF`)
6. Tap **Connect** → look for a GATT service with UUID `FFE0`
7. Screenshot the service and characteristic UUIDs

Once you have the MAC address:

1. Open `esphome/ble-proxy/bluetooth_proxy.yaml` in this project
2. Replace `AA:BB:CC:DD:EE:FF` in the `bed_mac_address:` line with your real MAC
3. Update the secrets file (copy `esphome/ble-proxy/secrets.yaml.template` → `secrets.yaml`)

### Step 3.2 — Deploy full config wirelessly (OTA)

1. Open the **ESPHome add-on web UI** in HA Green
2. Find the **"Sven & Son Bed Bridge"** device → three-dot menu → **Edit**
3. Replace the entire YAML with the contents of `esphome/ble-proxy/bluetooth_proxy.yaml`
4. Click **Save** → **Install → Wirelessly**
5. ESPHome compiles and uploads OTA (2–3 minutes)
6. The ESP32 reboots with full bed control firmware

### Step 3.3 — Add the Home Assistant package

This creates all 18 bed control button entities in HA:

1. In HA, go to **Settings → System → Storage → "Open in File Editor"** (or use the Studio Code Server add-on)
2. Navigate to your HA `config/` folder
3. Create a `packages/` subfolder if it doesn't exist
4. Upload / create `adjustable_bed.yaml` with the contents from `home-assistant/packages/adjustable_bed.yaml`
5. Edit `configuration.yaml` and add:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
6. **Restart Home Assistant** — Settings → System → Restart
7. 18 new `input_button.bed_*` entities appear

### Step 3.4 — Add the Lovelace dashboard

1. In HA, go to **Settings → Dashboards → Add Dashboard**
   - Name: `Bed Remote`, Icon: `mdi:bed`, Mode: **YAML**
2. Click the three-dot menu on the new dashboard → **Edit**
3. Paste the full contents of `home-assistant/lovelace/bed_dashboard.yaml`
4. Save — your full remote-control UI is live

---

## Phase 4 — BLE Command Calibration (capture real button codes)

The `cmd_*` byte values in `bluetooth_proxy.yaml` are placeholders. Real values must be captured:

1. Connect to the bed in **nRF Connect** → find the `FFE1` characteristic
2. Press each button on the physical remote
3. Watch the value update in nRF Connect — record each button's hex bytes
4. Update the `cmd_*` substitutions in `bluetooth_proxy.yaml`
5. Re-deploy OTA (no USB needed)

See `docs/BLE_SCANNING.md` for the full process and the automated scanning script.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No COM port in Edge | Install CH340 driver (Step 1.1), unplug/replug ESP32 |
| "Access denied" on COM port | Close Arduino IDE, PlatformIO, or any terminal app that may have the port |
| ESP32 not discovered in HA | Check router — is "sven-son-bed-bridge" assigned an IP? Reload ESPHome integration |
| OTA update fails | Move ESP32 closer to router; check WiFi signal sensor in HA |
| Bed doesn't respond | MAC address or UUID may be wrong — rescan with nRF Connect |
| Physical remote still works | ✅ Expected — BLE approach doesn't modify the remote |

For more detail see `docs/TROUBLESHOOTING.md`.
