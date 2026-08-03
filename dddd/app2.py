from flask import Flask, jsonify, render_template
import os

app = Flask(__name__, template_folder='templates') #초기화



# 고객 데이터 조회
@app.route('/customers')
def customers():
    import pymysql
    from pymysql.cursors import DictCursor

    conn = pymysql.connect(
        host='svc.sel3.cloudtype.app', user='root', 
        password='1234', db='BANG', 
        charset='utf8', port = 31776
    )
    cursor = conn.cursor(DictCursor)
    sql = '''
        select * from 고객
    '''
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return render_template('customers.html', data = result)

# @app.route('/test1')
# def test1():
#     return render_template('test1.html', score=100)


# @app.route('/assembly')
# def assembly():
#     import pymysql
#     from pymysql.cursors import DictCursor

#     import pymysql
#     conn = pymysql.connect(
#         host='svc.sel3.cloudtype.app', user='root', password='1234',
#         db='BANG', charset='utf8', port = 31776
#     )
#     cursor = conn.cursor(DictCursor)
#     sql = '''
#         select * from assembly_member
#         limit 0, 10
#     '''

#     cursor.execute(sql)
#     result = cursor.fetchall()
#     print(result)
#     result2 = jsonify(result)
#     cursor.close()
#     conn.close()

#     return result2

if __name__== '__main__':
    app.run(host = '0.0.0.0', port = 80, debug = True) #flask실행

