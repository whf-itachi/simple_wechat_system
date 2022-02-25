# Simple_Wechat_System
**一个简版的微信朋友圈发布、查看系统。**

前后端分离项目
简单的做了用户的创建、登录、动态的发布、动态的查看这四个接口。

### 说明：
- 用flask框架自带的session模块来做状态保持，使用redis来存储session值，用werkzeug模块的security来做用户密码的校验。
- 使用ORM框架SQLAlchemy来管理数据库调用。
- 用户上次的图片文件以图片的形式存在本地文件夹中，文件夹命名为动态id值。
- 动态查看接口，传给前端的图片为base64的字符串。

### 项目git地址:
`
git@github.com:whf-itachi/simple_wechat_system.git
`
