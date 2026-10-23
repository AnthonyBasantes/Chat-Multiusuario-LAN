
import socket
import threading
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class ClienteChat:
    def __init__(self, direccion_ip: str, puerto: int):
        self._direccion_ip = direccion_ip
        self._puerto = puerto

        self._conexion = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self._conectado = threading.Event()

    def conectar(self, alias: str):
        self._conexion.connect(
            (self._direccion_ip, self._puerto)
        )

        self._conexion.sendall(
            (alias + "\n").encode("utf-8")
        )

        self._conectado.set()

        logging.info(
            "Conectado al servidor como %s",
            alias
        )

        hilo = threading.Thread(
            target=self.recibir_mensajes,
            daemon=True
        )

        hilo.start()

    def recibir_mensajes(self):
        try:
            with self._conexion.makefile(
                "r", encoding="utf-8"
            ) as lector:

                while self._conectado.is_set():
                    mensaje = lector.readline()

                    if not mensaje:
                        print(
                            "\nEl servidor cerró la conexión."
                        )
                        break

                    print(
                        f"\n{mensaje.strip()}",
                        flush=True
                    )

        except (OSError, UnicodeError) as error:
            if self._conectado.is_set():
                logging.warning(
                    "Error al recibir mensajes: %s",
                    error
                )

        finally:
            self._conectado.clear()

    def enviar_mensajes(self):
        try:
            while self._conectado.is_set():
                mensaje = input()

                if not self._conectado.is_set():
                    break

                if mensaje.strip().lower() == "/salir":
                    break

                if mensaje.strip():
                    self._conexion.sendall(
                        (mensaje + "\n").encode("utf-8")
                    )

        except (OSError, EOFError, KeyboardInterrupt):
            logging.info("Finalizando cliente")

        finally:
            self.desconectar()

    def desconectar(self):
        self._conectado.clear()

        try:
            self._conexion.shutdown(
                socket.SHUT_RDWR
            )
        except OSError:
            pass

        self._conexion.close()

        logging.info("Cliente desconectado")


if __name__ == "__main__":
    PUERTO = 65432

    direccion_ip = input(
        "Ingrese la IP del servidor: "
    ).strip()

    alias = input(
        "Ingrese su alias: "
    ).strip()

    if not direccion_ip or not alias:
        print(
            "La IP y el alias son obligatorios."
        )
    else:
        cliente = ClienteChat(
            direccion_ip,
            PUERTO
        )

        try:
            cliente.conectar(alias)

            print("Escriba sus mensajes.")
            print(
                "Escriba /salir para desconectarse."
            )

            cliente.enviar_mensajes()

        except OSError as error:
            logging.error(
                "No se pudo conectar: %s",
                error
            )

            cliente.desconectar()
