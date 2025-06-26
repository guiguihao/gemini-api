# Gemini API Python 应用

🤖 一个功能丰富的 Google Gemini API Python 应用集合，包含基础文本生成、高级功能、聊天机器人等多种使用场景。

## 📋 功能特性

- ✅ **基础文本生成** - 简单的文本生成示例
- 💬 **多轮对话** - 支持上下文的聊天功能  
- 🌐 **文本翻译** - 多语言翻译支持
- 📄 **文本摘要** - 智能内容摘要
- 💻 **代码生成** - 根据描述生成代码
- ✍️ **创意写作** - 各种风格的创作
- 🖼️ **图像分析** - 图片内容理解（需要 Pillow）
- � **图片生成助手** - AI 图片提示词生成和优化
- 📝 **提示词工具** - 专业图片提示词生成器
- �🎯 **参数调节** - 温度、长度等生成参数控制
- 💾 **历史保存** - 对话历史存储功能

## 🚀 快速开始

### 1. 环境准备

    #### 推荐
    vscode 插件 Python Environment Manager (deprecated)
```bash

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API 密钥

**方法 1：环境变量（推荐）**
```bash
export GOOGLE_API_KEY='your_api_key_here'
```

**方法 2：.env 文件**
```bash

# 编辑 .env 文件，填入您的 API 密钥
```

### 3. 获取 API 密钥

1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 创建新的 API 密钥
3. 复制密钥并按上述方法配置

## 📱 使用示例

### 基础使用
```bash
python gemini_quickstart.py
```

### 聊天机器人
```bash
python gemini_chat.py
```

### 高级功能演示
```bash
python gemini_advanced.py
```

### 图片生成助手
```bash
python gemini_image_generation.py
```

### 简单提示词生成器
```bash
python image_prompt_generator.py
```

## 📁 文件说明

| 文件 | 功能描述 |
|------|----------|
| `gemini_quickstart.py` | 基础 API 调用示例 |
| `gemini_chat.py` | 命令行聊天机器人 |
| `gemini_advanced.py` | 高级功能集合（交互式演示） |
| `gemini_image_generation.py` | 图片生成助手（完整功能） |
| `image_prompt_generator.py` | 简单图片提示词生成器 |
| `config.py` | 配置管理模块 |
| `requirements.txt` | 项目依赖包 |
| `.env.example` | 环境变量配置示例 |

## 🛠️ 代码示例

### 基础文本生成
```python
import google.generativeai as genai
import os

# 配置 API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

# 生成文本
response = model.generate_content("写一个关于 小美 的故事")
print(response.text)
```

### 多轮对话
```python
# 开始聊天
chat = model.start_chat(history=[])

# 发送消息
response1 = chat.send_message("你好！")
print(response1.text)

response2 = chat.send_message("你记得我刚才说什么吗？")
print(response2.text)
```

### 图像分析
```python
from PIL import Image

# 加载图片
img = Image.open('image.jpg')

# 分析图片
vision_model = genai.GenerativeModel('gemini-2.5-flash')
response = vision_model.generate_content(["描述这张图片", img])
print(response.text)
```

### 图片提示词生成
```python
from image_prompt_generator import SimpleImagePromptGenerator

# 创建生成器
generator = SimpleImagePromptGenerator()

# 生成提示词
prompt = generator.generate_prompt(
    description="一只可爱的小猫在花园里玩耍",
    style="photorealistic"
)
print(prompt)

# 创建变体
variations = generator.create_variations(prompt, count=3)
for i, variation in enumerate(variations, 1):
    print(f"变体 {i}: {variation}")
```

## ⚙️ 配置选项

### 生成参数
- `temperature`: 0.0-2.0，控制输出随机性
- `top_p`: 0.0-1.0，核采样参数
- `top_k`: 1-100，候选词数量
- `max_output_tokens`: 最大输出长度

### 环境变量
```bash
GOOGLE_API_KEY=your_api_key        # 必需
DEFAULT_MODEL=gemini-2.5-flash     # 可选
DEFAULT_TEMPERATURE=0.7            # 可选
DEFAULT_MAX_TOKENS=1000           # 可选
```

## 🎯 应用场景

### 1. 内容创作
- 文章写作
- 创意故事
- 诗歌创作
- 营销文案

### 2. 编程助手
- 代码生成
- 代码解释
- 调试建议
- 技术文档

### 3. 学习辅助
- 知识问答
- 概念解释
- 学习计划
- 练习题生成

### 4. 日常工具
- 文本翻译
- 内容摘要
- 邮件写作
- 会议纪要

### 5. 图片创作
- AI 图片提示词生成
- 提示词优化和变体
- 创意图片描述
- 艺术风格建议
- 图片故事创作

## 🔧 故障排除

### 常见问题

**Q: 提示 "请设置 GOOGLE_API_KEY 环境变量"**
A: 请确保正确设置了 API 密钥环境变量或 .env 文件

**Q: 模型不可用错误**
A: 检查模型名称是否正确，可以运行 `gemini_advanced.py` 查看可用模型

**Q: 图像分析失败**
A: 确保安装了 Pillow 库：`pip install Pillow`

**Q: 请求超时或失败**
A: 检查网络连接，确认 API 密钥有效且有足够配额

### 错误代码
- `400`: 请求格式错误
- `401`: API 密钥无效
- `403`: 权限不足或配额超限
- `429`: 请求频率过高
- `500`: 服务器错误

## 📚 更多资源

- [Google AI Studio](https://makersuite.google.com/)
- [Gemini API 文档](https://ai.google.dev/docs)
- [Python SDK 文档](https://ai.google.dev/api/python/google/generativeai)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目仅供学习和研究使用。请遵守 Google Gemini API 的使用条款。

---

💡 **提示**: 请合理使用 API 配额，避免频繁请求。首次使用建议先运行基础示例测试连接。
