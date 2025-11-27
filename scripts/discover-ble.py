#!/usr/bin/env python3
"""
BLE Device Discovery Tool for Adjustable Beds
Scans for Bluetooth Low Energy devices and displays their services/characteristics
Use this to find your bed's MAC address, service UUIDs, and characteristic UUIDs
"""

import asyncio
import sys
from typing import Dict, List

try:
    from bleak import BleakScanner, BleakClient
except ImportError:
    print("❌ Error: 'bleak' library not installed")
    print("Install with: pip3 install bleak")
    sys.exit(1)


async def discover_devices():
    """Scan for BLE devices"""
    print("🔍 Scanning for BLE devices (10 seconds)...\n")
    
    devices = await BleakScanner.discover(timeout=10.0)
    
    if not devices:
        print("❌ No BLE devices found. Make sure:")
        print("   - Your bed controller is powered on")
        print("   - You're within Bluetooth range (< 30 feet)")
        print("   - Bluetooth is enabled on this computer")
        return []
    
    print(f"✅ Found {len(devices)} BLE devices:\n")
    
    for i, device in enumerate(devices, 1):
        name = device.name or "Unknown"
        rssi = device.rssi if hasattr(device, 'rssi') else "N/A"
        print(f"{i}. {name}")
        print(f"   MAC: {device.address}")
        print(f"   Signal: {rssi} dBm")
        print()
    
    return devices


async def explore_device(address: str):
    """Connect to device and list all services/characteristics"""
    print(f"\n🔗 Connecting to {address}...\n")
    
    try:
        async with BleakClient(address, timeout=20.0) as client:
            if not client.is_connected:
                print("❌ Failed to connect")
                return
            
            print("✅ Connected! Discovering services...\n")
            
            for service in client.services:
                print(f"📦 Service: {service.uuid}")
                print(f"   Description: {service.description}")
                
                for char in service.characteristics:
                    props = ", ".join(char.properties)
                    print(f"   ├─ Characteristic: {char.uuid}")
                    print(f"   │  Properties: {props}")
                    
                    # Try to read value if readable
                    if "read" in char.properties:
                        try:
                            value = await client.read_gatt_char(char.uuid)
                            print(f"   │  Current Value: {value.hex()}")
                        except Exception:
                            print(f"   │  Current Value: (unable to read)")
                    
                    # List descriptors
                    if char.descriptors:
                        for desc in char.descriptors:
                            print(f"   │  └─ Descriptor: {desc.uuid}")
                
                print()
            
            print("\n💡 Common bed controller patterns:")
            print("   - Service UUID often starts with 0xFFE0 or custom vendor UUID")
            print("   - Writable characteristic for commands (usually 0xFFE1)")
            print("   - Look for properties: 'write', 'write-without-response', 'notify'")
            
    except Exception as e:
        print(f"❌ Error: {e}")


async def monitor_notifications(address: str, service_uuid: str, char_uuid: str):
    """Monitor characteristic for notifications (useful to see remote button presses)"""
    print(f"\n📡 Monitoring {char_uuid} for notifications...")
    print("Press buttons on your physical remote and watch for data:\n")
    
    def notification_handler(sender, data):
        """Handle received notifications"""
        hex_data = " ".join(f"{b:02x}" for b in data)
        print(f"📩 Received: [{hex_data}]")
    
    try:
        async with BleakClient(address) as client:
            await client.start_notify(char_uuid, notification_handler)
            
            # Monitor for 60 seconds
            for i in range(60, 0, -1):
                print(f"⏱️  Monitoring... ({i}s remaining)", end="\r")
                await asyncio.sleep(1)
            
            await client.stop_notify(char_uuid)
            print("\n\n✅ Monitoring complete")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")


async def test_write(address: str, service_uuid: str, char_uuid: str, hex_value: str):
    """Test writing a command to a characteristic"""
    print(f"\n✍️  Writing to {char_uuid}...")
    
    try:
        # Convert hex string to bytes
        value_bytes = bytes.fromhex(hex_value.replace("0x", "").replace(" ", ""))
        print(f"   Data: {' '.join(f'{b:02x}' for b in value_bytes)}")
        
        async with BleakClient(address) as client:
            await client.write_gatt_char(char_uuid, value_bytes, response=False)
            print("✅ Write successful!")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def print_menu():
    """Display interactive menu"""
    print("\n" + "="*60)
    print("🛏️  BLE Bed Controller Discovery Tool")
    print("="*60)
    print("\n1. Scan for BLE devices")
    print("2. Explore device (list services/characteristics)")
    print("3. Monitor notifications (see button presses)")
    print("4. Test write command")
    print("5. Quick reference: Common bed commands")
    print("6. Exit")
    print()


def show_common_commands():
    """Display known command bytes for common bed controllers"""
    print("\n" + "="*60)
    print("📖 Common Bed Controller Commands")
    print("="*60)
    print("\n⚠️  These are examples from Richmat controllers.")
    print("Your bed may use different values - always verify with nRF Connect!\n")
    
    commands = {
        "Head Up": "40 02 70 00 01 0B 02 40",
        "Head Down": "40 02 70 00 02 0B 02 40",
        "Foot Up": "40 02 71 00 01 0B 02 40",
        "Foot Down": "40 02 71 00 02 0B 02 40",
        "Stop": "40 02 73 00 00 0B 40",
        "Flat": "40 02 72 00 01 0B 02 40",
        "Zero-G": "40 02 72 00 04 0B 02 40",
        "Anti-Snore": "40 02 72 00 02 0B 02 40",
        "Light": "40 02 74 00 01 0B 02 40",
    }
    
    print("Common Service UUID: 0xFFE0")
    print("Common Characteristic UUID: 0xFFE1\n")
    
    for cmd_name, hex_bytes in commands.items():
        print(f"  {cmd_name:15} → {hex_bytes}")
    
    print("\n💡 To test a command:")
    print("   1. Choose option 4 from main menu")
    print("   2. Enter your bed's MAC address")
    print("   3. Enter service UUID (e.g., FFE0)")
    print("   4. Enter characteristic UUID (e.g., FFE1)")
    print("   5. Paste command bytes (spaces optional)")
    print()


async def main():
    """Main interactive loop"""
    devices = []
    
    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()
        
        if choice == "1":
            devices = await discover_devices()
            
        elif choice == "2":
            if not devices:
                print("⚠️  Run scan first (option 1)")
                continue
            
            print("\nAvailable devices:")
            for i, dev in enumerate(devices, 1):
                print(f"{i}. {dev.name or 'Unknown'} ({dev.address})")
            
            idx = input("\nSelect device number (or enter MAC address): ").strip()
            
            if idx.isdigit() and 1 <= int(idx) <= len(devices):
                address = devices[int(idx) - 1].address
            else:
                address = idx
            
            await explore_device(address)
            
        elif choice == "3":
            address = input("Enter device MAC address: ").strip()
            service = input("Enter service UUID (e.g., FFE0): ").strip()
            char = input("Enter characteristic UUID (e.g., FFE1): ").strip()
            
            # Normalize UUIDs
            if len(service) == 4:
                service = f"0000{service}-0000-1000-8000-00805f9b34fb"
            if len(char) == 4:
                char = f"0000{char}-0000-1000-8000-00805f9b34fb"
            
            await monitor_notifications(address, service, char)
            
        elif choice == "4":
            address = input("Enter device MAC address: ").strip()
            service = input("Enter service UUID (e.g., FFE0): ").strip()
            char = input("Enter characteristic UUID (e.g., FFE1): ").strip()
            hex_val = input("Enter hex bytes (e.g., 40 02 73 00 00 0B 40): ").strip()
            
            # Normalize UUIDs
            if len(service) == 4:
                service = f"0000{service}-0000-1000-8000-00805f9b34fb"
            if len(char) == 4:
                char = f"0000{char}-0000-1000-8000-00805f9b34fb"
            
            await test_write(address, service, char, hex_val)
            
        elif choice == "5":
            show_common_commands()
            
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    print("🛏️  BLE Bed Discovery Tool")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        sys.exit(1)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
