import re

def validar_ip(ip):
    # Expresión regular para validar una dirección IP
    patron = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    
    # Usamos re.fullmatch para asegurarnos que la IP es completamente válida
    if re.fullmatch(patron, ip):
        return True
    return False

def cargar_ips_desde_archivo(archivo):
    # Lista para almacenar las IPs válidas y no válidas
    ips_validas = set()  # Usamos un set para eliminar duplicados automáticamente
    ips_no_validas = []

    try:
        # Abrimos el archivo y leemos línea por línea
        with open(archivo, 'r') as file:
            for linea in file:
                # Limpiamos la línea de posibles saltos de línea u espacios extra
                ip = linea.strip()
                
                # Validamos la dirección IP
                if validar_ip(ip):
                    ips_validas.add(ip)  # Añadimos la IP al set (elimina duplicados automáticamente)
                else:
                    ips_no_validas.append(ip)

    except FileNotFoundError:
        print(f"El archivo '{archivo}' no se encontró.")
        return [], []

    return list(ips_validas), ips_no_validas  # Convertimos el set de nuevo a lista

def generar_configuracion(ips_validas):
    # Generar la configuración de firewall con las IPs válidas
    config = "-> COMANDO CLI PARA CREAR DIRECCIONES <-\n"
    for ip in ips_validas:
        config += f"""
config firewall address
edit "{ip}"
set subnet {ip}/32
next
end
"""
    return config

def generar_configuracion_addrgrp(ips_validas):
    # Generar la configuración de addrgrp con las IPs válidas
    addrgrp_config = "-> COMANDO CLI PARA AGREGAR DIRECCIONES A GRUPO BLACKLIST <-\n"
    addrgrp_config += "config firewall addrgrp\nedit \"Blacklist9\"\n"
    for ip in ips_validas:
        addrgrp_config += f'append member "{ip}"\n'
    addrgrp_config += "next\nend\n"
    return addrgrp_config

# Nombre del archivo con las IPs
archivo_ips = 'ips.txt'

# Cargar y validar las IPs desde el archivo
ips_validas, ips_no_validas = cargar_ips_desde_archivo(archivo_ips)

# Mostrar los resultados
if ips_validas:
    # Generamos la configuración con las IPs válidas
    configuracion = generar_configuracion(ips_validas)
    print(configuracion)
    
    # Generamos la configuración para addrgrp
    addrgrp_config = generar_configuracion_addrgrp(ips_validas)
    print(addrgrp_config)

if ips_no_validas:
    print("\nDirecciones IP no válidas:")
    for ip in ips_no_validas:
        print(ip)
