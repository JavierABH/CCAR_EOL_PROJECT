from tcppinglib import tcpping
print(tcpping('192.168.163.137', 5555, 1, 1).is_alive)

import threading
from ping3 import ping

# Variable de bandera para indicar si se ha encontrado una IP que responde
ip_encontrada = None
lock = threading.Lock()  # Bloqueo para evitar condiciones de carrera

def ping_ip(ip):
    global ip_encontrada

    result = ping(ip)
    with lock:
        if result is not None and ip_encontrada is None:
            print(f"IP {ip} responde. Primera IP que responde: {ip}")
            ip_encontrada = ip

def main():
    # Definir el rango de direcciones IP
    # start_ip = "192.168.17.101"
    # end_ip = "192.168.17.250"
    start_ip = "10.220.48.221"
    end_ip = "10.220.48.224"

    # Crear una lista para almacenar los hilos
    threads = []

    # Iterar a través de las direcciones IP y crear un hilo para cada una
    for i in range(int(start_ip.split('.')[-1]), int(end_ip.split('.')[-1])+1):
        ip = f"192.168.17.{i}"
        thread = threading.Thread(target=ping_ip, args=(ip,))
        threads.append(thread)
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

    # Imprimir la IP encontrada (si hay alguna)
    if ip_encontrada is not None:
        print(f"La primera IP que responde es: {ip_encontrada}")
    else:
        print("Ninguna IP responde.")

if __name__ == "__main__":
    main()
