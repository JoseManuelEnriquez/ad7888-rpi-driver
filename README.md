# AD7888 Python Driver

Driver en Python para el ADC **AD7888** (12 bits, 8 canales, SPI) pensado para **Raspberry Pi** usando [`spidev`](https://pypi.org/project/spidev/).

![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-c51a4a.svg)

## Características

- Lectura de cualquier canal del AD7888 (AIN1–AIN8) con resolución de 12 bits.
- Selección de la referencia: interna (on-chip) o externa.
- Configuración del modo: normal mode (en futuras versiones se implementaran los demas modos)
- Selección del bus SPI (0 o 1) y del chip select (0 o 1).
- Sin dependencias aparte de `spidev`.
- Programa de prueba incluido que lee AIN1 y muestra el resultado por terminal.

## Hardware

### Conexión

| AD7888 | Raspberry Pi (SPI0) | Pin físico |
|--------|---------------------|------------|
| `DIN`  | MOSI (GPIO10)       | 19 |
| `DOUT` | MISO (GPIO9)        | 21 |
| `SCLK` | SCLK (GPIO11)       | 23 |
| `CS`   | CE0 (GPIO8)         | 24 |
| `VDD`  | 3V3                 | 1 |
| `AGND` / `DGND` | GND        | 6 |

> La tabla corresponde al bus SPI 0 con CE0. Si usas CE1 u otro bus SPI, ajusta los pines. Añade un condensador de desacoplo (p. ej. 100 nF + 10 µF) cerca de `VDD`, y recuerda que la tensión en las entradas analógicas **no debe superar la de alimentación del ADC**.

### Referencia

El AD7888 puede usar su referencia interna de 2,5 V o una externa en `REFIN`. La referencia que selecciones en el driver (`ON_CHIP_REFERENCE` o `EXTERNAL_REFERENCE`) debe coincidir con el hardware real.

## Requisitos

- Raspberry Pi con Raspberry Pi OS (o similar)
- Python 3.8 o superior
- SPI habilitado
- Librería `spidev`

## Instalación

### 1. Habilitar SPI

```bash
sudo raspi-config
# Interface Options -> SPI -> Enable
sudo reboot
```

Comprueba que existe el dispositivo:

```bash
ls /dev/spidev*
# /dev/spidev0.0  /dev/spidev0.1
```

### 2. Instalar dependencias

```bash
sudo apt update
sudo apt install -y python3-spidev
# o bien, con pip:
pip install spidev
```

### 3. Obtener el driver

```bash
git clone https://github.com/<usuario>/<repositorio>.git
cd <repositorio>
```

## Uso rápido

```python
from driver.ad7888 import AD7888
from driver.parameters import *
from time import sleep

def main():
    ad7888 = AD7888(0, 0)
    ad7888.set_reference(EXTERNAL_REFERENCE)
    try:
        print(ad7888.read_data())
    finally:
        ad7888.close()

if __name__ == "__main__":
    main()
```

También puedes indicar todos los parámetros al crear el objeto:

```python
adc = AD7888(
    bus=0,
    cs=0,
    channel=AIN1,
    ref=ON_CHIP_REFERENCE,
    mode=NORMAL_MODE,
)
```

## API

### Constructor

```python
AD7888(bus, cs, channel=AIN1, ref=ON_CHIP_REFERENCE, mode=NORMAL_MODE)
```

| Parámetro | Descripción | Valor por defecto |
|-----------|-------------|-------------------|
| `bus` | Bus SPI de la Raspberry Pi (`0` o `1`). | — |
| `cs` | Chip select (`0` o `1`). | — |
| `channel` | Canal de entrada inicial (`AIN1`–`AIN8`). | `AIN1` |
| `ref` | Referencia del ADC (`ON_CHIP_REFERENCE` o `EXTERNAL_REFERENCE`). | `ON_CHIP_REFERENCE` |
| `mode` | Modo de funcionamiento (power mode). | `NORMAL_MODE` |

### Métodos

| Método | Descripción |
|--------|-------------|
| `read_data()` | Realiza una conversión y devuelve el dato crudo (`raw_data`, 12 bits: 0–4095) del canal seleccionado. |
| `set_channel(channel)` | Selecciona el canal de entrada (`AIN1`–`AIN8`). |
| `set_reference(reference)` | Selecciona la referencia: `ON_CHIP_REFERENCE` o `EXTERNAL_REFERENCE`. |
| `set_power_mode(mode)` | Configura el modo de funcionamiento del ADC. |
| `close()` | Libera el dispositivo SPI. |

### Constantes (`parameters.py`)

| Grupo | Valores |
|-------|---------|
| Canales | `AIN1`, `AIN2`, `AIN3`, `AIN4`, `AIN5`, `AIN6`, `AIN7`, `AIN8` |
| Referencia | `ON_CHIP_REFERENCE`, `EXTERNAL_REFERENCE` |
| Modos de funcionamiento | `NORMAL_MODE`, ... *(completa con el resto de modos definidos en `parameters.py`)* |

## Detalles de la comunicación SPI

- **Velocidad:** el reloj SPI está fijado en **500 kHz**. Por ahora no se puede cambiar desde la API; se ofrecerá en futuras versiones.
- **Datos devueltos:** actualmente el driver solo devuelve el dato crudo (`raw_data`), sin conversión a tensión.
- **Conversión a tensión (manual):** si necesitas la tensión, puedes calcularla a partir de la referencia utilizada:

```
V = raw_data * (Vref / 4096)
```

## Programa de prueba

Se incluye un script que lee el canal AIN1 y muestra el resultado por terminal:

```bash
python3 test_ad7888.py
```

Salida de ejemplo:

```
AIN1: 2048
```

### Otras formas de probar el driver

- Conectar un potenciómetro a un canal y comprobar que el valor varía de forma lineal entre 0 y 4095.
- Conectar un canal a GND y a la referencia/`VDD` para validar los extremos.
- Medir la misma tensión con un multímetro y comparar con la lectura del driver.
- Usar una fuente de tensión conocida (p. ej. un divisor resistivo) y calcular el error.
- Probar el cambio de canal, de referencia y de modo de funcionamiento en caliente.
- Añadir tests unitarios con un mock de `spidev.SpiDev` para validar las tramas enviadas sin hardware.

## Solución de problemas

| Problema | Posible causa |
|----------|---------------|
| `FileNotFoundError: /dev/spidev0.0` | SPI no habilitado; revisa `raspi-config`. |
| `PermissionError` | Añade tu usuario al grupo `spi` (`sudo usermod -aG spi $USER`) o ejecuta con `sudo`. |
| Lecturas siempre 0 o 4095 | Revisa cableado, alimentación, referencia seleccionada y modo SPI. |
| Lecturas ruidosas | Mejora el desacoplo y acorta los cables. |

## Estructura del proyecto

```
.
├── driver/          # Contiene la API y las constantes
├── test/      # Contiene el programa de prueba
├── README.md
└── LICENSE
```

## Contribuir

Las issues y pull requests son bienvenidas. Si encuentras un fallo, abre una issue indicando modelo de Raspberry Pi, versión de Python y salida del programa de prueba.

## Licencia

Distribuido bajo licencia **MIT**. Consulta el archivo [`LICENSE`](LICENSE) para más información.

## Referencias

- [Datasheet del AD7888 (Analog Devices)](https://www.analog.com/en/products/ad7888.html)
- [Documentación de `spidev`](https://pypi.org/project/spidev/)
