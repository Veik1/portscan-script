import nmap
import json
import csv
import os
import sys
import time
import socket
import requests
import argparse
from datetime import datetime
from scapy.all import ARP, Ether, srp, IP, TCP, sr1, conf
from colorama import Fore, Back, Style, init

init(autoreset=True)

class Colors:
    """Clase para manejar colores de terminal"""
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    WHITE = Fore.WHITE
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL

class PortScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
        self.results = {}
        self.scan_history = []
        
    def clear_screen(self):
        """Limpia la pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """Muestra el banner del programa"""
        self.clear_screen()
        banner = f"""
{Colors.GREEN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   ██████╗  ██████╗ ██████╗ ████████╗███████╗ ██████╗ █████╗ ███╗   ██╗   ║
║   ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔════╝██╔══██╗████╗  ██║   ║
║   ██████╔╝██║   ██║██████╔╝   ██║   ███████╗██║     ███████║██╔██╗ ██║   ║
║   ██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║██║     ██╔══██║██║╚██╗██║   ║
║   ██║     ╚██████╔╝██║  ██║   ██║   ███████║╚██████╗██║  ██║██║ ╚████║   ║
║   ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝   ║
║                                                                          ║
║    {Colors.CYAN}Advanced Network Reconnaissance Tool{Colors.GREEN}       ║
║               {Colors.YELLOW}v2.0 - 2025{Colors.GREEN}                   ║
╚══════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
        """
        print(banner)
    
    def print_menu(self):
        """Muestra el menú principal"""
        menu = f"""
{Colors.GREEN}{Colors.BOLD}┌─────────────────────────────────────────────┐
│           MENÚ PRINCIPAL                    │
└─────────────────────────────────────────────┘{Colors.RESET}

{Colors.CYAN}[1]{Colors.WHITE}  Descubrimiento de dispositivos en red
{Colors.CYAN}[2]{Colors.WHITE}  Escaneo rápido de puertos (Top 100)
{Colors.CYAN}[3]{Colors.WHITE}  Escaneo completo de puertos (1-65535)
{Colors.CYAN}[4]{Colors.WHITE}  Escaneo de puertos personalizados
{Colors.CYAN}[5]{Colors.WHITE}  Escaneo de servicios y versiones
{Colors.CYAN}[6]{Colors.WHITE}  Detección de sistema operativo
{Colors.CYAN}[7]{Colors.WHITE}  Escaneo de vulnerabilidades
{Colors.CYAN}[8]{Colors.WHITE}  Banner Grabbing avanzado
{Colors.CYAN}[9]{Colors.WHITE}  Escaneo sigiloso (Stealth Scan)
{Colors.CYAN}[10]{Colors.WHITE} Detección de Firewall/IDS
{Colors.CYAN}[11]{Colors.WHITE} Exportar resultados (JSON/CSV/HTML)
{Colors.CYAN}[12]{Colors.WHITE} Ver historial de escaneos
{Colors.CYAN}[13]{Colors.WHITE} Análisis de servicios detectados
{Colors.CYAN}[14]{Colors.WHITE} Traceroute a objetivo
{Colors.CYAN}[0]{Colors.WHITE}  Salir

{Colors.GREEN}┌─────────────────────────────────────────────┐{Colors.RESET}
{Colors.GREEN}│{Colors.RESET} Selecciona una opción: """
        
        choice = input(menu)
        return choice
    
    def get_local_ip(self):
        """Obtiene la IP local del equipo"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0)
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            print(f"{Colors.RED}Error al obtener IP local: {e}{Colors.RESET}")
            return None
    
    def get_ip_range(self, ip):
        """Calcula el rango de red a partir de una IP"""
        if ip is None:
            return "192.168.1.0/24"
        segments = ip.split('.')
        base_ip = '.'.join(segments[:3])
        return f"{base_ip}.0/24"
    
    def discover_devices(self, interface=None):
        """Descubre dispositivos en la red local usando ARP"""
        print(f"\n{Colors.YELLOW}[*] Iniciando descubrimiento de dispositivos...{Colors.RESET}")
        
        local_ip = self.get_local_ip()
        if local_ip is None:
            print(f"{Colors.RED}[!] No se pudo obtener la IP local{Colors.RESET}")
            return []
        
        network = self.get_ip_range(local_ip)
        print(f"{Colors.CYAN}[*] Tu IP local: {local_ip}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Escaneando red: {network}{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Esto puede tomar unos segundos...{Colors.RESET}\n")
        
        try:
            arp = ARP(pdst=network)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp
            
            # Suprimir warnings de scapy
            conf.verb = 0
            result = srp(packet, timeout=3, verbose=False)[0]
            
            devices = []
            print(f"{Colors.GREEN}{Colors.BOLD}{'IP':<20} {'MAC Address':<20} {'Hostname'}{Colors.RESET}")
            print(f"{Colors.GREEN}{'-'*70}{Colors.RESET}")
            
            for sent, received in result:
                ip = received.psrc
                mac = received.hwsrc
                
                # Intentar obtener hostname
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    hostname = "N/A"
                
                devices.append({'ip': ip, 'mac': mac, 'hostname': hostname})
                print(f"{Colors.WHITE}{ip:<20} {Colors.CYAN}{mac:<20} {Colors.YELLOW}{hostname}{Colors.RESET}")
            
            print(f"\n{Colors.GREEN}[✓] Se encontraron {len(devices)} dispositivos{Colors.RESET}")
            self.results['device_discovery'] = devices
            
            return devices
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error en el descubrimiento: {e}{Colors.RESET}")
            return []
    
    def quick_scan(self, target):
        """Escaneo rápido de los 100 puertos más comunes"""
        print(f"\n{Colors.YELLOW}[*] Ejecutando escaneo rápido en {target}...{Colors.RESET}")
        
        try:
            self.nm.scan(target, arguments='-F -T4')
            return self._parse_scan_results(target)
        except Exception as e:
            print(f"{Colors.RED}[!] Error en escaneo rápido: {e}{Colors.RESET}")
            return None
    
    def full_scan(self, target):
        """Escaneo completo de todos los puertos"""
        print(f"\n{Colors.YELLOW}[*] Ejecutando escaneo completo en {target}...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] ADVERTENCIA: Esto puede tardar varios minutos{Colors.RESET}")
        
        try:
            self.nm.scan(target, arguments='-p- -T4')
            return self._parse_scan_results(target)
        except Exception as e:
            print(f"{Colors.RED}[!] Error en escaneo completo: {e}{Colors.RESET}")
            return None
    
    def custom_port_scan(self, target, ports):
        """Escaneo de puertos personalizados"""
        print(f"\n{Colors.YELLOW}[*] Escaneando puertos {ports} en {target}...{Colors.RESET}")
        
        try:
            self.nm.scan(target, ports=ports, arguments='-T4')
            return self._parse_scan_results(target)
        except Exception as e:
            print(f"{Colors.RED}[!] Error en escaneo personalizado: {e}{Colors.RESET}")
            return None
    
    def service_version_scan(self, target):
        """Escaneo de servicios y versiones"""
        print(f"\n{Colors.YELLOW}[*] Detectando servicios y versiones en {target}...{Colors.RESET}")
        
        try:
            self.nm.scan(target, arguments='-sV -T4')
            return self._parse_scan_results(target, show_version=True)
        except Exception as e:
            print(f"{Colors.RED}[!] Error en detección de servicios: {e}{Colors.RESET}")
            return None
    
    def os_detection(self, target):
        """Detección de sistema operativo"""
        print(f"\n{Colors.YELLOW}[*] Detectando sistema operativo de {target}...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] NOTA: Requiere privilegios de administrador{Colors.RESET}")
        
        try:
            self.nm.scan(target, arguments='-O -T4')
            
            if target in self.nm.all_hosts():
                if 'osmatch' in self.nm[target]:
                    print(f"\n{Colors.GREEN}{Colors.BOLD}Sistema Operativo Detectado:{Colors.RESET}")
                    for osmatch in self.nm[target]['osmatch']:
                        print(f"{Colors.CYAN}  - {osmatch['name']} (Precisión: {osmatch['accuracy']}%){Colors.RESET}")
                else:
                    print(f"{Colors.YELLOW}[!] No se pudo determinar el SO{Colors.RESET}")
            
            return self.nm[target] if target in self.nm.all_hosts() else None
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error en detección de SO: {e}{Colors.RESET}")
            return None
    
    def vulnerability_scan(self, target):
        """Escaneo de vulnerabilidades usando scripts NSE"""
        print(f"\n{Colors.YELLOW}[*] Escaneando vulnerabilidades en {target}...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Usando scripts NSE de Nmap{Colors.RESET}")
        
        try:
            self.nm.scan(target, arguments='--script vuln -T4')
            return self._parse_scan_results(target, show_scripts=True)
        except Exception as e:
            print(f"{Colors.RED}[!] Error en escaneo de vulnerabilidades: {e}{Colors.RESET}")
            return None
    
    def banner_grabbing(self, target, port):
        """Banner grabbing manual de un puerto específico"""
        print(f"\n{Colors.YELLOW}[*] Obteniendo banner de {target}:{port}...{Colors.RESET}")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((target, int(port)))
            
            # Enviar petición HTTP si es puerto web
            if port in [80, 8080, 443, 8443]:
                sock.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
            else:
                sock.send(b"\r\n")
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
            print(f"\n{Colors.GREEN}{Colors.BOLD}Banner obtenido:{Colors.RESET}")
            print(f"{Colors.CYAN}{banner}{Colors.RESET}")
            
            return banner
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error obteniendo banner: {e}{Colors.RESET}")
            return None
    
    def stealth_scan(self, target):
        """Escaneo sigiloso usando SYN scan"""
        print(f"\n{Colors.YELLOW}[*] Ejecutando escaneo sigiloso en {target}...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] NOTA: Requiere privilegios de administrador{Colors.RESET}")
        
        try:
            self.nm.scan(target, arguments='-sS -T2 -f')
            return self._parse_scan_results(target)
        except Exception as e:
            print(f"{Colors.RED}[!] Error en escaneo sigiloso: {e}{Colors.RESET}")
            return None
    
    def firewall_detection(self, target):
        """Detección de firewall/IDS"""
        print(f"\n{Colors.YELLOW}[*] Detectando firewall/IDS en {target}...{Colors.RESET}")
        
        try:
            self.nm.scan(target, arguments='-sA -T4')
            
            if target in self.nm.all_hosts():
                print(f"\n{Colors.GREEN}{Colors.BOLD}Análisis de Firewall:{Colors.RESET}")
                
                filtered_ports = 0
                for proto in self.nm[target].all_protocols():
                    for port in self.nm[target][proto].keys():
                        if self.nm[target][proto][port]['state'] == 'filtered':
                            filtered_ports += 1
                
                if filtered_ports > 0:
                    print(f"{Colors.RED}[!] Posible firewall detectado ({filtered_ports} puertos filtrados){Colors.RESET}")
                else:
                    print(f"{Colors.GREEN}[✓] No se detectó firewall evidente{Colors.RESET}")
            
            return self.nm[target] if target in self.nm.all_hosts() else None
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error en detección de firewall: {e}{Colors.RESET}")
            return None
    
    def traceroute(self, target):
        """Realiza un traceroute al objetivo"""
        print(f"\n{Colors.YELLOW}[*] Ejecutando traceroute a {target}...{Colors.RESET}")
        
        try:
            self.nm.scan(target, arguments='--traceroute')
            
            if target in self.nm.all_hosts() and 'trace' in self.nm[target]:
                print(f"\n{Colors.GREEN}{Colors.BOLD}Ruta a {target}:{Colors.RESET}")
                print(f"{Colors.GREEN}{'Hop':<5} {'IP':<20} {'RTT'}{Colors.RESET}")
                print(f"{Colors.GREEN}{'-'*40}{Colors.RESET}")
                
                for hop in self.nm[target]['trace']['hops']:
                    hop_num = hop['ttl']
                    hop_ip = hop['ipaddr']
                    hop_rtt = hop['rtt']
                    print(f"{Colors.WHITE}{hop_num:<5} {Colors.CYAN}{hop_ip:<20} {Colors.YELLOW}{hop_rtt} ms{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}[!] No se pudo obtener la ruta{Colors.RESET}")
            
            return self.nm[target] if target in self.nm.all_hosts() else None
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error en traceroute: {e}{Colors.RESET}")
            return None
    
    def _parse_scan_results(self, target, show_version=False, show_scripts=False):
        """Parsea y muestra los resultados de un escaneo"""
        if target not in self.nm.all_hosts():
            print(f"{Colors.RED}[!] No se encontraron resultados para {target}{Colors.RESET}")
            return None
        
        host = self.nm[target]
        results = {'target': target, 'scan_time': datetime.now().isoformat(), 'ports': []}
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}Resultados del escaneo para {target}:{Colors.RESET}")
        print(f"{Colors.CYAN}Estado del host: {host.state()}{Colors.RESET}\n")
        
        for proto in host.all_protocols():
            print(f"{Colors.GREEN}{Colors.BOLD}Protocolo: {proto.upper()}{Colors.RESET}")
            print(f"{Colors.GREEN}{'Puerto':<10} {'Estado':<12} {'Servicio':<20} {'Versión'}{Colors.RESET}")
            print(f"{Colors.GREEN}{'-'*80}{Colors.RESET}")
            
            ports = sorted(host[proto].keys())
            for port in ports:
                port_info = host[proto][port]
                state = port_info['state']
                service = port_info.get('name', 'unknown')
                version = port_info.get('version', '') if show_version else ''
                product = port_info.get('product', '') if show_version else ''
                
                color = Colors.GREEN if state == 'open' else Colors.RED
                version_str = f"{product} {version}".strip() if show_version else ''
                
                print(f"{color}{port:<10} {state:<12} {Colors.CYAN}{service:<20} {Colors.YELLOW}{version_str}{Colors.RESET}")
                
                results['ports'].append({
                    'port': port,
                    'protocol': proto,
                    'state': state,
                    'service': service,
                    'version': version_str
                })
                
                # Mostrar scripts si están disponibles
                if show_scripts and 'script' in port_info:
                    print(f"{Colors.MAGENTA}  Scripts:{Colors.RESET}")
                    for script_name, script_output in port_info['script'].items():
                        print(f"{Colors.YELLOW}    - {script_name}:{Colors.RESET}")
                        print(f"{Colors.WHITE}      {script_output[:200]}...{Colors.RESET}")
        
        self.results[f"scan_{target}_{int(time.time())}"] = results
        self.scan_history.append(results)
        
        return results
    
    def export_results(self, format_type='json'):
        """Exporta los resultados en el formato especificado"""
        if not self.results:
            print(f"{Colors.RED}[!] No hay resultados para exportar{Colors.RESET}")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type.lower() == 'json':
            filename = f"scan_results_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=4, ensure_ascii=False)
            print(f"{Colors.GREEN}[✓] Resultados exportados a {filename}{Colors.RESET}")
        
        elif format_type.lower() == 'csv':
            filename = f"scan_results_{timestamp}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Target', 'Port', 'Protocol', 'State', 'Service', 'Version'])
                
                for scan_key, scan_data in self.results.items():
                    if 'ports' in scan_data:
                        target = scan_data.get('target', 'N/A')
                        for port_info in scan_data['ports']:
                            writer.writerow([
                                target,
                                port_info.get('port', ''),
                                port_info.get('protocol', ''),
                                port_info.get('state', ''),
                                port_info.get('service', ''),
                                port_info.get('version', '')
                            ])
            print(f"{Colors.GREEN}[✓] Resultados exportados a {filename}{Colors.RESET}")
        
        elif format_type.lower() == 'html':
            filename = f"scan_results_{timestamp}.html"
            html_content = self._generate_html_report()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"{Colors.GREEN}[✓] Resultados exportados a {filename}{Colors.RESET}")
        
        else:
            print(f"{Colors.RED}[!] Formato no soportado: {format_type}{Colors.RESET}")
    
    def _generate_html_report(self):
        """Genera un reporte HTML de los resultados"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>PortScan - Reporte</title>
    <style>
        body {{ font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff00; padding: 20px; }}
        h1 {{ color: #00ff00; text-align: center; border-bottom: 2px solid #00ff00; }}
        h2 {{ color: #00ffff; margin-top: 30px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #003300; color: #00ff00; padding: 10px; text-align: left; }}
        td {{ border: 1px solid #004400; padding: 8px; }}
        tr:hover {{ background: #001100; }}
        .open {{ color: #00ff00; }}
        .closed {{ color: #ff0000; }}
        .filtered {{ color: #ffff00; }}
        .timestamp {{ color: #888; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>PortScan - Reporte de Escaneo</h1>
    <p class="timestamp">Generado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
"""
        
        for scan_key, scan_data in self.results.items():
            if 'ports' in scan_data:
                html += f"<h2>Escaneo: {scan_data.get('target', scan_key)}</h2>"
                html += f"<p class='timestamp'>Fecha: {scan_data.get('scan_time', 'N/A')}</p>"
                html += """
                <table>
                    <tr>
                        <th>Puerto</th>
                        <th>Protocolo</th>
                        <th>Estado</th>
                        <th>Servicio</th>
                        <th>Versión</th>
                    </tr>
                """
                
                for port_info in scan_data['ports']:
                    state_class = port_info.get('state', 'unknown')
                    html += f"""
                    <tr>
                        <td>{port_info.get('port', '')}</td>
                        <td>{port_info.get('protocol', '').upper()}</td>
                        <td class='{state_class}'>{state_class}</td>
                        <td>{port_info.get('service', '')}</td>
                        <td>{port_info.get('version', '')}</td>
                    </tr>
                    """
                
                html += "</table>"
        
        html += """
</body>
</html>
        """
        
        return html
    
    def show_scan_history(self):
        """Muestra el historial de escaneos"""
        if not self.scan_history:
            print(f"{Colors.YELLOW}[!] No hay escaneos en el historial{Colors.RESET}")
            return
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}Historial de Escaneos:{Colors.RESET}\n")
        
        for idx, scan in enumerate(self.scan_history, 1):
            target = scan.get('target', 'N/A')
            scan_time = scan.get('scan_time', 'N/A')
            num_ports = len(scan.get('ports', []))
            
            print(f"{Colors.CYAN}[{idx}]{Colors.WHITE} Target: {Colors.YELLOW}{target}{Colors.WHITE} | "
                  f"Tiempo: {Colors.YELLOW}{scan_time}{Colors.WHITE} | "
                  f"Puertos encontrados: {Colors.GREEN}{num_ports}{Colors.RESET}")
    
    def analyze_services(self):
        """Analiza los servicios detectados en todos los escaneos"""
        if not self.scan_history:
            print(f"{Colors.YELLOW}[!] No hay datos para analizar{Colors.RESET}")
            return
        
        service_count = {}
        port_count = {}
        
        for scan in self.scan_history:
            for port_info in scan.get('ports', []):
                service = port_info.get('service', 'unknown')
                port = port_info.get('port', 0)
                
                service_count[service] = service_count.get(service, 0) + 1
                port_count[port] = port_count.get(port, 0) + 1
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}Análisis de Servicios Detectados:{Colors.RESET}\n")
        
        print(f"{Colors.CYAN}{Colors.BOLD}Top 10 Servicios más comunes:{Colors.RESET}")
        for service, count in sorted(service_count.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"{Colors.WHITE}  {service:<20} {Colors.YELLOW}{count} ocurrencias{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}Top 10 Puertos más comunes:{Colors.RESET}")
        for port, count in sorted(port_count.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"{Colors.WHITE}  Puerto {port:<10} {Colors.YELLOW}{count} ocurrencias{Colors.RESET}")
    
    def pause(self):
        """Pausa la ejecución esperando input del usuario"""
        input(f"\n{Colors.GREEN}Presiona ENTER para continuar...{Colors.RESET}")
    
    def run(self):
        """Ejecuta el bucle principal del programa"""
        while True:
            self.print_banner()
            choice = self.print_menu()
            
            if choice == '0':
                print(f"\n{Colors.GREEN}¡Hasta luego!{Colors.RESET}")
                sys.exit(0)
            
            elif choice == '1':
                interface = input(f"\n{Colors.CYAN}Interfaz de red (dejar vacío para auto): {Colors.RESET}") or None
                self.discover_devices(interface)
                self.pause()
            
            elif choice == '2':
                target = input(f"\n{Colors.CYAN}IP objetivo: {Colors.RESET}")
                if target:
                    self.quick_scan(target)
                self.pause()
            
            elif choice == '3':
                target = input(f"\n{Colors.CYAN}IP objetivo: {Colors.RESET}")
                if target:
                    self.full_scan(target)
                self.pause()
            
            elif choice == '4':
                target = input(f"\n{Colors.CYAN}IP objetivo: {Colors.RESET}")
                ports = input(f"{Colors.CYAN}Puertos (ej: 80,443,8080 o 1-1000): {Colors.RESET}")
                if target and ports:
                    self.custom_port_scan(target, ports)
                self.pause()
            
            elif choice == '5':
                target = input(f"\n{Colors.CYAN}IP objetivo: {Colors.RESET}")
                if target:
                    self.service_version_scan(target)
                self.pause()
            
            elif choice == '6':
                target = input(f"\n{Colors.CYAN}IP objetivo: {Colors.RESET}")
                if target:
                    self.os_detection(target)
                self.pause()
            
            elif choice == '7':
                target = input(f"\n{Colors.CYAN}IP objetivo: {Colors.RESET}")
                if target:
                    self.vulnerability_scan(target)
                self.pause()
            
            elif choice == '8':
                target = input(f"\n{Colors.CYAN}IP objetivo: {Colors.RESET}")
                port = input(f"{Colors.CYAN}Puerto: {Colors.RESET}")
                if target and port:
                    self.banner_grabbing(target, port)
                self.pause()
            
            elif choice == '9':
                target = input(f"\n{Colors.CYAN}IP objetivo: {Colors.RESET}")
                if target:
                    self.stealth_scan(target)
                self.pause()
            
            elif choice == '10':
                target = input(f"\n{Colors.CYAN}IP objetivo: {Colors.RESET}")
                if target:
                    self.firewall_detection(target)
                self.pause()
            
            elif choice == '11':
                print(f"\n{Colors.CYAN}Formatos disponibles:{Colors.RESET}")
                print(f"{Colors.WHITE}  [1] JSON")
                print(f"{Colors.WHITE}  [2] CSV")
                print(f"{Colors.WHITE}  [3] HTML{Colors.RESET}")
                format_choice = input(f"{Colors.CYAN}Selecciona formato: {Colors.RESET}")
                
                formats = {'1': 'json', '2': 'csv', '3': 'html'}
                if format_choice in formats:
                    self.export_results(formats[format_choice])
                self.pause()
            
            elif choice == '12':
                self.show_scan_history()
                self.pause()
            
            elif choice == '13':
                self.analyze_services()
                self.pause()
            
            elif choice == '14':
                target = input(f"\n{Colors.CYAN}IP objetivo: {Colors.RESET}")
                if target:
                    self.traceroute(target)
                self.pause()
            
            else:
                print(f"{Colors.RED}[!] Opción no válida{Colors.RESET}")
                time.sleep(1)

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='PortScan - Herramienta avanzada de escaneo de redes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python portscan-script.py                    # Modo interactivo
  python portscan-script.py -t 192.168.1.1     # Escaneo rápido
  python portscan-script.py -t 192.168.1.1 -f  # Escaneo completo
        """
    )
    
    parser.add_argument('-t', '--target', help='IP o hostname objetivo')
    parser.add_argument('-f', '--full', action='store_true', help='Escaneo completo de puertos')
    parser.add_argument('-p', '--ports', help='Puertos a escanear (ej: 80,443 o 1-1000)')
    parser.add_argument('-s', '--service', action='store_true', help='Detectar servicios y versiones')
    parser.add_argument('-o', '--output', help='Archivo de salida (json/csv/html)')
    
    args = parser.parse_args()
    
    scanner = PortScanner()
    
    # Si se proporcionan argumentos, ejecutar en modo CLI
    if args.target:
        if args.full:
            scanner.full_scan(args.target)
        elif args.service:
            scanner.service_version_scan(args.target)
        elif args.ports:
            scanner.custom_port_scan(args.target, args.ports)
        else:
            scanner.quick_scan(args.target)
        
        if args.output:
            ext = args.output.split('.')[-1]
            scanner.export_results(ext)
    else:
        # Modo interactivo
        scanner.run()

if __name__ == "__main__":
    main()
