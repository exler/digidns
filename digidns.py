#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import socket
import dnslib
import json
from urllib.request import urlopen

RED, YELLOW, GREEN, WHITE, END = '\033[91m', '\33[93m', '\033[32m', '\33[97m', '\033[0m'
BANNER = """{}
    ██████╗ ██╗ ██████╗ ██╗██████╗ ███╗   ██╗███████╗
    ██╔══██╗██║██╔════╝ ██║██╔══██╗████╗  ██║██╔════╝
    ██║  ██║██║██║  ███╗██║██║  ██║██╔██╗ ██║███████╗
    ██║  ██║██║██║   ██║██║██║  ██║██║╚██╗██║╚════██║
    ██████╔╝██║╚██████╔╝██║██████╔╝██║ ╚████║███████║
    ╚═════╝ ╚═╝ ╚═════╝ ╚═╝╚═════╝ ╚═╝  ╚═══╝╚══════╝
    author: exler | source: https://github.com/EXLER/digidns
{}"""

def get_ip():
    # Get current public IP
    ip = urlopen('https://ident.me').read().decode('utf8')
    return ip

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Fake DNS server that spoofs specific hosts.")
    parser.add_argument('-i', '--show-ip', action='store_true', 
                        help="Show public IP address of this machine.")
    parser.add_argument('-s', '--source',
                        help="Domain of host to be spoofed.")
    parser.add_argument('-t', '--target',
                        help="IP address of target machine.")
    args = parser.parse_args()

    if args.show_ip:
        print(f"Your current IP address: {get_ip()}")

    elif args.source and args.target:
        if os.path.isfile('hosts.json'):
            with open('hosts.json', 'r') as f:
                data = json.load(f)
                data['hosts'].append({
                    'source': args.source,
                    'target': args.target
                })
            with open('hosts.json', 'w+') as f:
                json.dump(data, f, indent=4)
        else:
            with open('hosts.json', 'w') as f:
                data = {}
                data['hosts'] = []
                data['hosts'].append({
                    'source': args.source,
                    'target': args.target
                })
                json.dump(data, f, indent=4)
    
    elif (args.source and not args.target) or (args.target and not args.source):
        print("[!] Please supply both the source and target addresses.")

    else:
        # Print banner
        print(BANNER.format(RED, WHITE, END))

        # Load hosts
        if os.path.isfile('hosts.json'):
            with open('hosts.json', 'r') as f:
                data = json.load(f)
                hosts = data['hosts']
        else:
            print("[!] No 'hosts.json' file! Aborting..")
            raise SystemExit

        try:
            udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_s.bind(('localhost', 53))
        except:
            print("[!] Error while trying to bind socket to port 53. Please try again with root privileges.")
            raise SystemExit
        
        print("[!] Listening on localhost:53...")

        try:
            while True:
                data, addr = udp_s.recvfrom(1024)
                d = dnslib.DNSRecord.parse(data)

                for question in d.questions:
                    qdom = question.get_qname()
                    r = d.reply()

                    try:
                        for host in hosts:
                            if qdom.idna() == host['source']:
                                ip = host['target']
                                break
                            else:
                                ip = socket.gethostbyname(qdom.idna())
                    except Exception as e:
                        print(f"Exception caught: {e}")
                        ip = '127.0.0.1'
                    
                    r.add_answer(dnslib.RR(qdom, rdata=dnslib.A(ip), ttl=30))
                    print(f"[+] Request {qdom.idna()} -> {ip}")
        except KeyboardInterrupt:
            print("[!] Closing DNS server..")

        udp_s.close()

