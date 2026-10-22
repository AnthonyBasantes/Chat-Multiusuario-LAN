# Sistema de Chat Multiusuario en Red LAN por Consola

## Descripción del proyecto

Este proyecto consiste en el desarrollo de un sistema de chat multiusuario mediante Python y sockets TCP, que permite la comunicación entre diferentes computadoras conectadas a una misma red LAN.

El sistema utiliza programación concurrente para gestionar múltiples conexiones y permitir el envío y recepción de mensajes.

## Integrantes

- Anthony Basantes — Líder y desarrollador del servidor.
- Steven Panchi — Desarrollador del cliente.
- Daniel Lara — Responsable de pruebas y documentación.

## Tecnologías utilizadas

- Python 3
- Sockets TCP
- Threading
- Git y GitHub
- Ubuntu
- VSCodium

## Funcionalidades

- Comunicación entre computadoras de una red LAN.
- Conexión simultánea de múltiples clientes.
- Identificación de usuarios mediante alias.
- Envío y recepción de mensajes.
- Difusión de mensajes mediante broadcast.
- Registro de conexiones en el servidor.
- Programación concurrente mediante hilos.

## Estructura del proyecto

```text
Chat-Multiusuario-LAN/
├── servidor.py
├── cliente.py
├── prueba_cliente.py
└── README.md
```

## Requisitos

- Python 3 instalado.
- Computadoras conectadas a una misma red LAN.
- Dirección IP del equipo que ejecuta el servidor.
- Puerto TCP disponible.

## Ejecución del servidor

Abrir una terminal en la carpeta del proyecto y ejecutar:

```bash
python3 servidor.py
```

El servidor utiliza el puerto `65432` y escucha las conexiones mediante la dirección `0.0.0.0`.

## Ejecución de los clientes

Configurar en los archivos del cliente la dirección IP correspondiente a la computadora donde se ejecuta el servidor.

Después ejecutar:

```bash
python3 cliente.py
```

En otra computadora:

```bash
python3 prueba_cliente.py
```

En Windows, se puede utilizar `python` en lugar de `python3`, dependiendo de la instalación.

## Funcionamiento

1. El servidor inicia y espera conexiones TCP.
2. Los clientes se conectan utilizando la dirección IP y el puerto del servidor.
3. Cada cliente ingresa un alias.
4. Los usuarios pueden enviar mensajes desde sus respectivas terminales.
5. El servidor recibe los mensajes y los distribuye a los demás clientes conectados.

## Concurrencia

El servidor utiliza hilos para atender múltiples conexiones. Los clientes utilizan ejecución concurrente para recibir mensajes mientras el usuario escribe.

## Organización del código

El proyecto utiliza clases para separar responsabilidades relacionadas con la comunicación, administración de clientes y procesamiento de mensajes.

Se buscó aplicar principios SOLID y buenas prácticas de programación para facilitar el mantenimiento y la comprensión del código.

## Control de versiones

El proyecto se desarrolló utilizando GitHub y ramas independientes:

- `anthony-servidor`
- `steven-cliente`
- `daniel-pruebas`

## Evidencias

Las capturas del funcionamiento del sistema y del historial de GitHub se incluyen en la documentación de entrega.

## Conclusión

El proyecto permitió aplicar conceptos de sistemas distribuidos, programación concurrente, comunicación TCP y trabajo colaborativo mediante herramientas de control de versiones.
