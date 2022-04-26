with open("./testCase.input", "a+") as f:
    # generate i-i relation
    f.write("SHOW DATABASES\n")
    f.write("CREATE DATABASE DB\n")
    f.write("USE DB\n")
    f.write("CREATE TABLE I-I-1000 (COL1 int, COL2 int)\n")
    f.write("CREATE TABLE I-1-1000 (COL1 int, COL2 int)\n")
    f.write("CREATE TABLE I-I-10000 (COL1 int, COL2 int)\n")
    f.write("CREATE TABLE I-1-10000 (COL1 int, COL2 int)\n")
    f.write("CREATE TABLE I-I-100000 (COL1 int, COL2 int)\n")
    f.write("CREATE TABLE I-1-100000 (COL1 int, COL2 int)\n")
    for index in range(1, 1001):
        f.write(f"INSERT INTO I-I-1000 VALUES ({index}, {index})\n")
    for index in range(1, 1001):
        f.write(f"INSERT INTO I-1-1000 VALUES ({index}, 1)\n")
    for index in range(1, 10001):
        f.write(f"INSERT INTO I-I-10000 VALUES ({index}, {index})\n")
    for index in range(1, 10001):
        f.write(f"INSERT INTO I-1-10000 VALUES ({index}, 1)\n")
    for index in range(1, 100001):
        f.write(f"INSERT INTO I-I-100000 VALUES ({index}, {index})\n")
    for index in range(1, 100001):
        f.write(f"INSERT INTO I-1-100000 VALUES ({index}, 1)\n")