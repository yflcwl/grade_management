from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import re
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = '123456'
app.permanent_session_lifetime = timedelta(minutes=30)

# 使用字典存储用户数据
users_db = {
    '001': '001001',
    '002': '002002',
    '003': '003003'
}

# 使用字典存储成绩数据 - 优化结构便于自动渲染
score_db = {
    "001": {"姓名": "张三", "数学": 90, "语文": 80, "英语": 60, "Python Web": 97, "数据结构": 85, "计算机组成原理": 78},
    "002": {"姓名": "李四", "数学": 92, "语文": 99, "英语": 73, "Python Web": 98, "数据结构": 88, "计算机组成原理": 91},
    "003": {"姓名": "韩梅梅", "数学": 78, "语文": 68, "英语": 66, "Python Web": 99, "数据结构": 82, "计算机组成原理": 76}
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

#登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('score'))

    if request.method == 'POST':
        username = request.form.get('username', "").strip()
        password = request.form.get('password', "").strip()

        # 输入验证
        valid, msg = validate_input(username, password)
        if not valid:
            write_log(f"登录失败：非法输入 用户名={username}")
            return render_template('login.html', error=msg)

        # 用户名+密码验证
        if username in users_db and users_db[username] == password:
            session['username'] = username
            session.permanent = True
            write_log(f"用户 {username} 登录成功")
            return redirect(url_for('score'))
        else:
            write_log(f"用户 {username} 登录失败：密码错误")
            return render_template('login.html', error="用户名或密码错误")

    return render_template('login.html')

# 日志记录函数
def write_log(message):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'app.log')
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{time_str}] {message}\n")

#查看分数
@app.route('/score')
def score():
    username = session.get('username')
    if not username:
        write_log("未登录访问被拒绝：访问 /score")
        return redirect(url_for('login'))

    write_log(f"用户 {username} 查看成绩")

    if username in score_db:
        student_info = score_db[username]
        return render_template('score.html',
                               student_id=username,
                               student_info=student_info)
    else:
        return render_template('score.html',
                               student_id=username,
                               error='未找到成绩信息')

# 输入验证函数
def validate_input(username, password):
    # 去掉前后空格
    username = username.strip()
    password = password.strip()

    # 用户名必须是 3 位数字
    if not re.fullmatch(r"\d{3}", username):
        return False, "学号必须是 3 位数字，如 001"

    # 密码至少 6 位
    if len(password) < 6:
        return False, "密码长度至少为 6 位"

    return True, ""

#退出登录
@app.route('/logoff')
def logoff():
    username = session.get('username')
    write_log(f"用户 {username} 退出登录")
    session.clear()
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True, port=5000)