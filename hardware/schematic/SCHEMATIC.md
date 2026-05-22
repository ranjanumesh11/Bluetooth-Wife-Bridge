# Hardware Schematic — GPIO Optocoupler Bridge

## Overview

Each button on the Sven & Son remote PCB is a normally-open tactile switch that closes a circuit between two pads. The optocoupler (PC817) shunts those same two pads from the ESP32 GPIO pin without any electrical connection between the ESP32 and the remote's internal circuitry. This galvanic isolation protects the ESP32 from back-EMF and voltage differences.

---

## Per-Channel Circuit (repeat ×12)

```
ESP32 GPIO Pin
     │
     ▼
  [470Ω]         ← Current-limiting resistor (prevents LED overcurrent)
     │
     ▼
  ┌──────────┐
  │  PC817   │
  │  Pin 1 ──┼── Anode   (connected to resistor above)
  │  Pin 2 ──┼── Cathode (connected to ESP32 GND)
  │          │
  │  Pin 4 ──┼── Collector → Remote button pad A
  │  Pin 3 ──┼── Emitter  → Remote button pad B (common/GND side)
  └──────────┘
```

**When GPIO is HIGH (3.3 V):**
- Current flows: GPIO → 470Ω → PC817 LED → GND
- LED current ≈ (3.3 − 1.2) / 470 ≈ 4.5 mA (safe; PC817 rated 50 mA)
- Phototransistor saturates → pins 3-4 shorted → button "pressed"

**When GPIO is LOW (0 V):**
- No current → transistor off → button "released"

---

## Component Values

| Component | Value | Notes |
|---|---|---|
| R1–R12 | 470 Ω, 1/4 W | One per channel |
| U1–U12 | PC817A or PC817C | Any variant works; C has higher CTR |
| ESP32 | ESP-WROOM-32 38-pin | 3.3 V logic |
| Power | 5 V USB or regulated | ESP32 dev board via micro-USB |

---

## GPIO to Button Mapping

Defined in `esphome/gpio-relay/gpio_relay.yaml` substitutions block. Default mapping:

| GPIO | Button | Remote PCB Label |
|---|---|---|
| 4 | Head Up | HU |
| 5 | Head Down | HD |
| 18 | Foot Up | FU |
| 19 | Foot Down | FD |
| 21 | Lumbar Up | LU |
| 22 | Lumbar Down | LD |
| 23 | Preset: Flat | P1 |
| 25 | Preset: Zero-G | P2 |
| 26 | Preset: TV/Lounge | P3 |
| 27 | Massage Head | MH |
| 32 | Massage Foot | MF |
| 33 | Under-bed Light | UL |

> **Avoid using:** GPIO 0, 2, 12, 15 (strapping pins used at boot). GPIO 34–39 are input-only on ESP32 and cannot drive outputs.

---

## Remote PCB Disassembly Notes

1. Open the remote enclosure (typically 4 Phillips screws underneath the label).
2. Photograph the PCB front and back before desoldering anything.
3. Use a multimeter in continuity mode to identify button pads: one probe on the common ground plane, the other on each button pad until it beeps when the button is held.
4. Solder short jumper wires (28 AWG ribbon cable works well) to each button pad pair. Leave the original button switches in place — the optocoupler shunts in parallel and the physical remote still works normally.
5. Route the ribbon cable through a small notch filed in the enclosure edge, or drill a 5 mm exit hole.

---

## Safety Checklist

- [ ] Confirm remote runs on ≤ 5 V (measure across battery terminals).
- [ ] Confirm no pad exceeds the PC817 collector-emitter voltage rating (80 V).
- [ ] Verify 470 Ω limits LED current below 20 mA (safe margin under 50 mA max).
- [ ] Never connect ESP32 GND to remote's positive supply rail.
- [ ] Use hot glue or heatshrink over all solder joints to prevent shorts.
- [ ] Power ESP32 from a separate 5 V USB supply, not from the remote's batteries.
