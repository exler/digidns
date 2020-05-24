<p align="center"><img src="logo.png"></p>

# DigiDNS
DigiDNS uses Digispark's keyboard emulation on unblocked machines and overrides Windows DNS settings, pointing it to a custom Python server that spoofs chosen hosts.

## Requirements

* Arduino IDE >= 1.6.5 ([configured for Digispark](https://digistump.com/wiki/digispark/tutorials/connecting))
* Python 3

## Usage

### Host machine

Install Python dependency.
```bash
$ pip install dnslib
```

Change the `DNS_SERVER` constant in `digidns_windows.ino` file, then upload it to Digispark using Arduino IDE.  
Use the `--target` and `--source` parameters to add spoofed hosts and run the Python server.
```bash
$ sudo python3 digidns.py [-i | --show-ip] [-s | --source] [-t | --target]
```
### Target machine

Connect the Digispark to an unblocked Windows machine. When the built-in LED starts blinking the script is done and you can disconnect it.

## License

Copyright (c) 2019 by ***Kamil Marut***.

*digidns* is under the terms of the [MIT License](https://tldrlegal.com/license/mit-license), following all clarifications stated in the [license file](LICENSE).
