from executer import SQLExecuter

p = SQLExecuter()


p.execute("CREATE TABLE test { age int primary, name string }")
p.execute('insert into test values (1, 2)')