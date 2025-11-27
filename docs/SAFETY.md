# Safety Guidelines for Bed Control System

## ⚠️ Critical Safety Rules

### 1. Physical Remote is Primary
- **Always keep the physical remote accessible**
- The bed's original remote works independently of this system
- In any emergency, use the physical remote's stop button

### 2. Test Before Full Deployment
```
Testing Protocol:
1. Start with 1-second movements
2. Verify STOP command works instantly
3. Test each direction individually
4. Test all preset positions
5. Verify auto-stop timeout (30 sec)
6. Test with someone lying on bed
7. Test during WiFi/network outage
```

### 3. Never Override Built-in Safety Limits
- Don't modify bed's mechanical limit switches
- Don't extend movement durations beyond 30 seconds
- Don't bypass the bed's internal controller
- Don't use excessive force commands

---

## 🛡️ Built-in Safety Features

### Auto-Stop Timer
```yaml
# All movement commands include timeout
- platform: state
  entity_id:
    - switch.bed_head_up
    - switch.bed_head_down
    - switch.bed_foot_up
    - switch.bed_foot_down
  to: "on"
  for:
    seconds: 30
action:
  - service: switch.turn_on
    entity_id: switch.bed_emergency_stop
```

**What it does:**
- Monitors all movement switches
- If ON for more than 30 seconds, triggers emergency stop
- Prevents runaway movement if network fails

### Emergency Stop Command
- **Always available** in UI (top of dashboard)
- Sends universal stop byte sequence
- Resets all movement state variables
- Works even if other commands fail

### Hold-to-Move Pattern
```yaml
turn_on_action:
  - while:
      condition:
        lambda: 'return id(head_moving);'
      then:
        - ble_client.ble_write: [...]
        - delay: 300ms
turn_off_action:
  - globals.set:
      id: head_moving
      value: 'false'
  - switch.turn_on: bed_stop
```

**Why this is safe:**
- Requires continuous command stream (like holding a button)
- If WiFi drops, stream stops, motor stops
- Mimics physical remote behavior
- 300ms interval matches manufacturer spec

---

## 🚨 Emergency Procedures

### If Bed Won't Stop Moving

1. **Press physical remote STOP** (fastest)
2. Tap Emergency Stop in Home Assistant
3. Tap Emergency Stop on touchscreen display (if using ESP32-2432S028R)
4. Unplug bed controller power (last resort)

### If Commands Aren't Responding

1. Check BLE connection indicator
2. Move ESP32 closer to bed
3. Restart ESP32 controller
4. Use physical remote until connection restored

### If Bed Moves Unexpectedly

1. Press emergency stop immediately
2. Check Home Assistant automation logs
3. Disable bed automations temporarily
4. Review recent configuration changes

---

## 👥 User Safety Guidelines

### For People Using the Bed

**Before Movement:**
- Ensure no objects/pets in movement path
- Keep hands/arms clear of pinch points
- Ensure partner is aware of movement

**During Movement:**
- Stay alert and ready to stop
- Don't lean over bed edges during adjustment
- Watch for power cords getting caught

**For Children:**
- Keep controls password-protected
- Consider disabling voice commands
- Use physical remote lockout if available

### For Caregivers/Family

**Access Control:**
```yaml
# Require password for bed controls
homeassistant:
  auth_providers:
    - type: homeassistant
  customize:
    switch.bed_*:
      assumed_state: false
      require_confirm: true  # Optional: add confirmation dialogs
```

**Notifications:**
```yaml
automation:
  - alias: "Alert on bed movement"
    trigger:
      platform: state
      entity_id:
        - switch.bed_head_up
        - switch.bed_foot_up
    action:
      - service: notify.family_group
        data:
          message: "Bed is moving"
```

---

## 🔒 Security Best Practices

### 1. Secure Home Assistant Access

**Strong Authentication:**
- Use complex passwords (16+ characters)
- Enable two-factor authentication
- Create separate user accounts (don't share admin)

**Network Security:**
```yaml
# In configuration.yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 127.0.0.1
  ip_ban_enabled: true
  login_attempts_threshold: 3
```

### 2. Remote Access Security

**If using Nabu Casa:**
- ✅ Automatic SSL encryption
- ✅ No open ports on home network
- ✅ Regular security updates
- Still use strong HA password

**If self-hosting:**
```bash
# Use Cloudflare Tunnel or WireGuard VPN
# Never expose port 8123 directly to internet!

# Example WireGuard setup
apt install wireguard
wg genkey | tee privatekey | wg pubkey > publickey
# ... configure tunnel ...
```

### 3. ESP32 Security

**OTA Password Protection:**
```yaml
# In ESPHome config
ota:
  - platform: esphome
    password: !secret ota_password  # ALWAYS set this
```

**API Encryption:**
```yaml
api:
  encryption:
    key: !secret api_encryption_key  # Required for HA connection
```

**Disable Web Server in Production:**
```yaml
# Comment out after setup complete
# web_server:
#   port: 80
```

---

## ⚡ Electrical Safety

### Power Supply

**ESP32 Requirements:**
- 5V DC, 1A minimum (basic ESP32)
- 5V DC, 2A recommended (ESP32 with display)
- Use quality USB power adapter with overcurrent protection

**Bed Controller:**
- Don't modify bed's power supply
- Keep bed plugged into grounded outlet
- Consider UPS for ESP32 to prevent mid-movement power loss

### Installation

- ❌ Don't run wires where bed mechanism can pinch them
- ❌ Don't place ESP32 near bed motors (EMI interference)
- ✅ Use cable management/clips
- ✅ Keep connections dry (no liquids near electronics)

---

## 🏥 Medical Device Considerations

### If Bed is Medical Equipment

**Critical Warnings:**
- This project is **NOT medical-grade**
- Consult healthcare provider before modifications
- May void medical equipment warranty
- Insurance may not cover modified equipment

**Recommended:**
- Keep original remote as primary control
- Use this system only as convenience enhancement
- Document modifications for care team
- Test thoroughly with medical supervision

### For Users with Limited Mobility

**Accessibility Features:**
```yaml
# Large button dashboard (already included)
# Voice control setup
alexa:
  smart_home:
    filter:
      include_entities:
        - switch.bed_emergency_stop
        - button.bed_flat_position

# Automatic position alerts
automation:
  - alias: "Confirm bed position change"
    trigger:
      platform: state
      entity_id: button.bed_flat_position
    action:
      - service: tts.google_translate_say
        data:
          message: "Bed is moving to flat position"
```

---

## 📋 Pre-Deployment Checklist

### Hardware Installation
- [ ] ESP32 powered by wall adapter (not PC)
- [ ] ESP32 within 10 feet of bed controller
- [ ] Cables secured away from bed mechanisms
- [ ] Physical remote kept accessible
- [ ] No metal obstructions between ESP32 and bed

### Software Configuration
- [ ] Emergency stop tested and working
- [ ] Auto-stop timeout configured (30 sec)
- [ ] All command bytes verified with nRF Connect
- [ ] BLE connection stable for 24 hours
- [ ] Home Assistant authentication enabled
- [ ] OTA password set on ESP32
- [ ] API encryption enabled

### Functional Testing
- [ ] Each direction moves correctly
- [ ] Movements stop when released
- [ ] Emergency stop works instantly
- [ ] Preset positions accurate
- [ ] Auto-stop timeout triggers
- [ ] Works during WiFi reconnection
- [ ] Physical remote still functions

### User Training
- [ ] User knows location of physical remote
- [ ] User knows emergency stop locations
- [ ] User understands hold-to-move buttons
- [ ] User aware of 30-second timeout
- [ ] User has contact for technical support

---

## 🔍 Monitoring and Maintenance

### Regular Checks (Weekly)

```yaml
# Automation to remind you
automation:
  - alias: "Weekly bed system check reminder"
    trigger:
      platform: time
        at: "10:00:00"
    condition:
      - condition: time
        weekday: sun
    action:
      - service: notify.mobile_app
        data:
          title: "Bed System Maintenance"
          message: "Test emergency stop and check BLE connection"
```

**Test:**
1. Emergency stop response time
2. BLE connection stability
3. WiFi signal strength at ESP32
4. Battery level in physical remote
5. Bed mechanism sounds (listen for grinding)

### Log Analysis

Check Home Assistant logs for:
- Repeated connection failures
- Auto-stop timeout triggers (shouldn't happen often)
- Unusual command patterns
- Failed BLE writes

```bash
# View recent bed-related logs
grep -i "bed" /config/home-assistant.log | tail -50
```

---

## 📞 Support and Liability

### Getting Help

**Safe Resources:**
- GitHub Issues (this repo)
- Home Assistant Community Forums
- ESPHome Discord
- Manufacturer's support (for bed itself)

**Unsafe:**
- Random internet "hacks"
- Unauthenticated firmware
- Modifying bed's internal controller

### Liability Disclaimer

**YOU ACCEPT FULL RESPONSIBILITY FOR:**
- Property damage from malfunction
- Personal injury from misuse
- Warranty voidance on bed/controller
- Insurance implications

**THIS SYSTEM IS PROVIDED "AS-IS":**
- No guarantees of reliability
- Not certified for medical use
- Not tested by regulatory agencies
- Use at your own risk

**WHEN IN DOUBT:**
- Use the physical remote
- Consult the bed manufacturer
- Hire a professional integrator

---

## 🆘 Emergency Contact Template

Print and keep near bed:

```
═══════════════════════════════════════
    BED CONTROL SYSTEM - EMERGENCY
═══════════════════════════════════════

EMERGENCY STOP:
1. Press STOP on physical remote
2. Or tap RED emergency stop button
3. Or unplug bed controller

NORMAL ISSUES:
- WiFi down: Use physical remote
- Display frozen: Restart ESP32
- Bed not responding: Check BLE connection

TECHNICAL SUPPORT:
Name: _______________________________
Phone: ______________________________
Home Assistant URL: _________________

BED INFORMATION:
Brand: ______________________________
Model: ______________________________
Purchase Date: ______________________

ESP32 INFORMATION:
IP Address: _________________________
MAC Address: ________________________
Location: ___________________________

═══════════════════════════════════════
```

---

**Remember: The physical remote is your primary control. This system is a convenience enhancement, not a replacement.**
