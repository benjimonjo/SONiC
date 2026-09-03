
# Extreme Networks X440-G2 Hardware Reference




## Introduction
The X440-G2 is a high-performance networking platform designed for enterprise-grade applications. It features multiple ports, advanced I/O capabilities, and optimized power management.


- Ports:
  - **eth0**: 10Gbps
  - **eth1**: 10Gbps
  - **eth2**: 10Gbps
  - **eth3**: 10Gbps
- I/O Capabilities:
  - 4x SFP+ ports for 10Gbps connectivity.
  - High-speed data paths for optimized performance.
- Power Management:
  - Efficient power consumption with dynamic voltage and frequency scaling (DVFS).
  - Hot-swappable modules for easy maintenance.











## Hardware Specifications
### ASIC Model
The hardware is equipped with a Broadcom ASIC (ASIC1) that supports advanced networking features. The X440-G2 is designed to support a wide range of applications, including data center networks, branch offices, and campus environments.


### Port Mapping
- **eth0**: asic1.0 lane 0
- **eth1**: asic1.0 lane 1
- **eth2**: asic1.0 lane 2
- **eth3**: asic1.0 lane 3





## Documentation
- [SONiC Platform Integration Guide](/opt/sonic/docs/platform/platform-integration-guide.pdf)
- [Broadcom SAI SDK Documentation](/usr/include/broadcom-sai-sdk/sai)
- [EEPROM Format Documentation](/opt/sonic/docs/eeprom/eeprom-format.pdf)









## I2C Bus Mapping
- **i2c-0**: asic1.0 lane 4
- **i2c-1**: asic1.0 lane 5
- **i2c-2**: asic1.0 lane 6
- **i2c-3**: asic1.0 lane 7





## Power Consumption Specifications
- Efficient power consumption with dynamic voltage and frequency scaling (DVFS)
- Hot-swappable modules for easy maintenance


## Thermal Design Specifications
- Optimized thermal management using Extreme Networks x440-G2






## Performance Benchmarks
- Task-clock:CLOCK_PROCESS_CPUTIME,task-clock:CLOCK_THREAD_CPUTIME

































































































































































































































## Known Extremes Networks/Broadcom Errata
- Contact Extreme Networks support for detailed errata information

