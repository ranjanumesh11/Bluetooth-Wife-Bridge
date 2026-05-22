@echo off
echo ============================================================
echo  Sven and Son Bed Bridge -- Push to GitHub
echo ============================================================
echo.

cd /d "%~dp0"

git add .
git status

echo.
set /p MSG="Commit message (or press Enter for default): "
if "%MSG%"=="" set MSG=fix: all 18 remote buttons mapped, removed fake TV preset

git commit -m "%MSG%"
git push origin main

echo.
if %ERRORLEVEL%==0 (
    echo SUCCESS - pushed to GitHub!
) else (
    echo ERROR - check output above.
    echo If auth failed, update the remote URL with your new PAT:
    echo   git remote set-url origin https://YOUR_NEW_PAT@github.com/ranjanumesh11/Bluetooth-Wife-Bridge.git
)
echo.
pause
