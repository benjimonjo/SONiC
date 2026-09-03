# Extreme Networks X440-G2 SONiC Port - High Level Design

## Table of Contents
1. [Revision History](#revision-history)
2. [Scope](#scope)
3. [Definitions and Abbreviations](#definitions-and-abbreviations)
4. [Overview](#overview)
5. [Requirements](#requirements)
6. [Architecture](#architecture)
7. [High-Level Design](#high-level-design)
8. [SAI Implementation](#sai-implementation)
9. [Platform Management](#platform-management)
10. [Configuration](#configuration)
11. [Warm Boot Support](#warm-boot-support)
12. [Testing Plan](#testing-plan)
13. [References](#references)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-09-02 | SONiC Contributor | Initial draft |

---

## Scope

This document describes the SONiC port for the **Extreme Networks X440-G2** network switch. It covers the platform abstraction layer, hardware device drivers, SAI configuration, and management interfaces required to run SONiC on this device.

### Out of Scope
- Extreme-specific proprietary features not standardized in SONiC
- Detailed hardware debug procedures (refer to Extreme documentation)
- Production deployment guides

---

## Definitions and Abbreviations

| Term | Definition |
|------|-----------|
| X440-G2 | Extreme Networks X440-G2 switch model |
| ASIC | Application-Specific Integrated Circuit (Broadcom) |
| SAI | Switch Abstraction Interface |
| PAL | Platform Abstraction Layer |
| EEPROM | Electrically Erasable Programmable Read-Only Memory |
| PSU | Power Supply Unit |
| LED | Light Emitting Diode |
| SFP | Small Form-factor Pluggable transceiver |
| CPLD | Complex Programmable Logic Device |
| BMC | Baseboard Management Controller (if applicable) |
| I2C | Inter-Integrated Circuit bus |
| PDDF | Platform Driver Development Framework |

---

## Overview

### What is X440-G2?

The Extreme Networks X440-G2-48p-10G4 is a 52-port switch with:
- **ASIC Vendor**: Broadcom
- **ASIC Family**: Hurricane2, with two forwarding units; exact BCM part number remains unconfirmed
- **CPU**: Cavium Octeon III (MIPS64)
- **Port Configuration**: 48x 1GbE RJ45 + 4x 10GbE SFP+

### Why Port SONiC?

Porting SONiC to the X440-G2 enables:
- Open network operating system capabilities
- Vendor-neutral switch management
- Access to SONiC ecosystem features and innovations
- Community-driven feature development

### Key Platform Characteristics

[**FIXME: Fill in hardware-specific details**]

- Total front-panel data ports: 52
- Port types and speeds: 48x 1GbE RJ45 and 4x 10GbE SFP+
- Breakout capability: [Yes/No, if yes: how many ports?]
- Number of PSUs: [number]
- Number of fans: [number]
- CPU cores: [number]
- Management interfaces: [Ethernet, console, BMC]

---

## Requirements

### Functional Requirements

1. **Port Management**: All front panel ports must be operational with correct speed negotiation
2. **Platform Monitoring**: Real-time monitoring of thermal sensors, fan speeds, PSU status
3. **Packet Forwarding**: Standard L2/L3 forwarding with all Broadcom SAI-supported features
4. **LED Control**: System and port status LEDs must indicate operational state
5. **EEPROM**: System EEPROM must be readable for platform identification
6. **Transceiver Management**: SFP/QSFP transceivers must be hotswappable with proper detection

### Non-Functional Requirements

1. **Performance**: No performance degradation compared to vendor OS
2. **Reliability**: Stable operation with 24/7 uptime capability
3. **Warm Boot**: Support graceful restart preserving forwarding state
4. **Backward Compatibility**: Support existing SONiC deployment patterns

### Platform-Specific Requirements

[**FIXME: Add requirements discovered during hardware analysis**]

- I2C bus layout and device addresses
- BMC integration (if applicable)
- CPLD/FPGA functionality
- Special boot requirements
- Power management considerations

---

## Architecture

### High-Level System Architecture

```
┌─────────────────────────────────────────────────┐
│             SONiC OS Layer                       │
│  ├─ SWSS (Switch State Service)                │
│  ├─ syncd (SAI Datapath)                       │
│  └─ pmon (Platform Monitor)                    │
├─────────────────────────────────────────────────┤
│         Platform Abstraction Layer               │
│  ├─ sonic_platform (Python APIs)               │
│  ├─ Device Drivers (kernel)                    │
│  └─ Configuration Files                        │
├─────────────────────────────────────────────────┤
│           Hardware / ASIC Layer                 │
│  ├─ 2x Broadcom Hurricane2 forwarding units    │
│  ├─ Cavium Octeon III CPU (MIPS64)             │
│  ├─ Management I2C                             │
│  └─ Platform Devices (PSU, Fan, Sensors, etc.) │
└─────────────────────────────────────────────────┘
```

### Block Diagram

[**FIXME: Create or insert block diagram showing:**]
- CPU and ASIC connection
- I2C/BMC connectivity
- Port layout
- Power distribution
- Thermal sensors location

---

## High-Level Design

### 1. Platform Directory Structure

The platform-specific files are organized as follows:

```
sonic-buildimage/
├── device/
│   └── extreme/
│       └── mips64-extreme_x440g2-r0/
│           ├── platform_env.conf
│           ├── platform_asic_file
│           ├── plugins/
│           │   ├── eeprom.py
│           │   ├── psuutil.py
│           │   └── sfputil.py
│           ├── sonic_platform/
│           │   ├── __init__.py
│           │   ├── platform.py
│           │   ├── chassis.py
│           │   ├── module.py
│           │   ├── fan.py
│           │   ├── psu.py
│           │   ├── thermal.py
│           │   ├── sfp.py
│           │   ├── eeprom.py
│           │   └── watchdog.py
│           └── hwsku/
│               └── X440-G2/
│                   ├── port_config.ini
│                   ├── sai.profile
│                   ├── config.bcm
│                   └── qos.json
```

### 2. Port Configuration

**File**: `device/extreme/mips64-extreme_x440g2-r0/hwsku/X440-G2/port_config.ini`

This file defines the mapping between front-panel ports and internal switch fabric lanes.

```ini
# port_config.ini
# Example structure - FIXME: Update with actual port mapping
# Format: name alias asic_port_name asic_lane speed fec

# Format: PORT_NAME ALIAS ASIC_LANE_LIST SPEED[MTU LANE_PROFILE FEC_PROFILE]
Ethernet0 etp1 0 25000
Ethernet4 etp2 4 25000
# ... add all ports
```

**Discovery Required**:
- [ ] Total number of ports
- [ ] Port numbering scheme
- [ ] ASIC lane assignments
- [ ] Supported speeds per port
- [ ] Breakout port configurations

### 3. ASIC Configuration

**File**: `device/extreme/mips64-extreme_x440g2-r0/hwsku/X440-G2/config.bcm`

Broadcom SDK configuration file for ASIC initialization.

```bcm
# config.bcm - Broadcom ASIC Configuration
# FIXME: Identify required settings from X440-G2 specifications

# Core settings
l2_mem_entries=32768
l3_mem_entries=16384
ipv6_lpm_128b_enable=1

# Port configuration
# Speed mappings and lane configurations go here

# Memory and buffer settings
# Adjust based on ASIC model and port count

# ACL and flowtracker settings
pktpri_propagate_mapid=2
```

**Required Information**:
- [ ] ASIC memory configuration
- [ ] Default port speeds
- [ ] Buffer thresholds
- [ ] ACL memory allocation
- [ ] Specific Broadcom errata or workarounds

### 4. SAI Profile

**File**: `device/extreme/mips64-extreme_x440g2-r0/hwsku/X440-G2/sai.profile`

SAI configuration for proper SDK library initialization.

```
SAI_INIT_CONFIG_FILE=/usr/share/sonic/hwsku/config.bcm
SAI_PROFILE_ID=0
SAI_DEFAULT_VLAN_ID=1
```

### 5. Platform Devices & Monitoring

#### 5.1 I2C Device Tree

[**FIXME: Map I2C devices discovered on the platform**]

Example:
```
I2C Bus 0:
  - 0x50: System EEPROM
  - 0x48-0x4F: Thermal sensors

I2C Bus 1:
  - 0x58: PSU1
  - 0x59: PSU2

I2C Bus 2:
  - 0x60-0x6F: Fan modules
```

#### 5.2 Power Supply Unit (PSU) Monitoring

Provides:
- PSU presence detection
- Power consumption monitoring
- Status indication (fault, warning, normal)
- Access to PSU EEPROM

#### 5.3 Fan Monitoring & Control

Provides:
- Fan speed monitoring (RPM)
- PWM speed control
- Fault detection
- Automatic speed control

#### 5.4 Thermal Monitoring

Monitoring of:
- ASIC core temperature
- System ambient temperature
- PSU internal temperature
- Other location-specific sensors

**Thermal Thresholds** (typical, adjust based on hardware):
- Warning threshold: 85°C
- Shutdown threshold: 95°C
- Critical threshold: 105°C

#### 5.5 LED Control

Status indicators for:
- System LED (power, fault, warning)
- Port status LEDs (per-port activity, link)
- Fan LEDs (operational, fault)
- PSU LEDs (operational, fault)

### 6. System EEPROM

Stores:
- Serial number
- MAC address
- Hardware revision
- Manufacturing date
- Vendor information

**EEPROM Location**: I2C address [**FIXME: typically 0x50 or 0x56**]

### 7. Transceiver (SFP/QSFP) Management

Capabilities:
- Transceiver presence detection
- EEPROM reading (DOM, serial, vendor info)
- Status monitoring (link, signal detect)
- TX disable control (if supported)

---

## SAI Implementation

### 1. Required SAI Features

- **Port Management**: All supported speeds and FEC modes
- **L2 Switching**: VLAN, MAC learning, aging
- **L3 Routing**: Unicast and multicast
- **Buffer Management**: Shared and dedicated buffers
- **QoS**: Queue management, scheduling, shaping
- **ACL**: Ingress and egress rules
- **Counters**: Port, queue, and policer statistics
- **Mirror/Sflow**: Packet mirroring for analysis

### 2. Known ASIC Limitations

[**FIXME: Document any known Broadcom ASIC limitations or errata**]

---

## Platform Management

### 1. Configuration Database (CONFIG_DB) Schema

Standard SONiC schema applies. Platform-specific additions:

```json
{
  "PLATFORM_INFO": {
    "platform": {
      "asic_name": "FIXME_ASIC_MODEL",
      "port_count": "FIXME_NUMBER",
      "thermal_management": "enabled"
    }
  }
}
```

### 2. Platform Files Location

All platform-specific files are installed to:

```
/usr/share/sonic/device/extreme/mips64-extreme_x440g2-r0/
```

### 3. CLI Commands for Platform Management

```bash
# Show platform information
show platform summary

# Show fan status
show platform fan

# Show PSU status
show platform psustatus

# Show temperature
show platform temperature

# Show transceiver information
show interfaces transceiver

# LED control (if exposed)
# (Usually not exposed in standard SONiC, handled internally)
```

---

## Configuration

### 1. Boot Configuration

**ONIE Support**: X440-G2 should support standard ONIE for bootloader.

[**FIXME: Verify**]:
- [ ] ONIE version compatibility
- [ ] Boot device selection
- [ ] Grub configuration requirements

### 2. Kernel Configuration

Custom kernel modules may be required for:
- Platform device drivers
- I2C device drivers
- GPIO management
- CPLD/FPGA access (if applicable)

### 3. Device Tree

[**FIXME: Create device tree overlay if needed**]

---

## Warm Boot Support

### 1. Warm Boot Procedure

1. **Preserve State**: syncd dumps ASIC state to file
2. **Stop Services**: Graceful shutdown of SONiC services
3. **Kernel Reboot**: Reboot with preserved memory region
4. **State Restore**: syncd restores ASIC state
5. **Service Recovery**: Services resume with minimal packet loss

### 2. Platform-Specific Considerations

[**FIXME: Document any platform-specific warm boot requirements**]

---

## Testing Plan

### 1. Phase 1: Basic Functionality

- [ ] Boot SONiC successfully
- [ ] All ports visible and operational
- [ ] Port LED indicators functional
- [ ] PSU monitoring working
- [ ] Fan monitoring working
- [ ] Thermal monitoring functional
- [ ] No critical errors in logs

### 2. Phase 2: Packet Forwarding

- [ ] Intra-ASIC forwarding
- [ ] CPU-to-port forwarding
- [ ] Port-to-port throughput testing
- [ ] Verify wire-speed forwarding capability

### 3. Phase 3: Routing

- [ ] BGP peer establishment
- [ ] Route convergence
- [ ] IPv4 unicast routing
- [ ] IPv6 unicast routing
- [ ] Multicast routing (if supported)

### 4. Phase 4: Advanced Features

- [ ] ACL functionality
- [ ] QoS scheduling and shaping
- [ ] Sflow monitoring
- [ ] Counter collection
- [ ] Platform monitoring stability over extended uptime

### 5. Phase 5: Warm Boot Testing

- [ ] Warm reboot with active sessions
- [ ] Connection preservation during reboot
- [ ] Traffic loss measurement

---

## References

### SONiC Documentation

- [SONiC Platform API](../platform_api/new_platform_api.md)
- [PDDF (Platform Driver Development Framework)](../platform/brcm_pdk_pddf.md)
- [SONiC Multi-ASIC HLD](../multi_asic/SONiC_multi_asic_hld.md)
- [SAI Repository](https://github.com/opencomputeproject/SAI)

### External Documentation

[**FIXME: Add Extreme Networks and Broadcom SDK documentation**]

- Extreme Networks X440-G2 Hardware Manual
- Broadcom [ASIC Model] SDK Datasheet
- Broadcom SAI Programming Guide

### Similar Platform Implementations

- [Accton AS7326-56X](../../sonic-buildimage/device/accton/x86_64-accton_as7326_56x-r0/)
- [Arista DCS-7260CX3-64](../../sonic-buildimage/device/arista/x86_64-arista_dcs7260cx3_64-r0/)
- [Broadcom reference designs](https://github.com/sonic-net/sonic-buildimage/tree/master/device)

---

## Appendix: Hardware Discovery Checklist

### CPU & Storage

- [ ] CPU model and clock speed
- [ ] RAM size and type
- [ ] Storage device (SSD/eMMC) size
- [ ] Boot ROM details

### ASIC

- [ ] Exact Broadcom ASIC model and revision
- [ ] Memory configuration (DRAM amount)
- [ ] Support matrix (speeds, technologies)
- [ ] Known errata and workarounds

### Ports

- [ ] Total port count breakdown (by speed)
- [ ] Breakout capability details
- [ ] ASIC lane to physical port mapping
- [ ] Management port configuration (if separate)

### Power & Cooling

- [ ] PSU specifications and count
- [ ] Fan specifications and count
- [ ] Thermal sensor types and count
- [ ] Temperature monitoring protocol

### Management & Control

- [ ] I2C bus topology and device list
- [ ] BMC integration (if present)
- [ ] GPIO availability and usage
- [ ] CPLD/FPGA functionality
- [ ] Console UART details

### Interfaces

- [ ] Management Ethernet configuration
- [ ] Serial console (UART) details
- [ ] JTAG/debug interface availability
- [ ] USB or other service interfaces

---

**Document Status**: DRAFT - Awaiting hardware specifications and discovery phase completion
