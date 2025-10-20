# PortScan Advanced - Guía de Instalación

## Windows

### Opción 1: Instalación Automática (Recomendada)

1. **Instalar Python**
   - Descargar desde: https://www.python.org/downloads/
   - Marcar "Add Python to PATH" durante la instalación
   - Verificar: `python --version`

2. **Instalar Nmap**
   - Descargar desde: https://nmap.org/download.html
   - Ejecutar el instalador
   - Verificar: `nmap --version`

3. **Ejecutar el script**
   ```cmd
   # Doble clic en run.bat o desde CMD:
   run.bat
   ```
   
   El script `run.bat`:
   - Configura el terminal en verde
   - Verifica dependencias automáticamente
   - Instala paquetes necesarios
   - Ejecuta el programa

### Opción 2: Instalación Manual

```cmd
# 1. Clonar repositorio
git clone https://github.com/Veik1/portscan-script.git
cd portscan-script

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
python portscan-script.py
```

## Linux

### Ubuntu/Debian

```bash
# 1. Actualizar sistema
sudo apt-get update

# 2. Instalar dependencias del sistema
sudo apt-get install -y python3 python3-pip nmap git

# 3. Clonar repositorio
git clone https://github.com/Veik1/portscan-script.git
cd portscan-script

# 4. Dar permisos de ejecución al script
chmod +x run.sh

# 5. Ejecutar (con privilegios para funciones avanzadas)
sudo ./run.sh
```

### Fedora/RHEL/CentOS

```bash
# 1. Instalar dependencias
sudo dnf install -y python3 python3-pip nmap git

# 2. Clonar y ejecutar
git clone https://github.com/Veik1/portscan-script.git
cd portscan-script
chmod +x run.sh
sudo ./run.sh
```

### Arch Linux

```bash
# 1. Instalar dependencias
sudo pacman -S python python-pip nmap git

# 2. Clonar y ejecutar
git clone https://github.com/Veik1/portscan-script.git
cd portscan-script
chmod +x run.sh
sudo ./run.sh
```

## macOS

### Con Homebrew (Recomendado)

```bash
# 1. Instalar Homebrew (si no está instalado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar dependencias
brew install python nmap git

# 3. Clonar repositorio
git clone https://github.com/Veik1/portscan-script.git
cd portscan-script

# 4. Dar permisos de ejecución
chmod +x run.sh

# 5. Ejecutar
sudo ./run.sh
```

## Instalación de Dependencias de Python

### Todas las plataformas

```bash
# Ver requirements.txt para la lista completa
pip install -r requirements.txt

# O instalar manualmente:
pip install python-nmap scapy requests colorama
```

### Dependencias individuales

```bash
pip install python-nmap    # Interfaz Python para Nmap
pip install scapy          # Manipulación de paquetes de red
pip install requests       # Cliente HTTP
pip install colorama       # Colores en terminal
```

## Solución de Problemas

### Windows

**Error: "python no se reconoce como comando"**
```cmd
# Solución: Añadir Python al PATH
# 1. Buscar "Variables de entorno" en Windows
# 2. Editar PATH
# 3. Añadir: C:\Users\TuUsuario\AppData\Local\Programs\Python\Python3X
```

**Error: "pip no se reconoce como comando"**
```cmd
# Solución:
python -m pip install --upgrade pip
```

**Error: Scapy no funciona en Windows**
```cmd
# Solución: Instalar Npcap
# Descargar desde: https://npcap.com/#download
# Instalar con opción "WinPcap API-compatible Mode"
```

### Linux

**Error: Permission denied**
```bash
# Solución: Ejecutar con sudo
sudo python3 portscan-script.py
```

**Error: ModuleNotFoundError**
```bash
# Solución: Usar pip3 en vez de pip
pip3 install -r requirements.txt
```

**Error: Scapy requiere privilegios**
```bash
# Solución: Ejecutar como root
sudo python3 portscan-script.py
```

### macOS

**Error: No module named 'scapy'**
```bash
# Solución: Usar pip3
pip3 install scapy
```

**Error: Operation not permitted**
```bash
# Solución: Dar permisos de acceso completo al disco
# System Preferences > Security & Privacy > Privacy > Full Disk Access
# Añadir Terminal
```

## Verificación de Instalación

### Verificar Python

```bash
python --version
# o
python3 --version

# Debe mostrar: Python 3.7.x o superior
```

### Verificar Nmap

```bash
nmap --version

# Debe mostrar la versión de Nmap instalada
```

### Verificar Dependencias

```bash
python -c "import nmap; print('nmap: OK')"
python -c "import scapy; print('scapy: OK')"
python -c "import requests; print('requests: OK')"
python -c "import colorama; print('colorama: OK')"
```

## Actualización

### Desde Git

```bash
cd portscan-script
git pull origin main
pip install -r requirements.txt --upgrade
```

### Manual

1. Descargar la última versión desde GitHub
2. Reemplazar archivos
3. Actualizar dependencias: `pip install -r requirements.txt --upgrade`

## Desinstalación

### Eliminar programa

```bash
# Linux/macOS
rm -rf portscan-script

# Windows
rmdir /s portscan-script
```

### Eliminar dependencias

```bash
pip uninstall python-nmap scapy requests colorama -y
```

## Requisitos del Sistema

### Mínimos
- **CPU**: 1 GHz o superior
- **RAM**: 512 MB
- **Disco**: 100 MB de espacio libre
- **SO**: Windows 7+, Linux (kernel 3.x+), macOS 10.12+

### Recomendados
- **CPU**: 2 GHz dual-core
- **RAM**: 2 GB
- **Disco**: 500 MB de espacio libre
- **Red**: Interfaz de red activa

## Notas Importantes

**Privilegios de Administrador**
- Algunas funciones requieren privilegios elevados
- Windows: Ejecutar CMD como Administrador
- Linux/macOS: Usar `sudo`

**Firewall**
- Puede que necesites permitir Python en el firewall
- Algunas funciones pueden ser bloqueadas por antivirus

**Uso Legal**
- Solo usa esta herramienta en redes que controles
- Obtén autorización antes de escanear redes ajenas
- El uso indebido puede ser ilegal

## Soporte

Si tienes problemas:
1. Revisa esta guía de instalación
2. Consulta los [Issues en GitHub](https://github.com/Veik1/portscan-script/issues)
3. Abre un nuevo issue con detalles del problema
