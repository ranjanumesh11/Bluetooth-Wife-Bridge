# Bill of Materials — GPIO Optocoupler Approach

All parts available from Amazon, DigiKey, Mouser, or AliExpress.

| Qty | Part | Value / PN | Purpose | Approx. Cost |
|-----|------|-----------|---------|--------------|
| 1 | ESP-WROOM-32 dev board | 38-pin, any brand | Main controller | $5–8 |
| 12 | Optocoupler | PC817A or PC817C DIP-4 | Button isolation | $0.10–0.15 ea |
| 12 | Resistor | 470Ω 1/4W through-hole | LED current limit | $0.01 ea |
| 1 | Perfboard / protoboard | 5×7 cm double-sided | Mounting | $1–2 |
| 1 | 5V USB power supply | ≥ 500 mA | ESP32 power | $3–5 |
| 1 | Micro-USB cable | Any | Programming + power | Already owned |
| 1 | 28 AWG ribbon cable | 12-conductor, 30 cm | GPIO to optocouplers | $2–3 |
| 1 | 2.54 mm pin header strip | 40 pin | ESP32 socketing | $0.50 |
| 1 | Heat-shrink assortment | 2 mm + 4 mm | Insulation | $2 |

**Estimated total (Approach 2):** ~$20–25 USD

---

## Notes

- The PC817C variant has a higher Current Transfer Ratio (CTR ≥ 100%) compared to PC817A (CTR ≥ 50%), giving more reliable transistor saturation at low LED currents.
- If you're building the BLE proxy only (Approach 1), you need just the ESP32 dev board and a USB cable — total cost ~$6.
- Optional: a 3D-printed or small ABS project box to house the ESP32 and perfboard. Search "ESP32 project box 3D print" on Printables.com.
