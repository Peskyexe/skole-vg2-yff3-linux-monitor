#!/bin/bash

# Lager et virtuelt miljø
python3 -m venv .venv

# Aktiverer virtuele miljøet
source .venv/bin/activate

pip3 install psutil