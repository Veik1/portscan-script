@echo off
:: PortScan Advanced - Quick Start Guide
:: Este archivo muestra información rápida de ayuda

color 0A
cls

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║          PortScan Advanced - Guia Rapida de Inicio           ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo.
echo [1] INICIO RAPIDO
echo     Ejecuta: run.bat
echo.
echo [2] MODO INTERACTIVO
echo     python portscan-advanced.py
echo.
echo [3] ESCANEO RAPIDO
echo     python portscan-advanced.py -t IP_OBJETIVO
echo.
echo [4] ESCANEO COMPLETO
echo     python portscan-advanced.py -t IP_OBJETIVO -f
echo.
echo [5] AYUDA COMPLETA
echo     python portscan-advanced.py --help
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo EJEMPLOS:
echo   python portscan-advanced.py -t 192.168.1.1
echo   python portscan-advanced.py -t google.com -s
echo   python portscan-advanced.py -t 10.0.0.1 -p 80,443,22
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo DOCUMENTACION:
echo   README-ADVANCED.md  - Documentacion completa
echo   INSTALL.md          - Guia de instalacion
echo   EXAMPLES.md         - Ejemplos de uso
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
