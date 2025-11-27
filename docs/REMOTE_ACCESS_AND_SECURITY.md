# Remote Access & Security — Costs, Difficulty, Timeline

**Last updated:** November 27, 2025

This document summarizes remote access options for Home Assistant, the security actions you should take, estimated effort and costs, and copy-paste commands you can run.

## Short answer
- If you use the Home Assistant Companion app on the same local Wi‑Fi as your Home Assistant instance, you do NOT need remote access.
- If you want control from outside your home (cellular or another network), you need remote access: the easiest is **Nabu Casa** (~$6.50/month). Good self-hosted alternatives are **Tailscale** (easy, secure) or **WireGuard/VPN** and **Nginx + Let's Encrypt** (more work).

---

## One-line recommendations
- Quick & safe: Nabu Casa — 5–10 minutes setup, $6.50/month.
- Private & free for personal use: Tailscale — 10–30 minutes setup, minimal technical effort.
- Full control (advanced): Nginx + Let’s Encrypt — 30–90 minutes + domain + router config.

---

## Detailed breakdown (cost, difficulty, time, steps)

### 1) Long, unique passwords
- Cost: $0. Use a password manager (Bitwarden free).  
- Difficulty: trivial.  
- Time: 5–15 minutes.  
- Action: Create a 16+ character password for Home Assistant admin and router admin. Store it in the password manager.

### 2) Enable Two-Factor Authentication (2FA)
- Cost: $0.  
- Difficulty: trivial.  
- Time: 2–5 minutes.  
- How: Home Assistant UI → Profile (bottom left) → Enable Two-Factor Authentication → follow prompts with an Authenticator app.

### 3) HTTPS: Nabu Casa vs Let's Encrypt + Nginx
- Nabu Casa (Home Assistant Cloud)
  - Cost: ~$6.50/month.
  - Difficulty: trivial (UI driven).
  - Time: 5–10 minutes.
  - Pros: Managed certificates, no router changes, easy mobile login.
  - Cons: Ongoing subscription.
  - How to enable: Settings → Home Assistant Cloud → sign up and subscribe; install HA Companion and sign in.

- Let's Encrypt + Nginx
  - Cost: Domain (~$10/year optional). Let's Encrypt certs are free.
  - Difficulty: moderate.
  - Time: 30–90 minutes (depends on DNS/router).
  - Steps (high level): buy domain or use dynamic DNS, forward ports 80/443, install Nginx + Certbot, run Certbot to issue certs, configure reverse proxy to pass to `http://localhost:8123`.
  - Example commands (Debian/Ubuntu):

```bash
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx -y
sudo certbot --nginx -d home.example.com
```

### 4) Brute-force protection (fail2ban)
- Cost: $0.
- Difficulty: easy to moderate.
- Time: 15–45 minutes.
- How: install `fail2ban` and add a filter/jail for `nginx` or the Home Assistant logs. Start and enable service.

```bash
sudo apt update
sudo apt install fail2ban -y
sudo systemctl enable --now fail2ban
```

### 5) IP allowlists
- Cost: $0.
- Difficulty: moderate (depends on mobility).
- Time: 10–30 minutes.
- How: use `allow`/`deny` in Nginx, router firewall rules, or Tailscale ACLs. Tailscale avoids exposing ports and makes allowlisting trivial.

### 6) Keep Home Assistant & add-ons updated
- Cost: $0.
- Difficulty: trivial.
- Time: 5–30 minutes per update (create snapshot first).
- How: Supervisor → System → Create snapshot → Update Core / Supervisor / Add-ons.

### 7) Avoid exposing unnecessary services
- Cost: $0.
- Difficulty: trivial.
- Time: 10–20 minutes.
- How: review router port forwards and disable anything unnecessary. Prefer VPN/Tailscale to avoid port forwarding entirely.

### 8) Backups
- Cost: $0 (built-in snapshots); optional Google Drive add-on for remote storage may be used.
- Difficulty: trivial.
- Time: 10 minutes to enable and schedule.
- How: Supervisor → Backups → create snapshots and enable scheduled snapshots. Optionally install Google Drive Backup add-on.

### 9) Tailscale (recommended self-hosted alternative)
- Cost: Free for personal use.
- Difficulty: easy.
- Time: 10–30 minutes.
- Quick setup (Home Assistant host):

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# Visit the printed URL to authenticate device
```

Then install Tailscale app on your phone and sign in; access Home Assistant using its Tailscale IP.

### 10) WireGuard VPN (self-managed)
- Cost: $0 if hosted on your hardware.
- Difficulty: moderate.
- Time: 30–60 minutes to configure and test.
- How: follow WireGuard quickstart docs; configure server keys and client configs.

### 11) Overall timeline estimates
- Minimal baseline (local only): strong passwords + 2FA + backups = ~15–30 minutes.
- Nabu Casa remote access: ~5–10 minutes.
- Tailscale remote access: ~10–30 minutes.
- Nginx + Let’s Encrypt reverse proxy: ~30–90 minutes (depends on domain/router).
- Full hardening (fail2ban, IP allowlist, backups, updates): 1–3 hours total.

---

## Monetary summary
- Nabu Casa: ~$6.50/month
- Domain (optional): ~$10–15/year
- VPS (optional): $5+/month if hosting externally
- Tailscale: free for personal use
- Time cost: plan 1–3 hours to implement recommended measures

---

## Practical next steps (recommended)
1. If you want remote access quickly and with minimal risk: enable **Nabu Casa** (subscribe via Home Assistant UI).
2. If you prefer no subscription but want secure remote access: set up **Tailscale** on the HA host and your phone.
3. If you want a custom domain/URL: follow the Nginx + Certbot approach (requires domain and port forwarding).

---

## I can help with
- Walk you step-by-step through enabling Nabu Casa (UI walkthrough).
- Add a `docs/REMOTE_ACCESS.md` section with Tailscale commands tailored to your host OS.
- Provide an example `nginx` config + `certbot` command and a `fail2ban` sample for nginx logs.

Tell me which of the three options you want to use (Nabu Casa / Tailscale / Nginx + Let's Encrypt) and the OS of your Home Assistant host (Home Assistant OS, Raspberry Pi OS, Ubuntu, Docker host), and I will add step-by-step instructions to the repo and walk you through the setup.
