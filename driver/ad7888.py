#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ad7888.py
=========

Driver en Python para el ADC de 12 bits y 8 canales AD7888 (Analog Devices),
conectado por SPI a una Raspberry Pi mediante la librería ``spidev``.

Se utiliza para monitorizar el nivel de batería de la Raspberry Pi a través
de un ADC externo.

Autor:      José
GitHub:     https://github.com/JoseManuelEnriquez
Web:        https://embeddedbyjose.com
Versión:    0.1.0
Fecha:      2026-11-09
Licencia:   MIT

Copyright (c) 2026 José

Se concede permiso, libre de cargos, a cualquier persona que obtenga una copia
de este software y de los archivos de documentación asociados, para utilizar
el software sin restricción, incluyendo, sin limitación, los derechos de uso,
copia, modificación, fusión, publicación, distribución, sublicencia y/o venta
de copias del software, sujeto a las siguientes condiciones:

El aviso de copyright anterior y este aviso de permiso se incluirán en todas
las copias o partes sustanciales del software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O
IMPLÍCITA, INCLUYENDO, PERO NO LIMITADO A, GARANTÍAS DE COMERCIALIZACIÓN,
IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS
AUTORES O TITULARES DEL COPYRIGHT SERÁN RESPONSABLES DE NINGUNA RECLAMACIÓN,
DAÑO U OTRA RESPONSABILIDAD, YA SEA EN UNA ACCIÓN DE CONTRATO, AGRAVIO O DE
OTRO MODO, QUE SURJA DE O EN CONEXIÓN CON EL SOFTWARE O EL USO U OTROS TRATOS
EN EL SOFTWARE.

Dependencias:
    - spidev
    - parameters.py (constantes del AD7888: canales, modos de energía, etc.)
"""

import spidev
from .parameters import *

# Frecuencia del reloj SPI (SCLK) en Hz.
FREQUENCY = 100_000


class AD7888:
    """
    Controlador del ADC AD7888 por SPI.

    Gestiona la configuración del canal de entrada, la referencia de tensión
    y el modo de energía, y permite leer el resultado de la conversión.

    Atributos:
        spi:       Objeto ``spidev.SpiDev`` con el bus SPI abierto.
        channel:   Canal analógico seleccionado (AIN0..AIN7).
        ref:       Selección de la referencia de tensión (bit REF del
                   control register).
        mode:      Modo de energía actual (bits PM1/PM0).
        read_cb:   Función que ejecuta la lectura según el modo de energía.
    """

    def __init__(self, spi_bus, device_cs, channel=AIN1, ref=0, mode=NORMAL_MODE):
        """
        Abre el bus SPI y configura el ADC.

        Args:
            spi_bus:   Número del bus SPI (p. ej. 0 -> /dev/spidev0.x).
            device_cs: Línea de chip select del dispositivo (p. ej. 0 o 1).
            channel:   Canal de entrada analógica. Por defecto AIN1.
            ref:       Selección de referencia de tensión. Por defecto 0.
            mode:      Modo de energía inicial. Por defecto NORMAL_MODE.
        """
        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, device_cs)
        self.spi.max_speed_hz = FREQUENCY
        self.spi.mode = 0b11  # CPOL=1, CPHA=1: reloj en reposo ALTO, muestreo en flanco de subida
        self.spi.bits_per_word = 8

        self.set_channel(channel)
        self.set_reference(ref)
        self.set_power_mode(mode)

    def set_channel(self, channel):
        """
        Selecciona el canal analógico que se convertirá en la próxima lectura.

        Args:
            channel: Constante del canal (AIN0..AIN7) definida en parameters.py.
        """
        self.channel = channel

    def set_reference(self, reference):
        """
        Selecciona la fuente de referencia de tensión del ADC.

        Args:
            reference: Valor del bit REF del control register (0 o 1).
        """
        self.ref = reference

    def set_power_mode(self, mode):
        """
        Selecciona el modo de energía y asocia la función de lectura
        correspondiente.

        Args:
            mode: Una de las constantes NORMAL_MODE, SHUTDOWN_MODE,
                  AUTO_SHUTDOWN_MODE o STANDBY_MODE.

        Raises:
            ValueError: Si el modo no es válido.
        """
        # Tabla de despacho: modo de energía -> función que realiza la lectura
        handlers = {
            NORMAL_MODE: self._send_normal_mode,
            SHUTDOWN_MODE: self._send_shutdown_mode,
            AUTO_SHUTDOWN_MODE: self._send_auto_shutdown_mode,
            STANDBY_MODE: self._send_standby_mode,
        }
        if mode not in handlers:
            raise ValueError(f"Modo de energía no válido: {mode}")
        self.mode = mode              # bits PM1/PM0
        self.read_cb = handlers[mode]

    def _send_shutdown_mode(self):
        """Lectura en modo SHUTDOWN. Pendiente de implementar."""
        raise NotImplementedError

    def _send_auto_shutdown_mode(self):
        """Lectura en modo AUTO SHUTDOWN. Pendiente de implementar."""
        raise NotImplementedError

    def _send_standby_mode(self):
        """Lectura en modo STANDBY. Pendiente de implementar."""
        raise NotImplementedError

    def _send_normal_mode(self):
        """
        Realiza una conversión y devuelve el resultado en modo normal.

        El SPI está configurado a 8 bits por palabra, así que cada byte genera
        siempre 8 ciclos de reloj.

        Según el datasheet, el ADC en modo normal necesita 16 ciclos de SCLK
        para poder ver el resultado de la conversión. Por eso se envían dos
        bytes: el primero genera los 8 primeros ciclos para configurar el
        control register, y el segundo genera otros 8 ciclos para poder leer
        el resultado de la conversión.

        ANOTACIÓN: Se deben mantener los bits PM1 y PM0 para que funcione.

        Returns:
            int: Resultado de la conversión (12 bits, 0..4095).
        """
        # 16 ciclos de SCLK en una sola trama (CS bajo durante los 2 bytes).
        #ctrl = (self.channel << 3) | (self.ref << 2) | self.mode
        #ctrl = 0x20
        ctrl = 0x04
        print(hex(ctrl))
        rx = self.spi.xfer2([ctrl, 0x00])
        print(rx)
        # Trama de salida: 4 ceros + 12 bits de datos
        return ((rx[0] & 0x0F) << 8) | rx[1]

    def read_data(self):
        """
        Lee el valor del ADC usando la función asociada al modo de energía
        actual.

        Returns:
            int: Resultado de la conversión (12 bits).
        """
        return self.read_cb()

    def close(self):
        """Cierra el bus SPI y libera el dispositivo."""
        self.spi.close()
