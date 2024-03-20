from machine import Pin
import time
import gc

class Protocol:
    """
    Represents a protocol for transmitting signals using RC switches.

    Attributes:
        pulse_width_us (int): The duration of each pulse in microseconds.
        sync_pulses (int): The number of sync pulses to send before the data pulses.
        zero_pulses (int): The number of pulses to send for a '0' bit.
        one_pulses (int): The number of pulses to send for a '1' bit.
        inverted_signal (bool): If true, interchange high and low logic levels in all transmissions.
    """

    def __init__(self, pulse_width_us, sync_pulses, zero_pulses, one_pulses, inverted_signal) -> None:
        self.pulse_width_us = pulse_width_us
        self.sync_pulses = sync_pulses
        self.zero_pulses = zero_pulses
        self.one_pulses = one_pulses
         
        # By default, this library assumes that any signals it sends or receives
        # can be broken down into pulses which start with a high signal level,
        # followed by a a low signal level (e.g. PT 2260).
        #
        # But some devices do it the other way around, and start with a low
        # signal level, followed by a high signal level, e.g. the HT6P20B. To
        # accommodate this, one can set invertedSignal to true.
        self.inverted_signal = inverted_signal

protocols = [
    Protocol(350, (  1, 31 ), (  1,  3 ), (  3,  1 ), False ),    # protocol 1 (EV1527)
    Protocol(650, (  1, 10 ), (  1,  2 ), (  2,  1 ), False ),    # protocol 2
    Protocol(100, ( 30, 71 ), (  4, 11 ), (  9,  6 ), False ),    # protocol 3
    Protocol(380, (  1,  6 ), (  1,  3 ), (  3,  1 ), False ),    # protocol 4
    Protocol(500, (  6, 14 ), (  1,  2 ), (  2,  1 ), False ),    # protocol 5
    Protocol(450, ( 23,  1 ), (  1,  2 ), (  2,  1 ), True ),     # protocol 6 (HT6P20B)
    Protocol(150, (  2, 62 ), (  1,  6 ), (  6,  1 ), False ),    # protocol 7 (HS2303-PT, i. e. used in AUKEY Remote)
    Protocol(200, (  3, 130), (  7, 16 ), (  3,  16), False ),    # protocol 8 Conrad RS-200 RX
    Protocol(200, ( 130, 7 ), (  16, 7 ), ( 16,  3 ), True ),     # protocol 9 Conrad RS-200 TX
    Protocol(365, ( 18,  1 ), (  3,  1 ), (  1,  3 ), True ),     # protocol 10 (1ByOne Doorbell)
    Protocol(270, ( 36,  1 ), (  1,  2 ), (  2,  1 ), True ),     # protocol 11 (HT12E)
    Protocol(320, ( 36,  1 ), (  1,  2 ), (  2,  1 ), True )      # protocol 12 (SM5212)
]

class Transmitter:
    """
    Represents a transmitter for sending data using a specific protocol.

    Properties:
        transmitter_pin: The pin used for transmitting data.
        pulse_width_us: The pulse width in microseconds.
        protocol: The protocol used for transmitting data.
        num_retransmissions: The number of times to retransmit the data.
    """

    def __init__(self, pin, pulse_width_us=None, protocol=1, num_retransmissions=10):
        """
        Initializes a new instance of the Transmitter class.

        Args:
            pin: The pin used for transmitting data. Can be either a Pin object or the pin number.
            pulse_width_us: The pulse width in microseconds. If not provided, the default pulse width of the protocol will be used.
            protocol: The protocol used for transmitting data. Defaults to the first protocol in the list of available protocols.
            num_retransmissions: The number of times to retransmit the data. Defaults to 10.
        """

        if isinstance(pin, Pin):
            self.transmitter_pin = pin
        else:
            self.transmitter_pin = Pin(pin, Pin.OUT)

        if pulse_width_us is None:
            self.pulse_width_us = protocol.pulse_width_us
        else:
            self.pulse_width_us = pulse_width_us

        self.protocol = protocols[protocol - 1]
        self.num_retransmissions = num_retransmissions

    @micropython.native
    def transmit_pulses(self, pulses):
        """
        Transmits a sequence of pulses specified by the given tuple.

        Args:
            pulses: A tuple of pulse durations in multiples of the pulse width.
                    e.g. (5, 10) means for non-inverted signals, that the pin will be set 
                    to high for 5 * pulse width and then to low for 10 * pulse width. 
                    For inverted signals, the pin will be set to low for 5 * pulse width
                    and then to high for 10 * pulse width.

        """
        first_logic_level = 1
        second_logic_level = 0

        if self.protocol.inverted_signal:
            first_logic_level = 0
            second_logic_level = 1

        high_pulse_width = self.pulse_width_us * pulses[0]
        low_pulse_width = self.pulse_width_us * pulses[1]
        transmitter_pin = self.transmitter_pin # Cache object to avoid attribute lookups

        transmitter_pin.value(first_logic_level)
        time.sleep_us(high_pulse_width)
        transmitter_pin.value(second_logic_level)
        time.sleep_us(low_pulse_width)

    @micropython.native
    def send_data(self, data, length, msb_first=True):
        """
        Sends data using the specified protocol.

        Args:
            data: The data to be sent.
            length: The number of bits in the data.
            msb_first: Whether to send the most significant bit first. Defaults to True.

        """
        if msb_first:
            data_range = range(length-1, -1, -1)
        else:
            data_range = range(length)

        for _ in data_range:
            bit = (data >> _) & 1

            if bit == 1:
                self.transmit_pulses(self.protocol.one_pulses)
            else:
                self.transmit_pulses(self.protocol.zero_pulses)

    @micropython.native
    def send(self, data, length=None):
        """
        Sends data multiple times using the specified protocol.

        Args:
            data: The data to be sent. Can be either an integer or a binary string (e.g. "1011").
            length: The number of bits in the data. Required unless data is a binary string.

        """
        if isinstance(data, str):
            length = len(data)
            data = int(data, 2)

        for _ in range(self.num_retransmissions):
            gc.collect() # Avoid gargabe collection during transmission

            # The https://github.com/sui77/rc-switch library sends the sync pulses after the data pulses
            # but e.g. the EV1527 protocol wants the sync pulses to be sent before the data pulses (preamble)
            # However, sending the data pulses first seems to work with >=2 retransmissions
            # while sending the sync pulses first seems to work with >= 3 retransmissions
            self.send_data(data, length)
            self.transmit_pulses(self.protocol.sync_pulses)

        # Disable transmit after sending (i.e., for inverted protocols)
        self.transmitter_pin.value(0)
