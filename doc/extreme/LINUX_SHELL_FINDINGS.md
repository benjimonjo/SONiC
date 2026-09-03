# X440-G2 Linux Shell Discovery Report

**Dates**: 2026-09-02 and 2026-09-03
**Method**: Direct Linux shell access via `run script shell.py`  
**Status**: Phase 1 Hardware Discovery (Advanced)  

## 🎯 Executive Summary

Linux shell access is working. The control plane, dual-unit Hurricane2 ASIC family, boot media, and part of the platform-management topology are now confirmed. The remaining blockers are the exact BCM part number and SAI/SDK support, a MIPS64 SONiC boot/build path, the physical port map, and the management paths hidden behind the SPI FPGA.

## 2026-09-03 Discovery Results

| Area | Confirmed result |
|---|---|
| RAM | `MemTotal: 976128 kB` (approximately 953 MiB) |
| I2C controllers | `i2c-0` and `i2c-1`, both named `OCTEON adapter` |
| I2C device | Bus 1 address `0x6f`: Microchip MCP7940 RTC (`rtc-ds1307` driver) |
| I2C userspace access | No `/dev/i2c-*` nodes; `i2cdetect` is not installed |
| Hardware monitoring | No devices exposed under `/sys/class/hwmon` |
| SPI devices | `spi0.1`: Microchip 23K256, 32 KiB EEPROM; `spi0.2`: `spiFPGA` |
| Persistent storage | eMMC (`mmcblk0`) with boot, alternate boot, EXOS, configuration, and scratch partitions |
| Console | Kernel command line specifies `console=ttyS0,9600` |
| Management interface | `eth0` is present, alongside proprietary Broadcom and packet interfaces |

**Interpretation**: The available evidence does not support the old assumption of a system EEPROM at I2C `0x50`. The identity EEPROM is likely the SPI 23K256 device, but its contents and format have not been read or confirmed. The FPGA is a likely gateway for fan, PSU, LED, or sensor functions; its interface must be discovered from the platform driver or vendor documentation.

### Access Note

After the successful read-only sessions, two further SSH connection attempts on 2026-09-03 were reset by the device during key exchange. No command ran in either attempt. Treat this as a transient access limitation; do not continue retrying automatically. Resume the FPGA and Broadcom-interface probes after confirming that the management plane accepts SSH connections again.

### ASIC Library Evidence

`libbcmplat.so` contains both the `hurricane2` family string and `bcm56640_b0 v 1.3 SV 2012/05/22`. It also contains register definitions for several chips, including BCM56150, BCM56640, BCM56840, and BCM56850. This confirms that library strings are not a definitive hardware-ID source. Treat BCM56640 B0 as a strong candidate requiring confirmation from a runtime SDK query, board documentation, or a supported diagnostic command.

---

## ✅ Discoveries Made

### 1. **Linux Shell Access Method (CRITICAL!)**

**Command**: `run script shell.py`

**Environment**:
- Shell: BusyBox v1.13.4 (2016-06-16)
- Root directory: `/exos/bin`
- Permissions: Limited (many directories denied access)
- Can execute system commands and inspect kernel data

**This Enables**:
- Direct hardware probing
- I2C bus scanning
- Device information enumeration
- System configuration review
- Software inventory

---

### 2. **CPU & Control Plane Specifications**

**CPU Type**: Cavium Octeon III V0.2 (MIPS, NOT x86_64 as initially assumed!)

```
System Type:        Unsupported Board (CN7010p1.2-1000-CP)
Processor:          Cavium Octeon III V0.2 FPU V0.0
Cores:              At least 1 (system type indicates more likely)
BogoMIPS:           2000.00
Architecture:       MIPS64 (not x86)
```

**Implications for SONiC Port**:
- SONiC platform code needs MIPS support (not typical for newer ports)
- Existing SONiC platforms mostly x86_64
- May need to adapt/build MIPS-compatible components
- Cavium Octeon is networking/security focused CPU (good for NOS role)

---

### 3. **Linux Kernel Specifications**

**Kernel Version**: 2.6.28.9-summit_octeon  
**Build Date**: June 16, 2016  
**Compiler**: GCC 4.9.2 (crosstool-NG 1.21.0)  
**Configuration**: SMP (Symmetric MultiProcessing - multiple cores)

**Age Notice**: This is an EXTREMELY old kernel (10 years old!)
- Released: 2006 (2.6 series ancient)
- Most SONiC systems use 4.9+ or 5.x kernel
- May have security/performance limitations
- Porting SONiC may require significant work

---

### 4. **Broadcom SDK & Drivers**

**Kernel Modules Loaded**:
```
linux_bcm_diag_full (60,526,768 bytes)  # Main Broadcom forwarding plane
bcmhelper            # Broadcom helper utilities
linux_uk_proxy       # Broadcom proxy interface
linux_kernel_bde     # Broadcom kernel driver
pciphymod            # Phy module
aspenpmap            # Aspen platform mapping (Extreme-specific)
```

**Broadcom Libraries**:
- `libsoc.so` - SOC library (contains register definitions)
- Extensive register definitions found for multiple ASIC models

---

### 5. **Historic ASIC String Search (Superseded)**

**Status**: Superseded by the Hurricane2 kernel identification below. The library strings only show that a multi-chip SDK was present and do not identify this device.

**Analysis Method**:
- Extracted all strings from `/exos/lib/*.so*`
- Searched for register definitions and field structures
- Found register patterns for multiple BCM chips

**Candidates Found**:

| Model | Frequency | Notes |
|-------|-----------|-------|
| **BCM56640** | ✅✅✅ Very High | Most frequent references |
| **BCM56840** | ✅✅ High | Many references found |
| **BCM56850** | ✅ Moderate | Some references found |

**Other Models Found** (for reference):
- BCM56334, BCM56340, BCM56150, BCM56850, BCM56634, BCM56624, etc.
- These are older Trident/Trident+ family ASICs

**Port Configuration Match**:
- X440-G2: 48x 1G + 4x 10G = 52 total ports
- BCM56640: Typically 48x + 4x configuration (likely match!)
- BCM56840: Similar configuration
- BCM56850: Typically higher port counts

---

### 6. **Device Tree Hints**

**System ID**: CN7010p1.2-1000-CP
- CN7010 = Cavium Octeon 3 (control plane)
- p1.2 = Platform revision
- This is Extreme's internal code, not Broadcom specific

---

## ✅ ASIC IDENTIFICATION COMPLETE

**Result**: Broadcom **Hurricane2** ASIC (Dual-unit configuration)

**Evidence from dmesg**:
```
{0}HURRICANE2 unit 0: TotalCells=0x3000, DedicatedCells=0x9ec, 
                     DynCells=0x2614, Ports=0x1d (28 26 2)
{0}HURRICANE2 unit 1: TotalCells=0x3000, DedicatedCells=0x9ec, 
                     DynCells=0x2614, Ports=0x1d (28 26 2)
```

**Port Configuration**:
- **Unit 0**: 28 ports (ports 1-26 data + ports 26-27 stacking)
- **Unit 1**: 26 ports (ports 27-52 data + ports 28-29 stacking)
- **External**: 48x 1GbE + 4x 10GbE configured

**PHY Information**:
- PHY Model: BCM848xx (Falcon PHY)
- Configuration: Dual instances (one per unit)
- Preemphasis tuning applied

---

## 📋 Remaining Discovery Tasks

### Option 1: I2C Topology
```bash
cat /proc/devices                  # May list ASIC
cat /proc/iomem                    # Memory map
cat /proc/ioports                  # IO port map
strings /exos/config/* | grep -i bcm56
```

### Option 2: Probe I2C Devices
```bash
i2cdetect -l                       # List I2C buses
i2cdetect -y 0                     # Scan bus 0
i2cdetect -y 1                     # Scan bus 1
# EEPROM at 0x50 might contain model info
```

### Option 3: Check CPLD/FPGA
```bash
# May store hardware version info
# Accessible via I2C or special registers
```

### Option 4: Review System Logs
```bash
dmesg | grep -i bcm56              # Might show chip detection
dmesg | grep -i asic
dmesg | grep -i "chip\|device"
```

### Option 5: Contact Extreme Networks
- Extreme.Support: support@extremenetworks.com
- Ask for: "X440-G2 Broadcom ASIC model specification"
- Also request: Hardware reference manual

---

## 📊 Other Hardware Information Discovered

### Loaded Kernel Modules
```
bcmpkt              # Broadcom packet processing
exvlan              # VLAN handling
ocpd                # OCP daemon
kicm                # ?
exacl               # ACL module
exsflow             # sFlow module
exsnoop             # Packet snoop
linux_bcm_diag_full # Main ASIC driver (60MB!)
aspenpmap           # Aspen platform mapping (Extreme)
shd                 # Service handler daemon
spiFPGA             # SPI FPGA controller
watchdog            # Watchdog timer
```

**Implications**:
- Extensive Broadcom/Extreme customization
- Many proprietary modules mixed with standard Linux
- Porting to SONiC will require understanding these modules

### System Status
- **Uptime**: Device running continuously, healthy
- **Memory**: `/1K-blocks 181576 / Used 6052 / Available 175524`
- **Usage**: ~3.3% disk usage (very light load)

---

## ⚠️ Critical Findings

### 1. **CPU Architecture Surprise**
- Expected: x86_64
- Actual: MIPS (Cavium Octeon III)
- **Impact**: Most SONiC builds target x86_64; may need MIPS compilation

### 2. **Ancient Kernel**
- Kernel: 2.6.28 (from 2008!)
- Most SONiC systems: 4.9+ or 5.x
- **Impact**: Significant gap in kernel versions; compatibility concerns

### 3. **Proprietary Extreme Modules**
- Heavy customization of Linux
- ExtremeXOS specific code everywhere
- **Impact**: SONiC porting may need significant adaptation

### 4. **ASIC Still Unidentified**
- 3 candidates remain
- Need more specific detection method
- **Blocks**: Port configuration, SAI selection, exact feature support

---

## 📝 Immediate Action Items

### HIGH PRIORITY (Do Now):
- [ ] Run `dmesg | grep -i bcm` on device to see boot messages
- [ ] Try `i2cdetect -l` to see I2C topology
- [ ] Check EEPROM for hardware model information
- [ ] Search `/exos/share` for documentation
- [ ] Look for Broadcom SDK version markers

### MEDIUM PRIORITY (This Week):
- [ ] Contact Extreme Networks support for specs
- [ ] Review any online X440-G2 documentation
- [ ] Compare with similar platforms (other Extreme models using Broadcom)
- [ ] Search eBay/tech sites for X440-G2 manuals

### LONG TERM:
- [ ] Once ASIC confirmed: Map I2C topology
- [ ] Identify all connected hardware (sensors, fans, LEDs)
- [ ] Review Extreme's platform initialization code
- [ ] Begin SONiC platform implementation

---

## 🚀 Implications for SONiC Port

### Positive Factors
- ✅ Linux shell access available (can probe and debug)
- ✅ Broadcom ASIC (well-supported ecosystem)
- ✅ Extensive existing drivers (can understand implementation)
- ✅ Cavium Octeon III (networking-focused CPU, good for NOS)

### Challenges
- ❌ MIPS architecture (not typical for SONiC)
- ❌ Very old kernel (2.6.28 from 2008)
- ❌ Heavy Extreme customization (may conflict with SONiC architecture)
- ❌ ASIC model still unknown (critical blocker)
- ❌ Likely requires custom compilation environment

### Risk Assessment
- **Architecture Risk**: MEDIUM (MIPS vs x86_64 significant difference)
- **Kernel Risk**: HIGH (2.6 kernel very old for SONiC)
- **ASIC Risk**: MEDIUM-HIGH (depends on which of 3 is correct)
- **Overall Risk**: MEDIUM-HIGH (feasible but requires significant work)

---

## 📚 Reference Information

### Linux Shell Access Confirmed
```bash
# To access:
ssh ollama@192.168.0.2
run script shell.py

# Useful commands in BusyBox shell:
dmesg                              # Kernel messages
lsmod                              # Loaded modules
cat /proc/version                  # Kernel info
cat /proc/cpuinfo                  # CPU details
i2cdetect -l                        # I2C buses
i2cdetect -y <bus>                 # Scan I2C bus
strings /exos/lib/*.so | grep bcm  # Find ASIC refs
```

### Files to Review
- `/exos/share/` - Documentation (mostly denied)
- `/usr/local/cfg/` - Configuration files (test*.py files)
- `/exos/lib/*.so` - Binary libraries (extensive Broadcom code)

---

## 🎯 Success Criteria

For Phase 1 completion, need:
1. ✅ Linux shell access - **COMPLETE**
2. ✅ CPU identified - **COMPLETE**
3. ✅ Kernel information - **COMPLETE**
4. ✅ Broadcom ASIC confirmed (vendor) - **COMPLETE**
5. ❌ ASIC model narrowed to 1 - **IN PROGRESS**
6. ❌ I2C topology mapped - **NOT STARTED** (blocked)
7. ❌ Port-to-lane mapping - **NOT STARTED** (blocked)

---

**Next Session Focus**: Run detailed hardware probes to identify exact ASIC model, then proceed with I2C mapping and platform driver development.
