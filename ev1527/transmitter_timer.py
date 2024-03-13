import machine
import time

class Encoding:
    MANCHESTER = 1
    PWM = 2

class Transmitter:
    PREAMBLE = 0b11111111111111111111111111  # Custom preamble constant
    
    def __init__(self, pin_num, pulse_width_us=400, encoding=Encoding.PWM, num_retransmissions=3):
        self.transmitter_pin = machine.Pin(pin_num, machine.Pin.OUT)
        self.pulse_width_us = pulse_width_us
        self.encoding = encoding
        self.num_retransmissions = num_retransmissions
        self.transmission_count = 0

    def send(self, address, command):
        self.transmission_count = 0
        while self.transmission_count < self.num_retransmissions:
            # Combine preamble, sync bits, address, inverse address, command, and inverse command data
            preamble = self.PREAMBLE
            sync_bits = 0b11011000
            data = (preamble << 34) | (sync_bits << 26) | (address << 6) | (inv_address << 26) | (command << 2) | inv_command
            length = 82  # Total length is 82 bits (26 preamble + 8 sync bits + 20 address + 20 inverse address + 4 command + 4 inverse command)

            # Initiate transmission
            self.start_transmission(data, length)
            time.sleep_ms(10)  # Short delay before retransmission
            self.transmission_count += 1

    def start_transmission(self, data, length):
        self.data_to_transmit = data
        self.data_length = length
        self.transmit_index = 0
        self.timer = machine.Timer(0)
        self.timer.init(period=self.pulse_width_us, mode=machine.Timer.PERIODIC, callback=self.transmit_callback)

    def transmit_callback(self, timer):
        if self.transmit_index < self.data_length:
            # Transmit one bit of data
            bit = (self.data_to_transmit >> self.transmit_index) & 1
            if self.encoding == Encoding.MANCHESTER:
                self.send_bit_manchester(bit)
            elif self.encoding == Encoding.PWM:
                self.send_bit_pwm(bit)
            self.transmit_index += 1
        else:
            # Stop transmission when all bits have been transmitted
            self.stop_transmission()

    def stop_transmission(self):
        self.timer.deinit()  # Stop the timer
        self.transmit_index = 0

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


# Example usage
transmitter = Transmitter(pin_num=0, pulse_width_us=500, encoding=Encoding.PWM, num_retransmissions=5)

# Transmit data with address and command
address = 0b00011110110101110110
command = 0b0010

#01000110111010110 1110000

transmitter.send(address, command)
