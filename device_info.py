import pexpect
import re
from getpass import getpass

host = "10.10.20.48"
username = "developer"
password = getpass("Password: ")

print("Connecting to Cisco router...")

ssh = pexpect.spawn(
    f"ssh -o StrictHostKeyChecking=no {username}@{host}",
    encoding="utf-8",
    timeout=30
)

ssh.expect("Password:")
ssh.sendline(password)

ssh.expect(r"[>#]")

ssh.sendline("terminal length 0")
ssh.expect(r"[>#]")

# Get hostname
ssh.sendline("show running-config | include ^hostname")
ssh.expect(r"[>#]")
hostname_output = ssh.before

# Get IOS version
ssh.sendline("show version")
ssh.expect(r"[>#]")
version_output = ssh.before

hostname_match = re.search(r"^hostname\s+(\S+)", hostname_output, re.MULTILINE)
version_match = re.search(
    r"Cisco IOS XE Software, Version ([^\r\n]+)",
    version_output
)

hostname = hostname_match.group(1) if hostname_match else "Unknown"
ios_version = version_match.group(1) if version_match else "Unknown"

print("\n--- DEVICE INFORMATION ---")
print(f"Hostname: {hostname}")
print(f"IOS XE version: {ios_version}")
print(f"Management IP: {host}")

ssh.sendline("exit")
ssh.close()

print("\nConnection closed.")