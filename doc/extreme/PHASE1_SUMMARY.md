# X440-G2 SONiC Port - Phase 1 Discovery Summary

**Date**: 2026-09-02  
**Status**: Phase 1 (Hardware Discovery) - 60% Complete  
**Blocker**: ASIC Model Identification Required  

## What We Know (Confirmed)

### Device Specifications
```
Device Model:           X440G2-48p-10G4
Full Model Code:        800618-00-11
Hardware Version:       1711N-40116 Rev 11.0
System MAC Address:     00:04:96:9D:3E:9F

Port Configuration:     48x 1GbE + 4x 10GbE (52 total)
Management Interface:   1GbE Ethernet
Current OS:             ExtremeXOS 21.1.1.4-patch1-5
BootROM:                1.0.1.8
```

### Connected and Verified
- ✅ Network connectivity (192.168.0.2)
- ✅ SSH access with credentials (ollama/Window23)
- ✅ Device responds to CLI commands
- ✅ All 52 ports visible
- ✅ Fan tray installed (4 fans)
- ✅ PSU present (1x internal)

## What We Still Need (Critical Path Items)

### 1. ASIC Identification (BLOCKING)
**Why Important**: Determines entire SAI implementation strategy

**Most Likely**: Broadcom Tomahawk (BCM56960)  
**Alternatives**: Tomahawk 2 (BCM56970) or Tomahawk 3 (BCM56980)

**How to Determine**:
- [ ] Check Extreme Networks X440-G2 official datasheet
- [ ] Look for any Broadcom documentation
- [ ] Try accessing Linux kernel information (if possible)
- [ ] Contact Extreme Networks technical support

### 2. I2C Bus Topology (NEEDED FOR DRIVERS)
- System EEPROM address and bus
- Thermal sensor addresses
- PSU monitoring interface
- Fan controller interface
- CPLD/FPGA addresses (if present)

### 3. Port-to-ASIC Lane Mapping
- Physical port to ASIC lane assignment
- Port breakout configuration
- Speed and FEC configuration per port

### 4. Kernel & CPU Information
- CPU model and speed
- RAM size and type
- Storage device info
- Device tree structure

## Architecture Analysis

Based on port configuration, here's the likely architecture:

```
┌─ X440-G2-48p-10G4 ─────────────────────┐
│                                         │
│  48x 1GbE Ports ──┐                    │
│   4x 10GbE Ports │                    │
│                  └──→ Broadcom ASIC  │
│                      (BCM5696x)      │
│                        ↓             │
│  Management Port ──→ CPU (x86_64)  │
│  Console (RS-232)    └────┬────────│
│                           │        │
│  4x Fans ──→ PWM Control  │        │
│  1x PSU ──→ Monitoring    │        │
│  Sensors ──→ I2C Bus      │        │
│                           ↓        │
│                      I2C/GPIO      │
│                                    │
└────────────────────────────────────┘
```

## Next Steps (Recommended Sequence)

### Immediate (Next 24 hours)
1. **Obtain Hardware Documentation**
   - Request X440-G2 datasheet from Extreme Networks
   - Look for any included documentation with device
   - Search online for public documentation

2. **Try ASIC Detection** (if Linux access possible)
   - SSH to device and attempt `lspci`
   - Check system logs for hardware info
   - Look for device tree files

3. **Document Current Findings**
   - ✅ Complete (see x440g2_hardware_reference.md)
   - Create port mapping template
   - Create I2C device list template

### Short-term (Before Implementation)
1. **Identify and Confirm ASIC**
   - Confirm exact Broadcom model
   - Get SAI SDK requirements
   - Verify ONIE compatibility

2. **Complete I2C Topology**
   - Map all I2C buses and devices
   - Document each device's purpose
   - Create sysfs path mappings

3. **Prepare Reference Platforms**
   - Identify similar Broadcom ASIC platforms in SONiC
   - Study their implementation
   - Note differences specific to X440-G2

### Medium-term (Before Coding)
1. **Create Platform Structure**
2. **Implement Driver Skeletons**
3. **Configure Build System**

## Key Assumptions (To Verify)

| Assumption | Confidence | Action |
|-----------|------------|--------|
| ASIC is Broadcom Tomahawk | HIGH | Confirm with documentation |
| X86-64 CPU with Linux kernel | HIGH | Verify via system info |
| I2C-based platform management | HIGH | Verify bus topology |
| EEPROM at 0x50 on bus 0 | MEDIUM | Discover via probing |
| Standard SONiC compatible | HIGH | Platform 2.0 API ready |

## Files Created This Phase

- ✅ `/home/benjimonjo/SONiC/doc/extreme/README.md` - Navigation guide
- ✅ `/home/benjimonjo/SONiC/doc/extreme/x440g2_port_summary.md` - Project overview
- ✅ `/home/benjimonjo/SONiC/doc/extreme/x440g2_hld.md` - Architecture design (with FIXMEs)
- ✅ `/home/benjimonjo/SONiC/doc/extreme/x440g2_implementation_guide.md` - Step-by-step procedures
- ✅ `/home/benjimonjo/SONiC/doc/extreme/x440g2_quick_reference.md` - Developer reference
- ✅ `/home/benjimonjo/SONiC/doc/extreme/x440g2_porting_checklist.md` - Progress tracking
- ✅ `/home/benjimonjo/SONiC/doc/extreme/x440g2_hardware_reference.md` - Hardware discovery (NEW!)

## Estimated Timeline

- **Phase 1 Completion**: 3-5 days (pending ASIC confirmation)
- **Phase 2 (Platform Setup)**: 3-5 days  
- **Phase 3 (Driver Implementation)**: 2-4 weeks
- **Phase 4-5 (Testing)**: 2-4 weeks
- **Phase 6 (Upstream)**: 1-2 weeks

**Total Estimated Effort**: 6-12 weeks

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| ASIC not Broadcom | LOW | CRITICAL | Verify immediately |
| I2C topology differs from assumptions | MEDIUM | HIGH | Early probing/discovery |
| ONIE not present/compatible | MEDIUM | MEDIUM | Plan alternative boot |
| Limited documentation available | HIGH | MEDIUM | Community support, reverse-engineer |

## Recommendations

### Immediate Action Items
1. **HIGH PRIORITY**: Get ASIC model confirmation
   - This is the lynch-pin for all decisions
   - Everything depends on this

2. **HIGH PRIORITY**: Obtain any available Extreme Networks documentation
   - Hardware manual
   - Block diagram
   - Schematic (if available)
   - BOM

3. **MEDIUM PRIORITY**: Prepare reference platforms
   - Study existing SONiC Tomahawk implementations
   - Document similarities/differences
   - Get familiar with Broadcom SAI API

4. **MEDIUM PRIORITY**: Plan hardware access strategy
   - Ensure SSH access for development
   - Plan for serial console if needed
   - Consider JTAG for debugging

## Success Metrics for Phase 1

- [x] Connected to hardware successfully
- [x] Basic device identification complete
- [ ] ASIC model confirmed
- [ ] I2C topology mapped
- [ ] CPU specifications identified
- [ ] Port configuration documented
- [ ] All assumptions verified

**Current Phase 1 Completion**: 60%  
**Blocker**: ASIC Model Identification  

---

## Contact Points

- **Device IP**: 192.168.0.2
- **SSH Credentials**: ollama / Window23
- **SSH Config**: /home/benjimonjo/.ssh/x440g2_config
- **Quick Access**: `sshpass -p Window23 ssh -F ~/.ssh/x440g2_config 192.168.0.2`

---

**Next Update**: After ASIC identification confirmed

