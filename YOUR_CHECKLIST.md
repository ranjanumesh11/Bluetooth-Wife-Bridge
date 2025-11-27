# 🎯 Your Personal Setup Checklist

## Current Status: **Waiting for Hardware** 🛒

---

## ✅ COMPLETED (By Setup)
- [x] Repository structure created
- [x] ESPHome configs ready for HiLetgo ESP-WROOM-32
- [x] Home Assistant dashboard configured
- [x] Safety features built-in (auto-stop, emergency stop)
- [x] BLE discovery scripts prepared
- [x] Documentation complete

---

## 📋 YOUR ACTION ITEMS

### Priority 1: Hardware & Software Setup
- [ ] **Order HiLetgo ESP-WROOM-32** development board (~$10, 2-5 days shipping)
  - [Amazon Search](https://www.amazon.com/s?k=HiLetgo+ESP-WROOM-32)
  - Look for 38-pin DevKitC with Micro-USB
  
- [ ] **Install Home Assistant** (30 minutes)
  - Option A: Raspberry Pi with HA OS → [Download](https://www.home-assistant.io/installation/)
  - Option B: Docker on existing PC/server → See README Step 1
  - Access URL: `http://homeassistant.local:8123`
  - Mark complete when you can log in ✓

### Priority 2: Bed Discovery
- [ ] **Install nRF Connect app** on your phone (5 minutes)
  - [Android Link](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp)
  - [iOS Link](https://apps.apple.com/app/nrf-connect/id1054362403)

- [ ] **Discover your bed's Bluetooth profile** (15 minutes)
  - Open nRF Connect near your bed
  - Scan for devices (look for "Richmat", "BED", or generic names)
  - Connect and explore services
  - **Record these values:**
    - MAC Address: `___:___:___:___:___:___`
    - Service UUID: `0xFFE0` (or: `____________`)
    - Characteristic UUID: `0xFFE1` (or: `____________`)
  - Press remote buttons and watch for notifications
  - Note command bytes (e.g., Head Up = `0x01, 0x02`)

### Priority 3: ESP32 Setup (When Board Arrives)
- [ ] **Flash ESP32 with Bluetooth Proxy** (10 minutes)
  1. Plug ESP32 into computer via USB
  2. Visit https://web.esphome.io in Chrome/Edge
  3. Click "Connect" → Select "Bluetooth Proxy"
  4. Enter WiFi credentials (2.4GHz network only!)
  5. Wait for flash complete

- [ ] **Configure BLE Client** (10 minutes)
  1. Copy `esphome/secrets.yaml.example` → `secrets.yaml`
  2. Add your WiFi credentials
  3. Copy `esphome/bed-ble-client.yaml.example` → `bed-ble-client.yaml`
  4. Update with your bed's MAC address, UUIDs, and commands
  5. Deploy via ESPHome dashboard

### Priority 4: Home Assistant Integration
- [ ] **Install ESPHome add-on** in Home Assistant
  - Settings → Add-ons → ESPHome → Install

- [ ] **Adopt ESP32 device** in ESPHome dashboard
  - Should auto-discover after proxy flash

- [ ] **Deploy bed control dashboard**
  1. Home Assistant → Settings → Dashboards → Add Dashboard
  2. Copy contents from `homeassistant/bed-control-dashboard.yaml`
  3. Paste into raw config editor
  4. Customize entity names if needed

### Priority 5: Testing & Safety
- [ ] **Test each button locally** (30 minutes)
  - Start with short durations (2-3 seconds)
  - Verify all movements (Head Up/Down, Foot Up/Down, Flat, Zero-G)
  - Test Emergency Stop button
  - Verify auto-stop timer works (30 seconds max)

- [ ] **Read safety documentation**
  - Review `docs/SAFETY.md` thoroughly
  - Discuss with your wife how to use physical remote as backup
  - Test that physical remote still works independently

### Priority 6: Remote Access (Optional)
- [ ] **Enable remote access** (10 minutes + $6.50/month)
  - Option A: Nabu Casa (easiest) → HA Settings → Home Assistant Cloud
  - Option B: Self-hosted VPN → See `docs/REMOTE_ACCESS.md`

- [ ] **Test from outside home network**
  - Use phone on cellular data
  - Verify dashboard loads
  - Test one bed movement

---

## 🆘 If You Get Stuck

| Problem | Solution |
|---------|----------|
| ESP32 won't connect to WiFi | Check SSID/password, use 2.4GHz network only |
| Can't find bed in nRF Connect | Move closer (within 3-6 feet), ensure bed is powered |
| Commands don't work | Verify MAC/UUIDs, check `docs/COMMON_BED_COMMANDS.md` |
| HA can't see ESP32 | Check encryption key in ESPHome API settings |

**Full troubleshooting guide:** `docs/TROUBLESHOOTING.md`

---

## 📞 When to Report Back

**Tell me when you reach these milestones:**
1. ✅ Home Assistant is running
2. ✅ Bed's BLE profile discovered (MAC + UUIDs + command bytes)
3. ✅ ESP32 board arrived and flashed
4. ✅ First successful bed movement via dashboard!

---

## 🎉 Success Criteria

You'll know you're done when:
- ✅ Can control bed from Home Assistant dashboard
- ✅ All safety features working (auto-stop, emergency stop)
- ✅ Can access dashboard remotely (if desired)
- ✅ Wife is comfortable using both HA and physical remote
- ✅ Automations set up (optional: bedtime, wakeup routines)

---

**Estimated Total Time:** 2-3 hours (spread over 2-5 days waiting for hardware)

**Next Immediate Step:** Order ESP32 board + Install Home Assistant! 🚀
