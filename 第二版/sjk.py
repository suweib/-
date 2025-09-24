from pymysql import Connect

def readMysql():
    try:  # 异常处理
        con = Connect(
            host='localhost',  # 数据库地址
            port=3306,  # 端口
            user='root',  # 用户名
            passwd='123456',  # 密码
            db='python_l_x',  # 要操作的数据库名称
            charset='utf8',  # 编码方式
            autocommit=True  # 自动提交
        )
        read_cursor = con.cursor()  # 创建游标对象
        sql = "select password,username from xigoshang"
        read_cursor.execute(sql)  # 游标对象执行sql
        result = read_cursor.fetchall()  # 获取查询结果
        con.close()  # 关闭连接
        return result
    except Exception as e:  # 异常类型处理
        print('异常类型', e)#数据库