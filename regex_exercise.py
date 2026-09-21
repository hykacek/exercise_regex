#TASK 1
import re

log_lines = [
    "2024-01-15 10:02:11 INFO Server started on port 8080",
    "2024-01-15 10:03:47 ERROR Failed to connect to database",
    "2024-01-16 08:15:00 WARNING Disk usage at 85%",
    "2024-01-16 14:22:39 ERROR Timeout while fetching https://example.com/api",
    "2024-01-17 09:00:05 INFO User admin logged in from 192.168.1.10",
    "2024-01-17 11:41:18 DEBUG Cache cleared successfully",
    "2024-01-18 03:12:56 ERROR Connection refused from 192.168.1.55",
    "2024-01-18 23:59:02 INFO Backup completed in 42s",
]

for line in log_lines:
    if re.match(r"2024-01-16", line):
        print(line)

for line in log_lines:
    if re.search(r"ERROR|WARNING", line):
        print(line)

ipv4 = []
for line in log_lines:
    if re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", line):
        ipv4.extend(re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", line))
print(ipv4)

for line in log_lines:
    if re.search(r"42s", line):
        print(line)

for line in log_lines:
    if re.search(r"https://|http://", line):
        print(line)

if re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (INFO|ERROR|WARNING|DEBUG) .+", log_lines[0]):
    print("The log is correctly formatted.")