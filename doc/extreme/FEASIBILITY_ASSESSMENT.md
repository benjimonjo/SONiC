# X440-G2 SONiC Port Feasibility Assessment

**Date**: 2026-09-03  
**Decision**: Do not begin platform-driver or `port_config.ini` implementation yet.

## Assessment

The X440-G2 is not currently a conventional SONiC platform-porting task. The normal upstream porting workflow assumes that the target ASIC is already supported by the selected SAI stack and that a compatible SONiC image can be built and installed. The evidence gathered so far does not establish either condition for this platform:

- The control plane is Cavium Octeon III MIPS64, while the current SONiC release documentation describes an `amd64` kernel image.
- The device has two Broadcom Hurricane2 forwarding units, but the exact BCM part number, Broadcom SDK version, and multi-unit SAI capability are unknown.
- The installed ExtremeXOS kernel is Linux 2.6.28 and cannot be assumed to be a viable base for a current SONiC userspace or Broadcom kernel driver stack.
- ONIE availability and a non-destructive installation path have not been confirmed.

As a result, this work is currently an **OS/boot/SAI enablement investigation** rather than an ordinary platform package implementation.

## Evidence from Upstream SONiC

The [SONiC Porting Guide](https://github.com/sonic-net/SONiC/wiki/Porting-Guide) explicitly assumes an ASIC already supported by SAI/SONiC and places device-specific work in `sonic-buildimage`. It also identifies a Broadcom `config.bcm`, selected from `sai.profile`, as an essential platform artifact. The [Broadcom PDDF guide](https://github.com/sonic-net/SONiC/blob/master/doc/platform/brcm_pdk_pddf.md) similarly treats validated SAI support as a prerequisite to platform bring-up.

This checkout is the SONiC documentation repository. Implementation must take place in a separate `sonic-buildimage` working tree once the feasibility gates below pass.

## Required Gates

| Gate | Required evidence | Current state |
|---|---|---|
| SSH/shell access | Approved credential and Linux shell access | Passed: read-only shell discovery completed on 2026-09-03 |
| Hardware identity | Exact BCM part number and revision from SDK/device data | Open |
| SAI | Vendor-supported SAI package for that BCM device, MIPS64, and two units | Open |
| Kernel and BDE | Supported kernel plus a compatible Broadcom kernel driver/BDE | Open |
| Boot/install | Recoverable, documented image boot path (for example ONIE or serial recovery) | Open |
| Port map | Physical port → unit → BCM port/lane mapping, including stacking ports | Open |
| Platform management | I2C/SPI/GPIO map and device register semantics | Open |

## Next Evidence Collection

Once access is restored, capture the output of the commands in the [hardware reference](x440g2_hardware_reference.md#discovery-procedure). In addition, preserve these read-only artefacts where permitted:

```bash
cat /proc/meminfo
cat /proc/cmdline
cat /proc/mtd
cat /proc/partitions
mount
uname -a
dmesg | grep -Ei 'hurricane|bcm|bde|i2c|spi|fpga|onie|boot'
```

Record raw output first; infer component identities only after correlating it with a driver, device tree, SDK file, or vendor documentation. Never probe unknown I2C devices with forced access on the production switch.

## Implementation Entry Criteria

Create the X440-G2 platform in `sonic-buildimage` only after all of the following are satisfied:

1. A supported MIPS64 target image and a recoverable boot method have been demonstrated.
2. Broadcom has provided or validated a MIPS64-compatible SAI/SDK path for the exact dual-unit hardware.
3. A minimal `config.bcm` and port map initialise both units without exposing stacking ports as front-panel data ports.
4. The platform-management topology is sufficient to implement safe fan, PSU, thermal, EEPROM, and transceiver handling.

Until then, do not create placeholder lane maps, I2C addresses, SDK settings, or an x86_64 platform directory. Those values would look like implementation progress but are not testable on this hardware.
