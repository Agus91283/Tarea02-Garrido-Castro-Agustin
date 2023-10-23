import subprocess
import getopt
import sys

# Base de datos local que almacena datos mac con su fabricante
basedatoslocal = {
    "b4:b5:fe:92:ff:c5": "Hewlett Packard",
    "98:06:3c:92:ff:c5": "Samsung Electronics Co.Ltd",
    "30:AE:A4:3F:12:77": "Apple",
    "AC:F7:F3:aa:aa:aa": "Xiaomi",
    "00:01:97:bb:bb:bb": "Cisco",
    "FF-FF-FF-FF-FF-FF": "Broadcast",
    
}

# Función para obtener los datos de fabricación de una tarjeta de red por IP
def obtener_datos_por_ip(ip):
    try:
        # Ejecutar el comando "arp -a" para obtener la tabla ARP
        arp_salida = subprocess.check_output(["arp", "-a"], universal_newlines=True)
        # Buscar la entrada correspondiente a la IP especificada
        for i in arp_salida.splitlines():
            if ip in i:
                # Dividir la línea en columnas y extraer la dirección MAC
                j1 = i.split()
                if len(j1) >= 2:
                    mac = j1[1]
                    print(f"IP: {ip}")
                    obtener_datos_por_mac(mac)
                    return
        print(f"Error : ip is outside the host network")
    except subprocess.CalledProcessError:
        print("Error al ejecutar el comando arp.")
    except Exception as e:
        print(f"Error: {str(e)}")

# Función para obtener los datos de fabricación de una tarjeta de red por MAC
def obtener_datos_por_mac(mac):
    fabricante = basedatoslocal.get(mac, "Desconocido")
    print(f"MAC: {mac},\n Fabricante: {fabricante}")

# Función para obtener la tabla ARP
def obtener_tabla_arp():
    try:
        # Ejecutar el comando "arp -a" para obtener la tabla ARP
        arp_salida = subprocess.check_output(["arp", "-a"], universal_newlines=True)
        # Imprimir la tabla ARP
        print(arp_salida)
    except subprocess.CalledProcessError:
        print("Error al ejecutar el comando arp.")
    except Exception as e:
        print(f"Error: {str(e)}")

def main(argv):
    ip = None
    mac = None

    try:
        opts, args = getopt.getopt(argv, "i:m:", ["ip=", "mac="])
    except getopt.GetoptError:
        print("Parametros:  --ip <IP> | --mac <MAC>")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-m", "--mac"):
            mac = arg

    if ip:
        obtener_datos_por_ip(ip)
    elif mac:
        obtener_datos_por_mac(mac)
    else:
        obtener_tabla_arp()

if __name__ == "__main__":
    main(sys.argv[1:])
