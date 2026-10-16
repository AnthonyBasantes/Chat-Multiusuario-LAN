import socket

HOST = "172.17.44.239"
PUERTO = 65432

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect((HOST, PUERTO))

print("Conectado correctamente al servidor")

cliente.close()