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

if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo -e "${YELLOW}[!] pip3 no está instalado${NC}"
    echo "Instalando pip3..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Intentar instalar con apt-get (ignorando errores de repos)
        sudo apt-get install -y python3-pip 2>/dev/null
        
        # Si falla, intentar con ensurepip
        if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
            echo -e "${YELLOW}Intentando método alternativo...${NC}"
            python3 -m ensurepip --default-pip --user 2>/dev/null || \
            sudo apt-get install -y python3-pip --fix-missing 2>/dev/null || \
            wget -qO- https://bootstrap.pypa.io/get-pip.py | python3 - --user
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        python3 -m ensurepip --upgrade
    fi
    
    # Verificar si se instaló correctamente
    if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
        echo -e "${RED}[ERROR] No se pudo instalar pip3${NC}"
        echo -e "${YELLOW}Por favor, instálalo manualmente:${NC}"
        echo -e "${YELLOW}  sudo apt-get install python3-pip${NC}"
        echo -e "${YELLOW}O usa: python3 -m ensurepip --default-pip --user${NC}"
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
    
    # Intentar con pip3 primero
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt --break-system-packages 2>/dev/null || \
        pip3 install -r requirements.txt --user 2>/dev/null || \
        pip3 install -r requirements.txt 2>/dev/null
    # Si no hay pip3, usar python3 -m pip
    elif python3 -m pip --version &> /dev/null; then
        python3 -m pip install -r requirements.txt --break-system-packages 2>/dev/null || \
        python3 -m pip install -r requirements.txt --user 2>/dev/null || \
        python3 -m pip install -r requirements.txt 2>/dev/null
    fi
    
    # Verificar si se instalaron correctamente
    python3 -c "import nmap, scapy, colorama, requests" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] No se pudieron instalar las dependencias${NC}"
        echo -e "${YELLOW}Intenta instalarlas manualmente con alguno de estos comandos:${NC}"
        echo -e "${YELLOW}  pip3 install python-nmap scapy requests colorama --break-system-packages${NC}"
        echo -e "${YELLOW}  python3 -m pip install python-nmap scapy requests colorama --user${NC}"
        echo -e "${YELLOW}  sudo apt-get install python3-pip python3-scapy${NC}"
        exit 1
    fi
    echo -e "${GREEN}[OK] Dependencias instaladas correctamente${NC}"
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
python3 portscan-script.py "$@"

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${RED}El programa terminó con errores (código: $EXIT_CODE)${NC}"
    read -p "Presiona ENTER para salir..."
fi

exit $EXIT_CODE
