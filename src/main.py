#!/usr/bin/env python3
"""
Implementation script for X440-G2 SONiC port
This script will help with the systematic approach to porting SONiC to this device
"""

import subprocess
import sys
import os

class X440G2SONiCPorter:
    def __init__(self):
        self.device_ip = os.getenv("X440G2_HOST", "192.168.0.2")
        self.ssh_user = os.getenv("X440G2_SSH_USER", "ollama")
        self.ssh_pass = os.getenv("X440G2_SSH_PASSWORD")
        self.ssh_config = os.getenv("X440G2_SSH_CONFIG")
        self.current_phase = "discovery"
        
    def run_ssh_command(self, command):
        """Execute a command via SSH"""
        ssh_cmd = ["ssh"]
        if self.ssh_config:
            ssh_cmd.extend(["-F", self.ssh_config])
        ssh_cmd.extend([f"{self.ssh_user}@{self.device_ip}", command])
        if self.ssh_pass:
            ssh_cmd = ["sshpass", "-e", *ssh_cmd]
        try:
            environment = os.environ.copy()
            if self.ssh_pass:
                environment["SSHPASS"] = self.ssh_pass
            result = subprocess.run(
                ssh_cmd, capture_output=True, text=True, env=environment, check=False
            )
            if result.returncode:
                print(result.stderr.strip(), file=sys.stderr)
            return result.stdout
        except Exception as e:
            print(f"Error executing command: {e}")
            return None
    
    def check_asic_model(self):
        """Check the ASIC model using dmesg output"""
        print("Checking ASIC model...")
        dmesg_output = self.run_ssh_command("dmesg")
        
        if dmesg_output:
            # Look for HURRICANE2 in dmesg
            lines = dmesg_output.split('\n')
            for line in lines:
                if 'HURRICANE2' in line:
                    print(f"Found ASIC info: {line}")
                    return "HURRICANE2"
        return None
    
    def scan_i2c_buses(self):
        """Scan all I2C buses to map topology"""
        print("Scanning I2C buses...")
        i2cdetect_output = self.run_ssh_command("i2cdetect -l")
        
        if i2cdetect_output:
            print("I2C Bus Information:")
            print(i2cdetect_output)
            
            # Extract bus numbers
            buses = []
            for line in i2cdetect_output.split('\n'):
                if 'i2c-' in line:
                    # Parse bus number from output like "i2c-0"
                    parts = line.split('-')
                    if len(parts) > 1 and parts[1].isdigit():
                        buses.append(int(parts[1]))
            
            print(f"Found I2C buses: {buses}")
            
            print(
                "Bus enumeration only; do not scan unknown buses automatically. "
                "Record the bus list, review active drivers, then perform approved scans manually."
            )
                    
        return None
    
    def get_system_info(self):
        """Get basic system information"""
        print("Getting system information...")
        
        # CPU info
        cpu_info = self.run_ssh_command("cat /proc/cpuinfo")
        if cpu_info:
            print("CPU Info:")
            print(cpu_info[:500] + "..." if len(cpu_info) > 500 else cpu_info)
        
        # Memory info
        mem_info = self.run_ssh_command("cat /proc/meminfo | grep MemTotal")
        if mem_info:
            print("\nMemory Info:")
            print(mem_info)
        
        # Kernel version
        kernel_version = self.run_ssh_command("cat /proc/version")
        if kernel_version:
            print("\nKernel Version:")
            print(kernel_version)
            
        # Loaded modules
        modules = self.run_ssh_command("lsmod | grep bcm")
        if modules:
            print("\nLoaded Broadcom Modules:")
            print(modules)
    
    def create_port_config(self):
        """Refuse to generate an unverified port configuration."""
        raise RuntimeError(
            "Port configuration is blocked until the exact BCM device, SAI support, "
            "and physical port-to-lane map are verified."
        )
    
    def main(self):
        """Main execution flow"""
        print("=" * 60)
        print("X440-G2 SONiC Port Implementation")
        print("=" * 60)
        
        # Phase 1: Discovery
        print("\nPhase 1: Hardware Discovery")
        print("-" * 30)
        
        # Check ASIC model
        asic_model = self.check_asic_model()
        if asic_model:
            print(f"✅ Identified ASIC Model: {asic_model}")
        else:
            print("⚠️ Could not identify ASIC model")
            
        # Get system info
        self.get_system_info()
        
        # Scan I2C buses
        self.scan_i2c_buses()
        
        print("\n" + "=" * 60)
        print("Discovery collection complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Preserve the raw discovery output in doc/extreme/LINUX_SHELL_FINDINGS.md")
        print("2. Verify the exact BCM device and MIPS64 SAI/SDK support")
        print("3. Confirm a recoverable boot and install path")
        print("4. Only then create platform files in a sonic-buildimage checkout")

if __name__ == "__main__":
    porter = X440G2SONiCPorter()
    porter.main()
