import netifaces


def get_wlan0_ip():
    # Obtiene la información de la interfaz wlan0
    interface = netifaces.ifaddresses('wlan0')[netifaces.AF_INET]

    # Obtiene la dirección IP de la interfaz
    ip_address = interface[0]['addr']

    return ip_address


ip_address = get_wlan0_ip()
print(ip_address)
