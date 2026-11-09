#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parameters.py
=============

Constantes del ADC AD7888 (Analog Devices) para el driver ``ad7888.py``.

Definen los valores que se colocan en los campos del control register del
chip: selección de canal, modo de energía y fuente de referencia.

Formato del control register (8 bits, de MSB a LSB):

    | 7    | 6    | 5    | 4    | 3    | 2   | 1   | 0   |
    | ZERO | ZERO | ADD2 | ADD1 | ADD0 | REF | PM1 | PM0 |

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
"""

# ---------------------------------------------------------------------------
# Selección de canal de entrada analógica (bits ADD2..ADD0)
# Se desplazan 3 posiciones a la izquierda al construir el control register.
# ---------------------------------------------------------------------------
AIN1 = 0x00  # Canal 1 (ADD2..ADD0 = 000)
AIN2 = 0x01  # Canal 2 (ADD2..ADD0 = 001)
AIN3 = 0x02  # Canal 3 (ADD2..ADD0 = 010)
AIN4 = 0x03  # Canal 4 (ADD2..ADD0 = 011)
AIN5 = 0x04  # Canal 5 (ADD2..ADD0 = 100)
AIN6 = 0x05  # Canal 6 (ADD2..ADD0 = 101)
AIN7 = 0x06  # Canal 7 (ADD2..ADD0 = 110)
AIN8 = 0x07  # Canal 8 (ADD2..ADD0 = 111)

# ---------------------------------------------------------------------------
# Modos de energía (bits PM1..PM0)
# ---------------------------------------------------------------------------
NORMAL_MODE = 0x00         # Modo normal: el ADC está siempre encendido
SHUTDOWN_MODE = 0x01       # Apagado completo
AUTO_SHUTDOWN_MODE = 0x02  # Apagado automático al terminar la conversión
STANDBY_MODE = 0x03        # Modo en espera

# ---------------------------------------------------------------------------
# Fuente de referencia de tensión (bit REF)
# Se desplaza 2 posiciones a la izquierda al construir el control register.
# ---------------------------------------------------------------------------
ON_CHIP_REFERENCE = 0x00   # Referencia interna del chip
EXTERNAL_REFERENCE = 0x01  # Referencia externa (pin REF IN)
