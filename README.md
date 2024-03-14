# 📦 MicroPython RC Switch Package

This package contains an API to send signals over 433/315 Mhz based transmitters.
It is based on the [Arduino library](https://github.com/sui77/rc-switch) from Suat Özgür.

## 📖 Documentation
For more information on the features of this library and how to use them please read the documentation [here](./docs/).

## ✅ Supported Boards

Any board that can run a modern version of MicroPython is supported.
The library uses bit banging and supports that on any available GPIO pin.

## ⚙️ Installation

The easiest way is to use mpremote and mip: `mpremote mip install github:sebromero/micropython-rc-switch`

## 🧑‍💻 Developer Installation

The easiest way is to clone the repository and then run any example using `mpremote`.
The recommended way is to mount the root directory remotly on the board and then running an example script. e.g.

```
 mpremote connect mount src run ./examples/transmit_ev1527.py
```

## 🐛 Reporting Issues

If you encounter any issue, please open a bug report [here](https://github.com/sebromero/micropython-rc-switch/issues). 

## 💪 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 🤙 Contact

For questions, comments, or feedback on this package, please create an issue on this repository.