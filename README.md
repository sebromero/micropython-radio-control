# 📦 MicroPython Radio Control Package

This package contains an API to send signals over 433/315 MHz based transmitters.
It is based on the [Arduino library](https://github.com/sui77/rc-switch) from Suat Özgür.
This is a simple library that is meant to be easy to install and use.
If it doesn't fit your use case there is some related work you may want to check out:

- https://github.com/AdrianCX/pico433mhz
- https://github.com/peterhinch/micropython_remote

## 📖 Documentation

Minimal example for sending a signal:

```py
from radio_control import Transmitter
transmitter = Transmitter("D2") # Transmitter connected to pin D2
transmitter.send("001110101101011101100010") # Send 24bit code retrieved from remote control
```

By default the transmitter uses a protocol that works for many low cost remote control devices such as rc sockets (e.g. using the popular EV1527 encoder).
The protocol that shall be used can be changed through a parameter in the constructor.
For more information on the features of this library and how to use them please read the documentation [here](./docs/).

## ✅ Supported Microcontroller Boards

Any board that can run a modern version of MicroPython is supported.
The library uses bit banging and supports that on any available GPIO pin.

## ⚙️ Installation

The easiest way is to use mpremote and mip: 
```bash
mpremote mip install github:sebromero/micropython-radio-control
```

## 🧑‍💻 Developer Installation

The easiest way is to clone the repository and then run any example using `mpremote`.
The recommended way is to mount the root directory remotly on the board and then running an example script. e.g.

```bash
 mpremote connect mount src run ./examples/transmit_ev1527.py
```

## 🐛 Reporting Issues

If you encounter any issue, please open a bug report [here](https://github.com/sebromero/micropython-radio-control/issues). 

## 💪 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 🤙 Contact

For questions, comments, or feedback on this package, please create an issue on this repository.