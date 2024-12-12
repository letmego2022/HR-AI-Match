# HR-AI-Match

**HR-AI-Match** 是一个基于人工智能的匹配系统，旨在帮助企业从大量简历中快速筛选出最符合职位要求的候选人，提升招聘效率。该系统利用 AI 技术进行简历分析和匹配，自动提取技能和关键数据，帮助企业做出更快速的决策。

## 主要功能

- **AI 推荐**：使用机器学习算法，根据职位要求与候选人简历的匹配度，推荐最合适的候选人。
- **项目管理**：系统能够根据员工的项目经验、技能和兴趣，提供最适合的岗位建议。
- **技能提取**：自动从简历中提取技能数据，并进行分析和分类，帮助招聘人员准确了解候选人的能力。
  
## 项目截图

### 1. Dashboard

这是系统的主控制面板，用户可以快速查看各项统计数据和推荐的候选人。

![Dashboard](https://github.com/user-attachments/assets/f150b3b5-b4a5-4de0-bfe5-9654e0670c7b)

### 2. AI 推荐

AI 系统根据候选人的简历数据推荐最匹配的职位。

![AI 推荐](https://github.com/user-attachments/assets/58b6d439-03d2-40de-8be7-93c0f9ba5b3d)

### 3. 结果展示

AI 推荐结果将展示每个候选人和岗位的匹配度，帮助招聘人员做出决策。

![结果展示](https://github.com/user-attachments/assets/c7c21408-e940-4bc8-92ab-235e30c05052)

## 从简历中提取技能

系统能够自动从简历文件中提取候选人的技能数据。这一功能依赖于自然语言处理和机器学习模型，以便准确地识别候选人的技术栈、工作经历及其他重要信息。

### 技术栈

- **Flask**：用于后端 API 的开发。
- **Llama 3.1 70B**：AI 模型，用于文本分析和技能提取。
- **SQLite**：数据库存储候选人信息。
- **Bootstrap**：前端 UI 框架，提供响应式布局和样式。

## 安装和使用

1. 克隆仓库：
   ```bash
   git clone https://github.com/letmego2022/HR-AI-Match.git
   ```
   dev 分支
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行 Flask 应用：
   ```bash
   python app.py
   ```

4. 打开浏览器并访问 `http://127.0.0.1:5000` 查看应用。

## 贡献

欢迎贡献代码或提出问题！请使用 GitHub 提交 issue 或 pull request。

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.