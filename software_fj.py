
from abc import ABC, abstractmethod
from datetime import datetime
import logging

# ==================================================
# CONFIGURACION DEL ARCHIVO DE REGISTRO
# ==================================================

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# ==================================================
# EXCEPCIONES PERSONALIZADAS
# ==================================================

class ErrorSistema(Exception):
    pass


class DatosInvalidos(ErrorSistema):
    pass


class ServicioNoDisponible(ErrorSistema):
    pass


class ReservaIncorrecta(ErrorSistema):
    pass


# ==================================================
# CLASE ABSTRACTA ENTIDAD
# ==================================================

class Entidad(ABC):

    def __init__(self, identificacion):
        if not isinstance(identificacion, str) or not identificacion.strip():
            raise DatosInvalidos("La identificacion es obligatoria.")

        self._identificacion = identificacion.strip()

    @property
    def identificacion(self):
        return self._identificacion

    @abstractmethod
    def mostrar_informacion(self):
        pass


# ==================================================
# CLASE CLIENTE
# ==================================================

class Cliente(Entidad):

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidos("El nombre no puede estar vacio.")

        if not isinstance(correo, str) or "@" not in correo or "." not in correo:
            raise DatosInvalidos("El correo electronico no es valido.")

        if not isinstance(telefono, str) or not telefono.isdigit() or len(telefono) < 7:
            raise DatosInvalidos("El telefono no es valido.")

        self._nombre = nombre.strip()
        self._correo = correo.strip()
        self._telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    def mostrar_informacion(self):
        return (
            f"Cliente: {self._nombre} | "
            f"Identificacion: {self.identificacion} | "
            f"Correo: {self._correo} | "
            f"Telefono: {self._telefono}"
        )


# ==================================================
# CLASE ABSTRACTA SERVICIO
# ==================================================

class Servicio(ABC):

    def __init__(self, codigo, nombre, precio_base):

        if not isinstance(codigo, str) or not codigo.strip():
            raise DatosInvalidos("El codigo es obligatorio.")

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidos("El nombre es obligatorio.")

        if isinstance(precio_base, bool) or not isinstance(precio_base, (int, float)):
            raise DatosInvalidos("El precio debe ser numerico.")

        if precio_base <= 0:
            raise DatosInvalidos("El precio debe ser mayor que cero.")

        self.codigo = codigo.strip()
        self.nombre = nombre.strip()
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass


# ==================================================
# FUNCIONES DE VALIDACION DE COSTOS
# ==================================================

def validar_costos(impuesto, descuento):

    if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
        raise DatosInvalidos("El impuesto debe ser numerico.")

    if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
        raise DatosInvalidos("El descuento debe ser numerico.")

    if not 0 <= impuesto <= 100:
        raise DatosInvalidos("El impuesto debe estar entre 0 y 100.")

    if not 0 <= descuento <= 100:
        raise DatosInvalidos("El descuento debe estar entre 0 y 100.")


# ==================================================
# SERVICIO 1: RESERVA DE SALAS
# ==================================================

class ReservaSala(Servicio):

    def validar_parametros(self, duracion):

        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise DatosInvalidos("La duracion debe ser numerica.")

        if duracion <= 0:
            raise DatosInvalidos("La duracion debe ser positiva.")

    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        self.validar_parametros(duracion)
        validar_costos(impuesto, descuento)

        subtotal = self.precio_base * duracion
        total = subtotal + (subtotal * impuesto / 100)
        total = total - (total * descuento / 100)

        return round(total, 2)

    def describir_servicio(self):
        return "Reserva de salas para reuniones y eventos."


# ==================================================
# SERVICIO 2: ALQUILER DE EQUIPOS
# ==================================================

class AlquilerEquipo(Servicio):

    def validar_parametros(self, duracion):

        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise DatosInvalidos("La duracion debe ser numerica.")

        if duracion <= 0:
            raise DatosInvalidos("La duracion debe ser positiva.")

    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        self.validar_parametros(duracion)
        validar_costos(impuesto, descuento)

        subtotal = self.precio_base * duracion
        total = subtotal + (subtotal * impuesto / 100)
        total = total - (total * descuento / 100)

        return round(total, 2)

    def describir_servicio(self):
        return "Alquiler de equipos tecnologicos."


# ==================================================
# SERVICIO 3: ASESORIAS ESPECIALIZADAS
# ==================================================

class Asesoria(Servicio):

    def validar_parametros(self, duracion):

        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise DatosInvalidos("La duracion debe ser numerica.")

        if duracion <= 0:
            raise DatosInvalidos("La duracion debe ser positiva.")

    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        self.validar_parametros(duracion)
        validar_costos(impuesto, descuento)

        subtotal = self.precio_base * duracion
        total = subtotal + (subtotal * impuesto / 100)
        total = total - (total * descuento / 100)

        return round(total, 2)

    def describir_servicio(self):
        return "Asesorias especializadas en tecnologia y sistemas."


# ==================================================
# CLASE RESERVA
# ==================================================

class Reserva(Entidad):

    def __init__(self, codigo, cliente, servicio, duracion):

        super().__init__(codigo)

        if not isinstance(cliente, Cliente):
            raise ReservaIncorrecta("Debe ingresar un cliente valido.")

        if not isinstance(servicio, Servicio):
            raise ReservaIncorrecta("Debe ingresar un servicio valido.")

        servicio.validar_parametros(duracion)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Calculo con impuesto y descuento opcionales
    def procesar(self, impuesto=0, descuento=0):

        try:
            if self.estado not in ("Pendiente", "Confirmada"):
                raise ReservaIncorrecta(
                    "La reserva no puede procesarse en su estado actual."
                )

            costo = self.servicio.calcular_costo(
                self.duracion, impuesto, descuento
            )

            self.estado = "Procesada"

            logging.info(
                f"Reserva {self.identificacion} procesada. Total: {costo}"
            )

            return costo

        except ErrorSistema as error:
            logging.error(f"Error al procesar reserva: {error}")
            raise

    def confirmar(self):

        if self.estado != "Pendiente":
            raise ReservaIncorrecta(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.estado = "Confirmada"
        logging.info(f"Reserva {self.identificacion} confirmada.")

    def cancelar(self):

        if self.estado in ("Procesada", "Cancelada"):
            raise ReservaIncorrecta(
                "No se puede cancelar esta reserva."
            )

        self.estado = "Cancelada"
        logging.info(f"Reserva {self.identificacion} cancelada.")

    def mostrar_informacion(self):

        return (
            f"Reserva: {self.identificacion}\n"
            f"Cliente: {self.cliente.nombre}\n"
            f"Servicio: {self.servicio.nombre}\n"
            f"Duracion: {self.duracion}\n"
            f"Estado: {self.estado}\n"
            f"Fecha: {self.fecha}"
        )


# ==================================================
# CLASE PRINCIPAL DEL SISTEMA
# ==================================================

class SistemaSoftwareFJ:

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):

        try:
            if not isinstance(cliente, Cliente):
                raise DatosInvalidos("El cliente no es valido.")

            for existente in self.clientes:
                if existente.identificacion == cliente.identificacion:
                    raise DatosInvalidos("El cliente ya esta registrado.")

            self.clientes.append(cliente)

            logging.info(f"Cliente registrado: {cliente.nombre}")
            print("Cliente registrado correctamente.")

        except ErrorSistema as error:
            logging.error(f"Error al registrar cliente: {error}")
            print("Error:", error)

    def registrar_servicio(self, servicio):

        try:
            if not isinstance(servicio, Servicio):
                raise DatosInvalidos("El servicio no es valido.")

            for existente in self.servicios:
                if existente.codigo == servicio.codigo:
                    raise DatosInvalidos("El servicio ya existe.")

            self.servicios.append(servicio)

            logging.info(f"Servicio registrado: {servicio.nombre}")
            print("Servicio registrado correctamente.")

        except ErrorSistema as error:
            logging.error(f"Error al registrar servicio: {error}")
            print("Error:", error)

    def crear_reserva(self, codigo, cliente, servicio, duracion):

        try:
            if cliente not in self.clientes:
                raise ReservaIncorrecta("El cliente no esta registrado.")

            if servicio not in self.servicios:
                raise ServicioNoDisponible("El servicio no esta registrado.")

            for reserva in self.reservas:
                if reserva.identificacion == codigo:
                    raise ReservaIncorrecta("El codigo ya existe.")

            reserva = Reserva(codigo, cliente, servicio, duracion)

            self.reservas.append(reserva)

            logging.info(f"Reserva creada: {codigo}")

            print("Reserva creada correctamente.")

            return reserva

        except ErrorSistema as error:
            logging.error(f"Error al crear reserva: {error}")
            print("Error:", error)
            return None

        except Exception as error:
            logging.exception("Error inesperado al crear reserva.")
            raise ErrorSistema(
                "No fue posible crear la reserva."
            ) from error

    def listar_clientes(self):

        print("\n--- LISTADO DE CLIENTES ---")

        for cliente in self.clientes:
            print(cliente.mostrar_informacion())

    def listar_servicios(self):

        print("\n--- LISTADO DE SERVICIOS ---")

        for servicio in self.servicios:
            print(servicio.describir_servicio())

    def listar_reservas(self):

        print("\n--- LISTADO DE RESERVAS ---")

        for reserva in self.reservas:
            print(reserva.mostrar_informacion())
            print("-----------------------------")


# ==================================================
# PRUEBAS DEL SISTEMA
# ==================================================

if __name__ == "__main__":

    sistema = SistemaSoftwareFJ()

    print("\n===================================")
    print(" SISTEMA INTEGRAL SOFTWARE FJ")
    print("===================================")

    # OPERACION 1: Registro correcto de cliente

    print("\nOPERACION 1")

    cliente1 = Cliente(
        "1001", "Carlos Perez",
        "carlos@gmail.com", "3001234567"
    )

    sistema.registrar_cliente(cliente1)

    # OPERACION 2: Registro de segundo cliente

    print("\nOPERACION 2")

    cliente2 = Cliente(
        "1002", "Maria Lopez",
        "maria@gmail.com", "3101234567"
    )

    sistema.registrar_cliente(cliente2)

    # OPERACION 3: Registro incorrecto de cliente

    print("\nOPERACION 3")

    try:
        cliente_invalido = Cliente(
            "1003", "Juan", "correo_invalido", "123"
        )

        sistema.registrar_cliente(cliente_invalido)

    except DatosInvalidos as error:
        print("Registro rechazado:", error)
        logging.error(f"Cliente invalido: {error}")

    # OPERACION 4: Crear servicio de salas

    print("\nOPERACION 4")

    sala = ReservaSala(
        "S01", "Sala de reuniones", 50000
    )

    sistema.registrar_servicio(sala)

    # OPERACION 5: Crear servicio de equipos

    print("\nOPERACION 5")

    equipo = AlquilerEquipo(
        "E01", "Computador portatil", 30000
    )

    sistema.registrar_servicio(equipo)

    # OPERACION 6: Crear servicio de asesoria

    print("\nOPERACION 6")

    asesoria = Asesoria(
        "A01", "Asesoria en sistemas", 80000
    )

    sistema.registrar_servicio(asesoria)

    # OPERACION 7: Crear servicio incorrecto

    print("\nOPERACION 7")

    try:
        servicio_invalido = ReservaSala(
            "S02", "Sala invalida", -500
        )

        sistema.registrar_servicio(servicio_invalido)

    except DatosInvalidos as error:
        print("Servicio rechazado:", error)
        logging.error(f"Servicio invalido: {error}")

    # OPERACION 8: Crear, confirmar y procesar reserva

    print("\nOPERACION 8")

    reserva1 = sistema.crear_reserva(
        "R001", cliente1, sala, 2
    )

    if reserva1:
        reserva1.confirmar()

        total = reserva1.procesar(19, 10)

        print("Valor total de la reserva:", total)

    # OPERACION 9: Reserva con duracion incorrecta

    print("\nOPERACION 9")

    sistema.crear_reserva(
        "R002", cliente1, equipo, -2
    )

    # OPERACION 10: Crear y cancelar reserva

    print("\nOPERACION 10")

    reserva2 = sistema.crear_reserva(
        "R003", cliente2, equipo, 3
    )

    if reserva2:
        reserva2.cancelar()

        print("Estado de la reserva:", reserva2.estado)

    # OPERACION 11: Procesar reserva de asesoria

    print("\nOPERACION 11")

    reserva3 = sistema.crear_reserva(
        "R004", cliente2, asesoria, 2
    )

    if reserva3:
        print(
            "Costo de asesoria:",
            reserva3.procesar(19, 5)
        )

    # OPERACION 12: Confirmar reserva cancelada

    print("\nOPERACION 12")

    try:
        reserva2.confirmar()

    except ReservaIncorrecta as error:
        print("Operacion rechazada:", error)
        logging.error(f"Error de confirmacion: {error}")

    # OPERACION 13: Try, except, else y finally

    print("\nOPERACION 13")

    try:
        resultado = 100 / 5

    except ZeroDivisionError as error:
        print("Error matematico:", error)

    else:
        print("Calculo realizado correctamente:", resultado)

    finally:
        print("Finalizo la operacion matematica.")

    # OPERACION 14: Encadenamiento de excepciones

    print("\nOPERACION 14")

    try:
        try:
            numero = int("texto")

        except ValueError as error:
            raise ErrorSistema(
                "No se pudo convertir el dato."
            ) from error

    except ErrorSistema as error:
        print("Excepcion controlada:", error)
        logging.error(f"Excepcion encadenada: {error}")

    # OPERACION 15: Calculo con parametros opcionales

    print("\nOPERACION 15")

    try:
        costo_simple = sala.calcular_costo(2)
        costo_con_impuesto = sala.calcular_costo(2, 19)
        costo_con_descuento = sala.calcular_costo(2, 19, 10)

        print("Costo normal:", costo_simple)
        print("Costo con impuesto:", costo_con_impuesto)
        print("Costo con impuesto y descuento:", costo_con_descuento)

    except ErrorSistema as error:
        print("Error en el calculo:", error)

    # RESULTADOS FINALES

    print("\n===================================")
    print(" RESULTADOS FINALES DEL SISTEMA")
    print("===================================")

    sistema.listar_clientes()
    sistema.listar_servicios()
    sistema.listar_reservas()

    print("\nTotal de clientes:", len(sistema.clientes))
    print("Total de servicios:", len(sistema.servicios))
    print("Total de reservas:", len(sistema.reservas))

    print("\nEl sistema finalizo correctamente.")
    print("Los eventos y errores se guardaron en software_fj.log.")