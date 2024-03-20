from radio_control import Transmitter

# Example usage with adjustable pulse width and number of retransmissions
# By default, the transmitter will use protocol 1 (EV1527)
# When the pulse width is not specified, the default pulse width of the protocol will be used
transmitter = Transmitter("D2", pulse_width_us=315, num_retransmissions=5)  # Adjust parameters as needed

# Example address and command
address = 0b00111010110101110110 # 20 bit address
command = 0b0010 # 4 bit command
data = (address << 4) | command

# Send the data as a 24 bit integer (length needs to be specified)
transmitter.send(data, 24)

# ... or transmit the data as a string (length is automatically determined)
transmitter.send("001110101101011101100010")