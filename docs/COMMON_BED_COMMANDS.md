# Common Bed Controller Commands

This document contains known BLE command byte sequences for popular adjustable bed brands. **Always verify these commands work with YOUR specific bed model using nRF Connect before deploying!**

---

## 🔍 How to Use This Guide

1. Find your bed brand/controller below
2. Note the Service UUID and Characteristic UUID
3. Copy command bytes into your ESPHome configuration
4. **TEST with nRF Connect first** - don't trust blindly!
5. Adjust timing (300ms delay is typical) if needed

---

## Common Service/Characteristic UUIDs

Most adjustable beds use one of these patterns:

| Brand/Controller | Service UUID | Characteristic UUID | Notes |
|------------------|--------------|---------------------|-------|
| Richmat | `0xFFE0` | `0xFFE1` | Most common, many brands use this |
| Okin/DewertOkin | `0xFFE0` | `0xFFE1` | Same as Richmat protocol |
| Linak | `0x99FA0001-...` | `0x99FA0002-...` | Full 128-bit UUID |
| Leggett & Platt | `0xFFE0` | `0xFFE1` | Richmat OEM variant |
| Logicdata | `0xFFE0` | `0xFFE4` | Different characteristic |
| TiMOTION | Custom | Custom | Varies by model |

---

## Richmat Controllers

**Used by:** Sven & Son, Lucid, Zinus, many others

### Connection Details
```yaml
service_uuid: "0xFFE0"
characteristic_uuid: "0xFFE1"
```

### Commands (Hex Bytes)

#### Movement Commands (Hold-to-Move)
```yaml
head_up:        [0x40, 0x02, 0x70, 0x00, 0x01, 0x0B, 0x02, 0x40]
head_down:      [0x40, 0x02, 0x70, 0x00, 0x02, 0x0B, 0x02, 0x40]
foot_up:        [0x40, 0x02, 0x71, 0x00, 0x01, 0x0B, 0x02, 0x40]
foot_down:      [0x40, 0x02, 0x71, 0x00, 0x02, 0x0B, 0x02, 0x40]
stop:           [0x40, 0x02, 0x73, 0x00, 0x00, 0x0B, 0x40]
```

**Usage:** Send repeatedly every 300ms while button held, then send `stop` on release.

#### Preset Positions (Single Command)
```yaml
flat:           [0x40, 0x02, 0x72, 0x00, 0x01, 0x0B, 0x02, 0x40]
zero_gravity:   [0x40, 0x02, 0x72, 0x00, 0x04, 0x0B, 0x02, 0x40]
anti_snore:     [0x40, 0x02, 0x72, 0x00, 0x02, 0x0B, 0x02, 0x40]
lounge:         [0x40, 0x02, 0x72, 0x00, 0x03, 0x0B, 0x02, 0x40]
```

**Usage:** Send once, bed moves to position automatically.

#### Additional Features
```yaml
light_toggle:   [0x40, 0x02, 0x74, 0x00, 0x01, 0x0B, 0x02, 0x40]
massage_head:   [0x40, 0x02, 0x75, 0x00, 0x01, 0x0B, 0x02, 0x40]  # If equipped
massage_foot:   [0x40, 0x02, 0x76, 0x00, 0x01, 0x0B, 0x02, 0x40]  # If equipped
```

### Command Structure Breakdown
```
[0x40, 0x02, 0x70, 0x00, 0x01, 0x0B, 0x02, 0x40]
 │     │     │     │     │     │     │     │
 │     │     │     │     │     │     │     └─ End marker
 │     │     │     │     │     │     └─ Checksum?
 │     │     │     │     │     └─ Fixed value
 │     │     │     │     └─ Direction (0x01=up, 0x02=down)
 │     │     │     └─ Parameter
 │     │     └─ Function (0x70=head, 0x71=foot, 0x72=preset, etc.)
 │     └─ Command length?
 └─ Start marker
```

---

## Okin/DewertOkin Controllers

**Used by:** Tempur-Pedic, Ergomotion, Reverie

### Connection Details
```yaml
service_uuid: "0xFFE0"
characteristic_uuid: "0xFFE1"
```

### Commands
```yaml
# Very similar to Richmat, sometimes identical
head_up:        [0x40, 0x02, 0x70, 0x00, 0x01, 0x0B, 0x02, 0x40]
head_down:      [0x40, 0x02, 0x70, 0x00, 0x02, 0x0B, 0x02, 0x40]
foot_up:        [0x40, 0x02, 0x71, 0x00, 0x01, 0x0B, 0x02, 0x40]
foot_down:      [0x40, 0x02, 0x71, 0x00, 0x02, 0x0B, 0x02, 0x40]
stop:           [0x40, 0x02, 0x73, 0x00, 0x00, 0x0B, 0x40]

flat:           [0x40, 0x02, 0x72, 0x00, 0x01, 0x0B, 0x02, 0x40]
memory_1:       [0x40, 0x02, 0x72, 0x00, 0x05, 0x0B, 0x02, 0x40]
memory_2:       [0x40, 0x02, 0x72, 0x00, 0x06, 0x0B, 0x02, 0x40]
```

---

## Linak Controllers

**Used by:** IKEA, Herman Miller, some medical beds

### Connection Details
```yaml
service_uuid: "99FA0001-338A-1024-8A49-009C0215F78A"
characteristic_uuid: "99FA0002-338A-1024-8A49-009C0215F78A"
```

### Commands (Different Protocol!)
```yaml
# Linak uses different command structure
move_up:        [0x01, 0x01]  # Channel 1 up
move_down:      [0x01, 0x02]  # Channel 1 down
stop:           [0x01, 0x00]  # Channel 1 stop

# Multi-channel (for dual motors)
head_up:        [0x01, 0x01]  # Channel 1
foot_up:        [0x02, 0x01]  # Channel 2
both_up:        [0x03, 0x01]  # Both channels
```

**Note:** Simpler protocol, but channel mapping varies by bed model. Test carefully!

---

## Leggett & Platt (L&P) Controllers

**Used by:** Sealy, Beautyrest, Stearns & Foster

### Connection Details
```yaml
service_uuid: "0xFFE0"
characteristic_uuid: "0xFFE1"
```

### Commands
```yaml
# Similar to Richmat with minor variations
head_up:        [0x40, 0x02, 0x70, 0x00, 0x01, 0x0B, 0x02, 0x40]
head_down:      [0x40, 0x02, 0x70, 0x00, 0x02, 0x0B, 0x02, 0x40]
foot_up:        [0x40, 0x02, 0x71, 0x00, 0x01, 0x0B, 0x02, 0x40]
foot_down:      [0x40, 0x02, 0x71, 0x00, 0x02, 0x0B, 0x02, 0x40]
stop:           [0x40, 0x02, 0x73, 0x00, 0x00, 0x0B, 0x40]

# Preset buttons
preset_1:       [0x40, 0x02, 0x72, 0x00, 0x01, 0x0B, 0x02, 0x40]
preset_2:       [0x40, 0x02, 0x72, 0x00, 0x02, 0x0B, 0x02, 0x40]
preset_3:       [0x40, 0x02, 0x72, 0x00, 0x03, 0x0B, 0x02, 0x40]

# Some models have massage/vibration
massage_wave:   [0x40, 0x02, 0x75, 0x00, 0x01, 0x0B, 0x02, 0x40]
massage_pulse:  [0x40, 0x02, 0x75, 0x00, 0x02, 0x0B, 0x02, 0x40]
```

---

## Logicdata Controllers

**Used by:** Some European brands

### Connection Details
```yaml
service_uuid: "0xFFE0"
characteristic_uuid: "0xFFE4"  # Note: Different characteristic!
```

### Commands
```yaml
# Similar format to Richmat but different characteristic
head_up:        [0x40, 0x02, 0x70, 0x00, 0x01, 0x0B, 0x02, 0x40]
head_down:      [0x40, 0x02, 0x70, 0x00, 0x02, 0x0B, 0x02, 0x40]
# ... (rest similar to Richmat)
```

---

## Generic/Unknown Controllers

### Discovery Process

If your bed isn't listed, use nRF Connect to discover commands:

1. **Connect to bed in nRF Connect**
2. **Subscribe to notifications** on writable characteristics
3. **Press a button on physical remote**
4. **Note the hex bytes** sent (will show in notifications)
5. **Repeat for each button**
6. **Test by writing** same bytes back to characteristic

### Common Patterns

Most beds follow these patterns:

**Movement Commands:**
- Sent every 250-350ms while held
- Single byte or 8-byte sequences
- Often have start/end markers (0x40, 0xAA, 0xFF)

**Stop Commands:**
- Usually shortest sequence
- May be all zeros: `[0x00]`
- Or specific stop byte: `[0x73]`

**Preset Positions:**
- Single command (not repeated)
- Similar structure to movement but different function byte
- Bed handles the movement timing

---

## Command Timing Guidelines

### Hold-to-Move Behavior
```yaml
# Typical pattern in ESPHome
turn_on_action:
  - while:
      condition:
        lambda: 'return id(moving);'
      then:
        - ble_client.ble_write:
            id: bed_ble
            service_uuid: "FFE0"
            characteristic_uuid: "FFE1"
            value: [0x40, 0x02, 0x70, 0x00, 0x01, 0x0B, 0x02, 0x40]
        - delay: 300ms  # Adjust based on testing
```

**Delay timing:**
- **Too fast (< 200ms):** May overwhelm controller, cause errors
- **Too slow (> 500ms):** Jerky movement, motor start/stop
- **Recommended:** 250-350ms works for most beds

### Preset Positions
```yaml
# Send once, bed handles timing
on_press:
  - ble_client.ble_write:
      id: bed_ble
      service_uuid: "FFE0"
      characteristic_uuid: "FFE1"
      value: [0x40, 0x02, 0x72, 0x00, 0x01, 0x0B, 0x02, 0x40]
  # No loop needed, bed moves on its own
```

---

## Testing New Commands

### Safe Testing Protocol

```yaml
# Create test buttons in ESPHome
button:
  - platform: template
    name: "Test Command 1"
    on_press:
      - ble_client.ble_write:
          id: bed_ble
          service_uuid: "FFE0"
          characteristic_uuid: "FFE1"
          value: [0x40, 0x02, 0x70, 0x00, 0x01, 0x0B, 0x02, 0x40]
      - delay: 500ms  # Short duration for testing
      - ble_client.ble_write:  # Auto-stop after 500ms
          id: bed_ble
          service_uuid: "FFE0"
          characteristic_uuid: "FFE1"
          value: [0x40, 0x02, 0x73, 0x00, 0x00, 0x0B, 0x40]
```

**Test procedure:**
1. Start with 500ms duration
2. Have physical remote ready
3. Press test button
4. Verify correct direction/motor
5. Gradually increase duration
6. Log all working commands

---

## Contributing Your Commands

Found commands for a bed not listed? **Please contribute!**

### Submission Format

```markdown
## [Brand Name] [Model Number]

**Controller Type:** [Richmat/Okin/Linak/Other]
**Purchase Date:** [Approximate year]
**Retailer:** [Where purchased]

### Connection Details
Service UUID: 0xFFE0
Characteristic UUID: 0xFFE1

### Commands (Verified)
head_up:    [0x40, 0x02, 0x70, 0x00, 0x01, 0x0B, 0x02, 0x40]
head_down:  [0x40, 0x02, 0x70, 0x00, 0x02, 0x0B, 0x02, 0x40]
...

### Notes
- Command delay: 300ms works well
- Preset buttons work with single send
- Massage feature not tested
```

Submit via:
- GitHub PR to this repo
- GitHub Issue with "command-contribution" label
- Home Assistant Community Forums

---

## Troubleshooting Commands

### Command Not Working

**Check:**
1. ✅ Correct MAC address in config
2. ✅ Correct service/characteristic UUIDs
3. ✅ BLE connection established
4. ✅ Command bytes match exactly (no typos)
5. ✅ Using correct write type (write-without-response)

**Try:**
- Increase delay between commands
- Test with nRF Connect first
- Check ESPHome logs for BLE errors
- Move ESP32 closer to bed

### Wrong Motor Moving

**Issue:** Head command moves foot (or vice versa)

**Solutions:**
1. Swap head/foot command bytes
2. Check if bed wiring is reversed
3. Verify function byte in command
4. Test each motor independently

### Jerky Movement

**Issue:** Motor starts and stops repeatedly

**Solutions:**
- Decrease delay between commands (currently 300ms → try 250ms)
- Ensure while loop condition isn't flickering
- Check BLE signal strength
- Verify command format matches original remote

---

## Safety Reminder

**Before deploying any command:**
- ✅ Test with physical remote nearby
- ✅ Start with short durations (1-2 seconds)
- ✅ Verify stop command works
- ✅ Test each direction individually
- ✅ Have someone monitor the first full test

**Never:**
- ❌ Deploy untested commands
- ❌ Ignore unusual motor sounds
- ❌ Override built-in limits
- ❌ Use excessive command rates (< 100ms delay)

---

**Last Updated:** November 2025  
**Community Contributors:** [List maintained in GitHub]
