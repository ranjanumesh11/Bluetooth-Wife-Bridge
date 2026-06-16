# Contributing to BLE WiFi Bridge

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/ranjanumesh11/Bluetooth-Wife-Bridge.git
cd Bluetooth-Wife-Bridge
```

### 2. Enable Git Hooks (IMPORTANT!)
This project uses Git hooks to prevent common mistakes like case-sensitive branch naming conflicts.

**One-time setup:**
```bash
git config core.hooksPath .githooks
```

This enables the `pre-push` hook that will catch branch naming issues before they reach GitHub.

---

## Branch Naming Rules

⚠️ **Use lowercase for all branch names** — No exceptions!

### ❌ Bad (will be rejected):
- `DEV` (conflicts with `dev`)
- `Main` (conflicts with `main`)  
- `Feature-XYZ` (inconsistent casing)

### ✅ Good:
- `dev`
- `main`
- `feature-xyz`
- `bugfix-issue-123`

---

## Workflow

### Create a Feature Branch
```bash
# Make sure you're up to date
git checkout main
git pull origin main

# Create a new branch (use lowercase!)
git checkout -b feature-your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add your feature description"
```

### Push Your Branch
```bash
git push origin feature-your-feature-name
```

If you get an error about case conflicts, the `pre-push` hook caught it! 

**To fix:**
```bash
# Rename your branch to lowercase
git branch -m feature-your-feature-name

# Try pushing again
git push origin feature-your-feature-name
```

### Create a Pull Request
1. Go to [GitHub](https://github.com/ranjanumesh11/Bluetooth-Wife-Bridge)
2. Click "New Pull Request"
3. Select your branch and create the PR
4. Wait for GitHub Actions checks to pass
5. Request review

---

## GitHub Actions Protection

Two layers of protection prevent branch naming issues:

1. **Client-side (`.githooks/pre-push`)** — Catches problems before push
2. **Server-side (GitHub Actions workflow)** — Detects & deletes conflicting branches

If a bad branch gets pushed anyway, the GitHub Actions workflow will automatically delete it and notify you.

---

## Troubleshooting

### "pre-push hook rejected my push"
```bash
# Check your branch name
git branch

# If it's the wrong case, rename it
git branch -m correct-lowercase-name

# Try pushing again
git push origin correct-lowercase-name
```

### "My branch was deleted by GitHub Actions"
This means you pushed a branch with a case conflict. Check the Actions log:
1. Go to **Actions** tab on GitHub
2. Find the "Prevent Case-Sensitive Branch Conflicts" workflow run
3. It will show which branch was deleted and why

---

## Questions?

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for more help.
