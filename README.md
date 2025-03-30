# goit-algo2-hw-05
The repository for the 5th GoItNeo Design and Analysis of Algorithms homework


### Task 1: Checking password uniqueness using a Bloom filter

Create a function to check the uniqueness of passwords using a Bloom filter. This function should determine whether a password has been used before, without the need to store the passwords themselves.

#### Requirements:
1. Implement the BloomFilter class, which provides adding elements to the filter and checking for the presence of an element in the filter.

2. Implement the function check_password_uniqueness, which uses an instance of BloomFilter and checks a list of new passwords for uniqueness. It should return the check result for each password.

3. Ensure proper handling of all types of data. Passwords should be handled simply as strings, without hashing. Empty or incorrect values must also be taken into account and processed appropriately.

4. The function and class must work with large datasets while using minimal memory.

#### Results:
Bloom Filter Password Check:

Password 'password123': Already used

Password 'newpassword': Unique

Password 'admin123': Already used

Password 'guest': Unique

### Task 2: Comparison of HyperLogLog performance with exact count of unique elements

Create a script to compare the exact count of unique elements and the count using HyperLogLog.

#### Requirements:
1. Download the dataset from the real log file lms-stage-access.log, which contains information about IP addresses.

2. Implement a method for accurately counting unique IP addresses using a set structure.

3. Implement a method for approximate counting of unique IP addresses using HyperLogLog.

4. Conduct a comparison of the methods based on execution time.

#### Results:

| Method | Unique Count | Execution Time (sec) |
| ---- | ---- | ---- | 
| Exact Count  | 28 | 0.0017 |
| Custom HyperLogLog | 11045.308086634144 | 0.0585 |
| HyperLogLog (datasketch) | 28.023953075428718 | 0.2752 |