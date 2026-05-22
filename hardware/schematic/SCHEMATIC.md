# Hardware Schematic — GPIO Optocoupler Bridge (18-Channel)

## Overview

Each of the **18 buttons** on the Richmat HJH89 remote PCB is a normally-open
tactile switch that closes a circuit between two pads. The PC817 optocoupler
shunts those same two pads from the ESP32 GPIO pin — **with full galvanic
isolation** between the ESP32 and the remote's internal circuitry. This means
no shared ground, no back-EMF risk, and the physical remote still works normally
in parallel (the optocoupler is wired in parallel with each button).

---

## Per-Channel Circuit (repeat × 18)

```
ESP32 GPIO Pin (3.3 V logic)
     │
     ▼
  [470 Ω]        ← Current-limiting resistor (1/4 W through-hole)
     │
     ▼
  ┌──────────────┐
  │   PC817      │
  │              │
  │  Anode  [1] ◄── from resistor
  │  Cathode[2] ──── ESP32 GND
  │
  │  Collector[4] ──── Remote button pad A
  │  Emitter  [3] ──── Remote button pad B (common/GND side)
  └──────────────┘
```

**When GPIO is HIGH (3.3 V):**
- Current path: GPIO → 470 Ω → PC817 LED → GND
- LED current ≈ (3.3 − 1.2) / 470 ≈ **4.5 mA** (well within 50 mA LED max)
- Internal phototransistor saturates → pins 3–4 shorted → button "pressed"

**When GPIO is LOW (0 V):**
- No LED current → transistor off → button "released"

---

## Component Values

| Component | Value / Part | Notes |
|-----------|-------------|-------|
| R1–R18 | 470 Ω, 1/4 W through-hole | One per channel |
| U1–U18 | PC817C DIP-4 | PC817C preferred (higher CTR ≥ 100%) |
| ESP32 | ESP-WROOM-32D, 38-pin dev board | 3.3 V logic |
| Power | 5 V USB supply ≥ 500 mA | Micro-USB to ESP32 dev board |

---

## GPIO → Button Mapping (all 18 channels)

| GPIO | ESPHome ID | Remote Button | Remote Label |
|------|-----------|---------------|-------------|
| 4  | relay_head_up        | Head Up             | HEAD ▲      |
| 5  | relay_head_down      | Head Down           | HEAD ▼      |
| 13 | relay_head_tilt_up   | Head Tilt Up        | HEAD TILT ▲ |
| 14 | relay_head_tilt_down | Head Tilt Down      | HEAD TILT ▼ |
| 16 | relay_foot_up        | Foot Up             | FOOT ▲      |
| 17 | relay_foot_down      | Foot Down           | FOOT ▼      |
| 18 | relay_lumbar_up      | Lumbar Up           | LUMBAR ▲    |
| 19 | relay_lumbar_down    | Lumbar Down         | LUMBAR ▼    |
| 21 | relay_preset_flat    | Preset: Flat        | FLAT        |
| 22 | relay_preset_zerog   | Preset: Zero-G      | ZG          |
| 23 | relay_anti_snore     | Preset: Anti-Snore  | ANTI-SNORE  |
| 25 | relay_memory         | Memory Position     | MEMORY      |
| 26 | relay_massage_onoff  | Massage ON/OFF      | ON/OFF ~~~  |
| 27 | relay_massage_mode   | Massage Mode        | MODE ~~~    |
| 32 | relay_massage_head   | Massage: Head zone  | HEAD )))    |
| 33 | relay_massage_foot   | Massage: Foot zone  | FOOT )))    |
| 2  | relay_lights         | Under-Bed Light     | ☀ (rays)   |
| 15 | relay_flashlight     | Flashlight          | 🔦 (torch) |

### GPIO Safety Notes
- **GPIO 2**: Strapping pin — pulled LOW at boot. Optocouplers are active-HIGH (off at boot), so this is safe ✅
- **GPIO 15**: Strapping pin — most dev boards have a built-in pull-down. Verify LOW at boot before wiring ✅
- **GPIO 12**: ❌ Avoid — affects flash voltage level at boot
- **GPIO 34–39**: ❌ Input-only on ESP32; cannot drive optocouplers
- **GPIO 6–11**: ❌ Internal flash bus; never connect here

---

## Remote PCB Disassembly Procedure

1. **Photograph** the remote PCB front and back before doing anything.
2. Open the enclosure — typically 3–4 Phillips screws under the label/rubber pad.
3. With a **multimeter in continuity mode**, identify each button's two pads:
   - One probe on the common ground plane of the remote.
   - Touch the other probe to each button pad until it beeps when the button is held.
4. **Solder 28 AWG ribbon cable** wires to each pad pair. Tin the pads first; use ~300 °C iron with short dwell time.
5. **Do not remove the original button switches** — the optocouplers wire in parallel. The physical remote continues to work normally.
6. Route the ribbon cable through a small notch or 4–5 mm hole in the enclosure side.
7. Heatshrink all solder joints before closing the enclosure.

---

## Perfboard Layout Suggestion

Use a 7×9 cm double-sided perfboard:
- Arrange 18 PC817 ICs in two rows of 9
- Run a shared GND rail along the bottom
- Run individual 470 Ω resistors in-line between the GPIO header strip and each PC817 anode
- Use a 20-pin IDC socket for the ESP32 GPIO connections

---

## Safety Checklist

- [ ] Remote battery voltage measured at ≤ 5 V (nominal 3 V from 2× AAA)
- [ ] No remote pad exceeds PC817 VCEO rating (80 V) — ✅ for battery-powered remote
- [ ] 470 Ω limits LED current below 20 mA at 3.3 V — ✅ (~4.5 mA)
- [ ] GPIO 2 and 15 verified LOW at boot with optocouplers connected
- [ ] All joints heatshrunk or hot-glued before final assembly
- [ ] ESP32 powered from separate 5 V USB — **not** from remote batteries
- [ ] Common GND between ESP32 and remote only through PC817 emitter — no direct wire
