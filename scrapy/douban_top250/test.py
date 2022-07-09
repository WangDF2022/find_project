import pymysql
#----———洋接
connect=pymysql.connect(
    host='localhost',#衣地数落席
    user='root',
    password='123456',
    db='mydb2',
    charset='utf8')  #服务系名,账户,密号,数据库名称
cur=connect.cursor()
print(cur)

try:
    create_sqli = "create table stu(id int,name varchar(30),phone int);"
    cur.execute(create_sqli)
except Exception as e:
    print("创建数据表失败:",e)
else:
    print("创建数据表成功;")
#-海入-
try:
    insert_sqli="insert into stu values(001,'xiaoming',123456789);"
    cur.execute(insert_sqli)
except Exception as e:
    print("插入数据失败:",e)
else:
#如聚是源入数据,一定要超交数据,不然数辉库中拨不到要插入的数;
    connect.commit()
    print("插入数据成功;")