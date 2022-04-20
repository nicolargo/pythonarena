#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from rich import print
from rich.columns import Columns
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich.live import Live

from keyboard import KBHit

console = Console()
layout = Layout()
p1 = Panel("Hello, [red]World!", title="Welcome 1", subtitle="Thank you")
p2 = Panel("Hello, [red]World!", title="Welcome 2", subtitle="Thank you")
p3 = Panel("Hello, [red]World!", title="Welcome 3", subtitle="Thank you")
layout.split_column(
    Layout(p1, name="upper"),
    Layout(name="lower")
)
layout["lower"].split_row(
    Layout(p2, name="left"),
    Layout(p3, name="right"),
)

# Main

kb = KBHit()
with Live(console=console, screen=True, auto_refresh=False) as live:
    while True:
        live.update(layout, refresh=True)
        if kb.kbhit():
            c = kb.getch()
            if ord(c) == 27: # ESC
                break
        time.sleep(1)
kb.set_normal_term()
