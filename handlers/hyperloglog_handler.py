import json
import math
import mmh3
from datasketch import HyperLogLog

LOG_FILE = "lms-stage-access.log"

class CustomHyperLogLog:
    def __init__(self, p=12):
        self.p = p
        self.m = 1 << p  # Total registers (2^p)
        self.registers = [0] * self.m
        self.alpha = self._get_alpha()

    def _get_alpha(self):
        """Returns the correction constant based on p."""
        return 0.673 if self.p <= 16 else 0.7213 / (1 + 1.079 / self.m)

    def add(self, item):
        """Hashes an item and updates the register."""
        x = mmh3.hash(str(item), signed=False)
        j = x & (self.m - 1)
        w = x >> self.p
        self.registers[j] = max(self.registers[j], self._rho(w))

    def _rho(self, w):
        """Counts leading zeroes before the first 1 in binary representation."""
        return len(bin(w)) - 2 if w > 0 else 32

    def count(self):
        """Estimates the number of unique elements."""
        Z = sum(2.0 ** -r for r in self.registers)
        return self.alpha * self.m * self.m / Z

def load_ips_from_logfile(filename):
    """Loads IP addresses from a log file, ignoring invalid lines."""
    ip_list = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    ip = data.get("remote_addr")
                    if ip:
                        ip_list.append(ip)
                except (json.JSONDecodeError, TypeError):
                    pass
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return ip_list

class HyperLogLogHandler:
    def __init__(self, p=12):
        self.custom_hll = CustomHyperLogLog(p)
        self.hll_lib = HyperLogLog(p)

    def count_exact(self, ips):
        """Returns exact count of unique IPs using a set."""
        return len(set(ips))

    def count_custom_hll(self, ips):
        """Estimates unique IPs using custom HyperLogLog."""
        for ip in ips:
            self.custom_hll.add(ip)
        return self.custom_hll.count()

    def count_hll_lib(self, ips):
        """Estimates unique IPs using datasketch's HyperLogLog."""
        for ip in ips:
            self.hll_lib.update(ip.encode('utf-8'))
        return self.hll_lib.count()
