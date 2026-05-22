# Troubleshooting Guide

## ESP32 Won't Flash / Compile

**Error: `Failed to connect to ESP32`**
- Hold the BOOT button on the ESP32 while clicking Flash. Some dev boards require this.
- Check the USB cable — use a data cable, not a charge-only cable.
- Try a different USB port or a powered USB hub.

**Error: `No module named 'esphome'`**
- Reinstall: `pip install esphome --upgrade`
- If using the HA add-on, check that the add-on version is up to date.

---

## ESP32 Won't Connect to Wi-Fi

- Verify SSID and password in `secrets.yaml` (no trailing spaces).
- ESP-WROOM-32 only supports 2.4 GHz — if your SSID is 5 GHz only, it won't connect.
- Check your router's client isolation setting — if enabled, the ESP32 can't talk to HA.
- The fallback AP (`${device_name}-AP`) will appear if Wi-Fi fails. Connect to it and visit `192.168.4.1` to reconfigure.

---

## ESP32 Connects to Wi-Fi but Doesn't Appear in HA

- Ensure HA and the ESP32 are on the same subnet.
- In HA, go to **Settings → Devices & Services** and manually add the ESPHome device by IP (e.g., `192.168.1.120`).
- Check that your HA firewall allows port 6053 (ESPHome native API).
- Make sure the `api.encryption.key` in the YAML matches what you enter in HA during onboarding.

---

## BLE Proxy Issues (Approach 1)

**"Connected to bed controller" never appears in logs**
- The MAC address in your YAML may be wrong. Re-run the BLE scanner.
- The bed controller may already be connected to your phone/app. Close the Sven & Son app and disconnect from the bed in your phone's Bluetooth settings.
- Some beds have a 30-second pairing window after power-on. Power cycle the bed motor controller (unplug from wall, wait 10 seconds, replug).

**Commands sent but bed doesn't move**
- The characteristic UUID or command bytes are wrong. Re-sniff with Wireshark HCI log.
- Try increasing the BLE write delay from `100ms` to `500ms` — some controllers are slow.
- Check if the characteristic requires **Write** (expects ACK) vs **Write Without Response**. If `ble_client.ble_write` errors appear in logs, try the `without_response: true` option.

**BLE proxy drops connection frequently**
- Reduce the distance between ESP32 and bed controller. BLE range is typically 5–10 m but walls reduce this significantly.
- Check Wi-Fi and BLE coexistence: ESP32 shares the 2.4 GHz antenna. Place the ESP32 closer to your Wi-Fi AP or use a dedicated 2.4 GHz channel that doesn't overlap with BLE (BLE uses channels 37, 38, 39 which map to Wi-Fi channels 1, 6, 11).
- Set `power_save_mode: none` in the Wi-Fi config (already done in the provided YAML).

---

## GPIO Relay Issues (Approach 2)

**Button press works from HA but bed doesn't respond**
- Probe the optocoupler output pins (3 and 4) with a multimeter in continuity mode while triggering the switch from HA. You should hear a beep during the press duration.
- If no continuity: check the resistor value (470Ω), verify LED polarity (anode = pin 1 to GPIO, cathode = pin 2 to GND).
- If continuity present but bed doesn't respond: you may be connected to the wrong button pads. Re-probe the remote PCB with continuity mode.

**Remote stops working after wiring**
- The optocoupler wires may be shorting other pads on the PCB. Inspect with a magnifying glass and re-insulate any exposed wire with heat shrink.
- Confirm the remote still works by holding the physical button manually.

**`restore_mode: ALWAYS_OFF` warning at boot**
- This is expected — the warning means the GPIO is being forced LOW at startup to prevent stuck relays. It's not an error.

---

## Home Assistant Entity Issues

**Entity IDs don't match**
- ESPHome generates entity IDs from `name + device_name`. If you changed `device_name` in the YAML, the entity IDs will change. Update `home-assistant/packages/adjustable_bed.yaml` script targets to match.
- Navigate to **Settings → Devices → [Your bridge device]** in HA to see the exact entity IDs assigned.

**Input buttons don't trigger the relay**
- Check that the automation `bed_input_button_*` is enabled (not disabled) in **Settings → Automations**.
- Verify the ESPHome switch entity ID in the script matches what HA assigned.

---

## Getting Help

1. Check the [ESPHome documentation](https://esphome.io) for platform-specific options.
2. Search or post in the [Home Assistant Community forums](https://community.home-assistant.io).
3. Open an issue on [GitHub](https://github.com/ranjanumesh11/Bluetooth-Wife-Bridge/issues) with your ESPHome logs (set `logger: level: DEBUG` and paste the output).
