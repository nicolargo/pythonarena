#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rich import print
from rich.columns import Columns
from rich.panel import Panel
from rich.layout import Layout

p1 = Panel("Hello, [red]World!", title="Welcome 1", subtitle="Thank you")
p2 = Panel("Hello, [red]World!", title="Welcome 2", subtitle="Thank you")
p3 = Panel("Hello, [red]World!", title="Welcome 3", subtitle="Thank you")

layout = Layout()
layout.split_column(
    Layout(p1, name="upper"),
    Layout(name="lower")
)
layout["lower"].split_row(
    Layout(p2, name="left"),
    Layout(p3, name="right"),
)

print(layout)

