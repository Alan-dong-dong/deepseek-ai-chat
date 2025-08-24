# DeepSeek AI Chat Application（基于Reflex框架构建）

一个基于DeepSeek API的智能聊天应用，采用Reflex框架构建，具有科技感和小清新的UI设计。

## 🚀 特性

- **智能对话**: 基于DeepSeek API的强大AI对话能力
- **科技感UI**: 现代化的渐变设计和动画效果
- **响应式设计**: 适配各种屏幕尺寸
- **实时聊天**: 流畅的聊天体验
- **示例问题**: 预设问题快速开始对话
- **API密钥管理**: 安全的API密钥配置

## 🎨 UI设计特色

- 🌈 **渐变色彩**: 青色到蓝色的科技感渐变
- ✨ **动画效果**: 流畅的悬浮和过渡动画
- 🔮 **玻璃拟态**: 现代化的毛玻璃效果
- 🎯 **交互反馈**: 丰富的鼠标悬浮效果
- 📱 **响应式布局**: 完美适配移动端和桌面端

## 🛠️ 技术栈

- **前端框架**: Reflex (Python)
- **样式框架**: Tailwind CSS
- **AI服务**: DeepSeek API
- **HTTP客户端**: httpx
- **状态管理**: Reflex State

## 📦 安装和运行

### 1. 克隆项目

```bash
git clone https://github.com/Alan-dong-dong/deepseek-ai-chat.git
cd deepseek-ai-chat
```

### 2. 创建虚拟环境

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行应用

```bash
reflex run
```

应用将在 `http://localhost:3000` 启动。

## 🔑 配置API密钥

1. 访问 [DeepSeek官网](https://www.deepseek.com/) 获取API密钥
2. 在应用界面的API密钥输入框中输入您的密钥
3. 开始与AI对话

## 📝 使用说明

1. **设置API密钥**: 在页面顶部输入您的DeepSeek API密钥
2. **开始对话**: 在输入框中输入问题或点击预设的示例问题
3. **查看回复**: AI会实时回复您的问题
4. **继续对话**: 支持多轮对话，AI会记住上下文

## 🎯 示例问题

- 💻 帮我写一个Python函数
- 🧠 解释一下机器学习的概念
- ✍️ 给我一些创意写作的建议

## 📁 项目结构

```
deepseek-ai-chat/
├── my_app_name/
│   ├── __init__.py
│   └── my_app_name.py      # 主应用文件
├── assets/
│   └── favicon.ico
├── requirements.txt        # 项目依赖
├── rxconfig.py            # Reflex配置
├── .gitignore
└── README.md
```

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License

## 🙏 致谢

- [Reflex](https://reflex.dev/) - 优秀的Python Web框架
- [DeepSeek](https://www.deepseek.com/) - 强大的AI API服务
- [Tailwind CSS](https://tailwindcss.com/) - 现代化的CSS框架

---

**享受与AI的智能对话吧！** 🤖✨
