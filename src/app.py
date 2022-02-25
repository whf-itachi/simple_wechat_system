from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from wechat import create_app

app = create_app()
# 数据库迁移
db = SQLAlchemy(app)
Migrate(app, db=db)


if __name__ == "__main__":
    app.run()
