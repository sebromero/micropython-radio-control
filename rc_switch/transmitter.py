try:
    from machine import Pin
except ImportError:
    class Pin:
        OUT = "OUT"
        IN = "IN"
        PULL_UP = "PULL_UP"
        PULL_DOWN = "PULL_DOWN"
        IRQ_RISING = "IRQ_RISING"
        IRQ_FALLING = "IRQ_FALLING"
        IRQ_ANYEDGE = "IRQ_ANYEDGE"
        def __init__(self, pin_num, mode) -> None:
            pass
        def value(self, value):
            pass

import time

# Check if time module contains sleep_us function
try:
    time.sleep_us
except AttributeError:
    time.sleep_us = (lambda us: time.sleep(us / 1000000.0))

class Protocol:
    def __init__(self, pulse_width_us, sync_pulses, zero_pulses, one_pulses, inverted_signal) -> None:
        self.pulse_width_us = pulse_width_us
        self.sync_pulses = sync_pulses
        self.zero_pulses = zero_pulses
        self.one_pulses = one_pulses
        self.inverted_signal = inverted_signal

protocols = [
    Protocol(350, (  1, 31 ), (  1,  3 ), (  3,  1 ), False ),    # protocol 1 (EV1527)
    Protocol(650, (  1, 10 ), (  1,  2 ), (  2,  1 ), False ),    # protocol 2
    Protocol(100, ( 30, 71 ), (  4, 11 ), (  9,  6 ), False ),    # protocol 3
    Protocol(380, (  1,  6 ), (  1,  3 ), (  3,  1 ), False ),    # protocol 4
    Protocol(500, (  6, 14 ), (  1,  2 ), (  2,  1 ), False ),    # protocol 5
    Protocol(450, ( 23,  1 ), (  1,  2 ), (  2,  1 ), True ),     # protocol 6 (HT6P20B)
    Protocol(150, (  2, 62 ), (  1,  6 ), (  6,  1 ), False ),    # protocol 7 (HS2303-PT, i. e. used in AUKEY Remote)
    Protocol(200, (  3, 130), (  7, 16 ), (  3,  16), False ),     # protocol 8 Conrad RS-200 RX
    Protocol(200, ( 130, 7 ), (  16, 7 ), ( 16,  3 ), True ),      # protocol 9 Conrad RS-200 TX
    Protocol(365, ( 18,  1 ), (  3,  1 ), (  1,  3 ), True ),     # protocol 10 (1ByOne Doorbell)
    Protocol(270, ( 36,  1 ), (  1,  2 ), (  2,  1 ), True ),     # protocol 11 (HT12E)
    Protocol(320, ( 36,  1 ), (  1,  2 ), (  2,  1 ), True )      # protocol 12 (SM5212)
]

class Transmitter:

    def __init__(self, pin_num, pulse_width_us = None, protocol = protocols[0], num_retransmissions=10):
        self.transmitter_pin = Pin(pin_num, Pin.OUT)

        if pulse_width_us is None:
            self.pulse_width_us = protocol.pulse_width_us
        else:
            self.pulse_width_us = pulse_width_us
        
        self.protocol = protocol
        self.num_retransmissions = num_retransmissions

    def transmit_pulses(self, pulses):
        first_logic_level = 1
        second_logic_level = 0

        if self.protocol.inverted_signal:
            first_logic_level = 0
            second_logic_level = 1
        
        high_pulse_width = self.pulse_width_us * pulses[0]
        low_pulse_width = self.pulse_width_us * pulses[1]

        self.transmitter_pin.value(first_logic_level)
        time.sleep_us(high_pulse_width)
        self.transmitter_pin.value(second_logic_level)
        time.sleep_us(low_pulse_width)
            
    def send_data(self, data, length, msb_first=True):
        if msb_first:
            data_range = range(length-1, -1, -1)
        else:
            data_range = range(length)

        for _ in data_range:
            bit = (data >> _) & 1
            # print("Sending bit", bit)

            if bit == 1:            
                self.transmit_pulses(self.protocol.one_pulses)
            else:
                self.transmit_pulses(self.protocol.zero_pulses)

    def send(self, data, length = None):
        # If data is a string (of zeroes and ones), convert it to 
        # an integer with the same binary representation
        if isinstance(data, str):
            length = len(data)
            data = int(data, 2)

        for _ in range(self.num_retransmissions):
            self.send_data(data, length)
            self.transmit_pulses(self.protocol.sync_pulses)
            
        # Disable transmit after sending (i.e., for inverted protocols)
        self.transmitter_pin.value(0)

# Example usage with adjustable pulse width, encoding option, and number of retransmissions
transmitter = Transmitter("D2", pulse_width_us=315)  # Adjust parameters as needed

# Example address and command
address = 0b00011110110101110110
command = 0b0010
data = (address << 4) | command

# Transmit the data
#transmitter.send(data, 24)
transmitter.send("000111101101011101100010")