from parser import SQLParser

p = SQLParser()
# print(p.parse('SELECT * FROM table1 WHERE a=1'))
print(p.parse('INSERT INTO table1 (col1, col2, col3, col4) values (1, 2, 3, 4)'))

print(p.parse('INSERT INTO table1 values (1, 2, 3, 4)'))