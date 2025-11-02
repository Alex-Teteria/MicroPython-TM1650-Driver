# MicroPython TM1650 Driver

This repository contains a MicroPython driver for 4-digit 7-segment displays based on the TM1650 IC.

## Features

- Supports all 8 brightness levels (0–7)
- Display of numbers, letters, and special symbols (extensible character set)
- Direct control of individual segments (raw segment bytes per digit)
- Display on/off, display clear

## Requirements

- MicroPython (ESP32, ESP8266, Raspberry Pi Pico, etc.)
- 7-segment display with TM1650 controller
- I2C connection

## Wiring

Connect the SDA and SCL pins of the display to the appropriate pins on your microcontroller.

## Usage

### 1. Initialization

```python
from machine import I2C, Pin
from tm1650 import TM1650

# Adjust pins according to your board!
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)

disp = TM1650(i2c)
```

### 2. Brightness

```python
disp.set_brightness(5)  # 0 (min) ... 7 (max)
```

### 3. Displaying text

```python
disp.show('AbCd')
disp.show('1234')
```

### 4. Direct segment control

```python
# Each element is a byte defining the segments (GFEDCBA)
disp.set_segments([0x3F, 0x06, 0x5B, 0x4F])  # Displays '0123'
```

### 5. Lights a specific number of LEDs on a linear scale of 32 LEDs

```python
# Light the number of LEDs equal to num on a linear scale of 32 LEDs
num = 11
disp.show_num_on_scale(num)
```

### 6. Clearing the display

```python
disp.clear()
```

### 7. Turning the display on/off

```python
disp.display_off()
disp.display_on()
```

## Adding custom symbols

The `SEGMENTS` dictionary in `tm1650.py` can be extended with new characters by adding the corresponding segment masks.

## License

MIT

---

**Feedback and contributions are welcome!**
