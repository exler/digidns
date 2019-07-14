#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import argparse

RED, YELLOW, GREEN, WHITE, END = '\033[91m', '\33[93m', '\033[32m', '\33[97m', '\033[0m'
BANNER = """{}
██████╗  █████╗ ██████╗ ███████╗██████╗  █████╗ ██████╗ ██╗  ██╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
██████╔╝███████║██║  ██║███████╗██████╔╝███████║██████╔╝█████╔╝ 
██╔══██╗██╔══██║██║  ██║╚════██║██╔═══╝ ██╔══██║██╔══██╗██╔═██╗ 
██████╔╝██║  ██║██████╔╝███████║██║     ██║  ██║██║  ██║██║  ██╗
╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
    author: exler | source: https://github.com/EXLER/badspark{}
"""

if __name__ == "__main__":
    # Search script directory and write script names to list
    scripts = os.listdir(os.path.join(os.path.dirname(__file__), "scripts"))

    # Strip the scripts of file extension
    scripts_noext = []
    for el in scripts:
        scripts_noext.append(os.path.splitext(el)[0])

    # Parse arguments
    parser = argparse.ArgumentParser(description="Uploads chosen script to Digispark via serial port.")
    parser.add_argument("-s", "--script", choices=scripts_noext, required=True,
                        help="Script to be uploaded to Digispark.")
    parser.add_argument("-p", "--port", required=True,
                        help="Serial port for the Digispark, i.e. /dev/ttyS0")
    args = parser.parse_args()

    # Create path to script
    script_path = os.path.join(os.path.dirname(__file__), "scripts", scripts[scripts_noext.index(args.script)])

    # Print banner
    print(BANNER.format(RED, WHITE, END))

    # Confirming chosen options
    print("{}Uploading {} to serial port {}...{}\n".format(YELLOW, args.script, args.port, END))

    # Run the upload
    print("\t {}Captured Arduino IDE upload:\n\t------------------------------{}".format(YELLOW, END))
    subprocess.run(["arduino", "--upload", script_path, "--port", args.port],
                   shell=False, check=True)
    print("\t{}------------------------------{}".format(YELLOW, END))

    # Bye!
    print("\n{}Upload complete.{}".format(GREEN, END))
