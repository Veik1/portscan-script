import nmap
import json
import requests
import argparse
from scapy.all import ARP, Ether, srp
import socket

def ipFinder(interface):
    local_ip = getLocalIp()
    if local_ip is None:
        print("No se pudo obtener la IP local.")
        return []

    network = getIpRange(local_ip)
    print(f"Buscando dispositivos en la red: {network}")

    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, iface=interface, verbose=False)[0]

    devices = []
    for sent, received in result:
        devices.append(received.psrc)
        print(f"Dispositivo encontrado: {received.psrc}")

    return devices

def getLocalIp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error al obtener la IP local: {e}")
        return None

def getIpRange(ip):
    if ip is None:
        return "0.0.0.0/24"
    segmentosIp = ip.split('.')
    ipBase = '.'.join(segmentosIp[:3])
    return f"{ipBase}.0/24"

def scan_ports(ip):
    open_ports = {'TCP': [], 'UDP': []}
    nm = nmap.PortScanner()

    # Escaneo de puertos TCP
    print(f"Escaneando puertos TCP en {ip}...")
    try:
        nm.scan(ip, arguments='-p 1-1024')
        for port in nm[ip]['tcp']:
            banner = nm[ip]['tcp'][port].get('name', 'No banner')
            open_ports['TCP'].append((port, banner))
    except KeyError:
        print(f"No se encontraron puertos TCP abiertos en {ip}")
    except Exception as e:
        print(f"Error en el escaneo TCP: {e}")

    # Escaneo de puertos UDP
    print(f"Escaneando puertos UDP en {ip}...")
    try:
        nm.scan(ip, arguments='-sU -p 1-1024')
        for port in nm[ip]['udp']:
            banner = nm[ip]['udp'][port].get('name', 'No banner')
            open_ports['UDP'].append((port, banner))
    except KeyError:
        print(f"No se encontraron puertos UDP abiertos en {ip}")
    except Exception as e:
        print(f"Error en el escaneo UDP: {e}")

    return open_ports

def saveJson(data):
    with open('output.json', 'w') as f:
        json.dump(data, f, indent=4)

def send_results(url, data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("[OK]")
        else:
            print(f"[FAIL] Status Code: {response.status_code}")
    except requests.RequestException as e:
        print(f"[FAIL] {e}")

def main():
    parser = argparse.ArgumentParser(description='Busqueda de IP y puertos dentro de una red.')
    parser.add_argument('-i', '--interface', required=True, help='Interfaz de red a utilizar')
    args = parser.parse_args()

    interface = args.interface
    url = "http://127.0.0.1/example/fake_url.php"

    devices = ipFinder(interface)
    if not devices:
        print("No se encontraron dispositivos en la red.")
        return

    results_data = {}

    for ip in devices:
        print(f"\n{ip}")
        print("=" * 20)
        open_ports = scan_ports(ip)
        results_data[ip] = open_ports

        print("TCP:")
        if open_ports['TCP']:
            for port, banner in open_ports['TCP']:
                print(f"\t{port}: {banner}")
        else:
            print("\tNo se encontraron puertos TCP abiertos.")

        print("UDP:")
        if open_ports['UDP']:
            for port, banner in open_ports['UDP']:
                print(f"\t{port}: {banner}")
        else:
            print("\tNo se encontraron puertos UDP abiertos.")

    print(f"\nEnviando resultados a la URL {url} . . . ", end="")
    send_results(url, results_data)

    print("Generando fichero output.json... ", end="")
    saveJson(results_data)
    print("[OK]")

if __name__ == "__main__":
    main()
