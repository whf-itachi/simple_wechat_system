from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    nickname = db.Column(db.String(64), unique=True, index=True)
    gender = db.Column(db.Boolean, default=1, comment='默认1为男性，0为女性')
    password = db.Column(db.String(64))


class Dynamic(db.Model):
    id = db.Column(db.Integer, Primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    connect = db.Column(db.Text, comment='动态内容')
    create_time = db.Column(db.DateTime, server_default=db.func.now(), comment='创建时间')
    update_time = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), comment='修改时间')
