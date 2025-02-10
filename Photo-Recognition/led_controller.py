import machine
import utime as time

class LEDController:
    def __init__(self, pin_number):
        self.led = machine.Pin(pin_number, machine.Pin.OUT)

    def blink(self, interval=0.5, times=10):
        for _ in range(times):
            self.led.on()
            time.sleep(interval)
            self.led.off()
            time.sleep(interval)

    def breathe(self, duration=5, steps=50):
        for _ in range(duration):
            for i in range(steps):
                self.led.duty(i * (1023 // steps))
                time.sleep(0.01)
            for i in range(steps, -1, -1):
                self.led.duty(i * (1023 // steps))
                time.sleep(0.01)
