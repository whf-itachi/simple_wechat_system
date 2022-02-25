import base64
import os
import uuid

from flask import request, g, jsonify
from werkzeug.utils import secure_filename

from config import config
from wechat import db
from wechat.dynamic import dynamic_blu
from wechat.models import Dynamic
from wechat.utils import user_login_data


@dynamic_blu.route('/create', methods=["POST"])
@user_login_data
def dynamic_create():
    request_data = request.form.to_dict()
    # 文字内容存入数据库
    content = request_data.get("content")

    unique_code = str(uuid.uuid1()).replace('-', '')

    news = Dynamic()
    news.content = content
    news.user_id = g.user
    news.unique_code = unique_code

    try:
        db.session.add(news)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error='error', errmsg="数据保存失败")

    dynamic_info = Dynamic.query.filter_by(unique_code=unique_code).first()
    dynamic_id = dynamic_info.id

    # 图片存储
    file_path = os.path.abspath(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "images_file", f"{dynamic_id}"))
    images_datas = request.files.getlist('images')
    if images_datas:
        type_list = config.ALLOWED_EXTENSIONS

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        for file in images_datas:
            file_name = secure_filename(file.filename)  # 得到安全的文件名
            file_extension = file_name.rsplit('.', 1)[-1]
            if not file_name or file_extension not in type_list:
                return jsonify(error='error', errmsg="Invalid file type")

            image_file_path = os.path.join(file_path, file_name)
            file.save(image_file_path)

    return jsonify(error="success")


@dynamic_blu.route('/query', methods=["GET"])
@user_login_data
def dynamic_query():
    page = request.args.get('page', 1, type=int)
    offset = config.ARTISAN_POSTS_PER_PAGE
    # 根据用户id获取用户的动态数据
    dynamic_info = Dynamic.query.filter_by(user_id=g.user).all()
    total = len(dynamic_info)
    if not dynamic_info:
        return jsonify(error="success", errmsg="你还没有发布动态！")

    pagination = Dynamic.query.filter_by(user_id=g.user).order_by(Dynamic.id.desc()).paginate(page, per_page=offset)
    dynamic_info = pagination.items

    dynamic_list = list()

    for dynamic_data in dynamic_info:
        dy_dict = dynamic_data.to_dict()
        dynamic_id = dy_dict.get('id')
        # 图片读取
        file_path = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "images_file",
                                                 f"{dynamic_id}"))
        if not os.path.exists(file_path):
            dy_dict["images"] = []
        else:
            dy_dict['images'] = list()
            for file_name in os.listdir(file_path):
                front_file_path = os.path.join(file_path, file_name)
                # 身份证文件信息需按照路径查询,并且转换为base64编码数据
                with open(front_file_path, 'rb') as front_f:
                    front_utf8_data = str(base64.b64encode(front_f.read()), 'utf-8')
                    dy_dict['images'].append('data:image/png;base64,' + front_utf8_data)

        dynamic_list.append(dy_dict)

    return jsonify(error="success", data=dynamic_list, total=total)
