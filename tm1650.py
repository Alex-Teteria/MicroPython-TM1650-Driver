from machine import I2C, Pin
import time

class TM1650:
    # Основні адреси TM1650 для 4х7-сегментного дисплея
    ADDR_DISPLAY_BASE = 0x34  # адреса першого дисплея (0x34, 0x35, 0x36, 0x37)
    ADDR_CONTROL = 0x24       # адреса керуючого регістра

    # Маски сегментів: 0bGFEDCBA
    SEGMENTS = {
        ' ': 0x00, '-': 0x40, '_': 0x08, '=': 0x48,
        '0': 0x3F, '1': 0x06, '2': 0x5B, '3': 0x4F, '4': 0x66,
        '5': 0x6D, '6': 0x7D, '7': 0x07, '8': 0x7F, '9': 0x6F,
        'A': 0x77, 'b': 0x7C, 'C': 0x39, 'c': 0x58, 'd': 0x5E,
        'E': 0x79, 'F': 0x71, 'H': 0x76, 'h': 0x74, 'L': 0x38,
        'o': 0x5C, 'P': 0x73, 'U': 0x3E, 'u': 0x1C,
        'r': 0x50, 'J': 0x0E, 'n': 0x54, 'y': 0x6E,
        'seg_a': 0x01, 'seg_b': 0x02, 'seg_c': 0x04, 'seg_d': 0x08,
        'seg_e': 0x10, 'seg_f': 0x20, 'seg_g': 0x40, 'seg_dp': 0x80
        # Додавайте інші символи за потреби
        }

    def __init__(self, i2c, brightness=7):
        self.i2c = i2c
        self.brightness = brightness
        self.on = True
        self._update_control()

    def _update_control(self):
        # Формуємо байт керування: 0b1DBBCCCC
        # D (bit 0): вкл/викл дисплея, BB: яскравість 0..7
        control = 0x01 if self.on else 0x00
        control |= (self.brightness & 0x07) << 4
        self.i2c.writeto(self.ADDR_CONTROL, bytes([control]))

    def set_brightness(self, value):
        if value < 0:
            value = 0
        elif value > 7:
            value = 7
        self.brightness = value
        self._update_control()

    def display_on(self):
        self.on = True
        self._update_control()

    def display_off(self):
        self.on = False
        self._update_control()

    def clear(self):
        for pos in range(4):
            self.i2c.writeto(self.ADDR_DISPLAY_BASE + pos, bytes([0x00]))

    def write_raw(self, pos, value):
        """Вивести маску сегментів (байт) у позицію 0..3
           pos - позиція 0..3
           value - маска сегментів (байт)
        """
        if 0 <= pos <= 3:
            self.i2c.writeto(self.ADDR_DISPLAY_BASE + pos, bytes([value & 0xFF]))

    def show(self, data):
        """Вивести рядок (до 4 символів). Підтримує лише символи з SEGMENTS."""
        for i in range(4):
            if i < len(data):
                ch = data[i]
                seg = self.SEGMENTS.get(ch, 0x00)
                self.write_raw(i, seg)
            else:
                self.write_raw(i, 0x00)

    def set_segments(self, seg_list):
        """Пряме керування сегментами: список з 4 байтів, для кожної позиції"""
        for i in range(4):
            val = seg_list[i] if i < len(seg_list) else 0x00
            self.write_raw(i, val)
    
    def show_num_on_scale(self, num):
        '''Засвітити num світлодіодів на лінійній шкалі із 32 LED'''
        digit = num // 8
        rem = num % 8
        for i in range(3, 3-digit, -1):
            self.write_raw(i, 255)
        self.write_raw(3-digit, 2**rem-1)    

if __name__ == '__main__':
    # Приклад використання:
    # initialization
    i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=100_000)
    disp = TM1650(i2c)
    
    # set_brightness
    disp.set_brightness(3)
    
    # displaying text 'AbCd'
    disp.show('AbCd')
    time.sleep(1)
    
    # Direct segment control, displays '0123'
    disp.set_segments([0x3F, 0x06, 0x5B, 0x4F])  # 0123
    time.sleep(1)
    
    # Turning the display on/off
    disp.display_off()
    time.sleep(1)
    disp.display_on()
    time.sleep(1)
    
    # Sequential illumination of each segment on the last (fourth) character
    segments = ('seg_a', 'seg_b', 'seg_c', 'seg_d', 'seg_e',
                'seg_f', 'seg_g', 'seg_dp')
    for seg in segments:
        disp.set_segments([0, 0, 0, disp.SEGMENTS[seg]])
        time.sleep(1)

    for i in range(9):
        disp.write_raw(2, 2**i-1)
        time.sleep(1)
    
    # Sequential LED lighting on a linear scale of 32 LEDs
    disp.clear()
    for num in range(17):
        disp.show_num_on_scale(num)
        time.sleep(1)
    
    # Light the number of LEDs equal to num on a linear scale of 32 LEDs
    disp.clear()
    num = 11
    disp.show_num_on_scale(num)
    time.sleep(1)
    
    disp.clear()
