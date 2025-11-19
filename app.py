from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_123'
app.permanent_session_lifetime = timedelta(minutes=30)

# 使用字典存储用户数据
users_db = {
    '001': '001001',
    '002': '002002',
    '003': '003003'
}

# 使用字典存储成绩数据 - 优化结构便于自动渲染
score_db = {
    "001": {
        "姓名": "张三",
        "数学": 90,
        "语文": 80,
        "英语": 60,
        "Python Web": 97,
        "数据结构": 85,
        "计算机组成原理": 78
    },
    "002": {
        "姓名": "李四",
        "数学": 92,
        "语文": 99,
        "英语": 73,
        "Python Web": 98,
        "数据结构": 88,
        "计算机组成原理": 91
    },
    "003": {
        "姓名": "韩梅梅",
        "数学": 78,
        "语文": 68,
        "英语": 66,
        "Python Web": 99,
        "数据结构": 82,
        "计算机组成原理": 76
    }
}


# 请求钩子 - 检查用户是否登录
@app.before_request
def auth():
    if request.path.startswith('/static'):
        return
    if request.path == '/login':
        return
    if not session.get('username'):
        return redirect(url_for('login'))
    return None


@app.route('/')
def home():
    if session.get('username'):
        return redirect(url_for('score'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('score'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users_db and users_db[username] == password:
            session['username'] = username
            session.permanent = True
            return redirect(url_for('score'))
        else:
            return render_template('login.html', error='用户名或密码错误')

    return render_template('login.html')


@app.route('/score')
def score():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    if username in score_db:
        student_info = score_db[username]
        return render_template('score.html',
                               student_id=username,
                               student_info=student_info)
    else:
        return render_template('score.html',
                               student_id=username,
                               error='未找到成绩信息')


@app.route('/logoff')
def logoff():
    session.pop('username', None)
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)