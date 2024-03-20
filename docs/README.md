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

## 📡 Protocols

| Puls width | Sync Pulses | Zero Pulses | One Pulses | Inverted | Description                  |
|------------|-------------|-------------|------------|----------|----------------------------- |
| 350        | (  1, 31 )  | (  1,  3 )  | (  3,  1 ) | False    | Protocol 1 (e.g. EV1527)     |
| 650        | (  1, 10 )  | (  1,  2 )  | (  2,  1 ) | False    | Protocol 2                   |
| 100        | ( 30, 71 )  | (  4, 11 )  | (  9,  6 ) | False    | Protocol 3                   |
| 380        | (  1,  6 )  | (  1,  3 )  | (  3,  1 ) | False    | Protocol 4                   |
| 500        | (  6, 14 )  | (  1,  2 )  | (  2,  1 ) | False    | Protocol 5                   |
| 450        | ( 23,  1 )  | (  1,  2 )  | (  2,  1 ) | True     | Protocol 6 (HT6P20B)         |
| 150        | (  2, 62 )  | (  1,  6 )  | (  6,  1 ) | False    | Protocol 7 (HS2303-PT)       |
| 200        | (  3, 130)  | (  7, 16 )  | (  3,  16) | False    | Protocol 8 Conrad RS-200 RX  |
| 200        | ( 130, 7 )  | (  16, 7 )  | ( 16,  3 ) | True     | Protocol 9 Conrad RS-200 TX  |
| 365        | ( 18,  1 )  | (  3,  1 )  | (  1,  3 ) | True     | Protocol 10 (1ByOne Doorbell)|
| 270        | ( 36,  1 )  | (  1,  2 )  | (  2,  1 ) | True     | Protocol 11 (HT12E)          |
| 320        | ( 36,  1 )  | (  1,  2 )  | (  2,  1 ) | True     | Protocol 12 (SM5212)         |

## 👀 Examples

The following scripts are examples of how to use this package with a transmitter module:

- [transmit_ev1527.py](../examples/transmit_ev1527.py): Shows how to send data either as an integer or as a string consisting of ones and zeroes.
