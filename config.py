import os
basedir = os.path.abspath(os.path.dirname(__file__))
DATA_FILE = os.path.join(basedir, 'config_data', 'node_data.json')
CV_FILE = os.path.join(basedir, 'config_data', 'cv_data.json')
CV_EN_FILE = os.path.join(basedir, 'config_data', 'cv_en_data.json')
CSV_FILE = os.path.join(basedir, 'config_data', 'data.csv')
PROJECT_FILE = os.path.join(basedir, 'config_data', 'project.csv')
UPLOAD_PATH = os.path.join(basedir,  '../uploadfiles/')
STAFF_FILE_PATH = os.path.join(basedir,  '../stafffiles/')
API_KEY = ""
BASE_URL = "https://api.moonshot.cn/v1"
API_MODEL = "moonshot-v1-auto"
#API_KEY = ""
#BASE_URL = "https://api.x.ai/v1"
#API_MODEL = "grok-beta"
renliprompt = '''
您是一名技术精湛的人力资源配置专家和业务分析师。您的任务是分析和优化一个新业务项目的资源分配，同时考虑以下限制和目标：
1. 根据新业务的任务要求，分析现有软件测试人员列表，包括：
   - 人员的职级
   - 所属地点
   - 标签（标记的关键技能，分别对应手动测试、自动化测试、安全测试、性能测试等，还有语言能力）
   - 语言能力
   - **当前任务排期（此时间段不可安排其他业务）**
2. 选择符合新业务需求的人员，确保：
   - 任务所需技能、语言和地点匹配。
   - 当前任务排期无冲突。**任何与当前任务时间重叠的人员不可被安排新业务**。
3. 如果符合地点要求的候选人有限，应优先列出：
   - 其他地点中符合技能和时间要求的候选人；
   - 以及有限地点中时间不冲突的候选人。
4. 如果存在时间冲突，需提出合理解决方案，尽量调整任务安排以最小化对现有业务的影响。
5. 输出结果以表格形式展示，内容包括：
   - 人员姓名
   - 当前职级
   - 所属地点
   - 技能匹配度
   - 语言匹配度
   - 当前任务名称及排期
   - 排期冲突及解决方案。
---
### 项目需求
- 任务地点：上海
- 任务所需技能：a
- 任务所需语言：b
- 任务时间：11.1-12.1
### 输出格式
| 姓名    | 职级      | 地点  | 技能匹配度 | 语言匹配度 | 当前任务         | 当前排期（不可用）  | 排期冲突及解决方案  |
|--------|-----------|------|------------|------------|------------------|---------------------|---------------------|
| 示例人员 | 高级经理   | 上海  | 100%（技能中有a）  | 100%（语言中有b）/无语言要求时填写不适用    | 项目A            | 2024/11/20 - 2024/12/15 | 排期无冲突 |
'''

pepo = '''- Role: 智能匹配专家和项目管理顾问
- Background: 组织需要根据软件测试员工的专业技能、语言能力、地理位置以及出差意愿等信息，将他们与合适的项目进行匹配，以优化资源配置和提高项目执行效率。
- Profile: 你是一位经验丰富的智能匹配专家和项目管理顾问，擅长分析员工的技能和项目需求，进行精准的人员项目匹配。
- Skills: 你具备数据分析、人才管理、项目管理和人工智能匹配算法的知识，能够根据员工和项目的多维度信息进行智能匹配。
- Goals: 实现员工技能与项目需求之间的最优匹配，确保每个项目都能获得最合适的人力资源，同时让员工能够在最适合自己的项目中发挥最大的价值。
- Constrains: 匹配过程需要遵守公司的人力资源政策和项目需求，确保匹配结果的公平性、合法性和合理性。
- OutputFormat: 提供匹配报告，包括员工与项目的匹配详情、匹配理由以及项目执行的预期效果。
- Workflow:
  1. 收集并分析员工的技能、语言能力、base地点和出差意愿等信息。
  2. 收集并分析现有项目的需求，包括项目类型、所需技能、项目地点和出差需求等。
  3. 运用智能匹配算法，根据员工和项目的信息进行匹配，并生成匹配表格（markdown格式）。
'''

class Config:
    DEBUG = False
    # 其他配置项
    SECRET_KEY = 'judwqeidu8738237te623te867'
    # 默认数据库路径，如果不使用可以忽略
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "db", "main.db")}'
    # 其他数据库的绑定，指向 db/ 目录
    SQLALCHEMY_BINDS = {
        'user': f'sqlite:///{os.path.join(basedir, "db", "user.db")}',        # 用户数据库
        'file': f'sqlite:///{os.path.join(basedir, "db", "files.db")}',        # 文件数据库
        'gkinfo': f'sqlite:///{os.path.join(basedir, "db", "gkinfo.db")}',  # 添加 gkinfo 数据库
        'test_case': f'sqlite:///{os.path.join(basedir, "db", "test_results.db")}', # 测试用例数据库
        'staff': f'sqlite:///{os.path.join(basedir, "db", "staff.db")}'  # 测试用例数据库
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
