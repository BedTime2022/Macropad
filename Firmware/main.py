#code written with help/use of LLMS 

import board
import digitalio
import neopixel
import busio
import time
# -----------------------
# OLED SETUP (SSD1306)
# -----------------------
import adafruit_ssd1306
i2c = busio.I2C(board.A0, board.A1)  # SCL=A0 (GPIO26), SDA=A1 (GPIO27)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
def oled_print(text):
    oled.fill(0)
    oled.text(text, 0, 0, 1)
    oled.show()
oled_print("Booting...")
# -----------------------
# RGB LED STRIP
# -----------------------
NUM_LEDS = 5
pixels = neopixel.NeoPixel(board.A2, NUM_LEDS, brightness=0.3, auto_write=True)
def led_show_key(idx):
    pixels.fill((0, 0, 0))
    if 0 <= idx < NUM_LEDS:
        pixels[idx] = (0, 20, 150)  # blue highlight
# -----------------------
# KEYS (DIRECT GPIO)
# -----------------------
# Order: switch0 → Enter, switches 1-4 → D F J K
key_pins = [board.D0, board.D1, board.D2, board.D4, board.D3]
keys = []
for pin in key_pins:
    sw = digitalio.DigitalInOut(pin)
    sw.switch_to_input(pull=digitalio.Pull.UP)
    keys.append(sw)
key_labels = ["ENTER", "D", "F", "J", "K"]
# -----------------------
# USB KEYBOARD
# -----------------------
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
kbd = Keyboard(usb_hid.devices)
keycode_map = {
    "ENTER": Keycode.ENTER,
    "D": Keycode.D,
    "F": Keycode.F,
    "J": Keycode.J,
    "K": Keycode.K
}
# Track key state
key_state = [False] * 5
oled_print("READY")
# -----------------------
# MAIN LOOP
# -----------------------
while True:
    for i, sw in enumerate(keys):
        pressed = not sw.value
        if pressed and not key_state[i]:
            # key down
            key_state[i] = True
            label = key_labels[i]
            oled_print(f"Key: {label}")
            led_show_key(i)
            # send key
            kbd.press(keycode_map[label])
        if not pressed and key_state[i]:
            # key released
            key_state[i] = False
            kbd.release(keycode_map[key_labels[i]])
            oled_print("READY")
            pixels.fill((0, 0, 0))
    time.sleep(0.01)