# Ejemplos de Uso - PortScan Advanced

Esta guía contiene ejemplos prácticos de uso de PortScan Advanced para diferentes escenarios.

## Tabla de Contenidos

1. [Escaneos Básicos](#escaneos-básicos)
2. [Auditoría de Seguridad](#auditoría-de-seguridad)
3. [Análisis de Red](#análisis-de-red)
4. [Casos de Uso Específicos](#casos-de-uso-específicos)
5. [Automatización](#automatización)

---

## Escaneos Básicos

### 1. Descubrir dispositivos en tu red local

**Modo Interactivo:**
```bash
python portscan-advanced.py
# Seleccionar opción [1]
```

**Salida esperada:**
```
IP                   MAC Address          Hostname
----------------------------------------------------------------------
192.168.1.1          00:11:22:33:44:55    router.local
192.168.1.10         AA:BB:CC:DD:EE:FF    PC-Desktop
192.168.1.25         11:22:33:44:55:66    server.local

[✓] Se encontraron 3 dispositivos
```

### 2. Escaneo rápido de un servidor

```bash
# Modo CLI - Escaneo de top 100 puertos
python portscan-advanced.py -t 192.168.1.100

# Modo interactivo - Opción [2]
```

**Uso típico:** Verificación rápida de servicios en un servidor conocido

### 3. Escaneo completo

```bash
# ADVERTENCIA: Puede tardar varios minutos
python portscan-advanced.py -t 192.168.1.100 -f
```

**Uso típico:** Auditoría completa de seguridad

---

## Auditoría de Seguridad

### Escenario 1: Auditoría completa de servidor web

```bash
# Paso 1: Descubrimiento inicial
python portscan-advanced.py -t webserver.local

# Paso 2: Detección de servicios y versiones
# Opción [5] en menú interactivo
# IP: webserver.local

# Paso 3: Escaneo de vulnerabilidades
# Opción [7] en menú interactivo

# Paso 4: Exportar reporte
# Opción [11] -> Formato HTML
```

**Resultados esperados:**
```
Puerto     Estado       Servicio             Versión
--------------------------------------------------------------------------------
22         open         ssh                  OpenSSH 7.6p1 Ubuntu
80         open         http                 Apache 2.4.29
443        open         https                Apache 2.4.29
3306       open         mysql                MySQL 5.7.33
```

### Escenario 2: Verificar firewall correctamente configurado

```bash
# Ejecutar en modo interactivo
python portscan-advanced.py

# Opción [10] - Detección de Firewall
# IP: servidor-produccion.com
```

**Interpretación:**
- Muchos puertos "filtered" = Firewall activo ✅
- Puertos "closed" = Sin firewall o reglas permisivas ⚠️

### Escenario 3: Escaneo sigiloso para pentesting

```bash
# NOTA: Requiere privilegios de administrador
sudo python portscan-advanced.py

# Opción [9] - Escaneo Sigiloso
# IP: objetivo.com
```

**Beneficios:**
- Menos detectable por IDS/IPS
- No completa handshake TCP
- Útil para reconocimiento discreto

---

## Análisis de Red

### Mapeo completo de red corporativa

**Script de ejemplo:**

```bash
#!/bin/bash
# scan-network.sh - Escanea toda la red y genera reporte

# Descubrir dispositivos
python3 portscan-advanced.py << EOF
1

EOF

# Para cada IP encontrada, hacer escaneo de servicios
for ip in 192.168.1.{1..254}; do
    echo "Escaneando $ip..."
    python3 portscan-advanced.py -t $ip -s -o scan_${ip}.json
done

# Consolidar resultados
echo "Escaneos completados. Ver archivos scan_*.json"
```

### Monitoreo de cambios en servicios

**Primera ejecución (baseline):**
```bash
python portscan-advanced.py -t 192.168.1.100 -s -o baseline.json
```

**Ejecuciones posteriores:**
```bash
python portscan-advanced.py -t 192.168.1.100 -s -o current.json

# Comparar con herramienta diff
diff baseline.json current.json
```

---

## Casos de Uso Específicos

### Caso 1: Verificar servicios críticos activos

```bash
# Verificar servidor de base de datos
python portscan-advanced.py -t db-server.local -p 3306,5432,1433,27017

# Esperado: Puerto correspondiente OPEN
```

**Puertos comunes:**
- MySQL: 3306
- PostgreSQL: 5432
- SQL Server: 1433
- MongoDB: 27017
- Redis: 6379

### Caso 2: Identificar versiones desactualizadas

```bash
# Opción [5] - Detección de servicios y versiones
# Buscar versiones antiguas de:
# - OpenSSH < 8.0
# - Apache < 2.4.40
# - PHP < 7.4
# - MySQL < 8.0
```

**Acción:** Actualizar servicios con versiones vulnerables

### Caso 3: Detectar puertos no autorizados

```bash
# Escaneo completo de servidor en producción
python portscan-advanced.py -t prod-server.com -f -o production_audit.html

# Revisar el HTML generado
# Buscar puertos inesperados:
# - 23 (Telnet) ❌
# - 21 (FTP) ⚠️
# - 3389 (RDP expuesto a internet) ❌
# - Puertos altos no documentados ⚠️
```

### Caso 4: Banner Grabbing para identificar servicios

```bash
# Opción [8] - Banner Grabbing
# IP: 192.168.1.100
# Puerto: 80

# Resultado ejemplo:
HTTP/1.1 200 OK
Server: Apache/2.4.41 (Ubuntu)
X-Powered-By: PHP/7.4.3
```

**Información obtenida:**
- Servidor web: Apache
- Sistema operativo: Ubuntu
- Lenguaje: PHP 7.4.3

### Caso 5: Traceroute para diagnosticar conectividad

```bash
# Opción [14] - Traceroute
# IP: google.com

# Resultado muestra la ruta de paquetes
Hop   IP                   RTT
----------------------------------------
1     192.168.1.1          2.5 ms
2     10.0.0.1            15.3 ms
3     172.16.0.1          28.7 ms
...
```

---

## Automatización

### Script PowerShell (Windows)

```powershell
# scan-multiple.ps1
# Escanea múltiples objetivos y genera reportes

$targets = @(
    "192.168.1.100",
    "192.168.1.101",
    "192.168.1.102"
)

foreach ($target in $targets) {
    Write-Host "Escaneando $target..." -ForegroundColor Green
    python portscan-advanced.py -t $target -s -o "report_$target.html"
    Start-Sleep -Seconds 5
}

Write-Host "Todos los escaneos completados!" -ForegroundColor Green
```

**Ejecutar:**
```powershell
.\scan-multiple.ps1
```

### Script Bash (Linux/macOS)

```bash
#!/bin/bash
# daily-scan.sh - Escaneo diario automatizado

DATE=$(date +%Y%m%d)
LOG_FILE="scan_${DATE}.log"

echo "Iniciando escaneo diario: $DATE" | tee -a $LOG_FILE

# Red local
echo "Escaneando red local..." | tee -a $LOG_FILE
sudo python3 portscan-advanced.py << EOF | tee -a $LOG_FILE
1

EOF

# Servidores críticos
SERVERS=(
    "web-server.local"
    "db-server.local"
    "mail-server.local"
)

for server in "${SERVERS[@]}"; do
    echo "Escaneando $server..." | tee -a $LOG_FILE
    python3 portscan-advanced.py -t $server -s -o "${server}_${DATE}.json"
done

echo "Escaneo completado: $DATE" | tee -a $LOG_FILE

# Enviar email con resultados (opcional)
# mail -s "Reporte de Escaneo $DATE" admin@example.com < $LOG_FILE
```

**Configurar en crontab:**
```bash
# Ejecutar diariamente a las 2 AM
0 2 * * * /path/to/daily-scan.sh
```

### Integración con Python

```python
#!/usr/bin/env python3
# automated_scan.py - Ejemplo de integración

import subprocess
import json
from datetime import datetime

def scan_target(ip, output_file):
    """Ejecuta escaneo y retorna resultados"""
    cmd = f"python portscan-advanced.py -t {ip} -s -o {output_file}"
    subprocess.run(cmd, shell=True)
    
    # Leer resultados
    with open(output_file, 'r') as f:
        return json.load(f)

def main():
    targets = [
        '192.168.1.100',
        '192.168.1.101',
        '192.168.1.102'
    ]
    
    all_results = {}
    
    for target in targets:
        print(f"Escaneando {target}...")
        output = f"scan_{target}_{datetime.now().strftime('%Y%m%d')}.json"
        results = scan_target(target, output)
        all_results[target] = results
        
    # Procesar resultados
    print("\nResumen:")
    for target, data in all_results.items():
        open_ports = len([p for p in data.get('ports', []) if p['state'] == 'open'])
        print(f"{target}: {open_ports} puertos abiertos")

if __name__ == "__main__":
    main()
```

---

## Interpretación de Resultados

### Estados de Puertos

| Estado | Significado | Acción |
|--------|-------------|--------|
| **open** | Puerto abierto y servicio escuchando | Verificar si es necesario |
| **closed** | Puerto cerrado pero accesible | Normal si no hay servicio |
| **filtered** | Bloqueado por firewall | Verificar reglas de firewall |

### Priorización de Hallazgos

**Crítico:**
- Puertos de administración expuestos (22, 3389, 5900)
- Servicios con vulnerabilidades conocidas
- Versiones de software muy antiguas

**Advertencia:**
- Servicios en versiones no actuales
- Puertos no documentados abiertos
- Servicios innecesarios activos

**Información:**
- Servicios esperados en versiones actuales
- Puertos documentados y autorizados

---

## Consejos Profesionales

### 1. Escaneos Periódicos

```bash
# Establecer baseline de seguridad
python portscan-advanced.py -t servidor.com -f -o baseline_$(date +%Y%m%d).json

# Comparar mensualmente
# Buscar: nuevos puertos, servicios cambiados, versiones actualizadas
```

### 2. Documentar Todo

```bash
# Siempre exportar resultados
python portscan-advanced.py -t objetivo.com -s -o audit_$(date +%Y%m%d_%H%M%S).html

# Mantener histórico de escaneos
mkdir -p scans/$(date +%Y)/$(date +%m)
mv *.html scans/$(date +%Y)/$(date +%m)/
```

### 3. Combinar Herramientas

```bash
# PortScan Advanced para descubrimiento
python portscan-advanced.py -t 192.168.1.100 -s

# Luego usar herramientas especializadas:
# - Nikto para servidores web
# - SQLmap para bases de datos
# - Metasploit para exploits
```

### 4. Respeto a la Red

```bash
# Usar escaneo lento en producción
# Opción [9] - Escaneo Sigiloso (T2 timing)

# Evitar escaneos agresivos en horario laboral
# Programar escaneos para madrugada/fin de semana
```

---

## Consideraciones Legales

### Permitido

- Escanear tu propia red doméstica
- Auditar servidores de tu empresa (con autorización)
- Escanear VMs y laboratorios propios
- Investigación en entorno controlado

### Prohibido

- Escanear redes ajenas sin permiso
- Intentar explotar vulnerabilidades encontradas sin autorización
- Escanear infraestructura crítica
- Usar resultados con fines maliciosos

### Buenas Prácticas

1. **Obtener autorización por escrito** antes de escanear
2. **Informar al departamento IT** sobre pruebas planificadas
3. **Documentar scope y metodología** del escaneo
4. **Reportar hallazgos responsablemente**
5. **Respetar horarios y cargas del sistema**

---

## Solución de Problemas Comunes

### Problema: No encuentra dispositivos

```bash
# Solución: Especificar interfaz manualmente
# Windows: ipconfig
# Linux: ip addr o ifconfig

# Usar nombre de interfaz correcto en opción [1]
```

### Problema: Escaneo muy lento

```bash
# Usar escaneo rápido primero
# Opción [2] en vez de [3]

# O especificar puertos comunes
# Opción [4]: 80,443,22,21,3306,3389,5900
```

### Problema: "Permission denied"

```bash
# Ejecutar con privilegios elevados
# Windows: Run as Administrator
# Linux/macOS: sudo python3 portscan-advanced.py
```

---

## Recursos Adicionales

- [Nmap Reference Guide](https://nmap.org/book/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Port Numbers Registry](https://www.iana.org/assignments/service-names-port-numbers/)
- [CVE Database](https://cve.mitre.org/)

---

