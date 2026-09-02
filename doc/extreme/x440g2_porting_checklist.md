# X440-G2 SONiC Port - Comprehensive Checklist

Use this checklist to track progress through all phases of the porting effort.

## Phase 1: Hardware Analysis & Discovery

### 1.1 Documentation Gathering
- [ ] Obtained X440-G2 User Manual from Extreme Networks
- [ ] Obtained System Block Diagram
- [ ] Obtained Schematic (if available)
- [ ] Obtained Bill of Materials (BOM)
- [ ] Obtained Broadcom ASIC datasheet
- [ ] Identified exact Broadcom ASIC model (Tomahawk/TH2/TH3/TH4)
- [ ] Identified Broadcom ASIC revision number

### 1.2 Hardware Specifications
- [ ] CPU model and specs documented
- [ ] CPU core count verified
- [ ] RAM size confirmed
- [ ] Storage device type and size identified
- [ ] Total port count identified
- [ ] Port breakdown (25G, 100G, etc.) documented
- [ ] Port breakout capability documented (if any)

### 1.3 Power & Cooling
- [ ] PSU count documented
- [ ] PSU specs (voltage, capacity) documented
- [ ] PSU monitoring method identified (I2C, BMC, etc.)
- [ ] Number of fans documented
- [ ] Fan type and specs documented
- [ ] Fan speed control method identified
- [ ] Thermal sensor count and types identified
- [ ] Thermal sensor locations documented

### 1.4 Management Interfaces
- [ ] I2C bus topology mapped
  - [ ] Bus 0 devices listed
  - [ ] Bus 1 devices listed
  - [ ] Bus 2 devices listed
  - [ ] Additional buses (if any) listed
- [ ] System EEPROM address identified (e.g., 0x50 on bus 0)
- [ ] EEPROM format documented (TlvInfo, Extreme proprietary, etc.)
- [ ] BMC presence confirmed (if applicable)
- [ ] Serial console UART pins identified
- [ ] Console baud rate confirmed
- [ ] Management Ethernet interface identified
- [ ] JTAG/debug interface availability confirmed

### 1.5 I2C Device Mapping
- [ ] Complete I2C device address map created
- [ ] Sensor access methods documented
- [ ] CPLD/FPGA functionality identified
- [ ] GPIO availability documented (if applicable)
- [ ] All control lines mapped

### 1.6 Port Configuration Mapping
- [ ] Front panel port numbering scheme understood
- [ ] ASIC lane assignments documented
- [ ] Port-to-lane mapping table created
- [ ] Breakout port mappings created (if applicable)
- [ ] Speed capability per port documented

### 1.7 Reference Platforms Identified
- [ ] Similar Broadcom ASIC platforms found
- [ ] Reference platform code reviewed
- [ ] Key differences from reference identified

---

## Phase 2: Platform Foundation Setup

### 2.1 Directory Structure Creation
- [ ] Created `device/extreme/` directory
- [ ] Created `device/extreme/x86_64-extreme_x440g2-r0/` directory
- [ ] Created `sonic_platform/` subdirectory
- [ ] Created `hwsku/X440-G2/` subdirectory
- [ ] Created `plugins/` subdirectory (for legacy API if needed)

### 2.2 Platform Identification Files
- [ ] Created `platform_asic_file` with contents: `broadcom`
- [ ] Created `platform_env.conf` with appropriate environment variables
- [ ] Verified file permissions and ownership

### 2.3 Initial Python Package Setup
- [ ] Created `sonic_platform/__init__.py`
- [ ] Created `setup.py` for Python package
- [ ] Verified package can be imported

### 2.4 Installation Scripts
- [ ] Created `install.sh` script
- [ ] Script handles platform file installation
- [ ] Script handles kernel module loading (if needed)
- [ ] Script is executable and tested

---

## Phase 3: Driver Implementation

### 3.1 EEPROM Driver
- [ ] Created `eeprom.py` module
- [ ] Implemented EEPROM device path configuration
- [ ] Implemented `system_eeprom_info()` method
- [ ] Implemented `serial_number_str()` method
- [ ] Implemented `base_mac_addr()` method
- [ ] Tested EEPROM reading on actual hardware
- [ ] Verified EEPROM format compatibility

### 3.2 PSU Driver
- [ ] Created `psu.py` module
- [ ] Identified correct I2C bus and addresses for PSUs
- [ ] Implemented `get_presence()` method
- [ ] Implemented `get_status()` method
- [ ] Implemented `get_voltage()` method
- [ ] Implemented `get_current()` method
- [ ] Implemented `get_power()` method
- [ ] Implemented `get_powergood_status()` method
- [ ] Tested PSU monitoring on each PSU
- [ ] Verified fault detection works

### 3.3 Fan Driver
- [ ] Created `fan.py` module
- [ ] Identified correct I2C bus and addresses for fans
- [ ] Implemented `get_presence()` method
- [ ] Implemented `get_status()` method
- [ ] Implemented `get_speed()` method (RPM reading)
- [ ] Implemented `set_speed()` method (PWM control)
- [ ] Implemented `get_target_speed()` method
- [ ] Tested fan speed control (adjust PWM and verify RPM)
- [ ] Verified fan fault detection

### 3.4 Thermal Driver
- [ ] Created `thermal.py` module
- [ ] Mapped all thermal sensors to I2C devices or sysfs paths
- [ ] Implemented `get_temperature()` method
- [ ] Set appropriate temperature thresholds
- [ ] Implemented `get_high_threshold()` method
- [ ] Implemented `get_critical_high_threshold()` method
- [ ] Tested temperature reading accuracy
- [ ] Verified threshold alarm triggering

### 3.5 Transceiver (SFP) Driver
- [ ] Created `sfp.py` module
- [ ] Implemented `get_presence()` method
- [ ] Implemented `get_status()` method
- [ ] Implemented EEPROM reading (DOM data)
- [ ] Tested transceiver detection (insert/remove)
- [ ] Verified transceiver type detection (SFP vs QSFP)

### 3.6 Main Platform Class
- [ ] Created `platform.py` module
- [ ] Implemented `Platform` class
- [ ] Created `Chassis` class inheriting from `ChassisBase`
- [ ] Initialized all PSU objects
- [ ] Initialized all Fan objects
- [ ] Initialized all Thermal sensor objects
- [ ] Initialized all SFP/QSFP objects
- [ ] Implemented all required base class methods
- [ ] Tested platform object instantiation

### 3.7 Additional Components (as needed)
- [ ] Created `module.py` (if multi-module system)
- [ ] Created `watchdog.py` (if hardware watchdog present)
- [ ] Created `led.py` (if LED control needed)
- [ ] Created `sfp.py` (if transceiver management needed)

### 3.8 Code Quality
- [ ] All Python files pass flake8 linting
- [ ] All Python files pass pylint checks
- [ ] Proper exception handling in all methods
- [ ] Comprehensive docstrings for all public methods
- [ ] No hardcoded paths (use constants/configs)
- [ ] Proper logging implemented

---

## Phase 4: Configuration Files

### 4.1 Port Configuration (port_config.ini)
- [ ] Created `hwsku/X440-G2/port_config.ini`
- [ ] All front-panel ports listed
- [ ] Correct ASIC lane assignments for each port
- [ ] Correct speed for each port (25G, 100G, etc.)
- [ ] FEC settings configured appropriately
- [ ] MTU values set correctly
- [ ] No duplicate port names
- [ ] Port ordering matches hardware documentation
- [ ] Verified syntax with sonic-cfggen

### 4.2 SAI Configuration (sai.profile)
- [ ] Created `hwsku/X440-G2/sai.profile`
- [ ] Points to correct config.bcm file
- [ ] SAI_DEFAULT_VLAN_ID set to 1
- [ ] All required SAI parameters present

### 4.3 Broadcom ASIC Configuration (config.bcm)
- [ ] Created `hwsku/X440-G2/config.bcm`
- [ ] Identified correct ASIC model-specific settings
- [ ] All physical ports configured with correct speeds
- [ ] Lane configuration correct for breakout ports
- [ ] Memory settings appropriate for ASIC
- [ ] Buffer settings configured
- [ ] ACL memory allocation appropriate
- [ ] QoS configuration included
- [ ] Any required Broadcom errata workarounds applied
- [ ] Verified against Broadcom SDK documentation

### 4.4 QoS Configuration (qos.json)
- [ ] Created `hwsku/X440-G2/qos.json` (or verified standard settings)
- [ ] Queue mappings defined
- [ ] Scheduling algorithms configured
- [ ] Shaper rates configured (if needed)
- [ ] Buffer thresholds appropriate for port count

### 4.5 Cable Configuration (cable.json)
- [ ] Created `hwsku/X440-G2/cable.json` (optional)
- [ ] Cable specifications for each port type

---

## Phase 5: System Integration

### 5.1 Build System Integration
- [ ] Platform registered in build system
- [ ] Build target created: `sonic-extreme_x440g2-r0.bin`
- [ ] Platform makefile created (if needed)
- [ ] Kernel module compilation configured (if needed)
- [ ] Device tree compilation configured (if needed)

### 5.2 Initial Build & Packaging
- [ ] Successfully built SONiC image for platform
- [ ] Platform drivers packaged in image
- [ ] Configuration files included in image
- [ ] Python packages installable

### 5.3 ONIE Integration
- [ ] Verified ONIE support on X440-G2
- [ ] ONIE installer accepts SONiC image
- [ ] Boot sequence verified (ONIE → SONiC)
- [ ] Grub configuration appropriate

---

## Phase 6: Basic Functionality Testing

### 6.1 Boot Testing
- [ ] Image successfully flashed to X440-G2
- [ ] System boots successfully without errors
- [ ] All startup services come up
- [ ] No critical errors in syslog
- [ ] SONiC processes (swss, syncd, bgpd, etc.) start

### 6.2 Platform Detection
- [ ] `show platform summary` returns correct info
- [ ] Platform name identified correctly
- [ ] HwSKU identified correctly
- [ ] ASIC type detected correctly
- [ ] All platform details match hardware

### 6.3 Port Visibility & Status
- [ ] All ports appear in `show interfaces brief`
- [ ] Port numbering matches hardware
- [ ] Port speeds correct in interface status
- [ ] Port MTU settings correct
- [ ] No duplicate or missing ports

### 6.4 LED Functionality (Visual Check)
- [ ] System LED indicators turn on
- [ ] Power LED illuminates
- [ ] Port LED indicators present and functional
- [ ] LED patterns match expected behavior

### 6.5 PSU Monitoring
- [ ] PSU presence detected correctly
- [ ] PSU status monitored (OK/Fault)
- [ ] PSU voltage reading within expected range
- [ ] PSU current reading reasonable
- [ ] PSU power calculation correct
- [ ] `show platform psustatus` works

### 6.6 Fan Monitoring
- [ ] All fans detected at boot
- [ ] Fan speed (RPM) readings correct
- [ ] Fan status monitoring works
- [ ] Fan speed control responds to changes
- [ ] `show platform fan` works
- [ ] Fan fault detection functional

### 6.7 Thermal Monitoring
- [ ] All thermal sensors detected
- [ ] Temperature readings reasonable (within ±5°C of manual check)
- [ ] ASIC temperature reads correctly
- [ ] Ambient temperature sensor functional
- [ ] PSU temperature sensors working
- [ ] `show platform temperature` displays all sensors
- [ ] Temperature thresholds appropriate
- [ ] No false thermal alarms

### 6.8 EEPROM Access
- [ ] System EEPROM readable
- [ ] Serial number displays correctly
- [ ] MAC address correct
- [ ] Hardware revision accessible
- [ ] Manufacturer info correct

### 6.9 SFP/Transceiver Management
- [ ] Transceiver insertion detected
- [ ] Transceiver removal detected
- [ ] EEPROM readable for installed transceivers
- [ ] Transceiver type identified (SFP/QSFP)
- [ ] `show interfaces transceiver presence` works
- [ ] DOM (Digital Optical Monitoring) data accessible

### 6.10 System Health Monitoring
- [ ] `show system-health` status displays
- [ ] Health LED indicators work
- [ ] No spurious alarms
- [ ] System stable over 1+ hours uptime

---

## Phase 7: Layer 2 Testing

### 7.1 Basic Switching
- [ ] Create VLAN 100
- [ ] Add ports 1 and 2 to VLAN 100
- [ ] Connect cable between ports 1 and 2
- [ ] Verify MAC learning
- [ ] Verify traffic forwarding
- [ ] Verify MAC address table population

### 7.2 Port Status Changes
- [ ] Shut down port 1
- [ ] Verify port shows as down
- [ ] No shut port 1
- [ ] Verify port comes up
- [ ] Multiple up/down cycles work correctly

### 7.3 Multi-Port Testing
- [ ] Create VLAN with multiple ports
- [ ] Generate traffic between different port pairs
- [ ] Verify forwarding statistics
- [ ] Check for packet loss
- [ ] Monitor CPU usage

### 7.4 Broadcast Storm Control
- [ ] Send broadcast traffic
- [ ] Verify storm control limits if configured
- [ ] No system hang or crash

---

## Phase 8: Layer 3 Testing

### 8.1 Basic Routing
- [ ] Configure IP addresses on ports
- [ ] Ping between different subnets
- [ ] Verify routing table population
- [ ] Verify traffic forwarding statistics
- [ ] Check TTL decrements correctly

### 8.2 BGP Testing
- [ ] Configure BGP on SONiC device
- [ ] Establish BGP session with external peer
- [ ] Verify BGP neighbor status
- [ ] Advertise routes
- [ ] Verify routes learned from peer
- [ ] Send traffic across BGP routes

### 8.3 IPv4 & IPv6
- [ ] Configure IPv4 addresses
- [ ] Test IPv4 connectivity
- [ ] Configure IPv6 addresses
- [ ] Test IPv6 connectivity
- [ ] Verify dual-stack routing

### 8.4 ECMP
- [ ] Configure ECMP routes
- [ ] Verify traffic load balancing
- [ ] Monitor ECMP group status

---

## Phase 9: Advanced Features Testing

### 9.1 ACL Testing
- [ ] Configure ingress ACL
- [ ] Configure egress ACL
- [ ] Verify ACL counters
- [ ] Test various packet matching criteria
- [ ] Test permit and deny rules

### 9.2 QoS Testing
- [ ] Configure queue scheduling
- [ ] Configure queue shaping
- [ ] Generate traffic on different priority queues
- [ ] Verify queue statistics
- [ ] Test priority-based scheduling

### 9.3 Sflow/Telemetry
- [ ] Enable sFlow on ports
- [ ] Configure sFlow collector
- [ ] Verify sample packets received
- [ ] Check counter accuracy

### 9.4 Counters & Statistics
- [ ] Verify port statistics collection
- [ ] Check counter accuracy
- [ ] Monitor queue statistics
- [ ] Verify internal (ASIC) counter access

---

## Phase 10: Performance Testing

### 10.1 Throughput Testing
- [ ] Test 25G port throughput
- [ ] Test 100G port throughput
- [ ] Verify wire-speed forwarding capability
- [ ] Test at various packet sizes (64B, 256B, 512B, 1518B)
- [ ] Measure latency

### 10.2 CPU & Memory Usage
- [ ] Monitor CPU usage during forwarding
- [ ] Verify memory consumption reasonable
- [ ] Monitor for memory leaks over extended run
- [ ] Check thermal management CPU utilization

### 10.3 Stability Testing
- [ ] Run continuous forwarding for 24+ hours
- [ ] Monitor for crashes or hangs
- [ ] Check syslog for errors/warnings
- [ ] Verify temperature stays within limits

---

## Phase 11: Warm Boot Testing

### 11.1 Warm Boot Functionality
- [ ] Start forwarding traffic
- [ ] Issue warm reboot command
- [ ] Verify traffic resumes (minimal loss)
- [ ] Verify no BGP session drops
- [ ] Monitor forwarding state preservation

### 11.2 Warm Boot with Long Routes
- [ ] Configure large number of routes
- [ ] Perform warm reboot
- [ ] Verify all routes preserved

---

## Phase 12: Code Quality & Documentation

### 12.1 Code Quality
- [ ] All Python files pass flake8 checks
- [ ] All Python files pass pylint checks
- [ ] No hardcoded values (use configs)
- [ ] Proper exception handling throughout
- [ ] Comprehensive logging

### 12.2 Documentation
- [ ] Updated HLD with actual hardware specs
- [ ] Filled in all FIXME comments
- [ ] Created platform-specific troubleshooting guide
- [ ] Documented any platform-specific workarounds
- [ ] Created deployment guide for end users

### 12.3 Testing Documentation
- [ ] Test results compiled
- [ ] Known limitations documented
- [ ] Performance benchmarks recorded
- [ ] Test procedures documented

---

## Phase 13: Community & Upstream

### 13.1 Pre-Submission Review
- [ ] Code follows SONiC style guidelines
- [ ] All commits properly signed (`git commit -s`)
- [ ] Commit messages clear and descriptive
- [ ] No debug code or temporary files in submission
- [ ] License headers present where required

### 13.2 Upstream Submission
- [ ] Forked sonic-net/sonic-buildimage
- [ ] Created feature branch
- [ ] Submitted PR to sonic-buildimage
- [ ] Passed CI/CD pipeline checks
- [ ] Addressed review comments
- [ ] PR merged successfully

### 13.3 Community Engagement
- [ ] Announced port on SONiC community channels
- [ ] Participated in relevant discussions
- [ ] Offered to help other Extreme platform ports
- [ ] Contributed to SONiC documentation/wiki

---

## Final Sign-Off

- [ ] All phases completed
- [ ] All tests passed
- [ ] Code merged to upstream
- [ ] Platform documented
- [ ] Hardware working reliably
- [ ] Ready for production deployment

**Completion Date**: _______________

**Signed By**: _______________

---

## Notes & Observations

Use this section to record important findings, workarounds, and lessons learned:

```

[Record any platform-specific quirks, timing issues, workarounds, or valuable lessons learned]


```

---

## Known Limitations (if any)

- [ ] List any features not yet supported
- [ ] Document any performance limitations
- [ ] Note any known bugs or issues
- [ ] Plan for future enhancements

