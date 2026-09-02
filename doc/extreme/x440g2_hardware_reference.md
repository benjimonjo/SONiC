# Extreme Networks X440-G2 - Hardware Reference Document

**Discovery Date**: 2026-09-02  
**Device IP**: 192.168.0.2  
**Device Name**: benjimonjo-switch1  

## Device Identification

| Property | Value |
|----------|-------|
| Model | X440-G2-48p-10G4 |
| Full Model Code | 800618-00-11 |
| Hardware Version | 1711N-40116 Rev 11.0 |
| System MAC | 00:04:96:9D:3E:9F |
| Current OS | ExtremeXOS 21.1.1.4-patch1-5 |
| BootROM Version | 1.0.1.8 |
| Current Status | OPERATIONAL |
| Uptime | 2+ days |

## Ports Configuration

### Port Breakdown
- **48x 1GbE ports** (ports 1-48)
- **4x 10GbE ports** (ports 49-52)
- **Total**: 52 ports

### Port Details (Discovered)
```
Port 1:    1GbE - Not Ready
Port 2:    1GbE - Linked at 100Mbps (likely 1GbE capable)
Port 3-4:  1GbE - Linked at 1000Mbps
Port 5-8:  1GbE - Not Ready
Ports 49-52: 10GbE ports (specifics TBD)
```

### Port Numbering
- ✅ Ports 1-48: Standard 1GbE RJ45 connectors
- ✅ Ports 49-52: 10GbE SFP+ connectors
- **Lane mapping**: TBD (need to identify ASIC port assignments)

## Power Supply

| Component | Status | Type |
|-----------|--------|------|
| PSU-1 | Operational | Internal Power Supply |
| PSU-2 | Not Present | - |
| Total PSUs | 1 | - |

**Notes**: 
- Single internal PSU
- May be redundant design capable of supporting second PSU
- Current consumption and voltage ratings: TBD

## Cooling System

| Component | Count | Status | Details |
|-----------|-------|--------|---------|
| Fans | 4 | Mixed | 3 Failed @ 0 RPM, 1 OK @ 960 RPM |
| Fan Tray | 1 | Operational | Standard configuration |

**Important**: Some fans are not spinning - may indicate:
1. Not installed/present
2. Hardware issue with failed fans
3. Thermal shutdown or error condition

## Thermal Management

**Thermal Sensors**: TBD  
**Temperature Monitoring**: TBD  
**Shutdown Temperature**: TBD  
**Warning Thresholds**: TBD  

## ASIC & Forwarding Engine

### ✅ ASIC IDENTIFIED!

**ASIC Vendor**: Broadcom (Confirmed)

**ASIC Family**: **Hurricane2** (Broadcom entry/mid-range family)

**Key Findings**:
- **Dual-unit configuration**: Unit 0 and Unit 1 (each with own ASIC)
- **Initialization**: Both units initialized via `aspenCardInitSocBcm` 
- **Per-unit port configuration**: 
  - Unit 0: ~28 ports (includes 2 stacking ports: bcmport 26-27)
  - Unit 1: ~26 ports (includes 2 stacking ports: bcmport 28-29)
  - Total accessible: 48x 1GbE + 4x 10GbE (stacking ports are internal)
- **Memory per unit**: 12KB dedicated + 9.6KB dynamic cells
- **PHY configuration**: BCM848xx (Falcon) PHY on each unit

**Discovery Method**:
```
dmesg output:
{0}HURRICANE2 unit 0: TotalCells=0x3000, DedicatedCells=0x9ec, 
                     DynCells=0x2614, Ports=0x1d (28 26 2)
{0}HURRICANE2 unit 1: TotalCells=0x3000, DedicatedCells=0x9ec, 
                     DynCells=0x2614, Ports=0x1d (28 26 2)
```

**Important Note**:
Hurricane2 is typically for smaller switches (24-28 ports). The fact that X440-G2 has 48+4 ports across dual units suggests:
- Either special Hurricane2 variants with higher port counts
- Or Extreme is using "Hurricane2" as their codename for something else
- Further investigation needed to determine exact BCM model number

**ASIC Memory Configuration**: 
- Dedicated Cells: 0x9ec (2540 cells)
- Dynamic Cells: 0x2614 (9748 cells)
- Total Cells: 0x3000 (12288 cells)

**Buffer Pool**: ~12KB per unit (limited)
**L2 Table Size**: TBD  
**L3 Table Size**: TBD

## I2C Bus Topology

### System EEPROM
| Location | Address | Bus | Status |
|----------|---------|-----|--------|
| System EEPROM | 0x50 (TBD) | Bus 0 (TBD) | TBD |

### Thermal Sensors
- Location(s): TBD
- I2C Address(es): TBD  
- Type (LM75, TMP75, etc.): TBD
- Count: TBD

### PSU Monitoring
- PSU-1 Address: TBD
- I2C Bus: TBD
- Monitoring Type (SMBus, PMBus, etc.): TBD

### Fan Controller
- Controller Address: TBD
- I2C Bus: TBD
- PWM Control Support: TBD

### CPLD/FPGA
- Address: TBD
- I2C Bus: TBD
- Functions: LED, GPIO, Status monitoring

## LED Control

| LED | Purpose | Control Method | TBD |
|-----|---------|-----------------|-----|
| System LED | Power/Fault indicator | GPIO/I2C | TBD |
| Port LEDs | Per-port link status | ASIC native | TBD |
| Fan LEDs | Fan status | TBD | TBD |
| PSU LEDs | PSU status | TBD | TBD |

## Management Interfaces

| Interface | Type | Connectivity | Notes |
|-----------|------|--------------|-------|
| Management Ethernet | 10/100/1000 | Built-in | IP: 192.168.0.2 |
| Serial Console | RS-232 | DB9 (likely) | Speed: TBD, Pinout: TBD |
| JTAG | Debug | Test connector | TBD |

## CPU & Memory

**DISCOVERED via Linux Shell**:

| Component | Specification | Status |
|-----------|---------------|--------|
| CPU Model | Cavium Octeon III V0.2 | ✅ Confirmed |
| CPU Architecture | MIPS (NOT x86_64) | ✅ Confirmed |
| CPU Type | Unsupported Board (CN7010p1.2-1000-CP) | ✅ Confirmed |
| CPU Cores | 1 (shown, likely more) | Partial |
| CPU Speed | BogoMIPS: 2000.00 | Partial |
| RAM Size | TBD | TBD |
| RAM Type | TBD | TBD |
| Storage | TBD | TBD |

**Linux Kernel**:
- **Version**: 2.6.28.9-summit_octeon
- **Build Date**: Thu Jun 16 14:57:28 EDT 2016
- **Architecture**: MIPS64
- **Compiled by**: release-manager@currituck.extremenetworks.com

**Shell Access**: ✅ Linux shell accessible via `run script shell.py` in ExtremeXOS CLI

## Software Information

| Item | Value |
|------|-------|
| Current OS | ExtremeXOS 21.1.1.4-patch1-5 |
| BootROM | 1.0.1.8 |
| Diagnostics Version | 5.4 |
| ONIE Support | TBD (unknown) |
| Primary Image | 21.1.1.4 (currently booted) |
| Secondary Image | 21.1.1.4 (available) |

## Known Issues & Status

### Current Issues
1. **Fans**: 3 fans not spinning (0 RPM) - needs investigation
2. **ASIC Model**: Not yet identified - critical for SAI selection
3. **I2C Topology**: Not yet mapped - critical for platform drivers

### Missing Information (Priority Order)

**CRITICAL (needed before implementation)**:
- [ ] ASIC model and type
- [ ] ASIC SAI support status
- [ ] Broadcom SDK version compatibility
- [ ] I2C bus topology and device addresses
- [ ] Port-to-ASIC lane mapping
- [ ] EEPROM format and location

**IMPORTANT (needed for driver development)**:
- [ ] CPU model and specifications
- [ ] Memory configuration
- [ ] Thermal sensor types and addresses
- [ ] PSU monitoring interface
- [ ] Fan PWM control mechanism
- [ ] LED control method

**NICE-TO-HAVE (helpful for optimization)**:
- [ ] Power consumption specifications
- [ ] Thermal design specifications
- [ ] Performance benchmarks
- [ ] Known Extreme Networks/Broadcom errata

## Physical Specifications

| Aspect | Value | Status |
|--------|-------|--------|
| Form Factor | 1RU Rackmount | Confirmed |
| Port Density | 48x1G + 4x10G | Confirmed |
| Dimensions | TBD | TBD |
| Weight | TBD | TBD |
| Operating Temperature | TBD | TBD |
| Max Power Consumption | TBD | TBD |

## Next Steps for Hardware Discovery

1. **ASIC Identification** (CRITICAL)
   - Check Extreme Networks X440-G2 documentation
   - Look for any hardware datasheets
   - Contact Extreme Networks support
   - Attempt to access Linux kernel (if possible) to read hardware info

2. **I2C Bus Mapping**
   - Identify I2C buses and devices via Linux (if accessible)
   - Document all device addresses
   - Determine communication protocols

3. **Port Mapping**
   - Get physical-to-ASIC port mapping
   - Document lane configuration
   - Confirm breakout port configurations

4. **Documentation Collection**
   - Collect all available hardware manuals
   - Get Broadcom SAI SDK documentation (once ASIC identified)
   - Request EEPROM format documentation

## References & Resources

- Extreme Networks X440 Series Documentation
- Broadcom SAI SDK (version TBD)
- Broadcom BCM56960/BCM56970/BCM56980 Datasheets (as applicable)
- SONiC Platform Integration Guide

---

**Status**: Initial hardware discovery complete - awaiting ASIC identification  
**Last Updated**: 2026-09-02  
**Next Review**: After ASIC model confirmation

