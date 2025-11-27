#!/bin/bash
# Automated ESP32 Flashing Script
# Flashes ESPHome firmware to ESP32 for bed BLE control

set -e  # Exit on error

echo "🔧 ESP32 Bed Controller - Automated Flash Script"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root (needed for serial access on some systems)
if [[ $EUID -ne 0 ]] && groups | grep -q dialout; then
   echo -e "${YELLOW}⚠️  User not in 'dialout' group. You may need sudo for serial access.${NC}"
fi

# Detect ESPHome installation
if command -v esphome &> /dev/null; then
    ESPHOME_CMD="esphome"
    echo -e "${GREEN}✅ ESPHome found (standalone)${NC}"
elif command -v docker &> /dev/null && docker image inspect esphome/esphome &> /dev/null; then
    ESPHOME_CMD="docker run --rm -v \"${PWD}\":/config --device=/dev/ttyUSB0 -it esphome/esphome"
    echo -e "${GREEN}✅ ESPHome found (Docker)${NC}"
else
    echo -e "${RED}❌ ESPHome not found!${NC}"
    echo ""
    echo "Install options:"
    echo "  1. pip3 install esphome"
    echo "  2. docker pull esphome/esphome"
    echo ""
    read -p "Install via pip3 now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip3 install esphome
        ESPHOME_CMD="esphome"
    else
        exit 1
    fi
fi

# Detect serial port
echo ""
echo "🔍 Detecting ESP32 serial port..."
SERIAL_PORT=""

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if [ -e /dev/ttyUSB0 ]; then
        SERIAL_PORT="/dev/ttyUSB0"
    elif [ -e /dev/ttyACM0 ]; then
        SERIAL_PORT="/dev/ttyACM0"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    SERIAL_PORT=$(ls /dev/cu.usbserial-* 2>/dev/null | head -n 1)
    if [ -z "$SERIAL_PORT" ]; then
        SERIAL_PORT=$(ls /dev/cu.SLAB_USBtoUART 2>/dev/null | head -n 1)
    fi
fi

if [ -z "$SERIAL_PORT" ]; then
    echo -e "${RED}❌ No ESP32 found. Please connect via USB.${NC}"
    echo ""
    echo "Available ports:"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        ls /dev/tty* 2>/dev/null | grep -E "USB|ACM" || echo "  (none)"
    else
        ls /dev/cu.* 2>/dev/null || echo "  (none)"
    fi
    echo ""
    read -p "Enter serial port manually (or press Enter to exit): " MANUAL_PORT
    if [ -n "$MANUAL_PORT" ]; then
        SERIAL_PORT="$MANUAL_PORT"
    else
        exit 1
    fi
fi

echo -e "${GREEN}✅ Found ESP32 at: $SERIAL_PORT${NC}"

# Ask which config to flash
echo ""
echo "📝 Select configuration to flash:"
echo "  1. bed-ble-proxy.yaml (Simple BLE proxy - recommended first)"
echo "  2. bed-ble-client.yaml (Full controller with commands)"
echo "  3. Custom file path"
echo ""
read -p "Choose (1-3): " CONFIG_CHOICE

case $CONFIG_CHOICE in
    1)
        CONFIG_FILE="esphome/bed-ble-proxy.yaml"
        ;;
    2)
        CONFIG_FILE="esphome/bed-ble-client.yaml"
        if [ ! -f "$CONFIG_FILE" ]; then
            echo -e "${YELLOW}⚠️  bed-ble-client.yaml not found. Copy from .example first.${NC}"
            cp esphome/bed-ble-client.yaml.example "$CONFIG_FILE"
            echo -e "${GREEN}✅ Created bed-ble-client.yaml from template${NC}"
            echo ""
            echo -e "${YELLOW}⚠️  IMPORTANT: Edit this file and update:${NC}"
            echo "   - MAC address (line ~40)"
            echo "   - Service/Characteristic UUIDs"
            echo "   - Command bytes for your bed"
            echo ""
            read -p "Press Enter after editing, or Ctrl+C to abort..."
        fi
        ;;
    3)
        read -p "Enter config file path: " CONFIG_FILE
        ;;
    *)
        echo -e "${RED}❌ Invalid choice${NC}"
        exit 1
        ;;
esac

if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}❌ Config file not found: $CONFIG_FILE${NC}"
    exit 1
fi

# Check for secrets.yaml
if [ ! -f "esphome/secrets.yaml" ]; then
    echo -e "${YELLOW}⚠️  secrets.yaml not found. Creating from template...${NC}"
    cp esphome/secrets.yaml.example esphome/secrets.yaml
    echo -e "${GREEN}✅ Created secrets.yaml${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  REQUIRED: Edit esphome/secrets.yaml with your WiFi credentials!${NC}"
    echo ""
    read -p "Press Enter after editing, or Ctrl+C to abort..."
fi

# Validate secrets.yaml has real values
if grep -q "YourWiFiName\|YOUR_32_BYTE" esphome/secrets.yaml; then
    echo -e "${RED}❌ secrets.yaml contains placeholder values!${NC}"
    echo "Please edit esphome/secrets.yaml with real WiFi credentials and keys."
    exit 1
fi

# Compile check
echo ""
echo "🔨 Compiling firmware..."
if ! $ESPHOME_CMD compile "$CONFIG_FILE"; then
    echo -e "${RED}❌ Compilation failed. Check your YAML syntax.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Compilation successful${NC}"

# Flash
echo ""
echo "📤 Flashing to ESP32..."
echo -e "${YELLOW}   Hold the BOOT button on ESP32 if flash fails${NC}"
echo ""

if $ESPHOME_CMD run "$CONFIG_FILE" --device "$SERIAL_PORT"; then
    echo ""
    echo -e "${GREEN}✅ Flash successful!${NC}"
    echo ""
    echo "🎉 Next steps:"
    echo "  1. ESP32 should connect to your WiFi (check router)"
    echo "  2. Open Home Assistant → Settings → Devices"
    echo "  3. Look for 'Bed BLE Proxy' or 'Bed Controller' to adopt"
    echo "  4. Test with physical remote and monitor logs"
    echo ""
    echo "💡 View logs: esphome logs $CONFIG_FILE --device $SERIAL_PORT"
else
    echo ""
    echo -e "${RED}❌ Flash failed${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  - Hold BOOT button during flash"
    echo "  - Try different USB cable/port"
    echo "  - Install drivers: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers"
    echo "  - Check $SERIAL_PORT is correct"
    exit 1
fi
