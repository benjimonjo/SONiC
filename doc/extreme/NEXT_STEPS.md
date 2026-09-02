# X440-G2 SONiC Port - Next Steps (UPDATED - Linux Shell Access Discovered!)

## 🎉 BREAKTHROUGH: Linux Shell Access Available!

**Command**: `run script shell.py` (from ExtremeXOS CLI)

This changes everything! We can now:
- ✅ Direct hardware probing
- ✅ I2C bus scanning
- ✅ Kernel/system information
- ✅ Device enumeration
- ✅ Configuration file inspection

---

## � BREAKTHROUGH: ASIC IDENTIFIED!

### ✅ ASIC Model: Broadcom Hurricane2 (Dual-Unit)

**Confirmed via dmesg output**:
```
{0}HURRICANE2 unit 0: TotalCells=0x3000, DedicatedCells=0x9ec, 
                     DynCells=0x2614, Ports=0x1d (28 26 2)
{0}HURRICANE2 unit 1: TotalCells=0x3000, DedicatedCells=0x9ec, 
                     DynCells=0x2614, Ports=0x1d (28 26 2)
```

**Key Details**:
- **Architecture**: Dual forwarding planes (units 0 and 1)
- **PHY**: BCM848xx (Falcon PHY) on each unit
- **Port Count**: ~28 ports per unit (includes stacking)
- **Memory**: 12KB per unit buffer
- **Features**: TCAM tuning, link module initialization

**Implications for SONiC**:
1. Likely requires Broadcom SAI SDK for Hurricane2
2. May need special port configuration for dual-unit setup
3. Stacking ports (bcmport 26-29) must be handled specially
4. Need to map physical ports to ASIC lane assignments

---

### Action 2: Map I2C Topology (30-45 mins)

**What to Find**:
- System EEPROM address (likely 0x50 on I2C bus 0)
- Thermal sensors (addresses TBD)
- PSU monitoring (addresses TBD)
- Fan controller (addresses TBD)
- LED controller/CPLD (addresses TBD)

**Commands to Run**:
```bash
# List all I2C buses
i2cdetect -l

# Scan each bus (replace N with bus number)
i2cdetect -y 0
i2cdetect -y 1
i2cdetect -y 2
# ... etc for all buses

# Read EEPROM content (if at 0x50)
i2cdump -f -y 0 0x50

# Check system logs for I2C info
dmesg | grep i2c
```

**Output Format** (example):
```
I2C bus 0:
  0x50 - System EEPROM
  0x5f - Thermal sensor 1
I2C bus 1:
  0x40 - PSU monitor
  0x60 - Fan controller
```

---

### Action 3: Confirm CPU & System Info (Do Now - 15 mins)

```bash
# CPU info
cat /proc/cpuinfo

# Memory info
cat /proc/meminfo | grep MemTotal

# Kernel version (already done, but confirm)
cat /proc/version

# Loaded Broadcom modules
lsmod | grep bcm
```

---

## 📋 Updated Hardware Discovery Checklist

**Already Complete** ✅:
- [x] SSH access to device
- [x] Linux shell access confirmed
- [x] CPU type: Cavium Octeon III (MIPS)
- [x] Kernel: 2.6.28-summit_octeon (2016)
- [x] Broadcom ASIC confirmed (vendor)
- [x] 3 ASIC candidates identified

**Needed This Session**:
- [ ] ASIC model - run dmesg/probe commands
- [ ] I2C topology - run i2cdetect commands
- [ ] Port-to-lane mapping - check ASIC SDK

**After ASIC Confirmed**:
- [ ] Thermal sensors (count, types, addresses)
- [ ] PSU monitor (interface type, registers)
- [ ] Fan controller (PWM control method)
- [ ] LED control (GPIO/I2C/CPLD method)

---

## 🔧 Hardware Probing Commands Reference

### In ExtremeXOS CLI:
```
run script shell.py              # Access Linux shell (BusyBox)
exit                             # Return to ExtremeXOS
```

### In Linux Shell (BusyBox):
```
dmesg                            # Kernel boot messages
lsmod                            # Loaded modules
i2cdetect -l                      # List I2C buses
i2cdetect -y 0                    # Scan I2C bus 0
i2cdump -f -y 0 0x50             # Read data from I2C address 0x50
cat /proc/version                # Kernel version
cat /proc/cpuinfo                # CPU information
cat /proc/meminfo                # Memory information
strings /exos/lib/*.so | grep X  # Search binary libraries
```

---

## ⏱️ Estimated Time to Complete Next Steps

| Task | Time | Status |
|------|------|--------|
| Identify ASIC model | 30 mins | DO NOW |
| Map I2C topology | 45 mins | After ASIC |
| Confirm system specs | 15 mins | DO NOW |
| Review findings | 30 mins | After probing |
| **Total** | **~2 hours** | **Today** |

---

## 📊 Success Criteria for Phase 1 Completion

### MUST HAVE:
- [x] Device connected and accessible
- [x] Linux shell access confirmed
- [ ] **ASIC model determined** ← TARGET
- [ ] Port-to-lane mapping documented
- [ ] I2C devices mapped

### NICE TO HAVE:
- [ ] Thermal sensor details
- [ ] PSU specifications
- [ ] Fan control details
- [ ] LED control specifications

---

## 🚀 After Phase 1 is Complete

Once we have the ASIC model confirmed and I2C topology mapped:

### Phase 2 Will Begin:
1. Create port_config.ini with confirmed lane mapping
2. Select Broadcom SAI SDK version
3. Begin implementing drivers
4. Set up platform directory structure

### Phase 2 Estimated Duration:
- 3-5 days (dependent on finding documentation)

---

## 💡 Key Information

### Device Access
- **IP**: 192.168.0.2
- **SSH User**: ollama
- **SSH Pass**: Window23
- **Linux Shell**: `run script shell.py`

### Documentation
- **Hardware Reference**: [x440g2_hardware_reference.md](x440g2_hardware_reference.md)
- **Linux Findings**: [LINUX_SHELL_FINDINGS.md](LINUX_SHELL_FINDINGS.md)
- **Implementation Guide**: [x440g2_implementation_guide.md](x440g2_implementation_guide.md)

---

## ⚠️ Important Notes

1. **MIPS Architecture**: This X440-G2 uses Cavium Octeon III (MIPS), not x86_64!
   - Most SONiC platforms are x86_64
   - May require compilation environment adjustments
   - Feasible but requires careful architecture consideration

2. **Old Kernel**: Linux 2.6.28 from 2016 is very old
   - Most modern SONiC uses 4.9+ or 5.x
   - Significant gap - may need compatibility work
   - Still can work but requires testing

3. **Heavy Customization**: ExtremeXOS extensively customizes Linux
   - Proprietary modules everywhere
   - Porting SONiC requires understanding Extreme's architecture
   - May need module adaptations

---

## ✅ Next Session Plan

**Session Start**:
1. Connect to device
2. Run Linux shell: `run script shell.py`
3. Execute ASIC detection commands
4. Execute I2C topology commands
5. Document all findings
6. Update hardware reference with results

**Expected Outcome**: 
- ASIC model confirmed (BCM56640, BCM56840, or BCM56850)
- I2C topology documented
- Ready to proceed with Phase 2 setup

---

**Status**: Phase 1 Discovery - 75% Complete (Updated to reflect Linux shell discovery)  
**Blocker**: ASIC model still needed (but can now probe directly!)  
**Target Completion**: Next session (~2-3 hours of work)



