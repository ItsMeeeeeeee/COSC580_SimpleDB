from parser import SQLParser

p = SQLParser()
# print(p.parse('SELECT * FROM table1 WHERE a=1'))
print(p.parse('DELETE FROM table where col1 = 1 AND col2 = 2'))
