@echo off
REM ============================================================
REM push_to_github.bat
REM Run this once from your Windows machine to initialise the
REM local git repo and push everything to GitHub.
REM
REM Double-click this file OR run it from Command Prompt.
REM ============================================================

echo.
echo  Sven ^& Son Bed Bridge — GitHub Push Script
echo  ============================================
echo.

REM Change to the folder this script lives in
cd /d "%~dp0"

REM ── Git identity ────────────────────────────────────────────
git config user.name "Ranjan"
git config user.email "ranjanu.on@gmail.com"

REM ── Initialise repo if not already done ─────────────────────
IF NOT EXIST ".git" (
    echo  Initialising git repo...
    git init
    git branch -M main
) ELSE (
    echo  Git repo already initialised.
)

REM ── Set remote (update PAT if it expires) ───────────────────
git remote remove origin 2>nul
git remote add origin https://ranjanumesh11:YOUR_PAT_HERE@github.com/ranjanumesh11/Bluetooth-Wife-Bridge.git

REM ── Stage all files ──────────────────────────────────────────
echo.
echo  Staging files...
git add -A

REM ── Commit ──────────────────────────────────────────────────
echo.
echo  Creating initial commit...
git commit -m "feat: initial project scaffold

- ESPHome BLE proxy config (Approach 1)
- ESPHome GPIO relay config w/ optocouplers (Approach 2)
- Home Assistant package with all bed entities
- Example HA automations (morning, bedtime, movie night)
- Hardware schematic and BOM for optocoupler approach
- BLE scanning guide and Python BLE scanner script
- End-to-end setup guide and troubleshooting docs
- .gitignore (excludes secrets.yaml and build artifacts)"

REM ── Push ────────────────────────────────────────────────────
echo.
echo  Pushing to GitHub...
git push -u origin main --force

echo.
echo  ============================================
echo  Done! Check: https://github.com/ranjanumesh11/Bluetooth-Wife-Bridge
echo  ============================================
echo.
pause
