from parserSQL import *
from executorSQL import *

p = executorSQL.SQLExecuter()
p.execute("show database")
# p.execute("CREATE DATABASE db")
p.execute("USE db")
# p.execute("CREATE TABLE TABLE2 ( COL3 Boolean, COL2 int )")
# p.execute("INSERT INTO TABLE2 VALUES (No, 1)")
# p.execute("INSERT INTO TABLE2 VALUES (YES, 7)")
# p.execute("INSERT INTO TABLE2 VALUES (YES, 6)")
# p.execute("INSERT INTO TABLE2 VALUES (YES, 4)")
# p.execute("INSERT INTO TABLE2 VALUES (No, 9)")
# p.execute("INSERT INTO TABLE2 VALUES (YES, 11)")
# p.execute("INSERT INTO TABLE2 VALUES (YES, 15)")
# p.execute("INSERT INTO TABLE2 VALUES (YES, 18)")
# p.execute("INSERT INTO TABLE2 VALUES (No, 22)")
# p.execute("CREATE INDEX index1 ON TABLE1 (COL2) ")
p.execute("SELECT COL1, COL2 FROM TABLE1")
# p.execute("SELECT * FROM TABLE2")
# todo TABLE.COL --> CONDITION
# p.execute("UPDATE TABLE1 set COL1 = YES, COL2 = 6 WHERE COL2 = 4 OR COL2 = 10 ")
# p.execute("SELECT * FROM TABLE1 JOIN TABLE2 ON TABLE1.COL1 = TABLE2.COL3")
# p.execute("DELETE FROM TABLE1 WHERE COL2 = 1 ")
# p.execute("DELETE FROM TABLE1 WHERE COL2 = 1 OR COL1 = No")
# p.execute("DELETE FROM TABLE2 WHERE COL2 = 19")
# p.execute("SELECT * FROM TABLE1")
p.execute("EXIT")
