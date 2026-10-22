
import socket
import threading
import logging
from abc import ABC, abstractmethod

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class FormateadorMensaje(ABC):
    @abstractmethod
    def formatear(self, alias: str, mensaje: str) -> str:
        pass


class FormateadorChat(FormateadorMensaje):
    def formatear(self, alias: str, mensaje: str) -> str:
        return f"[{alias}]: {mensaje}"


class GestorClientes:
    def __init__(self):
        self._clientes = {}
        self._bloqueo = threading.Lock()

    def agregar(self, conexion, alias, direccion):
        with self._bloqueo:
            self._clientes[conexion] = {
                "alias": alias,
                "direccion": direccion,
                "bloqueo_envio": threading.Lock()
            }

    def eliminar(self, conexion):
        with self._bloqueo:
            return self._clientes.pop(conexion, None)

    def difundir(self, mensaje, remitente=None):
        with self._bloqueo:
            clientes = list(self._clientes.items())

        for conexion, datos in clientes:
            if conexion == remitente:
                continue

            try:
                with datos["bloqueo_envio"]:
                    conexion.sendall(
                        (mensaje + "\n").encode("utf-8")
                    )
            except OSError:
                logging.warning(
                    "Error al enviar a %s:%s",
                    *datos["direccion"]
                )
                self.desconectar(conexion)

    def desconectar(self, conexion):
        datos = self.eliminar(conexion)

        if datos is None:
            return

        try:
            conexion.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        conexion.close()

        ip, puerto = datos["direccion"]

        logging.info(
            "Cliente desconectado: %s | IP: %s | Puerto: %s",
            datos["alias"], ip, puerto
        )

        self.difundir(
            f"{datos['alias']} se ha desconectado del chat"
        )

    def cerrar_todos(self):
        with self._bloqueo:
            conexiones = list(self._clientes.keys())

        for conexion in conexiones:
            self.desconectar(conexion)


class ManejadorCliente:
    def __init__(
        self, conexion, direccion, formateador, gestor
    ):
        self._conexion = conexion
        self._direccion = direccion
        self._formateador = formateador
        self._gestor = gestor

    def procesar(self):
        try:
            with self._conexion:
                with self._conexion.makefile(
                    "r", encoding="utf-8"
                ) as lector:

                    alias = lector.readline().strip()

                    if not alias:
                        return

                    alias = alias[:30]

                    self._gestor.agregar(
                        self._conexion,
                        alias,
                        self._direccion
                    )

                    ip, puerto = self._direccion

                    logging.info(
                        "Cliente conectado: %s | IP: %s | Puerto: %s",
                        alias, ip, puerto
                    )

                    self._gestor.difundir(
                        f"{alias} se ha conectado al chat",
                        self._conexion
                    )

                    while True:
                        mensaje = lector.readline()

                        if not mensaje:
                            break

                        mensaje = mensaje.strip()

                        if not mensaje:
                            continue

                        texto = self._formateador.formatear(
                            alias, mensaje
                        )

                        logging.info(texto)

                        self._gestor.difundir(
                            texto,
                            self._conexion
                        )

        except (OSError, UnicodeError) as error:
            logging.warning(
                "Error con %s:%s: %s",
                *self._direccion, error
            )

        finally:
            self._gestor.desconectar(self._conexion)


class ServidorChat:
    def __init__(self, direccion_ip, puerto, formateador):
        self._direccion_ip = direccion_ip
        self._puerto = puerto
        self._formateador = formateador
        self._gestor = GestorClientes()

    def iniciar(self):
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as servidor:

            servidor.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1
            )

            servidor.bind(
                (self._direccion_ip, self._puerto)
            )

            servidor.listen()

            logging.info(
                "Servidor iniciado en %s:%s",
                self._direccion_ip, self._puerto
            )

            logging.info("Esperando conexiones...")

            try:
                while True:
                    conexion, direccion = servidor.accept()

                    manejador = ManejadorCliente(
                        conexion,
                        direccion,
                        self._formateador,
                        self._gestor
                    )

                    hilo = threading.Thread(
                        target=manejador.procesar,
                        daemon=True
                    )

                    hilo.start()

            except KeyboardInterrupt:
                logging.info(
                    "Servidor detenido por el usuario"
                )

            except OSError as error:
                logging.error(
                    "Error del servidor: %s", error
                )

            finally:
                self._gestor.cerrar_todos()
                logging.info("Servidor finalizado")


if __name__ == "__main__":
    DIRECCION_IP = "0.0.0.0"
    PUERTO = 65432

    servidor = ServidorChat(
        DIRECCION_IP,
        PUERTO,
        FormateadorChat()
    )

    servidor.iniciar()
