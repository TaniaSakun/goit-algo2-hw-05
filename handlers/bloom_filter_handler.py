import mmh3
from bitarray import bitarray

class BloomFilter:
    def __init__(self, size=1000, num_hashes=3):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, item):
        """Adds an item to the Bloom filter."""
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"Invalid password: {item}. Must be a non-empty string.")
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = 1

    def contains(self, item):
        """Checks if an item is in the Bloom filter (possible false positives)."""
        return all(self.bit_array[mmh3.hash(item, i) % self.size] for i in range(self.num_hashes))

class BloomFilterHandler:
    def __init__(self):
        self.bloom = BloomFilter()

    def check_password_uniqueness(self, pass_list):
        """Checks if passwords are unique using Bloom Filter."""
        results = {}
        for password in pass_list:
            if not isinstance(password, str) or not password.strip():
                results[password] = "Invalid password"
                continue
            if self.bloom.contains(password):
                results[password] = "Already used"
            else:
                results[password] = "Unique"
                self.bloom.add(password)
        return results
