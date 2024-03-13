from machine import Pin
import time

class Transmitter:
    
    def __init__(self, pin_num, pulse_width_us=400, num_retransmissions=3):
        self.transmitter_pin = Pin(pin_num, Pin.OUT)
        self.pulse_width_us = pulse_width_us
        self.num_retransmissions = num_retransmissions

    def send_bit_pwm(self, bit):
        self.transmitter_pin.value(bit)
        # If bit is 1, the pin will be set to high for three pulse widths and to low for one pulse width
        if bit == 1:
            time.sleep_us(self.pulse_width_us * 3)
            self.transmitter_pin.value(0)

        # If bit is 0, the pin will be set to high for one pulse width and to low for three pulse widths
        if bit == 0:
            time.sleep_us(self.pulse_width_us)
            self.transmitter_pin.value(1)
            time.sleep_us(self.pulse_width_us * 3)
            self.transmitter_pin.value(0)

    def send_data(self, data, length):
        for _ in range(length-1, -1, -1):
            self.send_bit_pwm((data >> _) & 1)


    def send_preamble(self):
        # Pin is set to high for one pulse width and to low for 31 pulse widths
        self.transmitter_pin.value(1)
        time.sleep_us(self.pulse_width_us)
        self.transmitter_pin.value(0)
        time.sleep_us(self.pulse_width_us * 31)

    def send(self, address, command):
        for _ in range(self.num_retransmissions):
            
            # Send preamble            
            self.send_preamble()

            # Send sync bits
            #sync_bits = 0b11011000
            #self.send_data(sync_bits, 8)

            # Send address
            self.send_data(address, 20)

            # Send inverse address
            #self.send_data(~address & 0xFFFFF, 20)

            # Send command
            self.send_data(command, 4)

            # Send inverse command
            #self.send_data(~command & 0xF, 4)

            # Add a short delay between retransmissions
            time.sleep_ms(10)
    
# Example usage with adjustable pulse width, encoding option, and number of retransmissions
transmitter = Transmitter(0, pulse_width_us=500, num_retransmissions=5)  # Adjust parameters as needed

# Example address and command
address = 0b00011110110101110110
command = 0b0010

# Transmit the data
transmitter.send(address, command)
