# SD CodeFree Reader

> Download, decode and export measurements from **SD CodeFree** blood glucose meters using the original USB serial cable.

Python application for communicating with **SD CodeFree** blood glucose meters through the original USB serial cable. The project is the result of reverse engineering the communication protocol and provides a complete solution for downloading and exporting stored measurements.

## Features

* Automatic serial port detection
* Automatic handshake
* Full memory download
* Date, time and glucose decoding
* JSON export
* CSV export
* Optional protocol analysis tools for reverse engineering

## Project status

**Current status:** Stable

Implemented features:

* Automatic serial port detection
* Automatic handshake
* Full memory download
* Record decoding
* JSON export
* CSV export
* Protocol analysis tools

Known limitations:

* The meter displays **E-5 Communication Error** after the transfer is complete. This does not affect the downloaded data and is believed to be related to the protocol session termination.

## Project structure

```text
main.py
protocol.py
decoder.py
protocol_analysis.py
constants.py
models.py
export_csv.py
output/
README.md
LICENSE
```

## Requirements

* Python 3.13 or newer
* pyserial

Install the required package:

```bash
pip install pyserial
```

## Usage

Run the application:

```bash
python main.py
```

The program will:

1. Detect the USB serial adapter.
2. Connect to the meter.
3. Download all stored measurements.
4. Decode the records.
5. Export the results to:

```text
output/readings.json
output/readings.csv
```

## Supported devices

* SD CodeFree blood glucose meter

## Hardware

The application communicates with the SD CodeFree blood glucose meter using the original USB serial cable.

![SD CodeFree connected to PC](docs/images/sd_codefree_connection.jpg)

The meter enters **PC mode** when connected, allowing the stored measurements to be downloaded over the serial interface.

## Notes

The communication protocol has been reverse engineered from the original device.

Some protocol fields are still under investigation. However, memory download, record decoding and data export are fully functional.

The project also contains optional protocol analysis tools that can be enabled during development to assist with reverse engineering and protocol validation.

## Acknowledgements

This project was inspired by the reverse engineering work of **Diego Elio Pettenò** and the **glucometer-protocols** project:

https://github.com/Flameeyes/glucometer-protocols

The original documentation and research were valuable in understanding the SD CodeFree communication protocol.

This project is an independent Python implementation with additional protocol analysis, automatic serial port detection, JSON/CSV export and a modular code structure.

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
