import socket
import threading
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class SocketClient:

    def __init__(self, host: str, port: int):

        self._host = host
        self._port = port

        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self._connected = False

    def connect(self, alias: str):

        self._socket.connect(
            (self._host, self._port)
        )

        self._connected = True

        self._socket.sendall(
            (alias + "\n").encode("utf-8")
        )

        logging.info(
            f"Conectado al servidor como {alias}"
        )

        thread = threading.Thread(
            target=self.receive_messages,
            daemon=True
        )

        thread.start()

    def receive_messages(self):

        try:
            reader = self._socket.makefile(
                "r",
                encoding="utf-8"
            )

            while self._connected:

                message = reader.readline()

                if not message:
                    break

                print(f"\n{message.strip()}")

        except (OSError, UnicodeError) as error:
            if self._connected:
                logging.error(
                    f"Error al recibir mensajes: {error}"
                )

        finally:
            self._connected = False

    def send_messages(self):

        try:
            while self._connected:

                message = input()

                if message.lower() == "/salir":
                    break

                if message.strip():

                    self._socket.sendall(
                        (message + "\n").encode("utf-8")
                    )

        except (OSError, EOFError, KeyboardInterrupt):
            logging.info("Finalizando cliente")

        finally:
            self.disconnect()

    def disconnect(self):

        self._connected = False

        try:
            self._socket.shutdown(
                socket.SHUT_RDWR
            )
        except OSError:
            pass

        self._socket.close()

        logging.info("Desconectado del servidor")


if __name__ == "__main__":

    HOST = "172.17.44.239"
    PORT = 65432

    alias = input("Ingrese su alias: ").strip()

    if not alias:
        print("El alias no puede estar vacío")
    else:
        client = SocketClient(
            HOST,
            PORT
        )

        try:
            client.connect(alias)

            print("Escriba sus mensajes")
            print("Escriba /salir para desconectarse")

            client.send_messages()

        except OSError as error:
            logging.error(
                f"No se pudo establecer la conexión: {error}"
            )
            client.disconnect()