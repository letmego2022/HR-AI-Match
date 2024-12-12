import sqlite3
import os

# 定义数据库文件路径
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "db", "gkinfo.db")

# 确保 db 目录存在
db_dir = os.path.join(basedir, "db")
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

# 连接到 SQLite 数据库
# 如果数据库文件不存在，会自动在当前目录创建:
conn = sqlite3.connect(db_path)

# 创建一个 Cursor:
cursor = conn.cursor()

# 执行一条 SQL 语句，创建 api_info 表:
cursor.execute('''
CREATE TABLE IF NOT EXISTS api_info (
    id INTEGER PRIMARY KEY,
    api_info TEXT NOT NULL,
    file_path VARCHAR(255) NOT NULL
)
''')

# 提交事务:
conn.commit()

# 关闭 Connection:
conn.close()