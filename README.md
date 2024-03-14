# Transmitter

```py
# Example usage with adjustable pulse width, encoding option, and number of retransmissions
transmitter = Transmitter("D2", pulse_width_us=315)  # Adjust parameters as needed

# Example address and command
address = 0b00011110110101110110
command = 0b0010
data = (address << 4) | command
transmitter.send(data, 24)

# Transmit the data
transmitter.send("000111101101011101100010")
```