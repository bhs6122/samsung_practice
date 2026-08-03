from flask import Flask, jsonify, render_template
from flask import request, session
from datetime import timedelta
app = Flask(__name__) #초기화
app.secret_key = '1234abcd'
app.permanent_session_lifetime = timedelta(minutes=30) 
# 세션유지시간 30분
 
# /login?user_id=abcd&user_pw=1   GET 방식
# 로그인
@app.route("/login")
def login():
    form = request.args
    user_id = form['user_id']
    user_pw = form['user_pw']
    # user 테이블에 암호화된 비번 비교 select
    # 로그인 성공 후 꼭 해야하는 작업은
    # 세션에 로그인 흔적 남기기
    session['user_id'] = user_id
    return f'{user_id}, {user_pw}'

@app.route("/join",methods=['GET','POST'])
def join():
    if request.method== 'GET':
        return render_template('join.html')
    else:
        form = request.form
        user_id = form['user_id']
        user_pw = form['user_pw']
        user_name = form['user_name'] 

        #비밀번호 암호화
        import hashlib
        old_pwd = '1234'

        m = hashlib.sha256()
        m.update(old_pwd.encode())
        new_pwd = m.hexdigest()
        #위 세줄과 동일한 코드
        #new_pwd = hashlib.sha256(old_pwd.encode()).hexdigest()

        print(new_pwd)

        import pymysql
        from pymysql.cursors import DictCursor
        
        conn = pymysql.connect(
            host='svc.sel3.cloudtype.app', user='root', 
            password='1234', db='ggoreb', 
            charset='utf8', port = 31776
        )
        cursor = conn.cursor(DictCursor)
        sql = '''
            insert into user
                (id, user_id, user_name, user_pw, created_at)
            values
                (null, %s, %s, %s, now())
        '''
        cursor.execute(sql, (user_id, user_name, user_pw))

        conn.commit()
        cursor.close()
        conn.close()

        return f'가입완료: {user_id}, {user_name}'

if __name__== '__main__':
    app.run(host = '0.0.0.0', port = 80, debug = True) #flask실행

