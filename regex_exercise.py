from __future__ import annotations

# TASK 1
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
    if re.search(r"\d+s$", line):
        print(line)

for line in log_lines:
    if re.search(r"https://|http://", line):
        print(line)

if re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (INFO|ERROR|WARNING|DEBUG) .+", log_lines[0]):
    print("The log is correctly formatted.")

#TASK 2
import re

def reverse_complement(seq) -> str:
    seq = seq[::-1]
    table = str.maketrans("ATCG", "TAGC")
    complemented = seq.translate(table)
    return complemented

class SequencingRead:
    def __init__(self,read_id, sequence):
        self.read_id = read_id
        self.sequence = sequence
    
    def matches_mid_pair(self, forward_mid, reverse_mid) -> bool:
        reverse_mid = reverse_complement(reverse_mid)
        if re.search(fr"^{forward_mid}", self.sequence) and re.search(fr"{reverse_mid}$", self.sequence):
            return True
        return False

    def trim_mid_pair(self, forward_mid, reverse_mid) -> str | None:
        if self.matches_mid_pair(forward_mid, reverse_mid) == True:
            reverse_mid = reverse_complement(reverse_mid)
            trimmed_sequence = re.sub(fr"^{forward_mid}", "", self.sequence)
            trimmed_sequence = re.sub(fr"{reverse_mid}$", "", trimmed_sequence)
            return trimmed_sequence
        return None
    
    def describe(self) -> str:
        length = len(self.sequence)
        return f"SequencingRead {self.read_id} {length}bp"

r1 = SequencingRead("demo_1", "AGCTTCGA" + "N" * 20 + reverse_complement("TGCAGGTC"))
print(r1.describe())
print(r1.matches_mid_pair("AGCTTCGA", "TGCAGGTC"))  # True
print(r1.matches_mid_pair("CGATCGAT", "GCTAGCTA"))  # False
print(r1.trim_mid_pair("AGCTTCGA", "TGCAGGTC"))     # 20 x "N"

#TASK 3
import re
import gzip
import csv
import os
from Bio import SeqIO

class Demultiplexer:
    def __init__(self, fasta_path, mid_table_path):
        self.reads = []
        with gzip.open(fasta_path, "rt") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                self.reads.append(SequencingRead(record.id, str(record.seq)))

        self.mids = []
        with open(mid_table_path, "r") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            self.assigned = {}
            for row in reader:
                label = f"{row['SampleID']}_{row['Description']}"
                self.mids.append((label, row['FBarcodeSequence'], row['RBarcodeSequence']))
                self.assigned[label] = []

        self.unassigned = []

    def assign_reads(self):
        for read in self.reads:
            for label, forward_mid, reverse_mid in self.mids:
                trimmed = read.trim_mid_pair(forward_mid, reverse_mid)
                if trimmed is not None:
                    self.assigned[label].append(SequencingRead(f"{read.read_id}", trimmed))
                    break
            else:
                self.unassigned.append(read)

    def report(self) -> None:
        report = []
        for label, reads in self.assigned.items():
            report.append(f"{label}\t{len(reads)}")
        report.append(f"Unassigned\t{len(self.unassigned)}")
        print("\n".join(report))
        return "\n".join(report)

    def write_fasta(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        for label, reads in self.assigned.items():
            if reads:
                output_path = os.path.join(output_dir, f"{label}.fasta")
                with open(output_path, "w") as file:
                    for r in reads:
                        file.write(f">{r.read_id}\n{r.sequence}\n")        

demux = Demultiplexer("fishes.fna.gz", "fishes_MIDs.csv")
demux.assign_reads()
print(demux.report())
demux.write_fasta("demux_output")



