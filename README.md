# Bluetooth-WiFi Bridge for Adjustable Bed Control

Turn your Bluetooth-only adjustable bed (Sven & Son, Richmat, Leggett & Platt, etc.) into a fully internet-controllable smart device using an ESP32, ESPHome, and Home Assistant.

## 🎯 What This Does

- **Remote Control**: Control your bed from anywhere in the world (not just Bluetooth range)
- **Voice Control**: "Alexa/Google, set bed to Zero-G position"
- **Automations**: Schedule bed positions based on time, presence, or other triggers
- **Accessibility**: Large, easy-to-tap buttons for anyone with mobility challenges
- **Safety First**: Built-in auto-stop timers and emergency stop controls

## 📦 What You Need

### Hardware
- **HiLetgo ESP-WROOM-32 Development Board** (~$10) - The recommended standard ESP32 board
  - 38-pin DevKitC form factor
  - Built-in Bluetooth (BLE 4.2+) and WiFi
  - Micro-USB cable for programming and power
- **USB power adapter** (5V, 1A minimum) or use USB port on your PC/Raspberry Pi
- **Home Assistant host** - Raspberry Pi 4, Intel NUC, or existing server
- **Your existing adjustable bed** with Bluetooth remote

> ✅ **Why HiLetgo ESP-WROOM-32?** Proven compatibility, wide community support, excellent BLE range, and no display complexity!

### Accounts (Optional but Recommended)
- **Nabu Casa Cloud** ($6.50/month) for secure remote access without VPN setup

## 🚀 Quick Start (30-Minute Setup)

### Step 1: Install Home Assistant (15 min)
```bash
# On Raspberry Pi - flash Home Assistant OS image
# Download from: https://www.home-assistant.io/installation/

# Or run in Docker on existing Linux machine:
docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=America/New_York \
  -v /PATH_TO_YOUR_CONFIG:/config \
  -v /run/dbus:/run/dbus:ro \
  --network=host \
  ghcr.io/home-assistant/home-assistant:stable
```

Access Home Assistant at `http://homeassistant.local:8123`

### Step 2: Flash ESP32 as Bluetooth Proxy (10 min)

1. **Using Web Flasher** (Easiest):
   - Visit https://web.esphome.io in Chrome/Edge
   - Connect ESP32 via USB
   - Click "Connect" and select "Bluetooth Proxy"
   - Enter your WiFi credentials
   - Wait for flash to complete

2. **Using ESPHome Dashboard** (More control):
   - Install ESPHome in Home Assistant (Settings → Add-ons → ESPHome)
   - Copy `esphome/bed-ble-proxy.yaml` from this repo
   - Update WiFi credentials
   - Click "Install" and choose "Plug into this computer"

### Step 3: Discover Your Bed's BLE Profile (10 min)

1. Install **nRF Connect** app on your phone:
   - [Android](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp)
   - [iOS](https://apps.apple.com/app/nrf-connect/id1054362403)

2. Open app and scan for devices near your bed
3. Connect to your bed controller (look for names like "Richmat", "BED", or generic "BLE Device")
4. Explore Services → Find writable characteristics (usually `0xFFE0`/`0xFFE1`)
5. Press a button on your physical remote and watch for notifications
6. **Record these values**:
   ```
   MAC Address: AA:BB:CC:DD:EE:FF
   Service UUID: 0xFFE0
   Characteristic UUID: 0xFFE1
   ```

### Step 4: Configure Your Setup

1. Copy `esphome/bed-ble-client.yaml.example` to `bed-ble-client.yaml`
2. Update with your values:
   ```yaml
   ble_client:
     - mac_address: "AA:BB:CC:DD:EE:FF"  # Your bed's MAC
       id: bed_ble
   ```

3. Find your bed's command bytes in `docs/COMMON_BED_COMMANDS.md` or discover them with nRF Connect

4. Deploy to ESP32:
   ```bash
   # From ESPHome dashboard or command line:
   esphome run esphome/bed-ble-client.yaml
   ```

### Step 5: Add Home Assistant Dashboard

1. Go to Home Assistant → Settings → Dashboards → Add Dashboard
2. Copy contents from `homeassistant/bed-control-dashboard.yaml`
3. Paste into your new dashboard (Edit → Raw configuration editor)
4. Customize button labels and entities to match your setup

## 📁 Repository Structure

```
Bluetooth-Wife-Bridge/
├── esphome/
│   ├── bed-ble-proxy.yaml           # ⭐ START HERE - Simple Bluetooth proxy (Step 2)
│   ├── bed-ble-client.yaml.example  # Full BLE client with commands (Step 4)
│   └── secrets.yaml.example         # WiFi credentials template
├── homeassistant/
│   ├── bed-control-dashboard.yaml   # Lovelace UI with large buttons
│   ├── automations.yaml.example     # Sample automations (bedtime, wakeup)
│   └── scripts.yaml.example         # Reusable position presets
├── scripts/
│   ├── discover-ble.py              # Auto-discover bed BLE profile
│   ├── test-commands.py             # Test command bytes before deploying
│   └── flash-esp32.sh               # Automated ESP32 flashing helper
├── docs/
│   ├── COMMON_BED_COMMANDS.md       # Known command bytes for popular brands
│   ├── SAFETY.md                    # ⚠️ READ THIS - Safety checklist
│   ├── TROUBLESHOOTING.md           # Common issues and fixes
│   └── REMOTE_ACCESS.md             # Nabu Casa vs VPN setup
└── README.md                        # This file
```

> 🎯 **Your Setup Path**: Use `bed-ble-proxy.yaml` first, then `bed-ble-client.yaml.example` once you discover your bed's commands.

## 🔒 Safety Features

- **Auto-Stop Timers**: All movements stop after 30 seconds automatically
- **Emergency Stop Button**: Always visible at top of dashboard
- **Confirmation Dialogs**: Optional prompts before major movements
- **Network Fallback**: Physical remote always works independently
- **Authentication**: All remote access requires login credentials

See `docs/SAFETY.md` for complete safety guidelines.

## 🌐 Remote Access Options

### Option A: Nabu Casa (Recommended for Beginners)
- Home Assistant → Settings → Home Assistant Cloud
- Subscribe ($6.50/month)
- Automatic HTTPS, no port forwarding needed
- Access via `https://your-instance.ui.nabu.casa`

### Option B: Self-Hosted (Advanced)
- Set up WireGuard VPN or Tailscale
- Or use Nginx reverse proxy with Let's Encrypt SSL
- See `docs/REMOTE_ACCESS.md` for detailed guides

## 🎨 Dashboard Features

- **Large Touch-Friendly Buttons**: Head Up/Down, Foot Up/Down, Flat, Zero-G
- **Saved Positions**: Quick recall of favorite configurations
- **Bed Light Control**: Toggle under-bed lighting
- **Status Indicators**: Shows current position/movement state
- **Dark Mode Compatible**: Easy to use at night

## 🔧 Advanced Customization

### Add Voice Control
```yaml
# Example Alexa integration
alexa:
  smart_home:
    filter:
      include_entities:
        - switch.bed_head_up
        - switch.bed_flat_position
```

### Create Automations
```yaml
# Auto-flat at bedtime
automation:
  - alias: "Flatten bed at 10 PM"
    trigger:
      platform: time
      at: "22:00:00"
    action:
      service: switch.turn_on
      entity_id: switch.bed_flat_position
```

See `homeassistant/automations.yaml.example` for more ideas.

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| ESP32 won't connect to WiFi | Double-check SSID/password, ensure 2.4GHz network |
| Bed not discovered | Move ESP32 closer (within 3-6 feet of bed controller) |
| Commands don't work | Verify MAC address, UUIDs, and command bytes with nRF Connect |
| HA can't see ESP32 | Check `api:` encryption key matches in HA settings |
| Movements don't stop | Increase `duration` in command loops, verify stop byte sequence |

Full guide: `docs/TROUBLESHOOTING.md`

## 📚 Additional Resources

- [ESPHome Bluetooth Proxy Docs](https://esphome.io/components/bluetooth_proxy.html)
- [Home Assistant BLE Integration](https://www.home-assistant.io/integrations/bluetooth/)
- [SmartBed MQTT Add-on](https://github.com/richardhopton/smartbed-mqtt)
- [Community Bed Control Thread](https://community.home-assistant.io/t/adjustable-bed-ble-control/)
- [nRF Connect User Guide](https://docs.nordicsemi.com/bundle/nrf-connect-device-manager/)

## 🤝 Contributing

Found command bytes for a new bed model? Have a better dashboard layout? PRs welcome!

## ⚠️ Disclaimer

This project interfaces with your bed's controller. While we've implemented safety features:
- Always test with short durations first
- Keep your physical remote accessible
- Don't override built-in safety limits
- Use at your own risk

Your bed's warranty may not cover modifications. The physical remote will always work regardless of this system's state.

## 📝 License

MIT License - See LICENSE file

---

## ✅ What's Done (Repository Setup Complete)

All configuration files, scripts, and documentation are ready for you:
- ✅ ESPHome configs for HiLetgo ESP-WROOM-32
- ✅ Home Assistant dashboard with large accessibility buttons
- ✅ Safety features (auto-stop, emergency stop)
- ✅ BLE discovery and testing scripts
- ✅ Complete documentation (safety, troubleshooting, remote access)

---

## 📋 What's Pending on Your Side

### 1. **Order/Receive Your HiLetgo ESP-WROOM-32** 
   - [Amazon Link](https://www.amazon.com/s?k=HiLetgo+ESP-WROOM-32) (~$10)
   - Look for the 38-pin development board with Micro-USB
   - **ETA**: Depends on shipping (2-5 days)

### 2. **Set Up Home Assistant** (30 minutes)
   - **Option A**: Flash Raspberry Pi with Home Assistant OS
     - Download: https://www.home-assistant.io/installation/
   - **Option B**: Run Docker on existing PC/server
     ```bash
     docker run -d --name homeassistant --privileged --restart=unless-stopped \
       -e TZ=America/New_York -v ~/homeassistant:/config \
       --network=host ghcr.io/home-assistant/home-assistant:stable
     ```
   - Access at `http://homeassistant.local:8123`

### 3. **Discover Your Bed's Bluetooth Profile** (15 minutes)
   - Install **nRF Connect** app on your phone ([Android](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp) / [iOS](https://apps.apple.com/app/nrf-connect/id1054362403))
   - Scan for your bed controller (near the bed)
   - Record:
     - MAC Address (e.g., `AA:BB:CC:DD:EE:FF`)
     - Service UUID (usually `0xFFE0`)
     - Characteristic UUID (usually `0xFFE1`)
   - Press physical remote buttons and watch for notifications to find command bytes

### 4. **Flash ESP32 & Deploy Configs** (20 minutes)
   - When board arrives:
     1. Flash `esphome/bed-ble-proxy.yaml` using ESPHome web installer
     2. Update `bed-ble-client.yaml.example` with your bed's MAC/UUIDs/commands
     3. Deploy to ESP32
     4. Add Home Assistant dashboard from `homeassistant/bed-control-dashboard.yaml`

### 5. **Test & Enable Remote Access** (Optional, 10 minutes)
   - Test all buttons locally first
   - Sign up for Nabu Casa ($6.50/month) or set up VPN (see `docs/REMOTE_ACCESS.md`)

---

## 🚀 Quick Start When Your Board Arrives

1. **Plug in ESP32** via USB to your computer
2. **Visit** https://web.esphome.io in Chrome/Edge
3. **Flash** the `bed-ble-proxy.yaml` config (enter WiFi credentials)
4. **Open Home Assistant** → ESPHome add-on
5. **Adopt** the new device and update with your bed's BLE details
6. **Deploy dashboard** and start testing!

---

## 📞 Next Immediate Action

**Tell me when you have:**
1. ✅ Home Assistant installed/running? → I'll help you set up ESPHome add-on
2. ✅ Bed's BLE profile discovered? → I'll customize your config files
3. ✅ ESP32 board arrived? → I'll guide you through flashing step-by-step

**Have questions?** Check `docs/TROUBLESHOOTING.md` or reply here!
