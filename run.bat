@echo off
:: PortScan Advanced - Launcher Script
:: Configura el terminal en verde y ejecuta el programa

:: Establecer color verde sobre fondo negro (0 = negro, A = verde claro)
color 0A

:: Título de la ventana
title PortScan Advanced - Network Reconnaissance Tool

:: Limpiar pantalla
cls

:: Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.7+ desde https://www.python.org/
    pause
    exit /b 1
)

:: Verificar si las dependencias están instaladas
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

:: Ejecutar el programa
cls
python portscan-advanced.py %*

:: Si el programa termina, mantener la ventana abierta
if errorlevel 1 (
    echo.
    echo El programa termino con errores
    pause
)
