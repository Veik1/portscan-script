#!/bin/bash

cd "$(dirname "$0")"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

clear
echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║               PortScan - Network Reconnaissance               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python3 no está instalado${NC}"
    echo "Por favor instala Python 3.7+ usando tu gestor de paquetes"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}[!] pip3 no está instalado${NC}"
    echo "Instalando pip3..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y python3-pip
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        python3 -m ensurepip --upgrade
    else
        echo -e "${RED}[ERROR] No se pudo instalar pip3${NC}"
        exit 1
    fi
fi

if ! command -v nmap &> /dev/null; then
    echo -e "${YELLOW}[!] Nmap no está instalado${NC}"
    echo "Instalando Nmap..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get install -y nmap
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install nmap
    else
        echo -e "${RED}[ERROR] Sistema operativo no soportado${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}[*] Verificando dependencias de Python...${NC}"
python3 -c "import nmap, scapy, colorama, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[!] Instalando dependencias de Python...${NC}"
    pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] No se pudieron instalar las dependencias${NC}"
        echo -e "${YELLOW}Intenta instalarlas manualmente con:${NC}"
        echo -e "${YELLOW}  pip3 install python-nmap scapy requests colorama${NC}"
        exit 1
    fi
fi

if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}[!] Algunas funciones requieren privilegios de root${NC}"
    echo -e "${YELLOW}[!] Considera ejecutar con: sudo ./run.sh${NC}"
    echo ""
    read -p "¿Continuar sin privilegios? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

clear
python3 portscan-advanced.py "$@"

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${RED}El programa terminó con errores (código: $EXIT_CODE)${NC}"
    read -p "Presiona ENTER para salir..."
fi

exit $EXIT_CODE
