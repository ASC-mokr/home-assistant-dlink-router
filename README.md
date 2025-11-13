# D-Link Router Integration for Home Assistant

Home Assistant custom integration for managing D-Link DIR-825 router.

## Features

- 📊 Monitor CPU Load (1, 5, 15 minutes)
- 💾 Monitor Memory Usage
- 📡 Monitor Traffic RX/TX per interface
- 🖥️ Monitor Connected Devices
- ⏱️ Monitor Uptime
- 🔌 Enable/Disable Interfaces
- 🔄 Reboot Router
- 🎯 Device Tracking

## Installation

### Manual

1. Copy `dlink_router` folder to `~/.homeassistant/custom_components/`
2. Restart Home Assistant
3. Go to **Settings → Devices & Services**
4. Search for **"D-Link Router"**
5. Fill in your router's IP, username, password

## Configuration

### Requirements

- Home Assistant 2024.1.0 or later
- SSH access enabled on D-Link DIR-825 router
- Router on local network

### Setup

1. **Enable SSH on router:**
   - http://192.168.0.1 → Settings → Management → SSH → Enable

2. **Add Integration:**
   - Settings → Devices & Services → "+ CREATE INTEGRATION"
   - Search: "D-Link Router"
   - Fill form:
     - IP Address: `192.168.0.1`
     - Username: `admin`
     - Password: `your_password`
     - SSH Port: `22`

## Supported Devices

- D-Link DIR-825 (1.0.4+)

## License

MIT License

## Author

Alex (https://github.com/ASC-mokr)

## Contributing

Feel free to open issues and pull requests!
