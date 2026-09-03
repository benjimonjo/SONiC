# Extreme Networks X440-G2 SONiC Port - Implementation Guide

> **Status — do not implement from the templates below yet.** The platform is MIPS64 with two Broadcom Hurricane2 forwarding units. Many legacy examples in this guide still assume an x86_64/Tomahawk platform and placeholder I2C addresses. Use the [hardware reference](x440g2_hardware_reference.md) and [next-steps plan](NEXT_STEPS.md) as the source of truth until the exact BCM device, SAI support, boot path, and port map are verified.

## Overview

This guide provides step-by-step instructions for porting SONiC to the Extreme Networks X440-G2 platform. It covers the complete development cycle from hardware analysis to testing.

## Table of Contents

1. [Phase 1: Hardware Analysis & Discovery](#phase-1-hardware-analysis--discovery)
2. [Phase 2: Platform Foundation Setup](#phase-2-platform-foundation-setup)
3. [Phase 3: Driver Implementation](#phase-3-driver-implementation)
4. [Phase 4: Configuration Files](#phase-4-configuration-files)
5. [Phase 5: Testing & Validation](#phase-5-testing--validation)
6. [Phase 6: Integration & Upstream](#phase-6-integration--upstream)

---

## Phase 1: Hardware Analysis & Discovery

### Step 1.1: Gather Hardware Documentation

**Objective**: Collect all available information about the X440-G2 hardware.

**Actions**:
1. Obtain from Extreme Networks:
   - Hardware User Manual
   - Block diagram
   - Schematic (if available)# X440-G2 SONiC Implementation Guide

## 🎯 Project Objective

Port SONiC to Extreme Networks X440-G2 switch with Broadcom Hurricane2 ASIC.

## 🔧 Hardware Details (Confirmed)

### ASIC Architecture
- **Model**: Broadcom Hurricane2 (Dual-Unit)
- **Units**: 2 forwarding planes
- **Ports per Unit**: ~28 ports (including stacking)
- **PHY Type**: BCM848xx (Falcon PHY)
- **Memory**: 12KB per unit buffer

### System Specifications
- **CPU**: Cavium Octeon III (MIPS architecture)
- **Kernel**: Linux 2.6.28-summit_octeon (2016)
- **Architecture**: MIPS (not x86_64)

## 📁 Directory Structure

```
sonic-platform-modules-extreme/
├── x440g2/
│   ├── platform/
│   │   ├── __init__.py
│   │   ├── sonic_platform.py
│   │   ├── port.py
│   │   └── chassis.py
│   ├── sfp/
│   │   ├── __init__.py
│   │   └── sfp.py
│   ├── thermal/
│   │   ├── __init__.py
│   │   └── thermal.py
│   ├── psu/
│   │   ├── __init__.py
│   │   └── psu.py
│   ├── fan/
│   │   ├── __init__.py
│   │   └── fan.py
│   └── config/
│       └── port_config.ini
├── tests/
│   └── test_x440g2.py
└── README.md
```

## 🛠️ Implementation Steps

### Phase 1: Hardware Discovery (Completed)
- [x] Linux shell access confirmed (`run script shell.py`)
- [x] ASIC model identified as Hurricane2
- [x] CPU architecture confirmed as MIPS
- [x] Kernel version identified (2.6.28)

### Phase 2: Port Configuration Setup

#### 1. Create Platform Directory Structure
```bash
mkdir -p sonic-platform-modules-extreme/x440g2/platform
mkdir -p sonic-platform-modules-extreme/x440g2/sfp
mkdir -p sonic-platform-modules-extreme/x440g2/thermal
mkdir -p sonic-platform-modules-extreme/x440g2/psu
mkdir -p sonic-platform-modules-extreme/x440g2/fan
```

#### 2. Create Port Configuration File
Create `port_config.ini` with the following structure:

```ini
[CONFIG]
asic_type=broadcom
chipset=hurricane2
units=2
ports_per_unit=28
total_ports=56
stacking_ports=26,27,28,29

[PORT_0]
lane=0
speed=1000

[PORT_1]
lane=1
speed=1000

# Continue for all ports...
```

#### 3. Implement Platform Classes

**sonic_platform.py**
```python
class X440G2Platform:
    def __init__(self):
        self.asic_type = "broadcom"
        self.chipset = "hurricane2"
        self.units = 2
        self.total_ports = 56
        
    def get_chassis_info(self):
        # Return chassis information
        pass
        
    def get_port_info(self, port_num):
        # Return port-specific information
        pass
```

### Phase 3: Driver Implementation

#### 1. Port Driver
- Implement BCM56640/BCM56840 driver interface
- Handle dual-unit ASIC configuration
- Support for stacking ports (26-29)

#### 2. SFP Driver
- Implement SFP module detection and monitoring
- Handle different SFP types (1G, 10G)
- I2C communication with SFP EEPROM

#### 3. Thermal Management
- Read thermal sensors from I2C buses
- Implement temperature monitoring
- Set up thermal thresholds

#### 4. Power Supply Monitoring
- Interface with PSU monitor via I2C
- Monitor power supply status and health
- Implement power management functions

#### 5. Fan Control
- Interface with fan controller via I2C
- Implement PWM control for fans
- Monitor fan speed and status

### Phase 4: Integration Testing

#### 1. Basic Port Configuration Test
```bash
# Test port creation
python3 -c "
from sonic_platform import X440G2Platform
platform = X440G2Platform()
print('Platform initialized successfully')
"
```

#### 2. Hardware Interface Tests
```bash
# Test I2C access
i2cdetect -y 0
i2cdetect -y 1
```

#### 3. Port Status Monitoring
```bash
# Check port status
cat /proc/net/dev
```

## 📊 Dependencies and Requirements

### Required Tools
- Python 3.x
- SAI SDK for Broadcom Hurricane2
- Cross-compilation environment for MIPS
- Linux kernel headers (2.6.28)

### System Prerequisites
```bash
# Install required packages
apt-get update
apt-get install build-essential python3-dev cross-compiler mips-linux-gnu-gcc

# Verify system capabilities
uname -a
python3 --version
   - BOM (Bill of Materials)
   - Thermal design specifications

2. Key information to extract:

```bash
# Create a hardware specification file
cat > /tmp/x440g2_hw_specs.txt << 'EOF'
# Extreme Networks X440-G2 Hardware Specifications

## CPU & System
- CPU Model: [FIXME]
- CPU Cores: [FIXME]
- RAM: [FIXME] GB
- Storage: [FIXME]
- BIOS/EFI: [FIXME]

## ASIC
- Vendor: Broadcom
- Model: [FIXME - e.g., Tomahawk3, Tomahawk4]
- Revision: [FIXME]
- Supported Speeds: [FIXME]

## Ports
- Total Ports: [FIXME]
- Port Types: [FIXME - e.g., 48x25G + 4x100G]
- Breakout Support: [FIXME]
- Management Port: [FIXME - Usually 10.x.x.x]

## Power & Cooling
- PSU Count: [FIXME]
- PSU Capacity: [FIXME]
- Fan Count: [FIXME]
- Fan Type: [FIXME]

## Management
- I2C Buses: [FIXME - Number and purpose]
- BMC: [FIXME - Present? Model?]
- Console: [FIXME - UART speed/pins]
- JTAG: [FIXME - Available for debug?]

## Key Devices (I2C Addresses)
- System EEPROM: [FIXME - Default 0x50]
- PSU Monitoring: [FIXME]
- Fan Control: [FIXME]
- Thermal Sensors: [FIXME]
- CPLD/FPGA: [FIXME]

## Connectivity
- Management Ethernet: [FIXME - Interface name, VLAN]
- Front Panel Ports: [FIXME - How connected to ASIC]

EOF

# Fill in the specifications as you gather information
```

### Step 1.2: Analyze Similar Platforms

Look at existing Broadcom-based SONiC platforms for reference:

```bash
# Navigate to existing platform implementations
cd ~/SONiC

# Look for Broadcom Tomahawk platforms (similar ASIC family)
find doc -name "*tomahawk*" -o -name "*trident*" | head -20

# Check existing platform implementations in sonic-buildimage (if available)
# Expected location (if you have the repo):
# sonic-buildimage/device/accton/x86_64-accton_as7326_56x-r0/
# sonic-buildimage/device/mellanox/x86_64-mlnx_msn2010-r0/
```

### Step 1.3: Document Hardware Details

Create a comprehensive hardware reference document:

```bash
mkdir -p ~/x440g2_port_data
cat > ~/x440g2_port_data/hardware_reference.md << 'EOF'
# X440-G2 Hardware Reference

## I2C Bus Topology

Document the I2C bus structure:

```
I2C Bus 0 (CPU-connected):
  Address 0x50 - System EEPROM
  Address 0x51 - [FIXME]
  
I2C Bus 1:
  Address 0x58 - PSU1
  Address 0x59 - PSU2
  
I2C Bus 2:
  Address 0x60 - Fan Controller 1
  Address 0x61 - Fan Controller 2
```

## Port Mapping

Create a detailed port mapping table:

| Front Panel | ASIC Port | Lanes | Speed | Type |
|------------|-----------|-------|-------|------|
| 1-48 (Eth0-Eth47) | [FIXME] | [FIXME] | 25G | RJ45 |
| 49-52 (Eth48-Eth51) | [FIXME] | [FIXME] | 100G | QSFP |

## GPIO and Control Lines

Document any GPIO usage:

GPIO 0 - LED: Status
GPIO 1 - LED: System
GPIO 2 - Button: Reset
...

## Power Rails

Document power distribution:
- 12V Rail: [FIXME]
- 5V Rail: [FIXME]
- 3.3V Rail: [FIXME]

EOF
```

### Step 1.4: Create I2C Device Tree

Document all I2C devices:

```bash
# First, if you have access to the hardware, probe I2C buses:
# ssh into the device or use i2ctools
i2cdetect -l   # List all I2C buses
i2cdetect 0    # Probe bus 0
i2cdetect 1    # Probe bus 1
# etc.

# Document findings in a file
```

---

## Phase 2: Platform Foundation Setup

### Step 2.1: Create Platform Directory Structure

```bash
# Assuming sonic-buildimage repo is available
cd ~/sonic-buildimage

# Create platform directory structure
mkdir -p device/extreme/x86_64-extreme_x440g2-r0/plugins/
mkdir -p device/extreme/x86_64-extreme_x440g2-r0/sonic_platform/
mkdir -p device/extreme/x86_64-extreme_x440g2-r0/hwsku/X440-G2/

# Create initial empty files
touch device/extreme/x86_64-extreme_x440g2-r0/platform_env.conf
touch device/extreme/x86_64-extreme_x440g2-r0/platform_asic_file
touch device/extreme/x86_64-extreme_x440g2-r0/hwsku/X440-G2/port_config.ini
touch device/extreme/x86_64-extreme_x440g2-r0/hwsku/X440-G2/sai.profile
touch device/extreme/x86_64-extreme_x440g2-r0/hwsku/X440-G2/config.bcm
```

### Step 2.2: Platform Identification Files

```bash
# platform_asic_file
cat > device/extreme/x86_64-extreme_x440g2-r0/platform_asic_file << 'EOF'
broadcom
EOF

# platform_env.conf
cat > device/extreme/x86_64-extreme_x440g2-r0/platform_env.conf << 'EOF'
# Platform environment configuration for X440-G2
# Set any boot-time environment variables here

# Example:
# PLATFORM_SPECIFIC_VAR=value
EOF
```

### Step 2.3: Create Installation Script

```bash
cat > device/extreme/x86_64-extreme_x440g2-r0/install.sh << 'EOF'
#!/bin/bash

# Installation script for X440-G2 platform
# Copies platform-specific files to correct locations during SONiC boot

PLATFORM_DIR="/usr/share/sonic/device/extreme/x86_64-extreme_x440g2-r0"
SONIC_VERSION_FILE="/etc/sonic/sonic-version.yml"

# This script is called during SONiC container initialization
# Platform-specific drivers and configurations are set up here

echo "Installing X440-G2 platform support..."

# Install platform files
mkdir -p "$PLATFORM_DIR"
cp -r * "$PLATFORM_DIR/"

# Any additional setup can go here
# For example: loading kernel modules, setting up I2C devices, etc.

echo "X440-G2 platform installation complete"
EOF

chmod +x device/extreme/x86_64-extreme_x440g2-r0/install.sh
```

---

## Phase 3: Driver Implementation

### Step 3.1: Implement EEPROM Driver

```python
# device/extreme/x86_64-extreme_x440g2-r0/plugins/eeprom.py

import os
import sys
from sonic_eeprom_base import EepromDecoder

class Eeprom(EepromDecoder):
    
    def __init__(self):
        # Specify the I2C device and address for system EEPROM
        self.name_field = "Product Name"
        self.serial_field = "Serial Number"
        
        # Path to EEPROM device
        # FIXME: Verify the correct I2C bus and address for X440-G2
        self.eeprom_path = "/sys/bus/i2c/devices/0-0050/eeprom"  # 0-0050 = I2C bus 0, addr 0x50
        
        super(Eeprom, self).__init__(self.eeprom_path, 0, '', True)
    
    def serial_number_str(self):
        """Return serial number as string"""
        (is_valid, data) = self.get_eeprom_field("Serial Number")
        if not is_valid:
            return "Unknown"
        return data
    
    def base_mac_addr(self):
        """Return base MAC address"""
        (is_valid, data) = self.get_eeprom_field("MAC Address")
        if not is_valid:
            return "00:00:00:00:00:00"
        return data
    
    def system_eeprom_info(self):
        """Return a dictionary of system EEPROM information"""
        info = super(Eeprom, self).system_eeprom_info()
        return info
```

### Step 3.2: Implement PSU Monitoring Driver

```python
# device/extreme/x86_64-extreme_x440g2-r0/sonic_platform/psu.py

import os
import re
from sonic_platform_base.psu_base import PsuBase

class Psu(PsuBase):
    
    def __init__(self, psu_index):
        PsuBase.__init__(self)
        self.index = psu_index
        
        # FIXME: Update with actual I2C addresses for X440-G2 PSU
        # Example: PSU1 at 0x58, PSU2 at 0x59
        self.psu_i2c_addr = 0x58 + psu_index
        self.psu_i2c_bus = 1  # FIXME: Verify I2C bus number
        
        # Sysfs paths for PSU monitoring
        self.psu_sysfs_path = f"/sys/bus/i2c/devices/{self.psu_i2c_bus}-00{self.psu_i2c_addr:02x}/"
    
    def get_presence(self):
        """Check if PSU is present"""
        # FIXME: Implement based on actual hardware
        # Usually involves checking GPIO or I2C device presence
        try:
            with open(os.path.join(self.psu_sysfs_path, "presence"), "r") as f:
                return f.read().strip() == "1"
        except:
            return False
    
    def get_status(self):
        """Check if PSU is operational"""
        # FIXME: Implement based on actual hardware
        try:
            with open(os.path.join(self.psu_sysfs_path, "psu_status"), "r") as f:
                status = f.read().strip()
                return status == "1"  # 1 = OK, 0 = Fault
        except:
            return False
    
    def get_voltage(self):
        """Get PSU output voltage in volts"""
        # FIXME: Implement based on actual hardware
        try:
            with open(os.path.join(self.psu_sysfs_path, "v_out"), "r") as f:
                # Assuming value is in mV
                return float(f.read().strip()) / 1000.0
        except:
            return 0.0
    
    def get_current(self):
        """Get PSU output current in amps"""
        # FIXME: Implement based on actual hardware
        try:
            with open(os.path.join(self.psu_sysfs_path, "i_out"), "r") as f:
                # Assuming value is in mA
                return float(f.read().strip()) / 1000.0
        except:
            return 0.0
    
    def get_power(self):
        """Get PSU output power in watts"""
        return self.get_voltage() * self.get_current()
    
    def get_powergood_status(self):
        """Check if PSU power is good"""
        return self.get_status()
    
    def set_status_led(self, color):
        """Set PSU status LED color"""
        # FIXME: Implement based on actual hardware
        pass
    
    def get_status_led(self):
        """Get PSU status LED color"""
        # FIXME: Implement based on actual hardware
        return "off"
```

### Step 3.3: Implement Fan Monitoring Driver

```python
# device/extreme/x86_64-extreme_x440g2-r0/sonic_platform/fan.py

import os
from sonic_platform_base.fan_base import FanBase

class Fan(FanBase):
    
    def __init__(self, fan_index):
        FanBase.__init__(self)
        self.index = fan_index
        
        # FIXME: Update with actual I2C addresses for X440-G2 fans
        # Example: Fans on I2C bus 2, controller at 0x60
        self.fan_i2c_bus = 2
        self.fan_i2c_addr = 0x60
        
        self.fan_sysfs_path = f"/sys/bus/i2c/devices/{self.fan_i2c_bus}-00{self.fan_i2c_addr:02x}/fan{fan_index}_"
    
    def get_presence(self):
        """Check if fan is present"""
        try:
            with open(os.path.join(self.fan_sysfs_path + "presence"), "r") as f:
                return f.read().strip() == "1"
        except:
            return False
    
    def get_status(self):
        """Check if fan is operational"""
        try:
            with open(os.path.join(self.fan_sysfs_path + "fault"), "r") as f:
                fault = f.read().strip()
                return fault == "0"  # 0 = OK, 1 = Fault
        except:
            return False
    
    def get_speed(self):
        """Get fan speed in RPM"""
        try:
            with open(os.path.join(self.fan_sysfs_path + "input"), "r") as f:
                return int(f.read().strip())
        except:
            return 0
    
    def get_speed_tolerance(self):
        """Get speed tolerance percentage"""
        return 10  # Typical +/- 10%
    
    def set_speed(self, pwm):
        """Set fan speed via PWM (0-100)"""
        # FIXME: Implement PWM control based on actual hardware
        pwm_value = int(pwm * 255 / 100)  # Convert percentage to 0-255
        try:
            sysfs_pwm_path = self.fan_sysfs_path.replace("fan_", "pwm")
            with open(sysfs_pwm_path, "w") as f:
                f.write(str(pwm_value))
            return True
        except:
            return False
    
    def get_target_speed(self):
        """Get target fan speed"""
        # FIXME: Implement based on actual hardware
        return 50  # Default 50%
    
    def set_status_led(self, color):
        """Set fan status LED"""
        pass
```

### Step 3.4: Implement Thermal Monitoring Driver

```python
# device/extreme/x86_64-extreme_x440g2-r0/sonic_platform/thermal.py

import os
from sonic_platform_base.thermal_base import ThermalBase

class Thermal(ThermalBase):
    
    # Thermal thresholds (adjust based on X440-G2 specifications)
    WARNING_THRESHOLD = 85
    CRITICAL_THRESHOLD = 95
    SHUTDOWN_THRESHOLD = 105
    
    def __init__(self, thermal_index, thermal_name):
        ThermalBase.__init__(self)
        self.index = thermal_index
        self.name = thermal_name
        
        # FIXME: Map thermal sensor locations to I2C devices
        # Example: ASIC temp at 0x4c on I2C bus 0
        # Ambient temp at 0x4d on I2C bus 0
        
        if "ASIC" in thermal_name:
            self.sensor_path = "/sys/bus/i2c/devices/0-004c/temp1_input"
        elif "Ambient" in thermal_name:
            self.sensor_path = "/sys/bus/i2c/devices/0-004d/temp1_input"
        else:
            self.sensor_path = f"/sys/class/thermal/thermal_zone{thermal_index}/temp"
    
    def get_temperature(self):
        """Get current temperature in Celsius"""
        try:
            with open(self.sensor_path, "r") as f:
                # Value is usually in milli-Celsius
                temp_mc = int(f.read().strip())
                return float(temp_mc) / 1000.0
        except:
            return 0.0
    
    def get_high_threshold(self):
        """Get warning threshold"""
        return float(self.WARNING_THRESHOLD)
    
    def set_high_threshold(self, threshold):
        """Set warning threshold"""
        pass  # Usually read-only from hardware
    
    def get_critical_high_threshold(self):
        """Get critical threshold"""
        return float(self.CRITICAL_THRESHOLD)
    
    def set_critical_high_threshold(self, threshold):
        """Set critical threshold"""
        pass
    
    def get_name(self):
        """Get sensor name"""
        return self.name
    
    def get_presence(self):
        """Check if sensor is present"""
        return os.path.exists(self.sensor_path)
    
    def get_status(self):
        """Check if sensor is operational"""
        temp = self.get_temperature()
        return temp > 0 and temp < 200  # Sanity check
```

### Step 3.5: Implement Main Platform Class

```python
# device/extreme/x86_64-extreme_x440g2-r0/sonic_platform/platform.py

from sonic_platform_base.platform_base import PlatformBase
from sonic_platform_base.chassis_base import ChassisBase

class Platform(PlatformBase):
    
    def __init__(self):
        PlatformBase.__init__(self)
        self.chassis = Chassis()
    
    def get_chassis(self):
        return self.chassis


class Chassis(ChassisBase):
    
    def __init__(self):
        ChassisBase.__init__(self)
        self._psu_list = []
        self._fan_list = []
        self._thermal_list = []
        self._sfp_list = []
        
        # Initialize platform components
        self._init_psu()
        self._init_fans()
        self._init_thermals()
        self._init_sfp()
    
    def _init_psu(self):
        """Initialize PSU objects"""
        # FIXME: Verify PSU count for X440-G2
        from psu import Psu
        for i in range(2):  # Assuming 2 PSUs
            self._psu_list.append(Psu(i))
    
    def _init_fans(self):
        """Initialize Fan objects"""
        # FIXME: Verify fan count for X440-G2
        from fan import Fan
        for i in range(4):  # Assuming 4 fans
            self._fan_list.append(Fan(i))
    
    def _init_thermals(self):
        """Initialize Thermal objects"""
        # FIXME: Verify thermal sensor count for X440-G2
        from thermal import Thermal
        self._thermal_list.append(Thermal(0, "ASIC Core Temp"))
        self._thermal_list.append(Thermal(1, "Ambient Temp"))
        self._thermal_list.append(Thermal(2, "PSU1 Temp"))
        self._thermal_list.append(Thermal(3, "PSU2 Temp"))
    
    def _init_sfp(self):
        """Initialize SFP/QSFP transceiver objects"""
        # FIXME: Implement SFP initialization
        pass
    
    def get_num_psus(self):
        return len(self._psu_list)
    
    def get_psu(self, index):
        return self._psu_list[index] if index < len(self._psu_list) else None
    
    def get_all_psus(self):
        return self._psu_list
    
    def get_num_fans(self):
        return len(self._fan_list)
    
    def get_fan(self, index):
        return self._fan_list[index] if index < len(self._fan_list) else None
    
    def get_all_fans(self):
        return self._fan_list
    
    def get_num_thermals(self):
        return len(self._thermal_list)
    
    def get_thermal(self, index):
        return self._thermal_list[index] if index < len(self._thermal_list) else None
    
    def get_all_thermals(self):
        return self._thermal_list
    
    def get_num_sfps(self):
        # FIXME: Return actual SFP count
        return 52  # Example: 48x25G + 4x100G
    
    def get_sfp(self, index):
        return self._sfp_list[index] if index < len(self._sfp_list) else None
    
    def get_all_sfps(self):
        return self._sfp_list
```

---

## Phase 4: Configuration Files

### Step 4.1: Create port_config.ini

This is critical for proper port numbering and speed configuration.

```bash
cat > device/extreme/x86_64-extreme_x440g2-r0/hwsku/X440-G2/port_config.ini << 'EOF'
# port_config.ini for Extreme X440-G2
# FIXME: Replace with actual port mapping from hardware documentation

# Format: port_name,alias,lanes,speed,fec,mtu,asic_port_name,phy_port_name
# Speed can be: 1000, 10000, 25000, 40000, 50000, 100000, 400000 (in Mbps)

# Example structure (MUST be updated with actual X440-G2 mapping):
Ethernet0,etp1,0,25000,auto,9100
Ethernet4,etp2,4,25000,auto,9100
Ethernet8,etp3,8,25000,auto,9100
Ethernet12,etp4,12,25000,auto,9100
Ethernet16,etp5,16,25000,auto,9100
Ethernet20,etp6,20,25000,auto,9100
Ethernet24,etp7,24,25000,auto,9100
Ethernet28,etp8,28,25000,auto,9100
Ethernet32,etp9,32,25000,auto,9100
Ethernet36,etp10,36,25000,auto,9100
Ethernet40,etp11,40,25000,auto,9100
Ethernet44,etp12,44,25000,auto,9100
Ethernet48,etp13,48,50000,auto,9100
Ethernet50,etp14,50,50000,auto,9100
Ethernet52,etp15,52,50000,auto,9100
Ethernet54,etp16,54,50000,auto,9100
# ... Continue for all ports ...

EOF
```

### Step 4.2: Create sai.profile

```bash
cat > device/extreme/x86_64-extreme_x440g2-r0/hwsku/X440-G2/sai.profile << 'EOF'
# SAI profile for X440-G2
# Broadcom SAI initialization configuration

SAI_INIT_CONFIG_FILE=/usr/share/sonic/hwsku/config.bcm
SAI_PROFILE_ID=0
SAI_DEFAULT_VLAN_ID=1
SAI_SWITCH_ID=0

EOF
```

### Step 4.3: Create Broadcom config.bcm

```bash
cat > device/extreme/x86_64-extreme_x440g2-r0/hwsku/X440-G2/config.bcm << 'EOF'
# Broadcom BCM configuration for X440-G2
# FIXME: Customize based on ASIC model and X440-G2 specifications

# Core settings
l2_mem_entries=32768
l3_mem_entries=16384
ipv6_lpm_128b_enable=1

# Port configuration
# Map physical ports to internal ASIC ports
# Format: port=<physical_port>:<speed>:<num_lanes>

# Example configuration (FIXME: Update with actual port mapping)
port=0:25
port=1:25
port=2:25
port=3:25
# ... Continue for all ports

# Packet prio to queue mapping
# Priority 0-7 maps to queues
pkt_pri_to_cosq_0=0
pkt_pri_to_cosq_1=1
pkt_pri_to_cosq_2=2
pkt_pri_to_cosq_3=3
pkt_pri_to_cosq_4=4
pkt_pri_to_cosq_5=5
pkt_pri_to_cosq_6=6
pkt_pri_to_cosq_7=7

EOF
```

---

## Phase 5: Testing & Validation

### Step 5.1: Basic Boot Test

```bash
# After building and flashing the SONiC image to X440-G2:

# 1. Boot into ONIE and install SONiC image
# 2. Boot into SONiC
# 3. Check basic system status

# SSH into the device
ssh admin@<management_ip>

# Verify platform detection
show platform summary

# Check for errors
sudo show system-health status
sudo dmesg | grep -i error | head -20
```

### Step 5.2: Port Functionality Test

```bash
# Verify all ports are visible
show interfaces brief

# Check port status
show interfaces status

# Test a port loopback
# Connect a cable from port 1 to port 2
config interface Ethernet0 shutdown
no config interface Ethernet0 shutdown
config interface Ethernet4 shutdown
no config interface Ethernet4 shutdown

# Send traffic and verify loopback

# Check port counters
show interfaces counters

# Check for packet loss
show interfaces counters detailed
```

### Step 5.3: Platform Monitoring Test

```bash
# Test PSU monitoring
show platform psustatus
show platform psuinfo

# Test fan monitoring
show platform fan

# Test thermal monitoring
show platform temperature
show system-health summary
```

### Step 5.4: Routing Test

```bash
# Configure BGP peer
config bgp 65001
  neighbor 192.168.1.1 remote-as 65002

# Verify BGP establishment
show bgp summary

# Add routes
config route add 10.0.0.0/8 192.168.1.1

# Test with traffic generator
```

### Step 5.5: Performance Test

```bash
# Test throughput on individual ports
# Use traffic generator or iperf

# Test wire-speed forwarding
# Monitor CPU usage to ensure minimal impact

# Test at various packet sizes (64B, 512B, 1518B)
```

---

## Phase 6: Integration & Upstream

### Step 6.1: Code Review & Testing

- [ ] Run linting tools (flake8, pylint) on Python code
- [ ] Ensure all Copyleft licenses are handled properly
- [ ] Sign off commits: `git commit -s`
- [ ] Create comprehensive test cases

### Step 6.2: Prepare for Upstream

1. **Documentation**:
   - Complete the HLD document with actual hardware details
   - Document port mapping clearly
   - Provide Extreme-specific hardware access guide

2. **Code Organization**:
   - Ensure directory structure follows SONiC conventions
   - Remove all FIXME comments or complete them
   - Add proper docstrings to all functions

3. **PR Submission**:
   - Fork SONiC buildimage repository
   - Create feature branch: `git checkout -b extreme/x440g2-port`
   - Commit changes with proper CLA signature
   - Submit PR to sonic-net/sonic-buildimage

### Step 6.3: Community Engagement

- Present port at SONiC community meetings
- Share experience on GitHub discussions
- Contribute to SONiC documentation and wiki
- Help with future Extreme platform ports

---

## Troubleshooting Guide

### Issue: Ports not appearing after boot

**Causes**:
- Incorrect port_config.ini mapping
- Missing SAI configuration
- ASIC initialization failure
- I2C device driver issues

**Solutions**:
1. Check SAI logs: `journalctl -u swss -n 50`
2. Verify port_config.ini against hardware
3. Review config.bcm for port definitions
4. Check I2C device presence: `i2cdetect -l`

### Issue: Platform monitoring not working

**Causes**:
- I2C device not recognized
- Python driver path issues
- sysfs mount problems
- Missing kernel modules

**Solutions**:
1. Verify I2C devices: `i2cdetect 0` (for bus 0)
2. Check driver logs: `dmesg | tail -50`
3. Verify sysfs: `ls -la /sys/bus/i2c/devices/`
4. Check Python path: `python3 -c "import sonic_platform"`

### Issue: Thermal shutdown at startup

**Causes**:
- Incorrect thermal sensor path
- Sensor reading error
- Out-of-date firmware

**Solutions**:
1. Verify sensor paths: `find /sys -name "*temp*" -type f`
2. Check sensor readings manually: `cat /sys/bus/i2c/devices/*/temp*`
3. Update BIOS/firmware to latest version
4. Adjust thermal thresholds if necessary (carefully!)

---

## References

- [SONiC Platform Development Guide](../platform_api/new_platform_api.md)
- [Broadcom SAI Documentation](https://github.com/opencomputeproject/SAI)
- [SONiC Community Slack](https://join.slack.com/t/natenetes/shared_invite/zt-h0ihe9gb-gD6KnR0BkLPrEZbfpFGmQQ)

---

**Status**: DRAFT - Customize for your X440-G2 configuration

EOF
```

Perfect! Now let me create a final reference document with quick commands:
<function_calls>
<invoke name="create_file">
<parameter name="content"># X440-G2 SONiC Porting - Quick Reference

## Essential Hardware Discovery Commands

```bash
# Run these commands on the hardware (once ONIE is available)

# Identify I2C devices
i2cdetect -l           # List all I2C buses
i2cdetect 0            # Scan bus 0
i2cdetect 1            # Scan bus 1
i2cdetect 2            # Scan bus 2
# Continue for all buses

# Read EEPROM
i2cdump -y 0 0x50      # Read EEPROM at address 0x50 on bus 0

# Identify CPU and ASIC
lscpu                  # CPU information
lspci                  # ASIC and device information
cat /proc/cpuinfo      # Detailed CPU info

# Check thermal sensors
find /sys -name "*temp*" -type f | head -20

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

## Common I2C Device Addresses

| Device | Typical Address | Bus | Purpose |
|--------|-----------------|-----|---------|
| System EEPROM | 0x50 | 0 | Platform ID, S/N, MAC |
| Thermal Sensor 1 | 0x4C | 0 | ASIC temp |
| Thermal Sensor 2 | 0x4D | 0 | Ambient temp |
| PSU 1 | 0x58 | 1 | Power supply monitoring |
| PSU 2 | 0x59 | 1 | Power supply monitoring |
| Fan Controller | 0x60-0x6F | 2 | Fan speed/PWM control |
| CPLD | 0x32 | Varies | LED, GPIO control |

**FIXME**: Update with actual X440-G2 device map

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
