# 连接数据库的配置信息

# MySQL所在的主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# MySQL上创建的数据库名称
DATABASE = "zhiliaooa"
# 连接MySQL的用户名，读者用自己的设置的
USERNAME = "root"
# 连接MySQL的密码，读者用自己的
PASSWORD = "rootroot"
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI