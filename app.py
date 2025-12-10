from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import re
import os
from datetime import datetime
<<<<<<< HEAD
=======

from flask_sqlalchemy import SQLAlchemy
>>>>>>> ca6e236 (修改为sqlit存储数据)

app = Flask(__name__)
app.secret_key = '123456'
app.permanent_session_lifetime = timedelta(minutes=30)

#if os.path.exists('tutorial.db'):
#   os.remove('tutorial.db')
#    print("已删除旧的数据库文件")

# 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'tutorial.db')
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy()
db.init_app(app)

class User(db.Model):
    __table__name='user'
    # id,单元格类型，唯一值
    id = db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.String(13),unique=True,nullable=False)
    password=db.Column(db.String(100),nullable=False)
    name=db.Column(db.String(5),nullable=False)
    math =db.Column(db.String(5),nullable=False)
    chinese=db.Column(db.String(5),nullable=False)
    english=db.Column(db.String(5),nullable=False)
    PythonWeb=db.Column(db.String(5),nullable=False)
    DataStructures=db.Column(db.String(5),nullable=False)
    ComputerOrganization=db.Column(db.String(5),nullable=False)


with app.app_context():
    db.create_all()
    try:
        new_user1 = User(user_id='001', password='001001', name="张三", math="90", chinese="80", english="60",
                         PythonWeb="97", DataStructures="85", ComputerOrganization="78")
        new_user2 = User(user_id='002', password='002002', name="李四", math="92", chinese="99", english="73",
                         PythonWeb="98", DataStructures="88", ComputerOrganization="91")
        new_user3 = User(user_id='003', password='003003', name="韩梅梅", math="78", chinese="68", english="66",
                         PythonWeb="99", DataStructures="82", ComputerOrganization="76")

        db.session.add(new_user1)
        db.session.add(new_user2)
        db.session.add(new_user3)
        db.session.commit()
        print("添加用户成功")
    except Exception as e:
        db.session.rollback()
        print(f"添加用户失败：{str(e)}")


# 使用字典存储用户数据
<<<<<<< HEAD
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
=======
# users_db = {
#     '001': '001001',
#     '002': '002002',
#     '003': '003003'
# }
#
# # 使用字典存储成绩数据 - 优化结构便于自动渲染
# score_db = {
#     "001": {"姓名": "张三", "数学": 90, "语文": 80, "英语": 60, "Python Web": 97, "数据结构": 85, "计算机组成原理": 78},
#     "002": {"姓名": "李四", "数学": 92, "语文": 99, "英语": 73, "Python Web": 98, "数据结构": 88, "计算机组成原理": 91},
#     "003": {"姓名": "韩梅梅", "数学": 78, "语文": 68, "英语": 66, "Python Web": 99, "数据结构": 82, "计算机组成原理": 76}
# }
>>>>>>> ca6e236 (修改为sqlit存储数据)

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
<<<<<<< HEAD
        if username in users_db and users_db[username] == password:
=======
        user = User.query.filter_by(user_id=username).first()
        if user and user.password == password:
>>>>>>> ca6e236 (修改为sqlit存储数据)
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

<<<<<<< HEAD
    if username in score_db:
        student_info = score_db[username]
=======
    user = User.query.filter_by(user_id=username).first()
    if user:
        student_info = {
            "姓名": user.name,
            "数学": user.math,
            "语文": user.chinese,
            "英语": user.english,
            "Python Web": user.PythonWeb,
            "数据结构": user.DataStructures,
            "计算机组成原理": user.ComputerOrganization
        }
>>>>>>> ca6e236 (修改为sqlit存储数据)
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