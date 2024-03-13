from machine import Pin
import time

class Encoding:
    MANCHESTER = 1
    PWM = 2

class Transmitter:
    PREAMBLE = 0b11111111111111111111111111  # Custom preamble constant
    
    def __init__(self, pin_num, pulse_width_us=400, encoding=Encoding.PWM, num_retransmissions=3):
        self.transmitter_pin = Pin(pin_num, Pin.OUT)
        self.pulse_width_us = pulse_width_us
        self.encoding = encoding
        self.num_retransmissions = num_retransmissions

    def send_bit_manchester(self, bit):
        if bit == 0:
            self.transmitter_pin.value(1)
            time.sleep_us(self.pulse_width_us // 2)
            self.transmitter_pin.value(0)
            time.sleep_us(self.pulse_width_us // 2)
        else:
            self.transmitter_pin.value(0)
            time.sleep_us(self.pulse_width_us // 2)
            self.transmitter_pin.value(1)
            time.sleep_us(self.pulse_width_us // 2)

    def send_bit_pwm(self, bit):
        self.transmitter_pin.value(bit)
        time.sleep_us(self.pulse_width_us)

    def send_data(self, data, length):
        for _ in range(length-1, -1, -1):
            if self.encoding == Encoding.MANCHESTER:
                self.send_bit_manchester((data >> _) & 1)
            elif self.encoding == Encoding.PWM:
                self.send_bit_pwm((data >> _) & 1)


    def send_ev1527(self, address, command):
        for _ in range(self.num_retransmissions):
            # Send preamble
            self.send_preamble()

            # Send address
            self.send_data(address, 20)

            # Send inverse address
            self.send_data(~address & 0xFFFFF, 20)

            # Send command
            self.send_data(command, 4)

            # Send inverse command
            self.send_data(~command & 0xF, 4)

            # Add a short delay between retransmissions
            time.sleep_ms(10)
    
    def send_preamble(self):
        for _ in range(26):
            if self.encoding == Encoding.MANCHESTER:
                self.send_bit_manchester((self.PREAMBLE >> (25 - _)) & 1)
            elif self.encoding == Encoding.PWM:
                self.send_bit_pwm((self.PREAMBLE >> (25 - _)) & 1)

# Example usage with adjustable pulse width, encoding option, and number of retransmissions
transmitter = Transmitter(0, pulse_width_us=500, encoding=Encoding.PWM, num_retransmissions=5)  # Adjust parameters as needed

# Example address and command
address = 0b00011110110101110110
command = 0b0010

# Transmit the data
transmitter.send_ev1527(address, command)
