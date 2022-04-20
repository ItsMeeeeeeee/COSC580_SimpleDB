from parserSQL import *
from executorSQL import *

p = executorSQL.SQLExecuter()
# "COL1": ['No', 'yes', 'yes', 'yes', 'No', 'yes', 'yes', 'yes', 'yes'],
# "COL2": [1, 7, 6, 4, 9, 11, 15, 18, 19],
# "__index__": [1, 2, 3, 4, 5, 6, 7, 8, 9]
p.execute("CREATE TABLE TABLE1 ( COL1 Boolean, COL2 int )")
p.execute("INSERT INTO TABLE1 VALUES (No, 1)")
p.execute("INSERT INTO TABLE1 VALUES (YES, 7)")
p.execute("INSERT INTO TABLE1 VALUES (YES, 6)")
p.execute("INSERT INTO TABLE1 VALUES (YES, 4)")
p.execute("INSERT INTO TABLE1 VALUES (No, 9)")
p.execute("INSERT INTO TABLE1 VALUES (YES, 11)")
p.execute("INSERT INTO TABLE1 VALUES (YES, 15)")
p.execute("INSERT INTO TABLE1 VALUES (YES, 18)")
p.execute("INSERT INTO TABLE1 VALUES (NO, 19)")
p.execute("INSERT INTO TABLE1 VALUES (YES, 19)")
p.execute("CREATE INDEX index1 ON TABLE1 (COL2) ")
p.execute("SELECT COL1 FROM TABLE1 WHERE COL1 = YES OR COL2 <= 10")