#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini API 高级功能应用
支持多轮对话、参数调节、多种应用场景
"""

import google.generativeai as genai
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

# 加载 .env 文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class GeminiAdvanced:
    def __init__(self, api_key: str = None, model_name: str = None):
        """初始化 Gemini 高级客户端"""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 GOOGLE_API_KEY 环境变量或传入 api_key 参数")
        
        genai.configure(api_key=self.api_key)
        
        # 从 .env 文件读取配置，如果没有则使用默认值
        self.model_name = model_name or os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")
        
        # 从 .env 文件读取安全设置配置
        safety_level = os.getenv("SAFETY_LEVEL", "BLOCK_MEDIUM_AND_ABOVE")
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": safety_level
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": safety_level
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": safety_level
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": safety_level
            }
        ]
        
        self.model = genai.GenerativeModel(
            self.model_name,
            safety_settings=self.safety_settings
        )
        self.chat_history: List[Dict] = []
        
        # 从 .env 文件读取生成配置
        self.default_config = {
            "temperature": float(os.getenv("DEFAULT_TEMPERATURE", "0.7")),
            "top_p": float(os.getenv("DEFAULT_TOP_P", "0.8")),
            "top_k": int(os.getenv("DEFAULT_TOP_K", "40")),
            "max_output_tokens": int(os.getenv("DEFAULT_MAX_TOKENS", "1000")),
        }
    
    def show_config(self):
        """显示当前配置"""
        print("⚙️ 当前 Gemini 配置：")
        print(f"   🤖 API密钥：{self.api_key[:8]}..." if self.api_key else "   ❌ 未设置API密钥")
        print(f"   🧠 模型名称：{self.model_name}")
        print(f"   🌡️ 温度参数：{self.default_config['temperature']}")
        print(f"   📝 最大输出：{self.default_config['max_output_tokens']} tokens")
        print(f"   🔧 Top-p：{self.default_config['top_p']}")
        print(f"   🔧 Top-k：{self.default_config['top_k']}")
        print(f"   💭 对话历史：{len(self.chat_history)} 条记录")
    
    def list_available_models(self):
        """列出可用的模型"""
        print("🤖 可用的 Gemini 模型：")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"   • {model.name}")
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        config = {**self.default_config, **kwargs}
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=config
            )
            
            # 详细的响应检查和错误处理
            if not response.candidates:
                return "❌ 生成失败：没有返回候选响应"
            
            candidate = response.candidates[0]
            
            # 检查 finish_reason
            if candidate.finish_reason == 1:  # STOP - 正常完成
                if candidate.content and candidate.content.parts:
                    return response.text
                else:
                    return "❌ 生成失败：响应内容为空"
            elif candidate.finish_reason == 2:  # MAX_TOKENS
                return "❌ 生成失败：达到最大token限制，请增加 max_output_tokens"
            elif candidate.finish_reason == 3:  # SAFETY
                return "❌ 生成失败：内容被安全过滤器阻止，请尝试修改提示词"
            elif candidate.finish_reason == 4:  # RECITATION
                return "❌ 生成失败：检测到重复内容"
            else:
                return f"❌ 生成失败：未知的finish_reason: {candidate.finish_reason}"
                
        except Exception as e:
            return f"❌ 生成失败：{e}"
    
    def start_chat(self, system_prompt: str = None):
        """开始聊天会话"""
        if system_prompt:
            self.chat_history = [{"role": "system", "content": system_prompt}]
        else:
            self.chat_history = []
        
        chat = self.model.start_chat(history=[])
        return chat
    
    def chat_with_history(self, message: str, chat_session=None) -> str:
        """带历史记录的聊天"""
        if chat_session is None:
            chat_session = self.model.start_chat(history=[])
        
        try:
            response = chat_session.send_message(message)
            
            # 记录对话历史
            self.chat_history.append({
                "timestamp": datetime.now().isoformat(),
                "user": message,
                "assistant": response.text
            })
            
            return response.text
        except Exception as e:
            return f"❌ 对话失败：{e}"
    
    def save_chat_history(self, filename: str = None):
        """保存对话历史"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chat_history_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.chat_history, f, ensure_ascii=False, indent=2)
        
        print(f"💾 对话历史已保存到：{filename}")
    
    def load_chat_history(self, filename: str):
        """加载对话历史"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.chat_history = json.load(f)
            print(f"📂 对话历史已从 {filename} 加载")
        except FileNotFoundError:
            print(f"❌ 文件 {filename} 不存在")
        except json.JSONDecodeError:
            print(f"❌ 文件 {filename} 格式错误")
    
    def analyze_image(self, image_path: str, prompt: str = "描述这张图片") -> str:
        """分析图片"""
        try:
            from PIL import Image
            
            # 打开图片
            img = Image.open(image_path)
            
            # 使用支持视觉的模型
            vision_model = genai.GenerativeModel('gemini-1.5-flash')
            response = vision_model.generate_content([prompt, img])
            
            return response.text
        except ImportError:
            return "❌ 请安装 Pillow 库：pip install Pillow"
        except Exception as e:
            return f"❌ 图片分析失败：{e}"
    
    def translate_text(self, text: str, target_language: str = "中文") -> str:
        """翻译文本"""
        prompt = f"请将以下文本翻译成{target_language}：\n\n{text}"
        return self.generate_text(prompt)
    
    def summarize_text(self, text: str, max_length: int = 200) -> str:
        """文本摘要"""
        prompt = f"请将以下文本总结为不超过{max_length}字的摘要：\n\n{text}"
        return self.generate_text(prompt, max_output_tokens=max_length*2)
    
    def generate_code(self, description: str, language: str = "Python") -> str:
        """代码生成"""
        prompt = f"请用{language}编写代码实现以下功能：\n\n{description}\n\n请提供完整的、可运行的代码，并包含必要的注释。"
        return self.generate_text(prompt)
    
    def creative_writing(self, topic: str, style: str = "现代散文") -> str:
        """创意写作"""
        prompt = f"请以{style}的风格，写一篇关于'{topic}'的文章。"
        return self.generate_text(prompt)

def interactive_demo():
    """交互式演示"""
    print("🚀 Gemini API 高级功能演示")
    print("="*50)
    
    try:
        gemini = GeminiAdvanced()
        
        while True:
            print("\n📋 请选择功能：")
            print("1. 📝 文本生成")
            print("2. 💬 多轮对话")
            print("3. 🌐 文本翻译")
            print("4. 📄 文本摘要")
            print("5. 💻 代码生成")
            print("6. ✍️  创意写作")
            print("7. 🖼️  图片分析")
            print("8. 🎨 图片生成助手")
            print("9. 📊 查看可用模型")
            print("10. ⚙️ 查看当前配置")
            print("0. 🚪 退出")
            
            choice = input("\n请输入选项 (0-10): ").strip()
            
            if choice == "0":
                print("👋 再见！")
                break
            elif choice == "1":
                prompt = input("请输入您的提示：")
                result = gemini.generate_text(prompt)
                print(f"\n🔮 生成结果：\n{result}")
            elif choice == "2":
                print("💬 开始多轮对话 (输入 'quit' 退出)：")
                chat = gemini.start_chat()
                while True:
                    user_input = input("\n您：")
                    if user_input.lower() == 'quit':
                        break
                    response = gemini.chat_with_history(user_input, chat)
                    print(f"🤖：{response}")
            elif choice == "3":
                text = input("请输入要翻译的文本：")
                lang = input("目标语言 (默认：中文)：") or "中文"
                result = gemini.translate_text(text, lang)
                print(f"\n🌐 翻译结果：\n{result}")
            elif choice == "4":
                text = input("请输入要摘要的文本：")
                result = gemini.summarize_text(text)
                print(f"\n📄 摘要结果：\n{result}")
            elif choice == "5":
                desc = input("请描述您想要的功能：")
                lang = input("编程语言 (默认：Python)：") or "Python"
                result = gemini.generate_code(desc, lang)
                print(f"\n💻 生成的代码：\n{result}")
            elif choice == "6":
                topic = input("写作主题：")
                style = input("写作风格 (默认：现代散文)：") or "现代散文"
                result = gemini.creative_writing(topic, style)
                print(f"\n✍️ 创作结果：\n{result}")
            elif choice == "7":
                image_path = input("请输入图片路径：")
                prompt = input("分析提示 (默认：描述这张图片)：") or "描述这张图片"
                result = gemini.analyze_image(image_path, prompt)
                print(f"\n🖼️ 分析结果：\n{result}")
            elif choice == "8":
                print("🎨 启动图片生成助手...")
                print("💡 提示：图片生成助手将在新窗口中运行")
                try:
                    import subprocess
                    import sys
                    subprocess.run([sys.executable, "gemini_image_generation.py"])
                except Exception as e:
                    print(f"❌ 启动图片生成助手失败：{e}")
                    print("请手动运行：python gemini_image_generation.py")
            elif choice == "9":
                gemini.list_available_models()
            elif choice == "10":
                gemini.show_config()
            else:
                print("❌ 无效选项，请重新选择")
    
    except Exception as e:
        print(f"❌ 初始化失败：{e}")
        print("请确保已设置 GOOGLE_API_KEY 环境变量")

if __name__ == "__main__":
    interactive_demo()
