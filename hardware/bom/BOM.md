# Bill of Materials — GPIO Optocoupler Approach (18-Channel)

All parts available from Amazon, DigiKey, Mouser, or AliExpress.

| Qty | Part | Value / PN | Purpose | Approx. Cost |
|-----|------|-----------|---------|--------------|
| 1  | ESP-WROOM-32 dev board | 38-pin, HiLetgo or similar | Main controller | $5–8 |
| 18 | Optocoupler | PC817C DIP-4 | Button isolation (one per button) | $0.10–0.15 ea |
| 18 | Resistor | 470 Ω, 1/4 W through-hole | LED current limit (one per channel) | $0.01 ea |
| 1  | Perfboard / protoboard | 7×9 cm double-sided | Mounting all 18 channels | $1–2 |
| 1  | 5 V USB power supply | ≥ 500 mA, micro-USB | ESP32 power | $3–5 |
| 1  | Micro-USB cable | Any | Programming + power | (likely owned) |
| 1  | 28 AWG ribbon cable | 18-conductor, ~40 cm | GPIO header to optocouplers | $2–3 |
| 1  | 2.54 mm pin header strip | 40-pin | ESP32 socketing | $0.50 |
| 1  | Heat-shrink assortment | 2 mm + 4 mm | Insulating solder joints | $2 |
| 1  | Fine-tip solder | 0.5 mm rosin-core | PCB pad soldering | $3–5 |

**Estimated total (Approach 2 — all 18 channels):** ~$20–28 USD

---

## Notes

- **PC817C vs PC817A**: The C variant has a higher Current Transfer Ratio (CTR ≥ 100%) vs the A variant (CTR ≥ 50%). Both work, but C gives more reliable transistor saturation at the ~4.5 mA LED current from a 3.3 V GPIO through 470 Ω.
- **Approach 1 (BLE proxy only)**: You need just the ESP32 dev board and a USB cable — total cost ~$6. No soldering required.
- **Split King beds**: If you have two separate bases, you'll need two ESP32 boards (one per side), each running its own ESPHome config. Use different `device_name` and static IP for each.
- **Optional enclosure**: A 3D-printed ABS project box keeps everything tidy. Search "ESP32 project box 3D print" on Printables.com or Thingiverse.

---

## Where to Buy (US)

| Supplier | Best for |
|----------|---------|
| Amazon | Fast delivery; search "PC817 optocoupler 20-pack" |
| AliExpress | Cheapest bulk pricing; allow 2–4 weeks shipping |
| DigiKey / Mouser | Guaranteed genuine parts, datasheets, fast ship |
| Adafruit | ESP32 dev boards with good documentation |
