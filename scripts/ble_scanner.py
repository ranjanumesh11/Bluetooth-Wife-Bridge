#!/usr/bin/env python3
"""
ble_scanner.py — BLE Discovery Helper for Sven & Son Adjustable Bed
=====================================================================
Scans for nearby BLE devices, connects to a selected device, and dumps
all GATT services and characteristics. Optionally subscribes to all
notify/indicate characteristics to capture incoming data (position feedback).

Requirements:
    pip install bleak

Usage:
    python ble_scanner.py                  # Scan and list devices
    python ble_scanner.py --mac AA:BB:...  # Connect directly by MAC
    python ble_scanner.py --scan-only      # Just print nearby devices
"""

import asyncio
import argparse
import logging
import sys
from bleak import BleakScanner, BleakClient
from bleak.exc import BleakError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

SCAN_DURATION = 10  # seconds


async def scan_devices() -> list:
    """Scan for BLE devices and return a sorted list."""
    log.info(f"Scanning for BLE devices for {SCAN_DURATION} seconds...")
    devices = await BleakScanner.discover(timeout=SCAN_DURATION)
    devices.sort(key=lambda d: d.rssi, reverse=True)  # Strongest signal first
    return devices


def print_devices(devices: list) -> None:
    """Pretty-print discovered devices."""
    print(f"\n{'='*60}")
    print(f"  Found {len(devices)} BLE device(s)")
    print(f"{'='*60}")
    print(f"  {'#':<4} {'MAC Address':<20} {'RSSI':<8} Name")
    print(f"  {'-'*55}")
    for i, d in enumerate(devices):
        name = d.name or "(unknown)"
        print(f"  {i:<4} {d.address:<20} {d.rssi:<8} {name}")
    print()


def notification_handler(sender, data):
    """Callback for incoming BLE notifications."""
    hex_data = " ".join(f"{b:02X}" for b in data)
    log.info(f"  ← NOTIFY from {sender}: [{hex_data}]")


async def explore_device(mac_address: str) -> None:
    """Connect to a device and dump all GATT services and characteristics."""
    log.info(f"Connecting to {mac_address}...")

    try:
        async with BleakClient(mac_address, timeout=15.0) as client:
            log.info(f"Connected: {client.is_connected}")

            print(f"\n{'='*60}")
            print(f"  GATT Profile for {mac_address}")
            print(f"{'='*60}\n")

            notify_chars = []

            for service in client.services:
                print(f"  SERVICE: {service.uuid}")
                print(f"    Description: {service.description}")

                for char in service.characteristics:
                    props = ", ".join(char.properties)
                    print(f"\n    CHARACTERISTIC: {char.uuid}")
                    print(f"      Handle:     {char.handle}")
                    print(f"      Properties: {props}")
                    print(f"      Description:{char.description}")

                    # Try to read readable characteristics
                    if "read" in char.properties:
                        try:
                            value = await client.read_gatt_char(char.uuid)
                            hex_val = " ".join(f"{b:02X}" for b in value)
                            print(f"      Value:      [{hex_val}]")
                        except BleakError as e:
                            print(f"      Value:      (read error: {e})")

                    # Collect notifiable characteristics
                    if "notify" in char.properties or "indicate" in char.properties:
                        notify_chars.append(char.uuid)

                    for descriptor in char.descriptors:
                        print(f"      DESCRIPTOR: {descriptor.uuid} (handle {descriptor.handle})")

                print()

            # Subscribe to all notify/indicate characteristics
            if notify_chars:
                print(f"\n  Subscribing to {len(notify_chars)} notify characteristic(s).")
                print("  Press Ctrl+C to stop. Try pressing buttons on the physical remote now.\n")
                for uuid in notify_chars:
                    await client.start_notify(uuid, notification_handler)
                    log.info(f"  Subscribed to {uuid}")

                try:
                    await asyncio.sleep(30)  # Listen for 30 seconds
                except asyncio.CancelledError:
                    pass
                finally:
                    for uuid in notify_chars:
                        try:
                            await client.stop_notify(uuid)
                        except Exception:
                            pass
            else:
                print("  No notify/indicate characteristics found.")
                print("  To capture write commands, use Android HCI snoop log + Wireshark.")
                print("  See docs/BLE_SCANNING.md for instructions.\n")

    except BleakError as e:
        log.error(f"BLE error: {e}")
        sys.exit(1)
    except asyncio.TimeoutError:
        log.error("Connection timed out. Is the bed powered on and in range?")
        sys.exit(1)


async def main(args) -> None:
    if args.mac:
        await explore_device(args.mac)
        return

    devices = await scan_devices()
    if not devices:
        log.warning("No devices found. Make sure Bluetooth is enabled and bed is powered on.")
        return

    print_devices(devices)

    if args.scan_only:
        return

    # Interactive selection
    print("Enter the device number to connect and explore (or press Enter to exit): ", end="")
    try:
        choice = input().strip()
        if not choice:
            return
        idx = int(choice)
        if 0 <= idx < len(devices):
            await explore_device(devices[idx].address)
        else:
            log.error(f"Invalid selection: {idx}")
    except (ValueError, EOFError):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="BLE discovery helper for Sven & Son adjustable bed bridge",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--mac",
        type=str,
        help="MAC address to connect to directly (e.g. AA:BB:CC:DD:EE:FF)",
    )
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="Only list nearby devices, do not connect",
    )
    args = parser.parse_args()

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("\nScan interrupted.")
