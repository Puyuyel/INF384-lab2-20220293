"""Modelo de pedido y transiciones de estado."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Estado(str, Enum):
    REGISTRADO = "registrado"
    PREPARADO = "preparado"
    DESPACHADO = "despachado"
    ENTREGADO = "entregado"
    ANULADO = "anulado"


TRANSICIONES = {
    Estado.REGISTRADO: {Estado.PREPARADO, Estado.ANULADO},
    Estado.PREPARADO: {Estado.DESPACHADO, Estado.ANULADO},
    Estado.DESPACHADO: {Estado.ENTREGADO},
    Estado.ENTREGADO: set(),
    Estado.ANULADO: set(),
}


class TransicionInvalida(Exception):
    """Se intento una transicion de estado no permitida."""


@dataclass
class Linea:
    sku: str
    cantidad: int
    precio_unitario: float

    def subtotal(self) -> float:
        return round(self.cantidad * self.precio_unitario, 2)


@dataclass
class Pedido:
    codigo: str
    cliente: str
    lineas: list[Linea] = field(default_factory=list)
    estado: Estado = Estado.REGISTRADO
    creado_en: datetime = field(default_factory=datetime.now)

    def agregar_linea(self, linea: Linea) -> None:
        if self.estado is not Estado.REGISTRADO:
            raise TransicionInvalida(
                "solo se pueden agregar lineas a un pedido registrado"
            )
        self.lineas.append(linea)

    def total(self) -> float:
        return round(sum(linea.subtotal() for linea in self.lineas), 2)

    def unidades(self) -> int:
        return sum(linea.cantidad for linea in self.lineas)

    def cambiar_estado(self, nuevo: Estado) -> None:
        permitidos = TRANSICIONES[self.estado]
        if nuevo not in permitidos:
            raise TransicionInvalida(
                f"no se puede pasar de {self.estado.value} a {nuevo.value}"
            )
        self.estado = nuevo

    def esta_cerrado(self) -> bool:
        return self.estado in (Estado.ENTREGADO, Estado.ANULADO)


def agrupar_por_cliente(pedidos: list[Pedido]) -> dict[str, list[Pedido]]:
    agrupados: dict[str, list[Pedido]] = {}
    for pedido in pedidos:
        agrupados.setdefault(pedido.cliente, []).append(pedido)
    return agrupados


def pedidos_abiertos(pedidos: list[Pedido]) -> list[Pedido]:
    return [p for p in pedidos if not p.esta_cerrado()]


def evaluar_prioridad_entrega(pedido: Pedido, dias_restantes: int, es_urgente: bool) -> int:
    """Estimación simple de prioridad de entrega.

    Devuelve un entero de 0 (baja) a 10 (máxima) según reglas heurísticas:
    - pedidos entregados o anulados => 0
    - si es urgente => prioridad alta
    - menos días restantes => mayor prioridad
    - pedidos con muchas unidades aumentan prioridad

    Esta función incluye condicionales y cálculo no trivial para provocar código
    sin pruebas en el pipeline.
    """
    if pedido.esta_cerrado():
        return 0

    prioridad = 0

    # Base por urgencia y días restantes
    if es_urgente:
        prioridad += 5
    if dias_restantes <= 0:
        prioridad += 4
    elif dias_restantes <= 2:
        prioridad += 3
    elif dias_restantes <= 5:
        prioridad += 2
    else:
        prioridad += 0

    # Ajuste por tamaño del pedido
    unidades = pedido.unidades()
    if unidades >= 100:
        prioridad += 3
    elif unidades >= 20:
        prioridad += 2
    elif unidades >= 5:
        prioridad += 1

    # Normalizar a 0-10
    if prioridad > 10:
        prioridad = 10
    if prioridad < 0:
        prioridad = 0

    return prioridad
