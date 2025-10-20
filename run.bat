@echo off

color 0A

title PortScan - Network Reconnaissance Tool

cd /d "%~dp0"

cls

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.7+ desde https://www.python.org/
    pause
    exit /b 1
)

echo Verificando dependencias...
python -c "import nmap, scapy, colorama, requests" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [!] Instalando dependencias necesarias...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

cls
python portscan-script.py %*

if errorlevel 1 (
    echo.
    echo El programa termino con errores
    pause
)
