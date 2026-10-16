import socket

HOST = "0.0.0.0"
PUERTO = 65432

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind((HOST, PUERTO))

servidor.listen()

print("Servidor iniciado correctamente")
print("Esperando conexiones...")

cliente, direccion = servidor.accept()

print("Cliente conectado desde:", direccion)