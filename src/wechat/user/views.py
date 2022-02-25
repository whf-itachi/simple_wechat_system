from flask import jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from wechat import db
from wechat.models import User
from wechat.user import user_blu


# 用户创建
@user_blu.route('/create', methods=['POST'])
def create_user():
    data = request.form.to_dict()
    name = data.get('name')
    nickname = data.get('nickname')
    gender = data.get('gender')

    if gender == '1':
        gender = True
    else:
        gender = False

    password = data.get('password')
    password_hash = generate_password_hash(password)

    # TODO:参数校验逻辑
    user_name = User.query.filter_by(name=name).first()
    if user_name:
        return jsonify(error='error', errmsg="用户名已存在")
    user_nick_name = User.query.filter_by(nickname=nickname).first()
    if user_nick_name:
        return jsonify(error='error', errmsg="该昵称已存在")

    try:
        # 创建用户
        new_user = User(name=name, nickname=nickname, gender=gender, password=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(error='success')
    except Exception as e:
        db.session.rollback()
        return jsonify(error='error', errmsg="用户创建失败")


# 用户登录
@user_blu.route('/logging', methods=['POST'])
def user_logging():
    data = request.form.to_dict()
    name = data.get('name')
    password = data.get('password')
    # TODO:参数校验逻辑
    user_info = User.query.filter_by(name=name).first()
    if not user_info:
        return jsonify(error='error', errmsg="用户不存在")

    password_hash = user_info.password

    try:
        # 密码校验
        if not check_password_hash(password_hash, password):
            return jsonify(error='error', errmsg="密码不正确")

        session['user_id'] = user_info.id
        return jsonify(error='success')
    except Exception as e:
        db.session.rollback()
        return jsonify(error='error', errmsg="登录失败")
