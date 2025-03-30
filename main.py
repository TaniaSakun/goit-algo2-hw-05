import timeit
from handlers.bloom_filter_handler import BloomFilterHandler
from handlers.hyperloglog_handler import HyperLogLogHandler, load_ips_from_logfile

LOG_FILE = "lms-stage-access.log"

def run_bloom_filter():
    bloom_handler = BloomFilterHandler()

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom_handler.bloom.add(password)

    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = bloom_handler.check_password_uniqueness(new_passwords_to_check)

    print("\nBloom Filter Password Check:")
    for password, status in results.items():
        print(f"Password '{password}': {status}")

def run_hyperloglog():
    ip_addresses = load_ips_from_logfile(LOG_FILE)
    hll_handler = HyperLogLogHandler(p=14)

    exact_time = timeit.timeit(lambda: hll_handler.count_exact(ip_addresses), number=5)
    custom_hll_time = timeit.timeit(lambda: hll_handler.count_custom_hll(ip_addresses), number=5)
    lib_hll_time = timeit.timeit(lambda: hll_handler.count_hll_lib(ip_addresses), number=5)

    exact_count = hll_handler.count_exact(ip_addresses)
    custom_hll_count = hll_handler.count_custom_hll(ip_addresses)
    lib_hll_count = hll_handler.count_hll_lib(ip_addresses)

    print("\nHyperLogLog Unique IP Estimation:")
    print(f"{'Method':24} {'Unique Count':<20} {'Execution Time (sec)'}")
    print(f"{'Exact Count':24} {exact_count:<20} {exact_time:.4f}")
    print(f"{'Custom HyperLogLog':24} {custom_hll_count:<20} {custom_hll_time:.4f}")
    print(f"{'HyperLogLog (datasketch)':24} {lib_hll_count:<20} {lib_hll_time:.4f}")

if __name__ == "__main__":
    run_bloom_filter()
    run_hyperloglog()
