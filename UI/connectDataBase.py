import pymysql


def db_select(sql):
    db = pymysql.connect(host='localhost', user='root', passwd='cug20211000986', database='students_score',
                         port=3306)
    select = db.cursor()
    select.execute(sql)
    result = select.fetchall()
    select.close()
    db.close()

    return result


def db_update(sql):
    db = pymysql.connect(host='localhost', user='root', passwd='cug20211000986', database='students_score',
                         port=3306)

    update = db.cursor()
    update.execute(sql)

    try:
        db.commit()
        print("修改成功")
        return True
    except:
        db.rollback()
        print("修改失败")
        return False


def db_insert(sql):
    db = pymysql.connect(host='localhost', user='root', passwd='cug20211000986', database='students_score',
                         port=3306)

    insert = db.cursor()
    insert.execute(sql)

    try:
        db.commit()
        print("插入成功")
        return True
    except:
        db.rollback()
        print("插入失败")
        return False

def db_delete(sql):
    db = pymysql.connect(host='localhost', user='root', passwd='cug20211000986', database='students_score',
                         port=3306)

    delete = db.cursor()
    delete.execute(sql)

    try:
        db.commit()
        print("删除成功")
        return True

    except:
        db.rollback()
        print("删除失败")
        return False