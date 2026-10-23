# Sistema de Chat Multiusuario en Red LAN por Consola

## 1. Descripción del proyecto

Este proyecto consiste en el desarrollo de un sistema de chat multiusuario utilizando Python y sockets TCP, que permite la comunicación en tiempo real entre diferentes computadoras conectadas a una misma red local (LAN).

El sistema implementa programación concurrente mediante hilos (`threading`), permitiendo que múltiples clientes se conecten simultáneamente, envíen mensajes y reciban información de otros participantes sin esperar una respuesta individual del servidor.

## 2. Integrantes y responsabilidades

- **Anthony Basantes:** Líder del equipo y desarrollador del servidor TCP, encargado de la administración de conexiones y difusión de mensajes.
- **Steven Panchi:** Desarrollador del cliente concurrente, responsable del envío y recepción simultánea de mensajes.
- **Daniel Lara:** Responsable de las pruebas de funcionamiento, verificación de conexiones LAN y documentación de evidencias.

## 3. Tecnologías utilizadas

- Python 3
- Sockets TCP
- Threading
- Programación orientada a objetos
- Principios SOLID y Clean Code
- Git y GitHub
- Ubuntu y VSCodium

## 4. Funcionalidades implementadas

- Comunicación entre múltiples computadoras conectadas a una red LAN.
- Conexión simultánea de varios clientes.
- Identificación de usuarios mediante alias.
- Envío y recepción concurrente de mensajes.
- Difusión de mensajes mediante broadcast.
- Registro dinámico de clientes conectados.
- Registro de direcciones IP y puertos al conectar y desconectar usuarios.
- Manejo de excepciones ante errores de conexión.
- Desconexión voluntaria mediante el comando `/salir`.
- Separación de responsabilidades mediante clases y métodos.

## 5. Estructura del proyecto

```text
Chat-Multiusuario-LAN/
├── servidor.py
├── cliente.py
├── prueba_cliente.py
└── README.md
```

**Descripción de los archivos:**

- `servidor.py`: administra las conexiones TCP, registra los clientes y distribuye los mensajes.
- `cliente.py`: permite a los usuarios conectarse al servidor, enviar mensajes y recibirlos simultáneamente.
- `prueba_cliente.py`: cliente utilizado para comprobar la comunicación y realizar pruebas del sistema.
- `README.md`: contiene la documentación técnica e instrucciones de ejecución.

## 6. Requisitos de ejecución

- Tener instalado Python 3.
- Disponer de una computadora para ejecutar el servidor.
- Contar con una o más computadoras cliente.
- Mantener los equipos conectados a la misma red LAN.
- Conocer la dirección IP local del servidor.
- Permitir las conexiones TCP al puerto `65432`.

## 7. Instrucciones de ejecución

### Paso 1. Iniciar el servidor

Abrir una terminal en la carpeta del proyecto y ejecutar:

```bash
python3 servidor.py
```

En Windows también puede utilizarse:

```bash
python servidor.py
```

El servidor escuchará en la dirección `0.0.0.0` y utilizará el puerto `65432`, permitiendo conexiones desde otros equipos de la red local.

### Paso 2. Identificar la IP del servidor

En Ubuntu ejecutar:

```bash
hostname -I
```

En Windows ejecutar:

```cmd
ipconfig
```

Identificar la dirección IPv4 correspondiente a la red LAN.

### Paso 3. Ejecutar el primer cliente

En otra computadora abrir una terminal y ejecutar:

```bash
python3 cliente.py
```

El programa solicitará:

```text
Ingrese la IP del servidor:
Ingrese su alias:
```

Introducir la dirección IP del servidor y un nombre de usuario.

### Paso 4. Ejecutar el segundo cliente

En otra terminal o computadora ejecutar:

```bash
python3 prueba_cliente.py
```

Ingresar la misma IP del servidor y un alias diferente.

### Paso 5. Enviar mensajes

Los usuarios podrán escribir mensajes desde sus terminales. El servidor los distribuirá automáticamente a los demás clientes conectados.

Ejemplo:

```text
[Steven]: Hola, ¿cómo están?
[Daniel]: Hola Steven, el chat funciona correctamente.
```

Para salir del chat escribir:

```text
/salir
```

## 8. Implementación de concurrencia

El sistema utiliza el módulo `threading` de Python para permitir la ejecución concurrente.

**En el servidor:** cada conexión entrante es atendida por un hilo independiente. Esto permite mantener varios clientes conectados simultáneamente sin que las operaciones de recepción de uno bloqueen a los demás.

**En el cliente:** se utiliza un hilo secundario para recibir mensajes mientras el hilo principal permite escribir y enviar información.

Además, el servidor utiliza mecanismos de sincronización para proteger el registro de clientes y coordinar operaciones de envío.

## 9. Aplicación de los principios SOLID y Clean Code

### Principio de responsabilidad única (SRP)

El servidor organiza sus funcionalidades en clases con responsabilidades diferenciadas:

- `GestorClientes`: administra las conexiones y la difusión de mensajes.
- `ManejadorCliente`: procesa los mensajes de cada cliente.
- `FormateadorChat`: define la presentación de los mensajes.
- `ServidorChat`: inicia el servidor y acepta nuevas conexiones.

### Principio abierto/cerrado (OCP)

El sistema utiliza una abstracción denominada `FormateadorMensaje`, que permite incorporar nuevos formateadores sin modificar la lógica principal de recepción y difusión de mensajes.

### Principio de sustitución de Liskov (LSP)

La clase `FormateadorChat` implementa el contrato definido por `FormateadorMensaje`, por lo que puede utilizarse donde se requiera dicha abstracción.

### Principio de segregación de interfaces (ISP)

La abstracción de formateo define únicamente la operación necesaria para transformar los mensajes, evitando exigir métodos adicionales a sus implementaciones.

### Principio de inversión de dependencias (DIP)

El servidor recibe un objeto formateador como dependencia, en lugar de crear directamente una implementación concreta dentro de su lógica de procesamiento.

### Buenas prácticas de Clean Code

- Nombres de clases, métodos y variables descriptivos en español.
- Separación de responsabilidades.
- Reutilización de métodos.
- Manejo de excepciones.
- Registro de eventos mediante `logging`.
- Organización modular y código legible.

## 10. Manejo de excepciones

El sistema contempla errores de comunicación y desconexiones inesperadas.

Cuando un cliente se desconecta, el servidor intenta liberar los recursos asociados, actualizar el registro de conexiones y notificar a los participantes restantes.

Se utilizan bloques `try`, `except` y `finally` para controlar situaciones como errores de red, cierre de conexiones y finalización del servidor.

## 11. Control de versiones y trabajo colaborativo

El proyecto se desarrolló mediante Git y GitHub, utilizando ramas independientes para organizar las responsabilidades:

- `anthony-servidor`
- `steven-cliente`
- `daniel-pruebas`
- `main`
- `correcciones-finales`

La rama `main` conserva la integración original del trabajo grupal y su historial de desarrollo.

La rama `correcciones-finales` contiene las mejoras de calidad de código, nombres en español y manejo de conexiones realizadas para la entrega definitiva.

## 12. Evidencias de funcionamiento

Se realizaron pruebas de comunicación entre computadoras conectadas a una red LAN, verificando el envío y recepción de mensajes entre diferentes participantes.

Las capturas del funcionamiento y del historial de GitHub se incluyen en la documentación del proyecto.

**Nota:** las capturas originales corresponden a las pruebas efectuadas en el laboratorio. La versión de la rama `correcciones-finales` requiere su propia verificación de funcionamiento.

## 13. Conclusión

Mediante el desarrollo de este proyecto logramos comprender el funcionamiento de la comunicación TCP en sistemas distribuidos, implementar programación concurrente y aplicar conceptos de programación orientada a objetos.

Aprendimos a gestionar conexiones simultáneas, implementar mecanismos de difusión de mensajes y organizar el código mediante responsabilidades separadas.

Finalmente, fortalecimos nuestras habilidades de trabajo colaborativo utilizando Git y GitHub para documentar las contribuciones de cada integrante y mantener un historial de desarrollo del proyecto.

## 14. Enlace de entrega

**Repositorio:** https://github.com/AnthonyBasantes/Chat-Multiusuario-LAN

**Rama de entrega:** `correcciones-finales`

**Enlace directo:** https://github.com/AnthonyBasantes/Chat-Multiusuario-LAN/tree/correcciones-finales
