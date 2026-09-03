# Extreme Networks X440-G2 Hardware Reference

**Model**: X440G2-48p-10G4
**Full model code**: 800618-00-11
**Hardware revision**: 1711N-40116 Rev 11.0
**Discovery date**: 2026-09-02
**Evidence status**: Confirmed findings are distinguished from items requiring on-device probing.

## Confirmed Platform Baseline

| Area | Confirmed finding | Source |
|---|---|---|
| Front-panel data ports | 48 × 1GbE plus 4 × 10GbE SFP+ (52 total) | ExtremeXOS inventory / port status |
| Switching architecture | Two Broadcom Hurricane2 forwarding units | Linux kernel log |
| Control-plane CPU | Cavium Octeon III V0.2 (CN7010), MIPS64 | `/proc/cpuinfo` |
| Kernel | Linux 2.6.28.9-summit_octeon, built 2016-06-16 | `/proc/version` |
| Vendor OS | ExtremeXOS 21.1.1.4-patch1-5 | Device inventory |
| Platform-management access | BusyBox shell available from ExtremeXOS via `run script shell.py` | On-device test |
| RAM | `MemTotal: 976128 kB` (approximately 953 MiB) | `/proc/meminfo` |
| Cooling | One fan tray with four fans reported | ExtremeXOS inventory |
| Power | One internal PSU reported; a second PSU is not present | ExtremeXOS inventory |

### Important Porting Consequence

This is a **MIPS64 control-plane platform**, not an x86_64 platform. Existing SONiC x86_64 platform paths, prebuilt packages, and the old ExtremeXOS kernel cannot be assumed to be reusable. A viable port needs a supported MIPS64 build and boot strategy, as well as a SAI implementation compatible with the two Hurricane2 units.

## Forwarding ASIC

Linux boot messages identify two Hurricane2 units:

```
HURRICANE2 unit 0: TotalCells=0x3000, DedicatedCells=0x9ec,
                   DynCells=0x2614, Ports=0x1d (28 26 2)
HURRICANE2 unit 1: TotalCells=0x3000, DedicatedCells=0x9ec,
                   DynCells=0x2614, Ports=0x1d (28 26 2)
```

| Property | Value | Confidence |
|---|---|---|
| ASIC vendor | Broadcom | Confirmed |
| ASIC family | Hurricane2 | Confirmed from kernel log |
| Number of forwarding units | 2 | Confirmed from kernel log |
| Total buffer cells per unit | `0x3000` (12,288) | Confirmed from kernel log |
| Dedicated / dynamic cells per unit | `0x9ec` / `0x2614` | Confirmed from kernel log |
| BCM56640 B0 | `libbcmplat.so` contains `bcm56640_b0 v 1.3` | Candidate only; shared library also contains other ASIC definitions |
| External port mapping | Not yet determined | Requires SDK/platform mapping evidence |
| Exact BCM part number and SDK/SAI support | Not yet determined | Requires vendor or SDK evidence |

The kernel message's port tuple is not a finished physical-port map. It establishes that the system has two forwarding units, but the physical-port-to-unit, BCM-port, lane, and stacking-port mapping remains an open discovery task. Likewise, a BCM56640 B0 string in a shared SDK library is insufficient to identify the installed chip, because the same library contains definitions for other ASICs.

## Physical Interfaces

| Interface | Confirmed details | Remaining work |
|---|---|---|
| Data ports 1–48 | 1GbE copper/RJ45 | Map each port to ASIC unit, BCM port, and lane |
| Data ports 49–52 | 10GbE SFP+ | Verify module cages, lane mapping, and supported optics |
| Management Ethernet | 10/100/1000 interface reported | Identify Linux interface, MAC source, and boot-time configuration |
| Console | Present in the product family; connector/pinout not verified | Verify physical connector and UART settings |
| Stacking | Kernel logs indicate stacking-related ports | Determine whether they can be disabled or require a SONiC-specific design |

## Control Plane and Software Inventory

| Property | Value |
|---|---|
| CPU | Cavium Octeon III V0.2 |
| CPU architecture | MIPS64 |
| Board identifier | `CN7010p1.2-1000-CP` |
| Reported BogoMIPS | 2000.00 |
| Kernel | `2.6.28.9-summit_octeon` |
| Shell | BusyBox v1.13.4 |
| Broadcom support modules observed | `linux_bcm_diag_full`, `bcmhelper`, `linux_uk_proxy`, `linux_kernel_bde`, `pciphymod` |
| Extreme platform modules observed | `aspenpmap`, `spiFPGA`, `watchdog` |

The boot command line specifies `console=ttyS0,9600`, one core (`coremask=0x1`, `numcores=1`), and boot partition 1. Storage is eMMC (`mmcblk0`) with boot, alternate boot, EXOS, configuration, and scratch partitions. ONIE availability and device-tree source remain unconfirmed.

## Platform Management

Two Octeon I2C adapters are exposed (`i2c-0` and `i2c-1`), but no `/dev/i2c-*` nodes exist and `i2cdetect` is not installed. The only enumerated I2C client is an MCP7940 RTC on bus 1 at `0x6f`; no hwmon devices are exposed. Do not implement drivers based on common example addresses.

| Component | Status | Evidence needed before implementation |
|---|---|---|
| System EEPROM | SPI candidate: Microchip 23K256 (32 KiB) at `spi0.1` | Confirm contents, format, and whether it carries chassis identity |
| Thermal sensors | Unknown | Device count, bus/address, sensor type, thresholds |
| PSU monitoring | Unknown | Interface, bus/address, status and telemetry registers |
| Fan controller | Unknown | Controller type, RPM/PWM paths, fault semantics |
| LEDs / CPLD / FPGA | `spi0.2` exposes `spiFPGA`; control path unknown | FPGA register map and fan/PSU/LED ownership |

The reported fan state (three at 0 RPM and one at 960 RPM) is an observation, not a diagnosis. Confirm the hardware inventory and platform alarm state before classifying any fan as failed.

## Discovery Procedure

Enter the Linux shell from the ExtremeXOS CLI:

```text
run script shell.py
```

Capture raw output with the commands below. This BusyBox image lacks `i2cdetect` and does not expose `/dev/i2c-*`; inspect sysfs rather than attempting a scan.

```bash
cat /proc/cpuinfo
cat /proc/meminfo
cat /proc/version
dmesg | grep -Ei 'hurricane|bcm|i2c|spi|fpga|fan|thermal|psu'
lsmod
ls -l /sys/class/i2c-dev
ls -l /sys/bus/i2c/devices
cat /sys/bus/i2c/devices/1-006f/name
ls -l /sys/bus/spi/devices
ls -l /sys/class/hwmon
ls -l /sys/class/net
```

Record the command, timestamp, raw output, and a cautious interpretation in `LINUX_SHELL_FINDINGS.md`. Do not use `i2cdump -f` against an unknown device in a production switch; forced reads can interfere with an active kernel driver.

## Completion Criteria Before Platform Code

- [ ] Exact BCM device/SDK identity and evidence of usable SAI support
- [ ] Supported boot and MIPS64 build strategy for SONiC
- [ ] Physical-port to ASIC-unit/BCM-port/lane map, including stacking ports
- [ ] I2C/SPI/GPIO topology and platform-device register maps
- [ ] EEPROM format and chassis identity source
- [ ] Fan, PSU, and thermal behaviour validated under safe test conditions

## References

- [Linux shell discovery report](LINUX_SHELL_FINDINGS.md)
- [Current discovery plan](NEXT_STEPS.md)
- [Porting high-level design](x440g2_hld.md)
