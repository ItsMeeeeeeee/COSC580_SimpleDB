from executorSQL import *

p = executorSQL.SQLExecuter()
p.execute("show databases")
# p.execute("CREATE DATABASE db")
p.execute("USE db")
# p.execute("CREATE TABLE Student ( ID int, NAME String)")
# p.execute("INSERT INTO Student VALUES (1, huaqiang)")
# p.execute("INSERT INTO Student VALUES (2, maigua)")
# p.execute("INSERT INTO Student VALUES (3, 51fan)")
# p.execute("INSERT INTO Student VALUES (4, madongmei)")
# p.execute("INSERT INTO Student VALUES (5, xialuo)")
# p.execute("INSERT INTO Student VALUES (6, zhang3)")
# p.execute("INSERT INTO Student VALUES (7, wang5)")
# p.execute("INSERT INTO Student VALUES (8, li4)")
#
# p.execute("CREATE TABLE Course ( ID int, CROUSE String)")
# p.execute("INSERT INTO Course VALUES (1, math)")
# p.execute("INSERT INTO Course VALUES (2, english)")
# p.execute("INSERT INTO Course VALUES (3, tech)")
# p.execute("INSERT INTO Course VALUES (4, C)")
# p.execute("INSERT INTO Course VALUES (5, C++)")
# p.execute("INSERT INTO Course VALUES (6, JAVA)")
# p.execute("INSERT INTO Course VALUES (7, Python)")


# p.execute("INSERT INTO TABLE2 VALUES (YES, 6)")
# p.execute("INSERT INTO TABLE2 VALUES (YES, 4)")
# p.execute("INSERT INTO TABLE2 VALUES (No, 9)")
# p.execute("INSERT INTO TABLE2 VALUES (YES, 11)")
# p.execute("INSERT INTO TABLE2 VALUES (YES, 15)")
# p.execute("INSERT INTO TABLE2 VALUES (YES, 18)")
# p.execute("INSERT INTO TABLE2 VALUES (No, 22)")
# p.execute("CREATE INDEX index1 ON TABLE1 (COL2) ")
# p.execute("SELECT * FROM Course WHERE ID > 5 AND ID < 10")
# p.execute("SELECT * FROM TABLE2")
# todo TABLE.COL --> CONDITION
# p.execute("UPDATE TABLE1 set COL1 = YES, COL2 = 6 WHERE COL2 = 4 OR COL2 = 10 ")
p.execute("SELECT * FROM Course JOIN Student ON Course.ID = Student.ID WHERE Course.ID > 3")
# p.execute("DELETE FROM TABLE1 WHERE COL2 = 1 ")
# p.execute("DELETE FROM TABLE1 WHERE COL2 = 1 OR COL1 = No")
# p.execute("DELETE FROM Student WHERE ID = 3")
# p.execute("SELECT * FROM TABLE1")
p.execute("EXIT")
