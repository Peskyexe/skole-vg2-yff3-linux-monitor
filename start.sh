#!/bin/bash

# Liste for å holde følge på Python prosess ID-er
pids=()

# Definerer en cleanup funksjon til å stoppe alle python scripts som kjører i bakgrunnen
cleanup() {
    echo -e "\n[!] Ctrl+C detected. Stopping background Python scripts and shutting down the dashboard..."

    kill "${pids[@]}" 2>/dev/null 
    wait "${pids[@]}" 2>/dev/null

    echo "[+] All Python scripts stopped, dashboard shutdown."

    exit 0
}

# Tilordner cleanup funksjonen til avslutnings- og avbruddssignaler
trap cleanup EXIT INT TERM

# Aktiverer virtuele miljøet for python moduler
source .venv/bin/activate

# Starer scriptsa og lagrer PID-ene deres
python3 src/collector.py &
pids+=($!)

python3 -m http.server 8000 &
pids+=($!)

echo "[+] Dashboard available at 'http://localhost:8000'. Press Ctrl + C to shutdown."
wait