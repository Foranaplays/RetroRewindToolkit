@echo off
setlocal
cd /d "%~dp0"
title Retro Rewind Toolkit - FINAL Single File

echo ============================================================
echo Retro Rewind Toolkit v0.13 RC - FINAL SINGLE FILE
echo ============================================================
echo.

where dotnet >nul 2>nul
if errorlevel 1 (
  echo ERROR: .NET 8 SDK not found.
  pause
  exit /b 1
)

if exist Release rmdir /s /q Release

dotnet publish RetroRewindToolkit.csproj ^
  -c Release ^
  -r win-x64 ^
  --self-contained false ^
  -p:PublishSingleFile=true ^
  -p:DebugType=None ^
  -p:DebugSymbols=false ^
  -o Release

if errorlevel 1 (
  echo.
  echo BUILD FAILED.
  pause
  exit /b 1
)

echo.
echo ============================================================
echo DONE
echo ============================================================
echo.
echo Expected final application:
echo   Release\RetroRewindToolkit.exe
echo.
echo IMPORTANT:
echo - Test Skip Tutorial, Money and Level before uploading.
echo - Then scan Release\RetroRewindToolkit.exe with VirusTotal.
echo.
pause
