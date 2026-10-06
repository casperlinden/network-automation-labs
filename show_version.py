import pexpect
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
print("Connected!")

# Disable paging
ssh.sendline("terminal length 0")
ssh.expect(r"[>#]")

# Run command
ssh.sendline("show version")
ssh.expect(r"[>#]")

output = ssh.before

print("\n--- SHOW VERSION ---")
print(output)

ssh.sendline("exit")
ssh.close()

print("\nConnection closed.")