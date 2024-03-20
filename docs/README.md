# 📖 Documentation

## ✨ Features

This library supports transmitting signals over a sub 1GHz signal (433 / 315 MHz).

## 💻 Usage

To use this library you can import the `Transmitter` class from the main module.
Then you need to initialize the transmitter object which allows you to send signals.
You can adjust `pulse_width_us` to match your specific receiver. `num_retransmissions` can be increased to improve the robustness of the signal transmission. You need to specify to which pin your transmitter is connected. This can be either a string or a `Pin` object.

```py
from radio_control import Transmitter
transmitter = Transmitter("D2", pulse_width_us=315, num_retransmissions=5)
transmitter.send("001110101101011101100010")
```

## 👀 Examples

The following scripts are examples of how to use this package with a transmitter module:

- [transmit_ev1527.py](../examples/transmit_ev1527.py): Shows how to send data either as an integer or as a string consisting of ones and zeroes.
