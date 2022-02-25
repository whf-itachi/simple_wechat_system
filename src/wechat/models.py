from wechat import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    nickname = db.Column(db.String(64), unique=True, index=True)
    gender = db.Column(db.Boolean, default=True, comment='默认True为男性，False为女性')
    password = db.Column(db.String(255), comment="密码")


class Dynamic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, comment='内容')
    unique_code = db.Column(db.String(255), comment='动态唯一编码')
    create_time = db.Column(db.DateTime, server_default=db.func.now(), comment='创建时间')
    update_time = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), comment='修改时间')

    def to_dict(self):
        """将对象转换为字典数据"""
        dynamic_dict = {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "unique_code": self.unique_code,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return dynamic_dict


