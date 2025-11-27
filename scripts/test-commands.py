#!/usr/bin/env python3
"""
BLE Command Tester for Adjustable Beds
Test command byte sequences before adding them to ESPHome
Helps verify commands work correctly
"""

import asyncio
import sys
import time

try:
    from bleak import BleakClient
except ImportError:
    print("❌ Error: 'bleak' library not installed")
    print("Install with: pip3 install bleak")
    sys.exit(1)


# Known command sets (update with your bed's values)
COMMAND_SETS = {
    "Richmat": {
        "service": "0000FFE0-0000-1000-8000-00805f9b34fb",
        "characteristic": "0000FFE1-0000-1000-8000-00805f9b34fb",
        "commands": {
            "head_up": "40 02 70 00 01 0B 02 40",
            "head_down": "40 02 70 00 02 0B 02 40",
            "foot_up": "40 02 71 00 01 0B 02 40",
            "foot_down": "40 02 71 00 02 0B 02 40",
            "stop": "40 02 73 00 00 0B 40",
            "flat": "40 02 72 00 01 0B 02 40",
            "zero_g": "40 02 72 00 04 0B 02 40",
            "anti_snore": "40 02 72 00 02 0B 02 40",
            "light": "40 02 74 00 01 0B 02 40",
        }
    },
    # Add other bed types here
}


async def send_command(address: str, service_uuid: str, char_uuid: str, 
                      hex_bytes: str, repeat: int = 1, delay: float = 0.3):
    """
    Send a BLE command to the bed
    
    Args:
        address: BLE MAC address
        service_uuid: Service UUID
        char_uuid: Characteristic UUID
        hex_bytes: Command as hex string (e.g., "40 02 70 00 01")
        repeat: Number of times to send (for hold-to-move commands)
        delay: Delay between repeats in seconds
    """
    try:
        # Convert hex string to bytes
        cmd_bytes = bytes.fromhex(hex_bytes.replace(" ", ""))
        
        print(f"📡 Connecting to {address}...")
        
        async with BleakClient(address, timeout=15.0) as client:
            if not client.is_connected:
                print("❌ Failed to connect")
                return False
            
            print(f"✅ Connected")
            print(f"📤 Sending command: {' '.join(f'{b:02x}' for b in cmd_bytes)}")
            
            for i in range(repeat):
                if repeat > 1:
                    print(f"   Attempt {i+1}/{repeat}...", end="\r")
                
                await client.write_gatt_char(char_uuid, cmd_bytes, response=False)
                
                if i < repeat - 1:  # Don't delay after last send
                    await asyncio.sleep(delay)
            
            if repeat > 1:
                print()  # New line after progress
            
            print("✅ Command sent successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_hold_pattern(address: str, service_uuid: str, char_uuid: str,
                           hex_bytes: str, duration: float = 3.0):
    """
    Test a hold-to-move command pattern (typical for bed motors)
    Sends command repeatedly for specified duration
    """
    print(f"🎯 Testing hold pattern for {duration} seconds...")
    
    cmd_bytes = bytes.fromhex(hex_bytes.replace(" ", ""))
    
    async with BleakClient(address) as client:
        start_time = time.time()
        count = 0
        
        while time.time() - start_time < duration:
            await client.write_gatt_char(char_uuid, cmd_bytes, response=False)
            count += 1
            elapsed = time.time() - start_time
            print(f"   Sending... {elapsed:.1f}s / {duration}s (count: {count})", end="\r")
            await asyncio.sleep(0.3)  # 300ms between sends
        
        print(f"\n✅ Sent {count} commands over {duration} seconds")


def interactive_test():
    """Interactive command testing"""
    print("🧪 BLE Command Tester\n")
    
    # Get connection details
    address = input("Enter bed MAC address: ").strip()
    
    print("\nKnown bed types:")
    for i, bed_type in enumerate(COMMAND_SETS.keys(), 1):
        print(f"{i}. {bed_type}")
    print(f"{len(COMMAND_SETS) + 1}. Custom")
    
    choice = input("\nSelect bed type: ").strip()
    
    if choice.isdigit() and int(choice) <= len(COMMAND_SETS):
        bed_type = list(COMMAND_SETS.keys())[int(choice) - 1]
        config = COMMAND_SETS[bed_type]
        service_uuid = config["service"]
        char_uuid = config["characteristic"]
        commands = config["commands"]
    else:
        service_uuid = input("Enter service UUID: ").strip()
        char_uuid = input("Enter characteristic UUID: ").strip()
        
        # Normalize short UUIDs
        if len(service_uuid) == 4:
            service_uuid = f"0000{service_uuid}-0000-1000-8000-00805f9b34fb"
        if len(char_uuid) == 4:
            char_uuid = f"0000{char_uuid}-0000-1000-8000-00805f9b34fb"
        
        commands = {}
    
    # Test loop
    while True:
        print("\n" + "="*60)
        print("Available commands:")
        
        if commands:
            for i, (name, hex_val) in enumerate(commands.items(), 1):
                print(f"{i}. {name.replace('_', ' ').title()}")
            print(f"{len(commands) + 1}. Custom command")
            print(f"{len(commands) + 2}. Test hold pattern")
            print(f"{len(commands) + 3}. Exit")
        else:
            print("1. Send custom command")
            print("2. Test hold pattern")
            print("3. Exit")
        
        cmd_choice = input("\nChoose command: ").strip()
        
        if commands and cmd_choice.isdigit():
            idx = int(cmd_choice)
            
            if idx <= len(commands):
                cmd_name = list(commands.keys())[idx - 1]
                hex_bytes = commands[cmd_name]
                
                print(f"\n🎯 Testing: {cmd_name.replace('_', ' ').title()}")
                print(f"📝 Bytes: {hex_bytes}")
                
                repeat = 1
                if "up" in cmd_name or "down" in cmd_name:
                    duration = input("Hold duration in seconds (default 2): ").strip()
                    duration = float(duration) if duration else 2.0
                    repeat = int(duration / 0.3)  # 300ms between commands
                
                asyncio.run(send_command(address, service_uuid, char_uuid, 
                                       hex_bytes, repeat=repeat))
                
            elif idx == len(commands) + 1:  # Custom
                hex_bytes = input("Enter hex bytes: ").strip()
                asyncio.run(send_command(address, service_uuid, char_uuid, hex_bytes))
                
            elif idx == len(commands) + 2:  # Hold pattern
                hex_bytes = input("Enter hex bytes: ").strip()
                duration = float(input("Duration (seconds): ").strip())
                asyncio.run(test_hold_pattern(address, service_uuid, char_uuid, 
                                             hex_bytes, duration))
                
            elif idx == len(commands) + 3:  # Exit
                break
        
        elif cmd_choice in ["1", "2", "3"] and not commands:
            if cmd_choice == "1":
                hex_bytes = input("Enter hex bytes: ").strip()
                asyncio.run(send_command(address, service_uuid, char_uuid, hex_bytes))
            elif cmd_choice == "2":
                hex_bytes = input("Enter hex bytes: ").strip()
                duration = float(input("Duration (seconds): ").strip())
                asyncio.run(test_hold_pattern(address, service_uuid, char_uuid, 
                                             hex_bytes, duration))
            else:
                break


def batch_test():
    """Test all commands in sequence"""
    print("🔄 Batch Command Test\n")
    
    address = input("Enter bed MAC address: ").strip()
    
    print("\nKnown bed types:")
    for i, bed_type in enumerate(COMMAND_SETS.keys(), 1):
        print(f"{i}. {bed_type}")
    
    choice = input("\nSelect bed type: ").strip()
    
    if not (choice.isdigit() and int(choice) <= len(COMMAND_SETS)):
        print("❌ Invalid selection")
        return
    
    bed_type = list(COMMAND_SETS.keys())[int(choice) - 1]
    config = COMMAND_SETS[bed_type]
    
    print(f"\n🔄 Testing all {bed_type} commands...")
    print("⚠️  Watch your bed carefully and be ready to stop!\n")
    input("Press Enter to continue (Ctrl+C to abort)...")
    
    results = {}
    
    for cmd_name, hex_bytes in config["commands"].items():
        print(f"\n▶️  Testing: {cmd_name.replace('_', ' ').title()}")
        print(f"   Bytes: {hex_bytes}")
        
        success = asyncio.run(send_command(
            address, 
            config["service"],
            config["characteristic"],
            hex_bytes
        ))
        
        results[cmd_name] = "✅" if success else "❌"
        
        await asyncio.sleep(2)  # Delay between tests
    
    print("\n" + "="*60)
    print("📊 Test Results:")
    print("="*60)
    for cmd, status in results.items():
        print(f"{status} {cmd.replace('_', ' ').title()}")


if __name__ == "__main__":
    print("🧪 BLE Command Tester for Adjustable Beds")
    print("="*60)
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        sys.exit(1)
    
    print("\n1. Interactive testing (recommended)")
    print("2. Batch test all commands")
    
    mode = input("\nChoose mode: ").strip()
    
    try:
        if mode == "1":
            interactive_test()
        elif mode == "2":
            asyncio.run(batch_test())
        else:
            print("❌ Invalid choice")
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
