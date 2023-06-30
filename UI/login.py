import pymysql

def db_login(db_username: str, db_password: str):
    connect_status = connect_test()

    if connect_status == True:
        db = pymysql.connect(host='localhost', user='root', passwd='cug20211000986', database='students_score',
                             port=3306)
        login_cursor = db.cursor()
        if db_username[0] == '1':
            login_cursor.execute("select password from stu_ac where sno = %s", db_username)
            stu_pw = login_cursor.fetchone()
            try:
                if stu_pw[0] == db_password:
                    print('学生登录成功')
                    return 1
                else:
                    print('密码错误')
                    return -1
            except:
                print('用户名不存在')
                return -1

        elif db_username[0] == '2':
            login_cursor.execute("select password from tea_ac where tno = %s", db_username)
            tea_pw = login_cursor.fetchone()
            try:
                if tea_pw[0] == db_password:
                    print('教师登录成功')
                    return 2
                else:
                    print('密码错误')
                    return -1
            except:
                print('用户名不存在')
                return -1

        elif db_username == 'admin':
            login_cursor.execute("select password from admin_ac where admin_id = %s", db_username)
            admin_pw = login_cursor.fetchone()
            try:
                if admin_pw[0] == db_password:
                    print('管理员登录成功')
                    return 3
                else:
                    print('密码错误')
                    return -1
            except:
                print('用户名不存在')
                return -1

        login_cursor.close()
        db.close()


    else:
        return -2


def connect_test():
    try:
        db = pymysql.connect(host='localhost', user='root', passwd='cug20211000986', database='students_score',
                             port=3306)
        db.close()
        return True
    except:
        print('数据库连接失败')
        return False



