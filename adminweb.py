from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory,jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
import string
import random
import re
from tika import parser
from tika import tika
import pandas as pd

UPLOAD_FOLDER = r'.\uploads'
files_db_path = 'db/files.db'
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'odt', 'ods', 'odp', 'rtf', 'html', 'htm', 'xml', 'zip', 'rar', 'gz', 'tar', 'swf', 'psd', 'svg', 'csv', 'json', 'epub', 'mp3', 'mp4', 'avi', 'mov', 'wmv', 'flv', 'm4v', 'mkv', 'webm', 'wav', 'aiff', 'aac', 'oga', 'ogv', 'm4a', '3gp', '7z', 'iso', 'dmg', 'xz', 'exe', 'dll', 'deb', 'rpm', 'msi', 'bat', 'sh', 'cmd', 'torrent', 'eml', 'msg', 'pst', 'dbx', 'ost', 'pst', 'ics', 'vcf', 'pps', 'pot', 'potx', 'ppa', 'ppam', 'sldm', 'sldx', 'thmx', 'onetoc', 'onetoc2', 'onetmp', 'thmx', 'docm', 'dotm', 'xlsb', 'xltx', 'xltm', 'xlsm', 'pptm', 'potm', 'ppsm'
}

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于保持会话安全
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
import json
def insert_file_data(userid, file_path, file_content):
    # 连接到数据库
    conn = sqlite3.connect(files_db_path)
    cursor = conn.cursor()
    try:
        # 插入数据的 SQL 语句，不再包含 fileid
        insert_sql = '''
        INSERT INTO files (userid, file_path, file_content)
        VALUES (?, ?, ?)
        '''
        
        # 执行插入数据的 SQL 语句
        cursor.execute(insert_sql, (userid, file_path, file_content))

        # 提交事务
        conn.commit()
        return True
    except sqlite3.Error as e:
        # 如果发生错误，则回滚事务
        conn.rollback()
        return f"Error occurred: {e}"
    finally:
        # 关闭连接
        conn.close()
class TikaDocumentProcessor:
    def __init__(self, server_url='http://localhost:9998'):
        # 设置Tika服务器地址
        os.environ['TIKA_SERVER_ENDPOINT'] = server_url
    
    def parse_document(self, file_path):
        """
        读取文档内容
        :param file_path: 文档路径
        :return: 文档解析后的内容
        """
        try:
            # 使用Tika解析文档
            parsed = parser.from_file(file_path)
            content = parsed.get('content', '')
            if content:
                print("文档解析成功！")
            else:
                print("文档内容为空。")
            return content
        except Exception as e:
            print(f"解析文档时出错: {e}")
            return None
    
    def process_content(self, content):
        """
        对文档内容进行处理（例如清理文本等）
        :param content: 原始文档内容
        :return: 处理后的内容
        """
        if not content:
            print("没有可以处理的文档内容。")
            return None
        try:
            # 去除多余的空格和换行符
            cleaned_content = re.sub(r'\s+', ' ', content).strip()
            #cleaned_content = self.clean_text(tmptext)
            print("文档内容处理完成。")
            return cleaned_content.lower()
        except Exception as e:
            print(f"处理文档内容时出错: {e}")
            return None
    def clean_text(self, text):
        """
        对文档内容进行处理（例如清理文本等）
        去除自然语言文本中的特殊字符（代码不处理）
        :param content: 原始文档内容
        :return: 处理后的内容
        """
        # 去除特殊字符
        text = re.sub(r'[^\w\s]', '', text)
        # 转为小写
        text = text.lower()
        return text
    def analyze_content(self, content):
        """
        对文档内容进行分析（例如统计词频、分析文本结构等）
        :param content: 处理后的文档内容
        :return: 分析结果
        """
        if not content:
            print("没有可以分析的文档内容。")
            return None
        try:
            # 简单示例：统计词频
            word_list = content.split()
            word_count = {}
            for word in word_list:
                word = word.lower()
                if word not in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] += 1
            print("文档分析完成。")
            return word_count
        except Exception as e:
            print(f"分析文档内容时出错: {e}")
            return None
class TextForModel:
    def __init__(self, cleaned_text):
        self.cleaned_text = cleaned_text

    def prepare_for_training(self, max_length=512):
        """
        处理混合语言文本，使用多种标点符号分割，并根据 max_length 控制每个片段的长度。
        """
        # 使用正则表达式匹配中英文标点符号（包括句号、问号、感叹号等）
        sentences = re.split(r'(?<=[。！？.!?])', self.cleaned_text)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            # 如果当前片段长度小于最大限制，继续添加
            if len(current_chunk) + len(sentence) <= max_length:
                current_chunk += sentence
            else:
                # 达到最大长度，存储当前片段并开始新的片段
                chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        # 添加最后一个片段
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def save_to_json(self, file_name):
        """
        将处理后的文本数据保存为 JSON 文件。
        """
        data = self.prepare_for_training()
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

# 生成随机的字符串
def random_string(length=10):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


# 数据库连接函数
def get_db_connection():
    conn = sqlite3.connect('db/user.db')
    conn.row_factory = sqlite3.Row
    return conn

# 数据库连接函数
def get_filesdb_connection():
    conn = sqlite3.connect('db/files.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    conn.close()
    conn1 = get_filesdb_connection()
    cur1 = conn1.cursor()
    cur1.execute('SELECT * FROM files')
    files = cur1.fetchall()
    conn1.close()
    return render_template('admin.html', users=users, files=files)

@app.route('/filesdb')
def filesdb():
    conn1 = get_filesdb_connection()
    cur1 = conn1.cursor()
    cur1.execute('SELECT * FROM files')
    files = cur1.fetchall()
    conn1.close()
    return render_template('filesdb.html', files=files)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        flash('User added successfully!')
        return redirect(url_for('index'))
    return render_template('add_user.html')

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('User deleted successfully!')
    return redirect(url_for('index'))

@app.route('/delete_file/<int:file_id>')
def delete_file(file_id):
    conn = get_filesdb_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM files WHERE fileid = ?', (file_id,))
    conn.commit()
    conn.close()
    flash('File deleted successfully!')
    return redirect(url_for('index'))

@app.route('/view_file#file_id=<int:file_id>')
def view_file(file_id):
    # 使用 file_id 从数据库中获取文件信息
    conn = get_filesdb_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM files WHERE fileid = ?", (file_id,))
    file = cur.fetchone()
    
    # 渲染一个模板来显示文件信息
    return render_template('view_file.html', file=file)

@app.route('/edit_user#<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    if user is None:
        flash('User not found!')
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        cur.execute('UPDATE users SET username = ?, password_hash = ? WHERE id = ?', (username, hashed_password, user_id))
        conn.commit()
        flash('User updated successfully!')
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_user.html', user=user)



@app.route('/Convert_to_training_data#file_id=<int:file_id>')
def Convert_to_training_data(file_id):
    # 使用 file_id 从数据库中获取文件信息
    conn = get_filesdb_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM files WHERE fileid = ?", (file_id,))
    file = cur.fetchone()
    if file:
    # 获取第四个字段（索引为3）
        text_field = file[3]
        # 检查数据类型并相应地处理
        if isinstance(text_field, bytes):
            # 如果数据是字节序列，解码为字符串
            text_data = text_field.decode('utf-8')
        else:
            # 如果数据已经是字符串，直接使用
            text_data = text_field
    text_processor = TextForModel(text_data)
	# 生成文件名
    file_name = f"./training_data/data_{random_string()}.json"
    text_processor.save_to_json(file_name)
    # 渲染一个模板来显示文件信息
	# 读取JSON文件内容
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 假设data是您要发送的字典
    data_json = json.dumps(data, ensure_ascii=False, indent=4)
    return render_template('view_json.html', data=data_json)

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})
    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        user_id = "admin"
        file.save(file_path)
        processor = TikaDocumentProcessor()
        # 解析文档
        content = processor.parse_document(file_path)
        #print(content)
        # 处理文档内容
        processed_content = processor.process_content(content)
        print(file_path, user_id,processed_content)
        if insert_file_data(userid=user_id, file_path=file_path, file_content=processed_content):
            return jsonify({'success': True, 'message': 'File uploaded successfully', 'filename': file.filename})
        else:
            return jsonify({'success': False, 'message': 'Failure to stock', 'filename': file.filename})
    else:
        return jsonify({'success': False, 'message': 'Invalid file type'})


if __name__ == '__main__':
    app.run(debug=False)