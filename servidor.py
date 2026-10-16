import socket
import threading
import logging
from abc import ABC, abstractmethod

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class MessageHandler(ABC):

    @abstractmethod
    def handle(self, alias: str, message: str) -> str:
        pass


class ChatMessageHandler(MessageHandler):

    def handle(self, alias: str, message: str) -> str:
        return f"{alias}: {message}"


class ClientManager:

    def __init__(self):
        self._clients = {}
        self._lock = threading.Lock()

    def add_client(self, client_socket, alias):
        with self._lock:
            self._clients[client_socket] = alias

    def remove_client(self, client_socket):
        with self._lock:
            self._clients.pop(client_socket, None)

    def broadcast(self, message, sender=None):
        with self._lock:
            clients = list(self._clients.keys())

        for client in clients:
            if client != sender:
                try:
                    client.sendall((message + "\n").encode("utf-8"))
                except OSError:
                    logging.warning("Error al enviar mensaje")


class ClientHandler:

    def __init__(self, client_socket, address, message_handler, client_manager):
        self._client_socket = client_socket
        self._address = address
        self._message_handler = message_handler
        self._client_manager = client_manager

    def process(self):
        alias = None

        try:
            with self._client_socket:
                reader = self._client_socket.makefile(
                    "r", encoding="utf-8"
                )

                alias = reader.readline().strip()

                if not alias:
                    return

                self._client_manager.add_client(
                    self._client_socket, alias
                )

                logging.info(
                    f"Cliente conectado: {alias} | "
                    f"IP: {self._address[0]} | "
                    f"Puerto: {self._address[1]}"
                )

                self._client_manager.broadcast(
                    f"{alias} se ha conectado al chat",
                    self._client_socket
                )

                while True:
                    message = reader.readline()

                    if not message:
                        break

                    message = message.strip()

                    if not message:
                        continue

                    formatted_message = self._message_handler.handle(
                        alias, message
                    )

                    logging.info(formatted_message)

                    self._client_manager.broadcast(
                        formatted_message,
                        self._client_socket
                    )

        except (OSError, UnicodeError) as error:
            logging.error(f"Error con {self._address}: {error}")

        finally:
            self._client_manager.remove_client(
                self._client_socket
            )

            if alias:
                logging.info(f"Cliente desconectado: {alias}")

                self._client_manager.broadcast(
                    f"{alias} se ha desconectado del chat"
                )


class ThreadedSocketServer:

    def __init__(self, host, port, message_handler):
        self._host = host
        self._port = port
        self._message_handler = message_handler
        self._client_manager = ClientManager()

        self._server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )

        self._server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

    def start(self):
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen()

        logging.info(
            f"Servidor iniciado en {self._host}:{self._port}"
        )
        logging.info("Esperando conexiones...")

        try:
            while True:
                client_socket, address = self._server_socket.accept()

                handler = ClientHandler(
                    client_socket,
                    address,
                    self._message_handler,
                    self._client_manager
                )

                thread = threading.Thread(
                    target=handler.process,
                    daemon=True
                )

                thread.start()

        except KeyboardInterrupt:
            logging.info("Servidor detenido por el usuario")

        finally:
            self._server_socket.close()


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 65432

    handler = ChatMessageHandler()
    server = ThreadedSocketServer(HOST, PORT, handler)

    server.start()