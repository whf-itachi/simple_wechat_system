import functools
from flask import session, g, url_for
from werkzeug.utils import redirect


# 登录状态检查
def user_login_data(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        # 获取到当前登录用户的id
        user_id = session.get("user_id")
        # 通过id获取用户信息
        if not user_id:
            return redirect(url_for("user.user_logging"))

        g.user = user_id
        return f(*args, **kwargs)

    return wrapper
