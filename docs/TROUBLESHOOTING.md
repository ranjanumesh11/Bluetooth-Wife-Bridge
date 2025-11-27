# Troubleshooting Guide

Common issues and solutions for the Bluetooth-WiFi bed control system.

---

## 🔍 Quick Diagnosis

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| ESP32 won't connect to WiFi | Wrong SSID/password, 5GHz network | Check `secrets.yaml`, use 2.4GHz WiFi |
| Bed not discovered in HA | Out of BLE range | Move ESP32 closer (< 10 feet) |
| Commands do nothing | Wrong MAC/UUIDs | Verify with nRF Connect |
| Display blank (ESP32-2432S028R) | Insufficient power | Use 5V 2A wall charger, not PC |
| Movements won't stop | Network issue | Use physical remote, check auto-stop |
| HA can't see ESP32 | API key mismatch | Check encryption key in both configs |

---

## WiFi Connection Issues

### ESP32 Won't Connect to WiFi

**Symptoms:**
- Device not showing in Home Assistant
- Can't ping ESP32 IP address
- Logs show "WiFi connect failed"

**Solutions:**

1. **Verify WiFi credentials** - Check `esphome/secrets.yaml` for exact SSID/password
2. **Ensure 2.4GHz network** - ESP32 does NOT support 5GHz WiFi
3. **Check WiFi range** - Move closer to router during initial setup
4. **Escape special characters** in password if needed

---

## Bluetooth Connection Issues

### Bed Not Discovered

**Solutions:**

1. **Check BLE range** - ESP32 must be within 10-30 feet
2. **Verify MAC address** in both `ble_client` and `binary_sensor` sections
3. **Ensure bed is powered on** and Bluetooth active
4. **Check logs** for "Starting BLE tracker" message

### Commands Don't Work

**Solutions:**

1. **Test with nRF Connect first** - Verify command bytes manually
2. **Check service/characteristic UUIDs** match your bed
3. **Review ESPHome logs** for "BLE write failed" errors
4. **Try different write response** parameter

---

## Display Issues (ESP32-2432S028R)

### Display Stays Blank

**Solutions:**

1. **Use 5V 2A wall charger** - PC USB insufficient
2. **Verify Arduino framework** in config
3. **Check display pin connections** in YAML

### Touch Not Responding

**Solutions:**

1. **Calibrate touchscreen** - Adjust x_min/x_max/y_min/y_max values
2. **Test with logger** - Add touch coordinate logging
3. **Verify touch pins** GPIO33 (CS) and GPIO36 (IRQ)

---

## Network/Remote Access Issues

### Can't Access from Outside Home

**Using Nabu Casa:**
- Verify subscription active
- Check entities exposed in Cloud settings

**Using VPN:**
- Ensure VPN connected on phone
- Use local IP when on VPN

---

## Safety Issues

### ⚠️ Bed Won't Stop Moving

**EMERGENCY:**
1. Press physical remote STOP
2. Press emergency stop in HA
3. Unplug bed power

**Then check:**
- Auto-stop automation is enabled
- Stop command works in nRF Connect
- Review recent changes

---

## Getting Help

**Before posting:**
- Collect ESPHome logs
- Test with physical remote
- Try troubleshooting steps above

**Support resources:**
- GitHub Issues
- Home Assistant Community Forums
- ESPHome Discord

See full troubleshooting guide above for detailed solutions to each issue.
