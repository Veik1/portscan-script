# PortScan Advanced

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-green)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

**Herramienta avanzada de reconocimiento y auditoría de redes con interfaz de terminal verde estilo hacker**

</div>

---

## Descripcion

**PortScan Advanced** es una herramienta profesional de escaneo de redes que combina multiples tecnicas de reconocimiento en una interfaz interactiva. Diseñada para profesionales de seguridad, administradores de sistemas y entusiastas de redes.

### Caracteristicas Principales

- **Interfaz interactiva** con menu verde estilo terminal
- **14 funcionalidades** de escaneo y reconocimiento
- **Multiples formatos** de exportacion (JSON, CSV, HTML)
- **Escaneos sigilosos** para evasion de IDS
- **Deteccion de SO y servicios** con Nmap
- **Historial y analisis** de escaneos
- **Multiplataforma** (Windows, Linux, macOS)

---

## Inicio Rapido

### Windows

```cmd
run.bat
```

### Linux/macOS

```bash
chmod +x run.sh
sudo ./run.sh
```

### Modo Interactivo

```bash
python portscan-script.py
```

---

## Funcionalidades

### 1. Descubrimiento de Dispositivos
- Escaneo ARP de red local
- Deteccion automatica de rango de red
- Resolucion de nombres de host
- Obtencion de direcciones MAC

### 2. Escaneo de Puertos
- **Escaneo Rapido**: Top 100 puertos mas comunes (~30 seg)
- **Escaneo Completo**: Todos los puertos 1-65535 (~10 min)
- **Escaneo Personalizado**: Puertos especificos o rangos

### 3. Deteccion de Servicios
- Identificacion de servicios y versiones
- Banner grabbing avanzado
- Analisis de respuestas de servicios

### 4. Deteccion de Sistema Operativo
- OS Fingerprinting con Nmap
- Identificacion de versiones de SO
- Porcentaje de precision

### 5. Escaneo de Vulnerabilidades
- Uso de scripts NSE de Nmap
- Deteccion de vulnerabilidades conocidas
- Analisis de seguridad de servicios

### 6. Escaneo Sigiloso
- SYN Scan (Half-open)
- Fragmentacion de paquetes
- Evasion de IDS/IPS

### 7. Deteccion de Firewall/IDS
- ACK Scan para detectar filtrado
- Identificacion de reglas de firewall
- Analisis de puertos filtrados

### 8. Exportacion de Resultados
- **JSON**: Para procesamiento automatico
- **CSV**: Para analisis en Excel
- **HTML**: Reporte visual profesional

### 9. Analisis Avanzado
- Historial de escaneos
- Estadisticas de servicios detectados
- Top puertos y servicios mas comunes

### 10. Traceroute
- Ruta de paquetes a objetivo
- Diagnostico de conectividad de red

---

## Instalacion

### Requisitos Previos

- Python 3.7 o superior
- Nmap instalado en el sistema
- Privilegios de administrador/root (para algunas funciones)

### Windows

```cmd
# 1. Instalar Python desde: https://www.python.org/
# 2. Instalar Nmap desde: https://nmap.org/download.html

# 3. Clonar repositorio
git clone https://github.com/Veik1/portscan-script.git
cd portscan-script

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar
run.bat
```

### Linux (Ubuntu/Debian)

```bash
# Instalar dependencias del sistema
sudo apt-get update
sudo apt-get install -y python3 python3-pip nmap git

# Clonar repositorio
git clone https://github.com/Veik1/portscan-script.git
cd portscan-script

# Instalar dependencias de Python
pip3 install -r requirements.txt

# Ejecutar
sudo ./run.sh
```

### macOS

```bash
# Instalar Homebrew (si no esta instalado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependencias
brew install python nmap git

# Clonar repositorio
git clone https://github.com/Veik1/portscan-script.git
cd portscan-script

# Instalar dependencias de Python
pip3 install -r requirements.txt

# Ejecutar
sudo ./run.sh
```

---

## Uso

### Menu Interactivo

```bash
# Iniciar menu interactivo
python portscan-script.py

# Navegar usando numeros (1-14)
# [1] Descubrimiento de dispositivos
# [2] Escaneo rapido de puertos
# [3] Escaneo completo de puertos
# ... y mas opciones
```

### Linea de Comandos

```bash
# Escaneo rapido
python portscan-script.py -t 192.168.1.1

# Escaneo completo
python portscan-script.py-t 192.168.1.1 -f

# Escaneo de puertos especificos
python portscan-script.py -t 192.168.1.1 -p 80,443,22,3306

# Deteccion de servicios
python portscan-script.py -t 192.168.1.1 -s

# Guardar resultados en JSON
python portscan-script.py -t 192.168.1.1 -o results.json

# Guardar resultados en HTML
python portscan-script.py -t 192.168.1.1 -s -o report.html

# Ver ayuda
python portscan-script.py --help
```

---

## Ejemplos de Salida

### Descubrimiento de Dispositivos

```
IP                   MAC Address          Hostname
----------------------------------------------------------------------
192.168.1.1          00:11:22:33:44:55    router.local
192.168.1.100        AA:BB:CC:DD:EE:FF    server.local
192.168.1.105        11:22:33:44:55:66    desktop.local

[OK] Se encontraron 3 dispositivos
```

### Escaneo de Puertos

```
Resultados del escaneo para 192.168.1.100:
Estado del host: up

Protocolo: TCP
Puerto     Estado       Servicio             Version
--------------------------------------------------------------------------------
22         open         ssh                  OpenSSH 8.2p1 Ubuntu
80         open         http                 Apache 2.4.41
443        open         https                Apache 2.4.41
3306       open         mysql                MySQL 8.0.23
```

---

## Codigo de Colores

La herramienta usa colores para facilitar la lectura:

- **Verde**: Puertos abiertos, operaciones exitosas
- **Rojo**: Puertos cerrados, errores
- **Amarillo**: Advertencias, informacion importante
- **Azul**: Informacion general, prompts
- **Magenta**: Scripts NSE, datos adicionales
- **Blanco**: Texto general, resultados

---

## Documentacion

- **[INSTALL.md](INSTALL.md)** - Guia de instalacion para todos los sistemas operativos
- **[EXAMPLES.md](EXAMPLES.md)** - 20+ ejemplos practicos de uso

---

## Consideraciones de Seguridad

**ADVERTENCIA LEGAL**:
- Esta herramienta es para uso educativo y profesional
- Solo escanea redes de tu propiedad o con autorizacion explicita
- El escaneo no autorizado es ilegal en muchas jurisdicciones
- El autor no se hace responsable del mal uso

### Permisos Necesarios

Algunas funciones requieren privilegios elevados:

**Windows**: Ejecutar CMD como Administrador  
**Linux/macOS**: Ejecutar con `sudo`

Funciones que requieren privilegios:
- Descubrimiento de dispositivos (ARP)
- Escaneo sigiloso (SYN Scan)
- Deteccion de sistema operativo
- Deteccion de firewall

---

## Casos de Uso

1. **Auditoria de Seguridad** - Pentesting profesional
2. **Inventario de Red** - Descubrimiento de activos
3. **Monitoreo** - Verificacion de servicios
4. **Educacion** - Aprendizaje de redes y seguridad
5. **Troubleshooting** - Diagnostico de problemas de red
6. **Cumplimiento** - Verificar politicas de seguridad
7. **DevOps** - Validar despliegues

---

## Contribuciones

Las contribuciones son bienvenidas! Si tienes ideas para mejorar la herramienta:

1. Fork el proyecto
2. Crea una rama para tu funcion (`git checkout -b feature/nueva-funcion`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcion'`)
4. Push a la rama (`git push origin feature/nueva-funcion`)
5. Abre un Pull Request

---

## Reportar Problemas

Si encuentras algun bug, por favor abre un [issue](https://github.com/Veik1/portscan-script/issues) con:
- Descripcion del problema
- Pasos para reproducirlo
- Sistema operativo y version de Python
- Logs de error (si aplica)

---

## Autor

**Veik1**
- GitHub: [@Veik1](https://github.com/Veik1)

---

## Licencia

Este proyecto esta bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para mas detalles.
