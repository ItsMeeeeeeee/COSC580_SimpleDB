from parserSQL import *
from executorSQL import *

p = executorSQL.SQLExecuter()
p.execute("show databases")
p.execute("CREATE DATABASE test")
p.execute("USE test")
# p.execute("CREATE TABLE TABLE2 ( COL1 int primary, COL3 Boolean, COL2 int )")
# p.execute("INSERT INTO TABLE2 VALUES (1, No, 1)")
# p.execute("INSERT INTO TABLE2 VALUES (2, YES, 7)")
# p.execute("INSERT INTO TABLE2 VALUES (3, YES, 6)")
# p.execute("INSERT INTO TABLE2 VALUES (4, YES, 4)")
# p.execute("INSERT INTO TABLE2 VALUES (5, No, 9)")
# p.execute("INSERT INTO TABLE2 VALUES (6, YES, 11)")
# p.execute("INSERT INTO TABLE2 VALUES (7, YES, 15)")
# p.execute("INSERT INTO TABLE2 VALUES (8, YES, 18)")
# p.execute("INSERT INTO TABLE2 VALUES (9, No, 22)")

# p.execute("CREATE INDEX index1 ON TABLE1 (COL2) ")
p.execute("SELECT * FROM TABLE2")
p.execute("UPDATE TABLE2 set COL1 = 2, COL3 = No, COL2 = 3 WHERE COL1 = 0")
p.execute("SELECT * FROM TABLE2")


# p.execute("SELECT * FROM TABLE2")
# p.execute("SELECT AVG(COL2), AVG(COL1) FROM TABLE2 WHERE COL2 > 18 GROUP BY COL3")
# p.execute("SELECT AVG(COL2), AVG(COL1) FROM TABLE2 GROUP BY COL3")
# p.execute("SELECT * FROM TABLE2 GROUP")
# p.execute("SELECT COL2 FROM TABLE2")
# p.execute("SELECT * FROM TABLE2")
# p.execute("UPDATE TABLE1 set COL1 = YES, COL2 = 6 WHERE COL2 = 4 OR COL2 = 10 ")
# p.execute("SELECT * FROM TABLE1 JOIN TABLE2 ON TABLE1.COL1 = TABLE2.COL3")
# p.execute("DELETE FROM TABLE1 WHERE COL2 = 1 ")
# p.execute("DELETE FROM TABLE1 WHERE COL2 = 1 OR COL1 = No")
# p.execute("DELETE FROM TABLE2 WHERE COL2 = 19")

p.execute("EXIT")
