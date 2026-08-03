from flask import Flask, jsonify, render_template #import flaskmodule
app = Flask(__name__) #초기화

@app.route('/') #요청주소
def hello_world(): #함수
    return 'Hello,World!!!!' #응답결과

@app.route('/test1')
def test1():
    return '<h1>test1</h1>test1 <style>h1 {color: red}</style>'

@app.route('/test2', methods=[ 'GET', 'POST' ])
def test2():
    return [1, 2, 3]        #jsonify는 json으로 변환시켜라 jsonify[1, 2, 3]
                            # 근데 업데이트되면서 그냥 써도 됨

@app.route('/test3/<tid>')
def test3(tid):
    return 'tid is %s' % tid

@app.route('/test4')
@app.route('/test4/<int:tid>')
def test4(tid=None):
    return 'test4 tid is %s' % tid

@app.route('/assembly')
def assembly():
    members = []

    import pymysql
    conn = pymysql.connect(
        host='svc.sel3.cloudtype.app', user='root', password='1234',
        db='BANG', charset='utf8', port = 31776
    )
    cursor = conn.cursor()
    sql = '''
        select * from assembly_member
        limit 0, 10
    '''

    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(result)  # <= 응답 리스트 또는 딕셔너리

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

if __name__== '__main__':
    app.run(host = '0.0.0.0', port = 80, debug = True) #flask실행

