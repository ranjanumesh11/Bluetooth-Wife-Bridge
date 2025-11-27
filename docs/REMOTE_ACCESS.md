# Remote Access Setup Guide

How to securely access your bed control system from anywhere in the world.

---

## Overview

You have three main options for remote access:

| Method | Difficulty | Cost | Security | Best For |
|--------|------------|------|----------|----------|
| **Nabu Casa Cloud** | ⭐ Easy | $6.50/month | ⭐⭐⭐⭐⭐ Excellent | Beginners, convenience |
| **Tailscale VPN** | ⭐⭐ Medium | Free | ⭐⭐⭐⭐⭐ Excellent | Tech-savvy, privacy-focused |
| **Cloudflare Tunnel** | ⭐⭐⭐ Hard | Free | ⭐⭐⭐⭐ Very Good | Advanced users |

**⚠️ Never expose port 8123 directly to the internet without a secure reverse proxy!**

---

## Option 1: Nabu Casa Cloud (Recommended)

### Why Choose Nabu Casa?

✅ **Easiest** - 5-minute setup, no technical knowledge  
✅ **Secure** - Automatic SSL/TLS encryption  
✅ **Supports Home Assistant** - Your subscription funds HA development  
✅ **No port forwarding** - Works behind any router/ISP  
✅ **Includes extras** - Google Assistant, Alexa integration  

### Setup Steps

1. **Subscribe**
   - Home Assistant → Settings → Home Assistant Cloud
   - Click "Start Free Trial" (1 month free)
   - Enter payment info ($6.50/month after trial)

2. **Configure**
   - Settings → Home Assistant Cloud → Enable
   - Wait 30 seconds for connection
   - Copy your remote URL: `https://abcdef12345.ui.nabu.casa`

3. **Test Access**
   - Disconnect from home WiFi (use cellular)
   - Open remote URL in browser
   - Log in with HA credentials
   - Test bed controls

4. **Mobile App Setup**
   - Install Home Assistant Companion app
   - Scan QR code (Settings → Cloud → Connect app)
   - Or manually enter remote URL
   - Enable notifications for bed alerts

### Secure Your Account

```yaml
# Enable two-factor authentication:
# Home Assistant → Profile → Enable Multi-Factor Auth
# Use authenticator app like Google Authenticator
```

**Security tips:**
- Use strong password (16+ characters)
- Enable 2FA/MFA
- Don't share login credentials
- Review Cloud logs monthly

---

## Option 2: Tailscale VPN (Free & Secure)

### Why Choose Tailscale?

✅ **Free** - Up to 100 devices  
✅ **Zero-config** - Mesh VPN, works everywhere  
✅ **Private** - Your traffic doesn't route through Tailscale  
✅ **Fast** - Direct peer-to-peer when possible  

### Setup Steps

1. **Create Tailscale Account**
   - Visit https://tailscale.com
   - Sign up (free personal account)
   - Download Tailscale app

2. **Install on Home Assistant**
   ```bash
   # Via Add-on (easiest):
   # Settings → Add-ons → Add-on Store → Tailscale
   # Click Install
   ```

   Configure the add-on:
   ```yaml
   # Add-on configuration
   tags:
     - tag:homeassistant
   ```

3. **Install on Your Phone**
   - Install Tailscale app ([iOS](https://apps.apple.com/app/tailscale/id1470499037) / [Android](https://play.google.com/store/apps/details?id=com.tailscale.ipn))
   - Log in with same account
   - Connect (toggle ON)

4. **Access Home Assistant**
   - Note Tailscale IP of HA (in Tailscale admin or app)
   - Example: `http://100.101.102.103:8123`
   - Bookmark this URL on phone
   - Works from anywhere when Tailscale connected

### Advanced: Tailscale Funnel (Public HTTPS)

```bash
# Make HA publicly accessible (optional):
tailscale funnel on 8123
# Get public URL like: https://homeassistant.tail-scale.ts.net
```

---

## Option 3: WireGuard VPN (DIY)

### Why Choose WireGuard?

✅ **Open source** - Audited, trusted  
✅ **Fast** - Modern, efficient protocol  
✅ **Self-hosted** - Complete control  

### Prerequisites

- Router with port forwarding
- Static IP or dynamic DNS
- Linux server (can run on HA host)

### Setup Steps

1. **Install WireGuard Server** (on Home Assistant host or separate machine)
   
   ```bash
   # On Ubuntu/Debian:
   sudo apt update
   sudo apt install wireguard

   # Generate server keys
   cd /etc/wireguard
   umask 077
   wg genkey | tee privatekey | wg pubkey > publickey
   ```

2. **Configure Server**
   
   ```bash
   # Create /etc/wireguard/wg0.conf:
   sudo nano /etc/wireguard/wg0.conf
   ```

   ```ini
   [Interface]
   PrivateKey = <SERVER_PRIVATE_KEY>
   Address = 10.0.0.1/24
   ListenPort = 51820
   SaveConfig = true

   # Enable forwarding
   PostUp = iptables -A FORWARD -i wg0 -j ACCEPT
   PostDown = iptables -D FORWARD -i wg0 -j ACCEPT
   ```

3. **Start WireGuard**
   ```bash
   sudo systemctl enable wg-quick@wg0
   sudo systemctl start wg-quick@wg0
   ```

4. **Configure Router**
   - Forward UDP port 51820 to WireGuard server IP
   - Set up dynamic DNS if you don't have static IP

5. **Configure Client** (your phone)
   
   ```bash
   # Generate client keys
   wg genkey | tee client_privatekey | wg pubkey > client_publickey
   ```

   Client config:
   ```ini
   [Interface]
   PrivateKey = <CLIENT_PRIVATE_KEY>
   Address = 10.0.0.2/24
   DNS = 1.1.1.1

   [Peer]
   PublicKey = <SERVER_PUBLIC_KEY>
   Endpoint = your-home-ip.dyndns.org:51820
   AllowedIPs = 192.168.1.0/24  # Your home network
   PersistentKeepalive = 25
   ```

6. **Add Client to Server**
   ```bash
   sudo wg set wg0 peer <CLIENT_PUBLIC_KEY> allowed-ips 10.0.0.2/32
   ```

7. **Install WireGuard app** on phone, import config, connect

---

## Option 4: Cloudflare Tunnel (Advanced)

### Why Choose Cloudflare?

✅ **Free** - No subscription  
✅ **DDoS protection** - Cloudflare network  
✅ **No port forwarding** - Outbound tunnel only  

### Setup Steps

1. **Install Cloudflared** on Home Assistant host
   
   ```bash
   # Via Add-on:
   # Settings → Add-ons → Repositories → Add
   # https://github.com/brenner-tobias/addon-cloudflared
   ```

2. **Authenticate**
   ```bash
   cloudflared tunnel login
   # Opens browser for Cloudflare authorization
   ```

3. **Create Tunnel**
   ```bash
   cloudflared tunnel create homeassistant
   # Note the tunnel ID
   ```

4. **Configure Tunnel**
   
   Create `~/.cloudflared/config.yml`:
   ```yaml
   tunnel: <TUNNEL_ID>
   credentials-file: /root/.cloudflared/<TUNNEL_ID>.json

   ingress:
     - hostname: homeassistant.yourdomain.com
       service: http://localhost:8123
     - service: http_status:404
   ```

5. **Add DNS Record**
   - Cloudflare dashboard → DNS
   - Add CNAME: `homeassistant` → `<TUNNEL_ID>.cfargotunnel.com`

6. **Start Tunnel**
   ```bash
   cloudflared tunnel run homeassistant
   ```

7. **Access** via `https://homeassistant.yourdomain.com`

---

## Security Best Practices (All Methods)

### 1. Strong Authentication

```yaml
# Home Assistant configuration.yaml
homeassistant:
  auth_providers:
    - type: homeassistant
    - type: trusted_networks
      trusted_networks:
        - 10.0.0.0/24  # Only your VPN network
      allow_bypass_login: false
```

### 2. Enable 2FA

- Home Assistant → Your Profile → Enable Multi-Factor Authentication
- Use TOTP app (Google Authenticator, Authy, etc.)
- Save backup codes in secure location

### 3. IP Ban Protection

```yaml
# configuration.yaml
http:
  ip_ban_enabled: true
  login_attempts_threshold: 3
```

### 4. Monitor Access

```yaml
# Log all logins
automation:
  - alias: "Alert on new login"
    trigger:
      platform: event
      event_type: homeassistant_start
    action:
      service: notify.mobile_app
      data:
        title: "Home Assistant Access"
        message: "Someone logged into HA"
```

### 5. Regular Updates

- Keep Home Assistant updated
- Update ESPHome firmware
- Check for security advisories monthly

---

## Mobile App Configuration

### iOS/Android Home Assistant Companion

1. **Install App**
   - [iOS App Store](https://apps.apple.com/app/home-assistant/id1099568401)
   - [Android Play Store](https://play.google.com/store/apps/details?id=io.homeassistant.companion.android)

2. **Add Server**
   - Nabu Casa: Scan QR code from Settings → Cloud
   - VPN: Enter `http://100.101.102.103:8123` (Tailscale IP)
   - Or local IP when home: `http://192.168.1.100:8123`

3. **Enable Notifications**
   - App → Settings → Companion App → Notifications
   - Allow permissions
   - Test with: `notify.mobile_app_your_phone` service

4. **Add Widgets** (optional)
   - iOS: Long-press home screen → Add Widget → Home Assistant
   - Android: Long-press home screen → Widgets → Home Assistant
   - Choose bed control buttons

---

## Testing Remote Access

### Checklist

- [ ] Disconnect from home WiFi (use cellular/mobile data)
- [ ] Open remote URL in browser
- [ ] Log in successfully
- [ ] Navigate to bed dashboard
- [ ] Press "Head Up" button (test for 1 second only)
- [ ] Verify bed responds
- [ ] Check emergency stop works
- [ ] Test mobile app access
- [ ] Verify notification delivery

### Troubleshooting Remote Access

**Can't connect from outside:**
- Check VPN/tunnel is running
- Verify firewall rules
- Confirm DNS resolves correctly
- Test from different network

**Slow response:**
- Use VPN for lower latency
- Check home internet upload speed
- Optimize HA (disable unnecessary integrations)

**Connection drops:**
- VPN: Enable keepalive
- Nabu Casa: Check subscription status
- Network: Verify stable home internet

---

## Cost Comparison

| Method | Setup Time | Monthly Cost | Yearly Cost |
|--------|------------|--------------|-------------|
| Nabu Casa | 5 min | $6.50 | $78 |
| Tailscale | 30 min | $0 | $0 |
| WireGuard | 2 hours | $0 | $0 |
| Cloudflare | 1 hour | $0 | $0 |

**Recommendation:**
- **Just want it to work:** Nabu Casa
- **Tech-savvy, want privacy:** Tailscale
- **Already have domain:** Cloudflare Tunnel
- **Maximum control:** WireGuard

---

## Support

Each method has its own support channels:

- **Nabu Casa:** support@nabucasa.com
- **Tailscale:** https://tailscale.com/contact/support
- **WireGuard:** https://lists.zx2c4.com/mailman/listinfo/wireguard
- **Cloudflare:** https://community.cloudflare.com

For Home Assistant questions: https://community.home-assistant.io

---

**Security Reminder:** Whatever method you choose, always use strong passwords and enable 2FA. Your bed controls could be a safety issue if accessed by unauthorized users.
