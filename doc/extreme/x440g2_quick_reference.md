# X440-G2 SONiC Porting - Quick Reference

## Essential Hardware Discovery Commands

```bash
# Run these read-only commands from the ExtremeXOS Linux shell (`run script shell.py`).
# ONIE availability is not confirmed.

# Identify I2C and SPI devices. The current BusyBox image has no `i2cdetect`
# and no `/dev/i2c-*` nodes.
ls -l /sys/class/i2c-dev
ls -l /sys/bus/i2c/devices
ls -l /sys/bus/spi/devices
cat /sys/bus/i2c/devices/1-006f/name

# The confirmed EEPROM candidate is SPI `spi0.1` (Microchip 23K256, 32 KiB).
# Do not read it until a safe driver interface and data format are known.

# Identify CPU and ASIC
lscpu                  # CPU information
lspci                  # ASIC and device information
cat /proc/cpuinfo      # Detailed CPU info

# Check thermal sensors. No hwmon devices are currently exposed.
ls -l /sys/class/hwmon

# List all GPIO
gpioinfo               # GPIO controller information

# Check power supplies
# (Device specific - depends on PSU monitoring interface)

# Network interfaces
ethtool -p <iface>    # Test port LED blinking
```

## Directory Structure Reference

```
sonic-buildimage/
├── device/
│   └── extreme/                                    # Vendor directory
│       └── x86_64-extreme_x440g2-r0/              # Platform directory
│           ├── plugins/                           # Legacy Python API
│           │   ├── __init__.py
│           │   ├── eeprom.py                     # EEPROM access
│           │   ├── psuutil.py                    # PSU control
│           │   └── sfputil.py                    # Transceiver control
│           │
│           ├── sonic_platform/                    # New Platform 2.0 API
│           │   ├── __init__.py                    # Package init
│           │   ├── platform.py                    # Platform class
│           │   ├── chassis.py                     # Chassis class
│           │   ├── module.py                      # Module (for modular systems)
│           │   ├── fan.py                         # Fan class
│           │   ├── psu.py                         # PSU class
│           │   ├── thermal.py                     # Thermal sensor class
│           │   ├── sfp.py                         # SFP transceiver class
│           │   ├── eeprom.py                      # EEPROM class
│           │   ├── watchdog.py                    # Watchdog class
│           │   └── led.py                         # LED class (optional)
│           │
│           ├── hwsku/
│           │   └── X440-G2/
│           │       ├── port_config.ini            # Port mapping
│           │       ├── sai.profile                # SAI config
│           │       ├── config.bcm                 # Broadcom ASIC config
│           │       ├── qos.json                   # QoS configuration
│           │       └── cable.json                 # Cable definitions (optional)
│           │
│           ├── platform_env.conf                  # Environment vars
│           ├── platform_asic_file                 # ASIC type: 'broadcom'
│           ├── install.sh                         # Installation script
│           └── setup.py                           # Python package setup
```

## File Content Quick Templates

### platform_asic_file
```
broadcom
```

### platform_env.conf
```
# Environment variables for X440-G2 boot
# Example:
# SKIP_ONIE_DHCP_IN_SECONDBOOT=yes
```

### sai.profile
```
SAI_INIT_CONFIG_FILE=/usr/share/sonic/hwsku/config.bcm
SAI_PROFILE_ID=0
SAI_DEFAULT_VLAN_ID=1
```

## Confirmed Management-Device Topology

| Device | Address / path | Status |
|--------|----------------|--------|
| Octeon I2C adapter | `i2c-0` | Present |
| Octeon I2C adapter | `i2c-1` | Present |
| MCP7940 RTC | I2C bus 1, `0x6f` | Present (`rtc-ds1307` driver) |
| Microchip 23K256 EEPROM | `spi0.1` | Present; format not confirmed |
| Platform FPGA | `spi0.2` | Present; register map not confirmed |
| Thermal / PSU / fan controller | Unknown | Not exposed through hwmon |

Do not infer a device address from common SONiC examples; the X440-G2 does not match the old `0x50` EEPROM assumption.

## Common Broadcom ASIC Models in Similar Devices

| Switch | ASIC | Ports | Common Platform |
|--------|------|-------|-----------------|
| Dell S6100 | BCM56960 | 32x40G | Tomahawk |
| Arista 7050 | BCM56960 | 32x40G + 2x10G | Tomahawk |
| Accton AS7326 | BCM56960 | 48x25G + 8x100G | Tomahawk |
| Mellanox SN2010 | Different | 32x100G | NVIDIA Spectrum |

**Research**: Find which platform is closest to X440-G2 and use as reference

## Development Workflow

```bash
# 1. Set up workspace
mkdir -p ~/sonic-development
cd ~/sonic-development
git clone https://github.com/sonic-net/sonic-buildimage.git
cd sonic-buildimage

# 2. Create feature branch
git checkout -b extreme/x440g2-port

# 3. Create platform directories
mkdir -p device/extreme/x86_64-extreme_x440g2-r0/sonic_platform
mkdir -p device/extreme/x86_64-extreme_x440g2-r0/hwsku/X440-G2

# 4. Implement drivers (iterative)
# ... Copy templates, implement, test ...

# 5. Build SONiC image
make configure PLATFORM=extreme
make target/sonic-extreme_x440g2-r0.bin

# 6. Test on hardware
# Flash to X440-G2, verify functionality

# 7. Submit for review
git add device/extreme/
git commit -s -m "Add Extreme Networks X440-G2 support"
git push origin extreme/x440g2-port
# Create PR on GitHub

# 8. Iterate based on review feedback
```

## Validation Checklist

### Pre-Submission
- [ ] All Python files pass flake8 linting
- [ ] All drivers implemented (no NotImplementedError)
- [ ] port_config.ini complete and validated
- [ ] Documentation updated with actual hardware specs
- [ ] Test results captured
- [ ] All commits signed with: `git commit -s`

### Post-Submission
- [ ] Address reviewer comments
- [ ] Run SONiC CI/CD tests
- [ ] Pass basic port tests
- [ ] Pass thermal monitoring tests
- [ ] Pass platform monitoring tests

## Key SONiC Slack Channels

- `#general` - General discussion
- `#platform` - Platform development
- `#broadcom` - Broadcom ASIC questions
- `#testing` - Testing and validation

## Useful External Links

- [SONiC GitHub](https://github.com/sonic-net)
- [SAI Repository](https://github.com/opencomputeproject/SAI)
- [Broadcom SDK Documentation](https://www.broadcom.com/)
- [I2C Tools Documentation](https://i2c.wiki.kernel.org/index.php/I2C_Tools)
- [Kernel SysFS Documentation](https://www.kernel.org/doc/html/latest/filesystems/sysfs.html)

## Build Time Optimization

```bash
# Clean rebuild
make clean
make all

# Incremental rebuild (faster)
make

# Build specific component
make target/sonic-broadcom.bin

# Build with specific options
make PLATFORM=extreme SONIC_DEBUGGING_ON=y
```

## Git Workflow

```bash
# Ensure proper commit signing
git config user.name "Your Name"
git config user.email "your.email@example.com"
git config user.signingkey <your-gpg-key>

# Commit with sign-off
git commit -s -m "Add X440-G2 support"

# View commits
git log --oneline -10

# Create pull request
# Go to GitHub and create PR from your branch
```

## Hardware Verification After Boot

```bash
# Log into SONiC
ssh admin@<mgmt_ip>

# Verify platform detection
admin@sonic:~$ show platform summary
Platform: x86_64-extreme_x440g2-r0
HwSKU: X440-G2
ASIC: broadcom
ASIC Count: 1

# Verify ports
admin@sonic:~$ show interfaces brief
Ethernet0         Ethernet0/1               up  up  
Ethernet4         Ethernet0/2               up  up  
...

# Verify platform monitoring
admin@sonic:~$ show platform temperature
Temp1: 52.3°C (OK)
Temp2: 41.2°C (OK)

# Check logs
sudo journalctl -xe | head -50
```

---

**Pro Tips**:
1. Start with a working reference platform, then adapt
2. Test incrementally - don't try to do everything at once
3. Keep detailed notes of hardware I2C addresses and pin configurations
4. Use `i2cdump` to verify sensor values before implementing drivers
5. Consult the SONiC community early and often
