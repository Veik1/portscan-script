-----

# portscan-script

**Script de Python diseñado para la búsqueda de dispositivos en red local, escaneo de puertos y generación de reportes de resultados.**

-----

Las funcionalidades de escaneo de red y puertos generalmente se implementan usando librerías especializadas.

  * **Librería `socket`** para la conexión y el escaneo de puertos TCP.
  * **Librería `scapy`** para la detección de dispositivos en la red local (ARP/ping sweeps).

-----

## Funcionalidad

`portscan-script` consolida tres funcionalidades clave para la auditoría y monitoreo de redes locales:

1.  **Búsqueda de Dispositivos en Red Local:** Identifica qué hosts (ordenadores, servidores, routers, etc.) están activos y accesibles dentro del rango de red especificado.
2.  **Escaneo de Puertos:** Una vez que un dispositivo es detectado, intenta conectarse a un rango de puertos TCP (o UDP) definidos para determinar cuáles están **abiertos** y escuchando conexiones.
3.  **Reporte de Resultados:** Presenta los resultados del escaneo de forma estructurada, mostrando los dispositivos activos junto con la lista de puertos abiertos para cada uno, facilitando el análisis.

-----

## Explicación del Funcionamiento

El script opera en dos fases principales, basándose en la arquitectura de red y la programación de sockets:

### 1\. Descubrimiento de Dispositivos (Device Discovery)

Para encontrar dispositivos activos en la red local, el script típicamente realiza un "barrido" a través de un rango de direcciones IP. Esto se puede lograr de dos maneras comunes:

  * **ARP Scan:** Envía peticiones ARP a todas las direcciones IP en el segmento de red. Los hosts que están activos y en la misma red responderán, revelando su existencia.
  * **ICMP/Ping Scan:** Envía paquetes ICMP (los que usa el comando `ping`) a un rango de IPs. Los hosts que responden indican que están activos.

### 2\. Escaneo de Puertos (Port Scanning)

Una vez que se tiene una lista de IPs activas, el script itera sobre un rango de puertos para cada IP.

  * Utiliza la funcionalidad de *sockets* de Python para intentar establecer una conexión **TCP** con un puerto específico de la IP objetivo.
  * Si la conexión se establece (`SYN` enviado y `SYN-ACK` recibido), el script determina que el puerto está **abierto**.
  * Si la conexión es rechazada (`RST` recibido) o si el intento falla por tiempo de espera (`timeout`), el puerto se considera **cerrado** o **filtrado**.

### 3\. Generación del Reporte

Finalmente, el script recopila los datos (IP, host, puertos abiertos) y los formatea. Esto a menudo incluye imprimir los resultados en la consola o guardarlos en un archivo (por ejemplo, `.txt` o `.csv`) para una posterior revisión.

-----

## Uso

### Requisitos

  * **Python 3.x** instalado.
  * Probablemente requiera la instalación de librerías de terceros (ej. `scapy`, `colorama`).

<!-- end list -->

```bash
# Ejemplo de instalación de dependencias
pip install -r requirements.txt
```

### Ejecución

El script, denominado **`portscan-script.py`**, probablemente requiere argumentos de línea de comandos para especificar el rango de red a escanear.

**Sintaxis (Inferencia Típica):**

```bash
python portscan-script.py <Dirección_IP_o_Rango_CIDR> [Opciones]
```

**Ejemplos de Uso (Inferencia):**

| Comando | Descripción |
| :--- | :--- |
| `python portscan-script.py 192.168.1.1/24` | Escanea todos los dispositivos en el segmento de red `192.168.1.0`. |
| `python portscan-script.py 192.168.1.10 -p 1-1000` | Escanea los puertos del **1 al 1000** en el host específico `192.168.1.10`. |
| `python portscan-script.py --help` | Muestra la ayuda y las opciones detalladas del script. |

-----

## ⚖️ Licencia

Este proyecto está bajo la **Licencia MIT**. Puedes encontrar los detalles completos en el archivo [LICENSE](https://www.google.com/search?q=LICENSE).
